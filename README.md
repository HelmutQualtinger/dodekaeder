# Dodekaeder

Two self-contained, single-file 3D dodecahedron apps built with [Three.js](https://threejs.org/). Each face of the solid is a circular portrait medallion; drag to rotate, click a face for details.

**Live:** https://helmutqualtinger.github.io/dodekaeder/

## Files

| File | What it is |
|---|---|
| `gemini.html` | **Austrian edition.** Mozart, Freud, Schwarzenegger, Kaiserin Elisabeth ("Sisi"), Schrödinger, Klimt, Schubert, Johann Strauss (Sohn), Hedy Lamarr, Falco, Landsteiner, Wittgenstein. Portraits are embedded as base64 (fully offline-capable). German UI. Names are hidden until you click a face. Installable as a PWA. |
| `twelve-legends.html` | **Original edition.** Einstein, Curie, Newton, Darwin, Tesla, Lovelace, Galileo, Hawking, Bohr, Franklin, Turing, Feynman. Portraits are fetched live from Wikimedia Commons at load time. English UI, hover tooltips instead of a click plaque. |
| `build_austrians.py` | Downloads portraits from Wikipedia, crops/enhances them, and (re-)embeds them as base64 into `gemini.html`. Only needed if you want to swap one of the 12 Austrians for someone else, or regenerate a portrait. |
| `manifest.json`, `sw.js`, `icons/` | PWA support for `gemini.html` — web app manifest, offline service worker, and app icons (192/512/512-maskable/apple-touch/favicon). |
| `images/` | Portrait JPGs/PNGs used as the source for `gemini.html`'s embedded base64, plus `social-preview.jpg` (the Open Graph / Twitter Card image). |
| `images_b64.json` | Leftover intermediate file from an earlier build step — not read by anything currently. Safe to ignore or delete. |

## Running it

These are plain HTML files — double-click to open in a browser, or for the full experience (PWA install, service worker, social-preview tags all need `http(s)`, not `file://`):

```bash
cd /Users/haraldbeker/Dodekaeder
python3 -m http.server 8080
# then open http://localhost:8080/gemini.html
```

## Installing `gemini.html` as an app (PWA)

No app store, no build tooling, no developer account — this works because the page ships a web app manifest, a set of icons, and a service worker.

- **Android (Chrome):** open the page → menu (⋮) → "App installieren" / "Zum Startbildschirm hinzufügen".
- **iOS (Safari):** open the page → Share icon → "Zum Home-Bildschirm".

Once installed it launches full-screen (no browser chrome) and works offline — all 12 portraits are embedded in the HTML itself, so only the Google Fonts stylesheet and the Three.js library need to have been fetched once (the service worker caches them after first load).

> Real native `.apk` / `.ipa` store builds are a different, much bigger undertaking — they need Xcode, Android Studio, a paid Apple Developer account, and a Google Play account, none of which can be set up from here. The PWA above is the app-like install path that works today with no accounts.

## Social media preview (Open Graph / Twitter Card)

`gemini.html`'s `<head>` has `og:*` and `twitter:*` tags pointing at `https://helmutqualtinger.github.io/dodekaeder/...` and `images/social-preview.jpg` (a real screenshot of the app, 1200×630). If this ever moves to a different domain, update those tags accordingly.

After any change to the deployed page, re-check the preview (both cache aggressively, so force a re-scrape):
- Facebook/WhatsApp/LinkedIn: https://developers.facebook.com/tools/debug/
- X/Twitter: https://cards-dev.twitter.com/validator

## Licensing note on portraits

All 12 Austrian portraits are public domain or CC BY-SA (Wikimedia Commons), **except Falco's**, which is a fair-use press photo hosted on English Wikipedia rather than Commons. Fine for personal/local use; if you deploy this publicly, consider swapping it via `build_austrians.py` for a freely-licensed alternative.
