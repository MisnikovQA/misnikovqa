#!/usr/bin/env python3
import random, hashlib, json, os, yaml
CACHE = "posted_cache.json"

def load_topics(path="topics.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_cache():
    if os.path.exists(CACHE):
        return json.load(open(CACHE, "r", encoding="utf-8"))
    return {"hashes": []}

def save_cache(c):
    json.dump(c, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def make_post():
    data = load_topics()
    t = random.choice(data["templates"]).strip()
    tags = " ".join(random.sample(data["hashtags"], k=min(4, len(data["hashtags"]))))
    parts = [p.strip() for p in t.split("\n") if p.strip()]
    text = "\n".join(parts) + "\n\n" + tags
    return text[:1300]

def main():
    c = load_cache()
    text = make_post()
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
    for _ in range(2):
        if h in c["hashes"]:
            text = make_post()
            h = hashlib.sha256(text.encode("utf-8")).hexdigest()
        else:
            break
    c["hashes"] = (c["hashes"] + [h])[-40:]
    save_cache(c)
    print(text)

if __name__ == "__main__":
    main()
