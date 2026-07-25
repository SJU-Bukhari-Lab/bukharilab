#!/usr/bin/env python3
"""Audit every external URL rendered in the built Jekyll site.

Permanent failures (404/410), invalid URLs, and failed GitHub repository links
cause a non-zero exit. Sites that deliberately block automated clients
(401/403/429/451) are reported separately rather than misclassified as broken.
"""

from __future__ import annotations

import argparse
import json
import ssl
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler, HTTPSHandler

SUCCESS = set(range(200, 400))
PERMANENT_FAILURE = {404, 410}
RESTRICTED = {401, 403, 429, 451, 999}
TRANSIENT = {408, 425, 500, 502, 503, 504}
USER_AGENT = (
    "Mozilla/5.0 (compatible; BukhariLabLinkAudit/1.0; "
    "+https://bukharilab.org)"
)


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.urls: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)

        if tag == "link":
            rel_tokens = {
                token.strip().lower()
                for token in str(attrs_dict.get("rel", "")).split()
                if token.strip()
            }
            if rel_tokens & {"preconnect", "dns-prefetch"}:
                return

        for attr in ("href", "src"):
            value = attrs_dict.get(attr)
            if value and value.startswith(("http://", "https://")):
                self.urls.add(urldefrag(value)[0])


@dataclass
class Result:
    url: str
    status: int | None
    category: str
    final_url: str | None = None
    detail: str = ""


def collect_urls(site_dir: Path) -> list[str]:
    urls: set[str] = set()
    for html_file in site_dir.rglob("*.html"):
        parser = LinkParser()
        try:
            parser.feed(html_file.read_text(encoding="utf-8", errors="replace"))
        except OSError as exc:
            raise RuntimeError(f"Could not read {html_file}: {exc}") from exc
        urls.update(parser.urls)
    return sorted(urls)


def ssl_context() -> ssl.SSLContext:
    try:
        import certifi  # type: ignore
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def request_once(url: str, method: str, timeout: float) -> tuple[int, str]:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/json,*/*;q=0.8",
    }
    if method == "GET":
        headers["Range"] = "bytes=0-2047"
    request = Request(url, headers=headers, method=method)
    opener = build_opener(HTTPRedirectHandler(), HTTPSHandler(context=ssl_context()))
    with opener.open(request, timeout=timeout) as response:
        # Read a tiny amount so servers complete the request, while avoiding downloads.
        if method == "GET":
            response.read(2048)
        return int(response.status), response.geturl()


def check_url(url: str, timeout: float, retries: int) -> Result:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return Result(url, None, "broken", detail="Malformed external URL")

    last_detail = ""
    for attempt in range(retries + 1):
        for method in ("HEAD", "GET"):
            try:
                status, final_url = request_once(url, method, timeout)
                if status in SUCCESS:
                    return Result(url, status, "ok", final_url)
                if status in PERMANENT_FAILURE:
                    if method == "HEAD":
                        continue
                    return Result(url, status, "broken", final_url, "Permanent HTTP failure")
                if status in RESTRICTED:
                    if method == "HEAD":
                        continue
                    return Result(url, status, "restricted", final_url, "Automated access restricted")
                if status in TRANSIENT:
                    last_detail = f"Transient HTTP {status}"
                    break
                if status == 405 and method == "HEAD":
                    continue
                return Result(url, status, "unresolved", final_url, f"Unexpected HTTP {status}")
            except HTTPError as exc:
                status = int(exc.code)
                final_url = exc.geturl()
                if status in PERMANENT_FAILURE:
                    if method == "HEAD":
                        continue
                    return Result(url, status, "broken", final_url, "Permanent HTTP failure")
                if status in RESTRICTED:
                    if method == "HEAD":
                        continue
                    return Result(url, status, "restricted", final_url, "Automated access restricted")
                if status == 405 and method == "HEAD":
                    continue
                if status in TRANSIENT:
                    last_detail = f"Transient HTTP {status}"
                    break
                return Result(url, status, "unresolved", final_url, str(exc))
            except (URLError, TimeoutError, ssl.SSLError, OSError) as exc:
                last_detail = str(exc)
                if method == "HEAD":
                    continue
                break
        if attempt < retries:
            time.sleep(0.6 * (attempt + 1))

    return Result(url, None, "unresolved", detail=last_detail or "No response")


def print_group(label: str, results: Iterable[Result]) -> None:
    items = list(results)
    if not items:
        return
    print(f"\n{label} ({len(items)}):")
    for result in items:
        status = f"HTTP {result.status}" if result.status is not None else "no status"
        suffix = f" -> {result.final_url}" if result.final_url and result.final_url != result.url else ""
        detail = f" [{result.detail}]" if result.detail else ""
        print(f"  - {status}: {result.url}{suffix}{detail}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("site_dir", nargs="?", default="_site")
    parser.add_argument("--timeout", type=float, default=12.0)
    parser.add_argument("--retries", type=int, default=1)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--report", default="_site/external-link-report.json")
    parser.add_argument(
        "--strict-unresolved",
        action="store_true",
        help="Also fail on timeouts, DNS errors, and unexpected status codes.",
    )
    args = parser.parse_args()

    site_dir = Path(args.site_dir)
    if not site_dir.is_dir():
        print(f"ERROR: built site directory does not exist: {site_dir}", file=sys.stderr)
        return 2

    urls = collect_urls(site_dir)
    print(f"Checking {len(urls)} unique external URLs...")

    results: list[Result] = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = {
            pool.submit(check_url, url, args.timeout, max(0, args.retries)): url
            for url in urls
        }
        for future in as_completed(futures):
            results.append(future.result())

    results.sort(key=lambda item: item.url)
    groups = {
        category: [item for item in results if item.category == category]
        for category in ("broken", "unresolved", "restricted", "ok")
    }

    print_group("BROKEN LINKS", groups["broken"])
    print_group("UNRESOLVED LINKS", groups["unresolved"])
    print_group("AUTOMATION-RESTRICTED LINKS", groups["restricted"])

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(
            {
                "summary": {key: len(value) for key, value in groups.items()},
                "results": [asdict(item) for item in results],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "\nExternal-link summary: "
        f"{len(groups['ok'])} OK, "
        f"{len(groups['restricted'])} restricted, "
        f"{len(groups['unresolved'])} unresolved, "
        f"{len(groups['broken'])} broken."
    )
    print(f"Report: {report_path}")

    if groups["broken"]:
        return 1
    if args.strict_unresolved and groups["unresolved"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
