#!/usr/bin/env python3
"""Refresh the lab's full public GitHub repository directory.

Pulls every public, non-fork repository from the bukharilab GitHub account
directly (no manually maintained link list required) and writes
_data/github_repos.yaml, mirroring how _cite/cite.py pulls the full
publication list from ORCID/PubMed/Scholar rather than a hand-typed catalog.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "PyYAML is required. Install dependencies with "
        "'python3 -m pip install -r _cite/requirements.txt'."
    ) from exc

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = ROOT / "_data" / "github_repos.yaml"
ACCOUNT = "bukharilab"

# Repos on the account that aren't lab research output and shouldn't appear
# on the public site, even though they're real non-fork public repos.
EXCLUDED_REPOS = {
    "bukharilab",  # GitHub profile README repo
    "mysite",  # personal homepage, not lab software
    "datasciencecoursera",  # personal coursework, not lab research
    "sebi",  # excluded per lab request
}


def github_get(path: str, token: str):
    request = Request(f"https://api.github.com{path}")
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("User-Agent", "bukharilab-website")
    if token:
        request.add_header("Authorization", f"Bearer {token}")

    with urlopen(request, timeout=20) as response:
        return json.loads(response.read())


def fetch_all_repos(token: str) -> list[dict]:
    # A single max-size page comfortably covers this account's repo count;
    # revisit with pagination if it ever grows past 100.
    return github_get(f"/users/{ACCOUNT}/repos?per_page=100&type=owner", token)


def fetch_languages(full_name: str, token: str) -> list[str]:
    try:
        by_bytes = github_get(f"/repos/{full_name}/languages", token)
    except (HTTPError, URLError) as error:
        print(f"  WARNING: {full_name} languages lookup failed: {error}")
        return []
    if not isinstance(by_bytes, dict):
        return []
    return [name for name, _ in sorted(by_bytes.items(), key=lambda kv: kv[1], reverse=True)[:3]]


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN", "")

    try:
        repos = fetch_all_repos(token)
    except HTTPError as error:
        if error.code == 403:
            raise SystemExit(
                "GitHub API rate-limited (403). Set GITHUB_TOKEN to raise the limit, or wait and retry."
            ) from error
        raise SystemExit(f"GitHub API request failed: HTTP {error.code}") from error
    except URLError as error:
        raise SystemExit(f"GitHub API request failed: {error}") from error

    repos = [r for r in repos if not r.get("fork") and r["name"] not in EXCLUDED_REPOS]
    print(f"Found {len(repos)} non-fork public repositories for {ACCOUNT} (after exclusions)")

    entries = []
    for repo in repos:
        full_name = repo["full_name"]
        print(f"Fetching languages for {full_name}")
        languages = fetch_languages(full_name, token)
        if not token:
            time.sleep(0.5)  # be polite to the anonymous rate limit

        entries.append(
            {
                "name": repo["name"],
                "description": repo.get("description"),
                "link": repo["html_url"],
                "stars": repo.get("stargazers_count", 0),
                "languages": languages,
                "updated": (repo.get("pushed_at") or "")[:10] or None,
                "archived": bool(repo.get("archived", False)),
                "open_issues": repo.get("open_issues_count", 0),
            }
        )

    entries.sort(key=lambda e: e["name"].lower())

    OUTPUT_FILE.write_text(
        "# DO NOT EDIT, GENERATED AUTOMATICALLY\n\n" + yaml.dump(entries, sort_keys=False, allow_unicode=True)
    )
    print()
    print(f"Wrote {len(entries)} repositories to {OUTPUT_FILE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
