#!/usr/bin/env python3
"""Download, enhance and embed 12 famous Austrians into gemini.html"""

import os, sys, json, base64, time, ssl, urllib.request, urllib.parse, re
from pathlib import Path

# ── PIL ──────────────────────────────────────────────────────────────────────
try:
    from PIL import Image, ImageEnhance, ImageFilter, ImageOps
except ImportError:
    os.system("uv pip install Pillow --quiet")
    from PIL import Image, ImageEnhance, ImageFilter, ImageOps

import io

IMAGES_DIR = Path("/Users/haraldbeker/Dodekaeder/images")
IMAGES_DIR.mkdir(exist_ok=True)

# ── 12 Famous Austrians ──────────────────────────────────────────────────────
AUSTRIANS = [
    {
        "id": "mozart",
        "name": "Wolfgang Amadeus Mozart",
        "shortName": "Mozart",
        "field": "Classical Composition",
        "years": "1756 – 1791",
        "desc": "Prolific genius of the Classical era, composing over 800 works including symphonies, operas, and chamber music before his death at 35.",
        "wiki": "https://en.wikipedia.org/wiki/Wolfgang_Amadeus_Mozart",
        "color": "#2d4a6e",
        "cropY": 0.40,
        "wiki_title": "Wolfgang_Amadeus_Mozart",
    },
    {
        "id": "freud",
        "name": "Sigmund Freud",
        "shortName": "Freud",
        "field": "Psychoanalysis",
        "years": "1856 – 1939",
        "desc": "Founder of psychoanalysis, he developed groundbreaking theories of the unconscious mind, dreams, and the structure of the psyche.",
        "wiki": "https://en.wikipedia.org/wiki/Sigmund_Freud",
        "color": "#3b2a4a",
        "cropY": 0.40,
        "wiki_title": "Sigmund_Freud",
    },
    {
        "id": "schwarzenegger",
        "name": "Arnold Schwarzenegger",
        "shortName": "Schwarzenegger",
        "field": "Actor & Politician",
        "years": "1947 –",
        "desc": "Seven-time Mr. Olympia, Hollywood action icon (The Terminator), and 38th Governor of California — the ultimate self-made man.",
        "wiki": "https://en.wikipedia.org/wiki/Arnold_Schwarzenegger",
        "color": "#1e3d2f",
        "cropY": 0.38,
        "wiki_title": "Arnold_Schwarzenegger",
    },
    {
        "id": "sisi",
        "name": "Empress Elisabeth",
        "shortName": "Sisi",
        "field": "Empress of Austria",
        "years": "1837 – 1898",
        "desc": "The beloved 'Sisi', Empress of Austria and Queen of Hungary, renowned for her beauty, independence, and tragic assassination in Geneva.",
        "wiki": "https://en.wikipedia.org/wiki/Empress_Elisabeth_of_Austria",
        "color": "#5a2d4a",
        "cropY": 0.36,
        "wiki_title": "Empress_Elisabeth_of_Austria",
    },
    {
        "id": "schrodinger",
        "name": "Erwin Schrödinger",
        "shortName": "Schrödinger",
        "field": "Quantum Physics",
        "years": "1887 – 1961",
        "desc": "Nobel Prize-winning physicist who formulated the Schrödinger equation and devised the famous cat thought experiment that challenged quantum reality.",
        "wiki": "https://en.wikipedia.org/wiki/Erwin_Schr%C3%B6dinger",
        "color": "#1a3a5c",
        "cropY": 0.40,
        "wiki_title": "Erwin_Schrödinger",
    },
    {
        "id": "klimt",
        "name": "Gustav Klimt",
        "shortName": "Klimt",
        "field": "Symbolist Painting",
        "years": "1862 – 1918",
        "desc": "Leader of the Vienna Secession movement, famous for his sensuous gold-leaf masterpieces including 'The Kiss' and the Beethoven Frieze.",
        "wiki": "https://en.wikipedia.org/wiki/Gustav_Klimt",
        "color": "#7a5a1a",
        "cropY": 0.38,
        "wiki_title": "Gustav_Klimt",
    },
    {
        "id": "schubert",
        "name": "Franz Schubert",
        "shortName": "Schubert",
        "field": "Romantic Composition",
        "years": "1797 – 1828",
        "desc": "Prolific Viennese composer who created over 600 lieder, 9 symphonies, and extraordinary chamber music in just 31 years of life.",
        "wiki": "https://en.wikipedia.org/wiki/Franz_Schubert",
        "color": "#2d3a5c",
        "cropY": 0.38,
        "wiki_title": "Franz_Schubert",
    },
    {
        "id": "strauss",
        "name": "Johann Strauss II",
        "shortName": "Strauss II",
        "field": "Waltz & Operetta",
        "years": "1825 – 1899",
        "desc": "The 'Waltz King' of Vienna, composer of 'The Blue Danube', 'Tales from the Vienna Woods', and the beloved operetta 'Die Fledermaus'.",
        "wiki": "https://en.wikipedia.org/wiki/Johann_Strauss_II",
        "color": "#4a1a2d",
        "cropY": 0.38,
        "wiki_title": "Johann_Strauss_II",
    },
    {
        "id": "lamarr",
        "name": "Hedy Lamarr",
        "shortName": "Lamarr",
        "field": "Actress & Inventor",
        "years": "1914 – 2000",
        "desc": "Hollywood star and self-taught inventor whose frequency-hopping spread-spectrum technology co-patented in 1942 laid the groundwork for Wi-Fi and Bluetooth.",
        "wiki": "https://en.wikipedia.org/wiki/Hedy_Lamarr",
        "color": "#4a2d1a",
        "cropY": 0.36,
        "wiki_title": "Hedy_Lamarr",
    },
    {
        "id": "falco",
        "name": "Falco",
        "shortName": "Falco",
        "field": "Pop & Rock Music",
        "years": "1957 – 1998",
        "desc": "The only German-language artist to reach #1 in the US. 'Rock Me Amadeus' made him a global star and a beloved icon of Austrian pop culture.",
        "wiki": "https://en.wikipedia.org/wiki/Falco_(musician)",
        "color": "#1a2d4a",
        "cropY": 0.38,
        "wiki_title": "Falco_(musician)",
    },
    {
        "id": "landsteiner",
        "name": "Karl Landsteiner",
        "shortName": "Landsteiner",
        "field": "Immunology & Medicine",
        "years": "1868 – 1943",
        "desc": "Discoverer of blood groups A, B, O and AB, enabling safe blood transfusions. Nobel Prize in Physiology or Medicine (1930).",
        "wiki": "https://en.wikipedia.org/wiki/Karl_Landsteiner",
        "color": "#1a3d2d",
        "cropY": 0.40,
        "wiki_title": "Karl_Landsteiner",
    },
    {
        "id": "wittgenstein",
        "name": "Ludwig Wittgenstein",
        "shortName": "Wittgenstein",
        "field": "Philosophy of Language",
        "years": "1889 – 1951",
        "desc": "One of the 20th century's most influential philosophers, who transformed analytic philosophy twice — first with the Tractatus, then with Philosophical Investigations.",
        "wiki": "https://en.wikipedia.org/wiki/Ludwig_Wittgenstein",
        "color": "#2d2d3a",
        "cropY": 0.40,
        "wiki_title": "Ludwig_Wittgenstein",
    },
]

# ── Downloader ────────────────────────────────────────────────────────────────
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

def fetch(url, retries=3):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
                return r.read()
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                raise e

def get_wiki_thumb(title, width=320):
    """Get thumbnail URL from Wikipedia REST API, strip UTM params, try fallback sizes"""
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
    data = json.loads(fetch(url))
    thumb = data.get("thumbnail", {}).get("source", "")
    original = data.get("originalimage", {}).get("source", "")

    # Try different sizes — Wikimedia only accepts certain values
    for size in [320, 256, 480, 640, 200]:
        if thumb:
            # Rewrite size and strip query string
            t = re.sub(r'/\d+px-', f'/{size}px-', thumb)
            t = t.split('?')[0]
            try:
                fetch(t)  # probe
                return t
            except Exception:
                continue

    # Fall back to original image (unscaled)
    if original:
        return original.split('?')[0]
    return ""

def download_portrait(person):
    dest = IMAGES_DIR / f"{person['id']}.jpg"
    if dest.exists() and dest.stat().st_size > 5000:
        print(f"  ✓ {person['id']} already exists, skipping download")
        return dest

    print(f"  ↓ Downloading {person['name']}...")
    thumb = get_wiki_thumb(person["wiki_title"], width=400)
    if not thumb:
        print(f"    ✗ No thumbnail found for {person['name']}")
        return None

    print(f"    URL: {thumb}")
    raw = fetch(thumb)
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    img.save(str(dest), "JPEG", quality=90)
    time.sleep(1.2)
    return dest

# ── Image enhancement ─────────────────────────────────────────────────────────
def enhance_portrait(path, crop_y=0.40):
    """Crop around the face (with headroom margin) and boost contrast/saturation.

    Two lessons baked in here from a prior bad batch:
    - The crop square's side is min(w*0.95, h), not a fixed 0.8*w — on a
      landscape-oriented source (wide, short) the old fixed width-based side
      could exceed the image's own height, forcing a non-square crop that
      then got stretched by the resize below.
    - zoom=0.95 (not ~0.8) leaves real headroom above the hair. The page
      renders this image ~10% larger than its circular frame (so the focal
      point can be centered without exposing an edge), so a tight crop with
      no margin gets its own hairline pushed outside the visible circle.
    """
    img = Image.open(str(path)).convert("RGB")
    w, h = img.size

    zoom = 0.95
    side = min(int(w * zoom), h)
    crop_x1 = int((w - side) / 2)
    crop_x2 = crop_x1 + side
    face_center_px = int(h * crop_y)
    half = int(side / 2)
    crop_y1 = max(0, min(face_center_px - half, h - side))
    crop_y2 = crop_y1 + side
    img = img.crop((crop_x1, crop_y1, crop_x2, crop_y2))
    img = img.resize((640, 640), Image.LANCZOS)

    # Enhance
    img = ImageEnhance.Contrast(img).enhance(1.45)
    img = ImageEnhance.Brightness(img).enhance(1.05)
    img = ImageEnhance.Color(img).enhance(1.25)
    img = ImageEnhance.Sharpness(img).enhance(1.50)

    img.save(str(path), "JPEG", quality=88)
    return path

# ── Base64 embed ──────────────────────────────────────────────────────────────
def to_b64(path):
    ext = Path(path).suffix.lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{data}"

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=== Downloading & processing 12 famous Austrians ===\n")

    b64_map = {}
    for person in AUSTRIANS:
        print(f"[{person['id']}] {person['name']}")
        try:
            path = download_portrait(person)
            if path:
                enhance_portrait(path, person["cropY"])
                b64_map[person["id"]] = to_b64(path)
                print(f"    ✓ Done ({Path(path).stat().st_size // 1024} KB)")
        except Exception as e:
            print(f"    ✗ ERROR: {e}")

    print(f"\nEmbedded {len(b64_map)}/12 portraits")

    if len(b64_map) < 12:
        print("Some portraits missing — aborting HTML update.")
        sys.exit(1)

    # ── Patch gemini.html ────────────────────────────────────────────────────
    html_path = "/Users/haraldbeker/Dodekaeder/gemini.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Replace PEOPLE array
    # Note: cropY here is always 0.5, not p['cropY'] — enhance_portrait() already
    # re-centers the face to the middle of the saved square image using that
    # value, so reusing it at render time would double-apply the offset.
    people_js_entries = []
    for p in AUSTRIANS:
        entry = f"""    {{
      id: "{p['id']}",
      name: "{p['name']}",
      shortName: "{p['shortName']}",
      field: "{p['field']}",
      years: "{p['years']}",
      desc: "{p['desc']}",
      wiki: "{p['wiki']}",
      color: "{p['color']}",
      cropY: 0.5
    }}"""
        people_js_entries.append(entry)
    new_people = "  const PEOPLE = [\n" + ",\n".join(people_js_entries) + "\n  ];"

    html = re.sub(
        r'const PEOPLE = \[.*?\];',
        new_people,
        html,
        flags=re.DOTALL
    )

    # 2. Replace BASE64_IMAGES block
    b64_lines = []
    for pid, b64 in b64_map.items():
        b64_lines.append(f'    {pid}: "{b64}"')
    new_b64_block = "  const BASE64_IMAGES = {\n" + ",\n".join(b64_lines) + "\n  };"

    html = re.sub(
        r'const BASE64_IMAGES = \{.*?\};',
        new_b64_block,
        html,
        flags=re.DOTALL
    )

    # 3. Update page title
    html = html.replace(
        "<title>Twelve Legends · Dodecahedron</title>",
        "<title>Twelve Famous Austrians · Dodecahedron</title>"
    )
    html = html.replace(
        "Twelve Legends",
        "Twelve Famous Austrians"
    )

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    size_kb = os.path.getsize(html_path) // 1024
    print(f"\n✅ gemini.html updated! ({size_kb} KB)")

if __name__ == "__main__":
    main()
