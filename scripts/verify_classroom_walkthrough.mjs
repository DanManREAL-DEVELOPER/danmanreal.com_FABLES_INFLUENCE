#!/usr/bin/env node
import { createServer } from "node:http";
import { existsSync, mkdtempSync, readFileSync, rmSync, statSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { spawn, spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const htmlPath = join(repoRoot, "FABLES_INFLUENCE_CLASSROOM_WALKTHROUGH.html");
const proofDir = mkdtempSync(join(tmpdir(), "fables-classroom-proof-"));
const results = [];

function record(name, details = {}) {
  results.push({ name, status: "PASS", details });
}

function fail(name, message, details = {}) {
  const error = new Error(`${name}: ${message}`);
  error.details = details;
  throw error;
}

function assert(name, condition, message, details = {}) {
  if (!condition) fail(name, message, details);
  record(name, details);
}

function count(pattern, text) {
  const match = text.match(pattern);
  return match ? match.length : 0;
}

function extractModule(html) {
  const match = html.match(/<script type="module">([\s\S]*?)<\/script>/);
  if (!match) fail("module extraction", "missing module script");
  return match[1];
}

async function listen(server) {
  await new Promise((resolveListen, rejectListen) => {
    server.once("error", rejectListen);
    server.listen(0, "127.0.0.1", resolveListen);
  });
  return server.address().port;
}

function startServer() {
  return createServer((req, res) => {
    try {
      const requested = decodeURIComponent(new URL(req.url || "/", "http://127.0.0.1").pathname);
      if (!["/", "/FABLES_INFLUENCE_CLASSROOM_WALKTHROUGH.html"].includes(requested)) {
        res.writeHead(404); res.end("not found"); return;
      }
      res.writeHead(200, { "content-type": "text/html; charset=utf-8" });
      res.end(readFileSync(htmlPath));
    } catch {
      res.writeHead(400); res.end("bad request");
    }
  });
}

async function ownDebugPort(profile, proc) {
  const path = join(profile, "DevToolsActivePort");
  for (let attempt = 0; attempt < 120; attempt++) {
    if (proc.exitCode !== null || proc.signalCode !== null) throw new Error("Owned Chrome exited before debugger startup");
    if (existsSync(path)) {
      const port = Number(readFileSync(path, "utf8").split("\n")[0]);
      if (Number.isInteger(port) && port > 0 && port < 65536) return port;
    }
    await new Promise(resolveWait => setTimeout(resolveWait, 100));
  }
  throw new Error("Owned Chrome debugger startup timed out");
}

async function stopOwnedChrome(proc) {
  if (proc.exitCode !== null || proc.signalCode !== null) return;
  const exited = new Promise(resolveExit => proc.once("exit", resolveExit));
  proc.kill("SIGTERM");
  let timer;
  await Promise.race([exited, new Promise(resolveWait => { timer = setTimeout(resolveWait, 3000); })]);
  clearTimeout(timer);
  if (proc.exitCode === null && proc.signalCode === null) { proc.kill("SIGKILL"); await exited; }
}

async function waitForJson(url, timeoutMs = 12000) {
  const start = Date.now();
  let lastError = null;
  while (Date.now() - start < timeoutMs) {
    try {
      const response = await fetch(url);
      if (response.ok) return response.json();
      lastError = new Error(`${response.status} ${response.statusText}`);
    } catch (error) {
      lastError = error;
    }
    await new Promise(resolveWait => setTimeout(resolveWait, 180));
  }
  throw lastError || new Error(`timed out waiting for ${url}`);
}

function findChrome() {
  for (const cmd of ["google-chrome", "chromium", "chromium-browser"]) {
    const found = spawnSync("bash", ["-lc", `command -v ${cmd}`], { encoding: "utf8" });
    if (found.status === 0 && found.stdout.trim()) return found.stdout.trim();
  }
  fail("chrome discovery", "no Chrome/Chromium executable found");
}

async function withChrome(pageUrl, fn) {
  const chrome = findChrome();
  const profile = mkdtempSync(join(tmpdir(), "fables-proof-chrome-"));
  const proc = spawn(chrome, [
    "--headless=new",
    "--remote-debugging-port=0",
    `--user-data-dir=${profile}`,
    "--no-first-run",
    "--noerrdialogs",
    "--disable-gpu-sandbox",
    "--enable-unsafe-webgpu",
    "--window-size=1440,1100",
    "about:blank"
  ], { stdio: "ignore" });

  try {
    const debugPort = await ownDebugPort(profile, proc);
    const version = await waitForJson(`http://127.0.0.1:${debugPort}/json/version`);
    const browserWs = new WebSocket(version.webSocketDebuggerUrl);
    await new Promise((resolveOpen, rejectOpen) => {
      const timer = setTimeout(() => rejectOpen(new Error("browser websocket timeout")), 8000);
      browserWs.onopen = () => { clearTimeout(timer); resolveOpen(); };
      browserWs.onerror = () => { clearTimeout(timer); rejectOpen(new Error("browser websocket failed")); };
    });

    let id = 0;
    const pending = new Map();
    const events = [];
    browserWs.onmessage = event => {
      const msg = JSON.parse(event.data);
      if (msg.id && pending.has(msg.id)) {
        pending.get(msg.id)(msg);
        pending.delete(msg.id);
        return;
      }
      if (msg.sessionId && msg.method === "Runtime.exceptionThrown") {
        events.push(`EX:${msg.params.exceptionDetails.text}:${msg.params.exceptionDetails.exception?.description || ""}`);
      }
      if (msg.sessionId && msg.method === "Runtime.consoleAPICalled" && ["error", "warning"].includes(msg.params.type)) {
        events.push(`${msg.params.type}:${msg.params.args.map(arg => arg.value || arg.description || "").join(" ")}`);
      }
    };

    function send(method, params = {}, sessionId, timeout = 12000) {
      return new Promise((resolveSend, rejectSend) => {
        const call = { id: ++id, method, params };
        if (sessionId) call.sessionId = sessionId;
        const timer = setTimeout(() => {
          pending.delete(call.id);
          rejectSend(new Error(`${method} timeout`));
        }, timeout);
        pending.set(call.id, msg => {
          clearTimeout(timer);
          if (msg.error) rejectSend(new Error(`${method}: ${msg.error.message}`));
          else resolveSend(msg);
        });
        browserWs.send(JSON.stringify(call));
      });
    }

    try {
      const target = await send("Target.createTarget", { url: "about:blank" });
      const targetId = target.result.targetId;
      const attach = await send("Target.attachToTarget", { targetId, flatten: true });
      const sessionId = attach.result.sessionId;
      await send("Runtime.enable", {}, sessionId);
      await send("Page.enable", {}, sessionId);
      // The portable proof is offline. Historical real-GPU proof is a separate artifact.
      await send("Page.addScriptToEvaluateOnNewDocument", { source: "Object.defineProperty(navigator, 'gpu', {value: undefined});" }, sessionId);
      await send("Emulation.setDeviceMetricsOverride", { width: 1440, height: 1100, deviceScaleFactor: 1, mobile: false }, sessionId);
      await send("Page.navigate", { url: pageUrl }, sessionId);
      const output = await fn({ send, sessionId, events, targetId, version });
      await send("Target.closeTarget", { targetId }).catch(() => {});
      browserWs.close();
      return output;
    } catch (error) {
      browserWs.close();
      throw error;
    }
  } finally {
    await stopOwnedChrome(proc);
    try {
      rmSync(profile, { recursive: true, force: true });
    } catch {
      // Chrome can release profile files slightly after SIGTERM; cleanup is not test evidence.
    }
  }
}

function writeScreenshot(name, data) {
  const file = join(proofDir, name);
  writeFileSync(file, Buffer.from(data, "base64"));
  return file;
}

function screenshotName(index, id) {
  return `${String(index + 1).padStart(2, "0")}-${id}.png`;
}

async function main() {
  const html = readFileSync(htmlPath, "utf8");
  const moduleCode = extractModule(html);

  assert("html file exists", existsSync(htmlPath), "missing classroom walkthrough HTML", { htmlPath });
  assert("html is substantial", html.length > 90000, "HTML is unexpectedly small", { bytes: html.length });
  assert("html is ASCII", [...html].every(char => char.charCodeAt(0) <= 127), "non-ASCII characters found");
  assert("no TODO/FIXME markers", !/TODO|FIXME/.test(html), "unfinished marker found");
  assert("no obvious secret literals", !/(sk-[A-Za-z0-9]|BEGIN [A-Z ]*PRIVATE KEY|AKIA[0-9A-Z]{16}|password\s*=|secret\s*=|token\s*=)/.test(html), "secret-like literal found");

  const moduleFile = join(proofDir, "module-check.mjs");
  writeFileSync(moduleFile, moduleCode);
  const syntax = spawnSync(process.execPath, ["--check", moduleFile], { encoding: "utf8" });
  assert("module syntax", syntax.status === 0, "module script syntax failed", { stderr: syntax.stderr.trim() });

  const requiredSections = ["home", "map", "steps", "files", "generated", "uses", "teacher", "glossary", "questions"];
  for (const id of requiredSections) {
    assert(`section #${id}`, html.includes(`id="${id}"`), `missing section ${id}`);
  }

  const requiredCopy = [
    "10-year-old answer",
    "Say it to a kid",
    "Teacher bridge",
    "30-second demo",
    "Common mix-up",
    "Question Engine",
    "FABLES_HARNESS",
    "verify_bundle.py",
    "GENESIS_PROMPT.md",
    "DanManREAL DESIGN",
    "Three.js WebGPU running"
  ];
  for (const phrase of requiredCopy) {
    assert(`copy includes ${phrase}`, html.includes(phrase), `missing phrase: ${phrase}`);
  }

  const designTokens = [
    "--dmr-brand-blue: #197cc1",
    "--dmr-brand-green: #1fb06f",
    "--dmr-paint-blue: #12b7f8",
    "--dmr-paint-green: #26f296",
    "--dmr-frame-metal: #755934",
    "--dmr-frame-metal-bright: #b18b4e",
    "--dmr-jewel-blue: #0cb6f8",
    "--dmr-jewel-depth: #156faa",
    "--dmr-bg-abyss: #030c09",
    "--dmr-frame-charcoal: #1d2322"
  ];
  for (const token of designTokens) {
    assert(`DanManREAL token ${token.split(":")[0]}`, html.includes(token), `missing token ${token}`);
  }
  assert("DanManREAL frame primitives", count(/metal-frame/g, html) >= 5 && html.includes("id=\"dmr-goo\"") && html.includes("paint-rail") && html.includes("jewel"), "missing frame/paint/jewel primitives");
  assert("Three.js WebGPU wiring", html.includes('"three/webgpu"') && html.includes("new THREE.WebGPURenderer") && html.includes("navigator.gpu"), "missing WebGPU wiring");

  const server = startServer();
  const port = await listen(server);
  const url = `http://127.0.0.1:${port}/FABLES_INFLUENCE_CLASSROOM_WALKTHROUGH.html`;
  record("local server", { url });

  try {
    for (const route of ["/.git/config", "/README.md", "/.env", "/%2e%2e%2fother", "/%ZZ"]) {
      const response = await fetch(`http://127.0.0.1:${port}${route}`);
      assert(`server refuses ${route}`, [400, 404].includes(response.status), "server exposed an unrelated path");
    }
    const runtime = await withChrome(url, async ({ send, sessionId, events }) => {
      await send("Runtime.evaluate", {
        expression: `new Promise(resolve => {
          let tries = 0;
          const tick = () => {
            tries++;
            const ready = window.__FABLES_CLASSROOM_READY && document.querySelectorAll('.stage-button').length === 12 && document.querySelectorAll('.term-card').length === 9;
            if (ready || tries > 150) resolve({ ready: !!ready, tries });
            else setTimeout(tick, 100);
          };
          tick();
        })`,
        awaitPromise: true,
        returnByValue: true
      }, sessionId, 22000);

      const stateExpr = `(() => {
        const stageResults = [...document.querySelectorAll('.stage-button')].map(button => {
          button.click();
          return { id: button.dataset.answer, title: document.querySelector('#answerTitle')?.textContent || '' };
        });
        const fileResults = [...document.querySelectorAll('.file-card')].map(button => {
          button.click();
          return document.querySelector('#answerTitle')?.textContent || '';
        });
        const generatedResults = [...document.querySelectorAll('.generated-card')].map(button => {
          button.click();
          return document.querySelector('#answerTitle')?.textContent || '';
        });
        const useResults = [...document.querySelectorAll('.use-card')].map(button => {
          button.click();
          return document.querySelector('#answerTitle')?.textContent || '';
        });
        const term = [...document.querySelectorAll('.term-card')].find(card => card.textContent.includes('Verifier'));
        term?.click();
        const glossaryVerifier = {
          title: document.querySelector('#glossaryTitle')?.textContent || '',
          kid: document.querySelector('#glossaryKid')?.textContent || '',
          demo: document.querySelector('#glossaryDemo')?.textContent || '',
          mistake: document.querySelector('#glossaryMistake')?.textContent || '',
          sources: document.querySelectorAll('#glossarySources .source-pill').length,
          challenges: document.querySelectorAll('#glossaryChallenges .challenge-chip').length,
          answerTitle: document.querySelector('#answerTitle')?.textContent || ''
        };
        document.querySelector('#questionSearch').value = 'wargame';
        document.querySelector('#questionSearch').dispatchEvent(new Event('input', { bubbles: true }));
        const firstQuestion = document.querySelector('.question-chip');
        firstQuestion?.click();
        const questionResult = {
          visible: document.querySelectorAll('.question-chip').length,
          title: document.querySelector('#answerTitle')?.textContent || '',
          kicker: document.querySelector('#answerKicker')?.textContent || ''
        };
        const sections = [...document.querySelectorAll('section[id]')].map(section => ({ id: section.id, top: Math.round(section.getBoundingClientRect().top + window.scrollY), height: Math.round(section.getBoundingClientRect().height) }));
        return JSON.stringify({
          ready: window.__FABLES_CLASSROOM_READY || null,
          backend: window.__DMR_FIELD_BACKEND || null,
          renderer: document.querySelector('#rendererStatus')?.textContent || null,
          canvas: [...document.querySelectorAll('canvas')].map(c => ({ w: c.width, h: c.height, clientW: c.clientWidth, clientH: c.clientHeight })),
          counts: {
            sections: document.querySelectorAll('section[id]').length,
            stages: document.querySelectorAll('.stage-button').length,
            files: document.querySelectorAll('.file-card').length,
            generated: document.querySelectorAll('.generated-card').length,
            uses: document.querySelectorAll('.use-card').length,
            lessons: document.querySelectorAll('.lesson-step').length,
            terms: document.querySelectorAll('.term-card').length,
            topics: document.querySelectorAll('#topicList .small-chip').length,
            visibleQuestions: document.querySelectorAll('.question-chip').length,
            questionCount: (window.__FABLES_CLASSROOM_READY || {}).questionCount || null
          },
          stageResults,
          fileResults,
          generatedResults,
          useResults,
          glossaryVerifier,
          questionResult,
          sections
        });
      })()`;
      const evaluated = await send("Runtime.evaluate", { expression: stateExpr, returnByValue: true }, sessionId, 18000);
      const state = JSON.parse(evaluated.result.result.value);

      const screenshots = [];
      for (const [index, section] of state.sections.entries()) {
        const y = Math.max(0, section.top - 40);
        const height = Math.min(1200, Math.max(760, section.height + 80));
        await send("Runtime.evaluate", { expression: `window.scrollTo(0, ${y})` }, sessionId);
        await new Promise(resolveWait => setTimeout(resolveWait, 220));
        const shot = await send("Page.captureScreenshot", {
          format: "png",
          fromSurface: true,
          captureBeyondViewport: true,
          clip: { x: 0, y, width: 1440, height, scale: 1 }
        }, sessionId, 15000);
        screenshots.push({
          id: section.id,
          file: writeScreenshot(screenshotName(index, section.id), shot.result.data)
        });
      }

      return { state, events, screenshots };
    });

    const { state, events, screenshots } = runtime;
    assert("runtime no console errors", events.length === 0, "runtime console/exception events found", { events });
    assert("runtime ready object", state.ready?.stageCount === 12 && state.ready?.questionCount === 500, "ready object missing expected counts", { ready: state.ready });
    assert("runtime WebGPU or explicit fallback", state.ready?.backend === "webgpu" || state.ready?.backend === "fallback", "missing backend", { backend: state.ready?.backend });
    assert("renderer text", /WebGPU|Fallback/.test(state.renderer || ""), "renderer status not populated", { renderer: state.renderer });
    if (state.ready?.backend === "webgpu") {
      assert("WebGPU canvas nonzero", state.canvas.some(c => c.w > 300 && c.h > 300 && c.clientW > 300 && c.clientH > 300), "WebGPU canvas dimensions too small", { canvas: state.canvas });
    }
    assert("runtime counts", state.counts.sections === 9 && state.counts.stages === 12 && state.counts.files === 12 && state.counts.generated === 8 && state.counts.uses === 18 && state.counts.lessons === 7 && state.counts.terms === 9 && state.counts.topics === 11 && state.counts.questionCount === 500, "unexpected rendered counts", state.counts);
    assert("all stage clicks answer", state.stageResults.length === 12 && state.stageResults.every(item => item.title.length > 0), "stage click answer missing", { stageResults: state.stageResults });
    assert("all file cards answer", state.fileResults.length === 12 && state.fileResults.every(Boolean), "file card answer missing");
    assert("all generated cards answer", state.generatedResults.length === 8 && state.generatedResults.every(Boolean), "generated card answer missing");
    assert("all use cases answer", state.useResults.length === 18 && state.useResults.every(Boolean), "use case answer missing");
    assert("glossary word lab interaction", state.glossaryVerifier.title === "Verifier" && state.glossaryVerifier.sources >= 2 && state.glossaryVerifier.challenges === 3 && /referee|checker/i.test(state.glossaryVerifier.kid), "glossary verifier interaction failed", state.glossaryVerifier);
    assert("question search interaction", state.questionResult.visible > 0 && state.questionResult.kicker === "Student question" && state.questionResult.title.toLowerCase().includes("wargame"), "question search/click failed", state.questionResult);
    assert("all section screenshots saved", screenshots.length === 9 && screenshots.every(item => existsSync(item.file) && statSync(item.file).size > 20000), "missing or tiny section screenshot", {
      screenshots: screenshots.map(item => ({ id: item.id, file: item.file, bytes: existsSync(item.file) ? statSync(item.file).size : 0 }))
    });
  } finally {
    server.close();
  }

  const proof = {
    htmlPath,
    proofDir,
    passed: results.length,
    results
  };
  writeFileSync(join(proofDir, "verification-results.json"), `${JSON.stringify(proof, null, 2)}\n`);
  console.log(JSON.stringify(proof, null, 2));
}

main().catch(error => {
  const failure = {
    status: "FAIL",
    message: error.message,
    details: error.details || null,
    passedBeforeFailure: results
  };
  console.error(JSON.stringify(failure, null, 2));
  process.exit(1);
});
