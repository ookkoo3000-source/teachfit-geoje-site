import os, sys, re, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_image
ROOT = gen_image.ROOT

def posts():
    src = open(os.path.join(ROOT, "build.py"), encoding="utf-8").read()
    for m in re.finditer(r'"slug": "([^"]+)",\s*"title": "([^"]+)"', src):
        yield m.group(1), m.group(2)

if __name__ == "__main__":
    for slug, title in posts():
        out = os.path.join(ROOT, "blog", "img", slug + ".webp")
        if os.path.exists(out):
            continue
        name = title.split(" ")[0]
        for attempt in range(3):
            try:
                gen_image.generate(name, slug)
                break
            except Exception as e:
                print("retry", slug, str(e)[:120]); time.sleep(8)
        time.sleep(2)
    print("ALL DONE")
