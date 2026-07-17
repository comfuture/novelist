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
  assert.match(html, /codex plugin marketplace add comfuture\/novelist --ref main/);
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

test("ships real brand assets and removes the starter preview", async () => {
  await access(new URL("public/logo.png", root));
  await assert.rejects(access(new URL("app/_sites-preview", root)));
  const packageJson = await readFile(new URL("package.json", root), "utf8");
  assert.doesNotMatch(packageJson, /react-loading-skeleton/);
});
