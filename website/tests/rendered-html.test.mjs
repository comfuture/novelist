import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);

async function render(pathname = "/") {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}-${pathname}`);
  const { default: worker } = await import(workerUrl.href);
  return worker.fetch(
    new Request(`https://novelist.example${pathname}`, { headers: { accept: "text/html" } }),
    { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
    { waitUntil() {}, passThroughOnException() {} },
  );
}

test("renders the Novelist landing page and installation path", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  const html = await response.text();
  assert.match(html, /<title>Novelist — Build continuity-safe novels<\/title>/i);
  assert.match(html, /Keep the whole novel in view/);
  assert.match(html, /codex plugin add novelist@openai-curated-remote/);
  assert.match(html, /claude plugin install novelist@novelist/);
  assert.match(html, /agy plugins install https:\/\/github\.com\/comfuture\/novelist/);
  assert.match(html, /create-scaffold\.sh/);
  assert.match(html, /worldbuilding, characters, materials, plots/);
  assert.match(html, /Nine focused workflows/);
  assert.match(html, /Review analytically/);
  assert.match(html, /only when you delegate the full journey/);
  assert.doesNotMatch(html, /A Codex plugin for long-form fiction/);
  assert.match(html, /Created by Changkyun Kim/);
  assert.doesNotMatch(html, /codex-preview|react-loading-skeleton/);
});

for (const [pathname, heading] of [
  ["/privacy", "Privacy Policy"],
  ["/terms", "Terms of Use"],
  ["/support", "Support"],
  ["/releases", "Release Notes"],
]) {
  test(`renders ${pathname}`, async () => {
    const response = await render(pathname);
    assert.equal(response.status, 200);
    const html = await response.text();
    assert.match(html, new RegExp(`<h1[^>]*>${heading}<\\/h1>`, "i"));
    assert.match(html, /comfuture@gmail\.com/);
  });
}

test("renders the breaking-layout migration note", async () => {
  const response = await render("/releases");
  assert.equal(response.status, 200);
  const html = await response.text();
  assert.match(html, /Novelist 0\.1\.1/);
  assert.match(html, /clone-first scaffold users/);
  assert.match(html, /MIGRATION\.md/);
});

test("renders the analytical-review release boundary", async () => {
  const response = await render("/releases");
  assert.equal(response.status, 200);
  const html = await response.text();
  assert.match(html, /Novelist 0\.2\.0 — Analytical Review/);
  assert.match(html, /Novelist 0\.2\.0 expands the plugin to nine skills/);
  assert.match(html, /only to fully autonomous start-to-publication work/);
  assert.match(html, /deterministic EPUB publication/);
});

test("ships real brand assets and removes the starter preview", async () => {
  await access(new URL("public/logo.png", root));
  await assert.rejects(access(new URL("app/_sites-preview", root)));
  const packageJson = await readFile(new URL("package.json", root), "utf8");
  assert.doesNotMatch(packageJson, /react-loading-skeleton/);
});
