import sys, os, json, base64, io, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def key():
    for line in open(os.path.join(ROOT, ".env.local"), encoding="utf-8"):
        if line.startswith("GEMINI_IMAGE_KEY="):
            return line.strip().split("=", 1)[1]

PROMPT = """A clean, minimal, professional graphic design template for an educational advertisement. Square image with rounded corners on a slightly larger pale green geometric background with a subtle block pattern. The interior features a soft geometric abstract room layout in mint green and white tones, suggesting a room with a window. The top text in bold navy brackets reads "[{school}]". Below it is the large, very bold navy central title "1:1 화상과외". Below the main title is smaller navy text "내신 관리 | 30분 무료체험". A clean white horizontal bar at the top and two small yellow decorative dots. At the bottom, a rounded rectangular button-like element contains small navy text "무료 체험". Clean even lighting, all Korean text must be rendered exactly and legibly."""

def generate(school, slug, model="gemini-3.1-flash-image"):
    url = "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent?key={}".format(model, key())
    body = {"contents": [{"parts": [{"text": PROMPT.format(school=school)}]}],
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
