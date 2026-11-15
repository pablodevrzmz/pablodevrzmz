#!/usr/bin/env python3
"""Fill the README section between <!-- LATEST:START --> and <!-- LATEST:END -->.

    python3 scripts/update_latest.py README.md latest.json

Lists the newest PyPI releases of my packages and my merged pull requests in other people's
repositories, newest first. Runs every night in .github/workflows/latest.yml; the source of this
file and of latest.json is the private jp_cvs repo (profile/site.yaml, site/profile/).
Standard library only. Writes the file only when the section changed; exits 0 either way.
"""
import json, os, re, sys, urllib.parse, urllib.request
from pathlib import Path

START, END = "<!-- LATEST:START -->", "<!-- LATEST:END -->"


def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json",
                                               "User-Agent": "profile-latest-section"})
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def md(s):
    """Escape a title for a markdown link label."""
    return re.sub(r"([\[\]<>*_`])", r"\\\1", s)


def releases(packages):
    out = []
    for p in packages:
        d = get(f"https://pypi.org/pypi/{p}/json")
        v = d["info"]["version"]
        files = d["releases"].get(v) or []
        if files:
            date = files[0]["upload_time"][:10]
            out.append((date, f"- [{md(p)} {v}](https://pypi.org/project/{p}/{v}/) released on PyPI, {date}"))
    return out


def merged_prs(cfg):
    q = f"is:pr is:merged author:{cfg['author']} " + " ".join(f"-user:{o}" for o in cfg.get("exclude_owners", []))
    url = "https://api.github.com/search/issues?" + urllib.parse.urlencode(
        {"q": q, "sort": "updated", "order": "desc", "per_page": 20})
    out = []
    for it in get(url)["items"]:
        repo = it["repository_url"].split("/repos/", 1)[1]
        date = ((it.get("pull_request") or {}).get("merged_at") or it["closed_at"])[:10]
        out.append((date, f"- [{md(it['title'])}]({it['html_url']}) merged into `{repo}`, {date}"))
    return out


def section(cfg):
    items = releases(cfg.get("pypi", []))
    if cfg.get("merged_prs"):
        items += merged_prs(cfg["merged_prs"])
    items = [line for _, line in sorted(items, reverse=True)[: cfg.get("limit", 6)]]
    return "\n".join(["## Latest", ""] + items) if items else ""


def main():
    readme, config = Path(sys.argv[1]), Path(sys.argv[2])
    text = readme.read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise SystemExit(f"{readme}: LATEST markers not found")
    body = section(json.loads(config.read_text(encoding="utf-8")))
    new = re.sub(re.escape(START) + r".*?" + re.escape(END),
                 lambda _: f"{START}\n{body}\n{END}" if body else f"{START}\n{END}", text, flags=re.S)
    if new != text:
        readme.write_text(new, encoding="utf-8")
        print("README.md: latest section updated")
    else:
        print("README.md: no change")


if __name__ == "__main__":
    main()
