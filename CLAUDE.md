# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Two independent, self-contained, single-file HTML/Three.js apps. There is no build step, no package manager, no bundler, and no test suite — each `.html` file is the entire app (markup, CSS, and JS in one file) and is opened directly or served as a static file.

- `gemini.html` — "Austrian edition": 12 Austrians (Mozart, Freud, Schwarzenegger, Kaiserin Elisabeth/"Sisi", Schrödinger, Klimt, Schubert, Johann Strauss (Sohn), Hedy Lamarr, Falco, Landsteiner, Wittgenstein). German UI. Portraits are embedded as base64 (fully offline-capable). Names/fields are intentionally hidden until a face is clicked (deliberate UX choice — don't add them back onto the medallion texture). PWA-installable (`manifest.json`, `sw.js`, `icons/`).
- `twelve-legends.html` — original edition (Einstein, Curie, Newton, Darwin, Tesla, Lovelace, Galileo, Hawking, Bohr, Franklin, Turing, Feynman). English UI. Portraits are fetched live from Wikimedia Commons at load time (no embedded images). Hover shows a tooltip instead of a click-to-open plaque.

The two files share no code — changes to one do not affect the other. Don't assume a fix in one is automatically needed in the other.

## Commands

No lint/build/test commands exist in this repo. The only "workflow" is:

```bash
# Serve locally (required for PWA install, service worker, and manifest/icon
# fetches to work — file:// is fine for just eyeballing the 3D scene, but
# service-worker registration silently no-ops without http(s)/localhost)
cd /Users/haraldbeker/Dodekaeder
python3 -m http.server 8080
# open http://localhost:8080/gemini.html or /twelve-legends.html
```

To regenerate/re-embed the Austrian portraits in `gemini.html` (e.g. to swap one person's photo):

```bash
python3 build_austrians.py
```

This downloads portraits from Wikipedia, crops/enhances them, and rewrites both the `PEOPLE` array and `BASE64_IMAGES` block in `gemini.html` via regex — it will clobber any hand-edits made directly to those two blocks in `gemini.html` if rerun.

There is no automated test suite. Verification in this repo has always been manual: serve the file locally, drive it with a browser tool (screenshot + `read_console_messages`), and visually check the 3D render. When changing geometry/UV/animation code, do this rather than assuming the math is right from reading it.

## Architecture notes that aren't obvious from a quick read

**Custom per-face UV mapping on `THREE.DodecahedronGeometry`.** Both apps need each of the dodecahedron's 12 pentagonal faces to show a *undistorted circular photo medallion*, but Three.js's built-in UVs for `DodecahedronGeometry` are a spherical projection, not a per-face planar one. Both files therefore discard the default UVs/normals and rebuild them from the raw vertex positions. The non-obvious, empirically-verified fact this depends on: `DodecahedronGeometry`'s non-indexed position buffer lays out each face as 3 fan triangles of 9 vertices, and the **shared fan vertex sits at buffer slots 2, 5, 8 — not slot 0**. (It's tempting to assume slot 0 from a superficial read of the Three.js source; that assumption produces silently-wrong, mirrored/streaked textures — this was an actual bug caught and fixed in this repo.) If you ever touch this geometry code, re-verify the vertex layout against the live `THREE.DodecahedronGeometry` output in a browser console rather than trusting a re-derivation from memory.

**Safe content radius inside a pentagon face.** Because a face is a pentagon, not a circle, content drawn on its texture (the photo circle, any rings) must stay within roughly the pentagon's inradius, not its circumradius, or it gets clipped on some rotations but not others (looks fine in one orientation, clipped in another — easy to miss if you only check one static screenshot). Both files derive/comment this radius near the UV-mapping code; keep new decorative elements inside it.

**`gemini.html` internals**: `PEOPLE` (array of `{id, name, shortName, field, years, desc, wiki, color, cropY}`) drives everything — `BASE64_IMAGES[id]` supplies the embedded photo, `generateFaceTexture(person, img)` draws the per-face canvas texture, click handling opens the bottom "plaque" (name/field/years/desc/Wikipedia link) via `showPlaque`/`hidePlaque`, and `rotateToFace` does a quaternion slerp to bring a clicked/selected face to face the camera. Idle auto-rotation is a deliberate multi-axis "tumble" (sum of a few slow, incommensurate sine waves per axis in the render loop), not a single fixed-axis spin — don't simplify it back to `rotation.y += const`.

**Licensing**: all 12 Austrian portraits are public domain or CC BY-SA except Falco's, which is a fair-use press photo from English Wikipedia (not Commons). Fine for local/personal use; flag it if this is ever deployed publicly, and see `build_austrians.py` if it needs swapping.

**Social preview tags in `gemini.html`** (`og:*`/`twitter:*` in `<head>`) point at a placeholder domain (`https://example.com/gemini/...`) — these need to be updated to the real deployed URL before the link preview will actually work when shared, since crawlers fetch them directly and can't reach local disk.

**Stray/unused files**: `images_b64.json` at the repo root is a leftover intermediate from an earlier build step and isn't read by anything currently. `images/` contains both the 12 Austrian source photos (used) and the original 12 non-Austrian portraits from before `gemini.html` was re-themed (no longer referenced by either HTML file, since `twelve-legends.html` fetches its own images live from the network).

## Editor / agent config found in this environment

A **Gemini CLI** config exists at the user level (`~/.gemini/settings.json`, `~/.gemini/GEMINI.md`) — not project-specific to this repo. It was not read (per policy, foreign-agent configs aren't inspected directly). If you want to bring anything from it (MCP servers, slash commands, subagents, skills, instructions) into Claude Code, run `/import` to scan and list what's importable, then `/import --yes=<digest>` to apply.
