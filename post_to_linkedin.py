#!/usr/bin/env python3
import os, sys, requests, subprocess

LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_PERSON_URN   = os.getenv("LINKEDIN_PERSON_URN")
LINKEDIN_VERSION      = os.getenv("LINKEDIN_VERSION", "202502")

def gen_text() -> str:
    res = subprocess.run([sys.executable, "compose_post.py"], capture_output=True, text=True, check=True)
    return res.stdout.strip()

def post_to_linkedin(text: str):
    url = "https://api.linkedin.com/rest/posts"
    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "LinkedIn-Version": LINKEDIN_VERSION,
    }
    payload = {
        "author": LINKEDIN_PERSON_URN,
        "commentary": text,
        "visibility": "PUBLIC",
        "distribution": {"feedDistribution":"MAIN_FEED","targetEntities":[],"thirdPartyDistributionChannels":[]},
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    r = requests.post(url, headers=headers, json=payload, timeout=45)
    if not r.ok:
        raise SystemExit(f"LinkedIn error {r.status_code}: {r.text}")
    print("OK:", r.headers.get("x-restli-id", "<no-id>"))

def main():
    if not LINKEDIN_ACCESS_TOKEN or not LINKEDIN_PERSON_URN:
        raise SystemExit("Missing LINKEDIN_ACCESS_TOKEN or LINKEDIN_PERSON_URN")
    text = gen_text()
    post_to_linkedin(text)

if __name__ == "__main__":
    main()
