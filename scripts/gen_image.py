import sys, os, json, base64, io, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def key():
    for line in open(os.path.join(ROOT, ".env.local"), encoding="utf-8"):
        if line.startswith("GEMINI_IMAGE_KEY="):
            return line.strip().split("=", 1)[1]

PROMPT = """A clean, professional graphic design template for an educational advertisement for Geoje island (a coastal shipbuilding city in Korea). Square image with rounded corners on a slightly larger pale sky-blue background with a subtle block pattern. Color palette: deep navy blue, sea blue, white, with small coral-orange accents. Scene style: {motif}. Keep the scene soft, flat and geometric, and keep it away from the center so the text stays perfectly legible. The top text in bold navy brackets reads "[{school}]". Below it is the large, very bold navy central title "1:1 화상과외". Below the main title is smaller navy text "내신 관리 | 30분 무료체험". A clean white horizontal bar at the top and two small coral-orange decorative dots. At the bottom, a rounded rectangular button-like element contains small navy text "무료 체험". Clean even lighting. IMPORTANT: all Korean text must be rendered exactly as written, character by character, sharp and legible, with no extra or altered text."""

MOTIFS = [
    "a soft geometric window view of a calm blue sea with gentle wave lines and a distant island",
    "a soft geometric coastal lighthouse silhouette on the horizon with layered waves",
    "a soft geometric shipyard scene with a large ship silhouette and a tall crane on the sea horizon",
    "a soft geometric bridge crossing the sea at sunset with coral-orange sky tones",
    "a soft geometric seaside cliff with a small sailboat and layered blue waves",
    "a soft geometric view of round pebble beach and gentle waves with a few seagulls",
    "a soft geometric camellia island coast with rocks and a small boat under a pale sky",
    "a soft geometric harbor with two small fishing boats and rippling water",
]

def motif_for(slug):
    return MOTIFS[sum(ord(c) for c in slug) % len(MOTIFS)]

def generate(school, slug, model="gemini-3.1-flash-image"):
    url = "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent?key={}".format(model, key())
    body = {"contents": [{"parts": [{"text": PROMPT.format(school=school, motif=motif_for(slug))}]}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "1:1"}}}
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.load(r)
    for part in d["candidates"][0]["content"]["parts"]:
        inline = part.get("inlineData") or part.get("inline_data")
        if inline:
            raw = base64.b64decode(inline["data"])
            break
    else:
        raise RuntimeError("no image: " + json.dumps(d)[:300])
    from PIL import Image
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    print("original", im.size, len(raw))
    im.thumbnail((720, 720))
    out = os.path.join(ROOT, "blog", "img", slug + ".webp")
    im.save(out, "WEBP", quality=82)
    print("saved", out, os.path.getsize(out))

if __name__ == "__main__":
    generate(sys.argv[1], sys.argv[2])
