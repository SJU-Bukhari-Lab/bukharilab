#!/usr/bin/env python3
"""Optimize a generated Jekyll site without changing source design files.

The script operates only on the generated ``_site`` directory:
- bundles local CSS and JavaScript to reduce HTTP requests;
- converts large raster images to WebP when the result is materially smaller;
- optimizes existing large WebP images in place;
- adds safe lazy-loading, async decoding, and intrinsic dimensions to images;
- preloads the homepage skyline and adds font connection hints.

Original SCSS, JavaScript, Markdown, YAML, and image source files remain untouched.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote, urlparse

try:
    from PIL import Image, ImageOps
except ImportError as exc:  # pragma: no cover - clear runtime guidance
    raise SystemExit(
        "Pillow is required. Install it with: python3 -m pip install Pillow"
    ) from exc


LOCAL_CSS_RE = re.compile(
    r"<link\b(?=[^>]*\brel=[\"'][^\"']*stylesheet[^\"']*[\"'])"
    r"(?=[^>]*\bhref=[\"'](?P<href>[^\"']*/_styles/[^\"']+\.css(?:\?[^\"']*)?)[\"'])[^>]*>",
    re.IGNORECASE,
)
LOCAL_JS_RE = re.compile(
    r"<script\b(?=[^>]*\bsrc=[\"'](?P<src>[^\"']*/_scripts/[^\"']+\.js(?:\?[^\"']*)?)[\"'])[^>]*>\s*</script>",
    re.IGNORECASE,
)
IMG_TAG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
ATTR_RE_TEMPLATE = r"\b{attr}\s*=\s*([\"'])(.*?)\1"

TEXT_SUFFIXES = {".html", ".css", ".js", ".xml", ".json", ".txt"}
RASTER_SUFFIXES = {".png", ".jpg", ".jpeg"}


@dataclass
class Report:
    css_files_bundled: int = 0
    css_bytes_before: int = 0
    css_bytes_after: int = 0
    js_files_bundled: int = 0
    js_bytes_before: int = 0
    js_bytes_after: int = 0
    images_converted: int = 0
    webp_images_recompressed: int = 0
    image_bytes_before: int = 0
    image_bytes_after: int = 0
    html_files_updated: int = 0
    image_tags_lazy_loaded: int = 0
    image_dimensions_added: int = 0


def sha12(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:12]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def extract_attr(tag: str, attr: str) -> str | None:
    match = re.search(ATTR_RE_TEMPLATE.format(attr=re.escape(attr)), tag, re.IGNORECASE)
    return match.group(2) if match else None


def has_attr(tag: str, attr: str) -> bool:
    return re.search(rf"\b{re.escape(attr)}\s*=", tag, re.IGNORECASE) is not None


def add_attrs(tag: str, attrs: list[tuple[str, str]]) -> str:
    additions = "".join(f' {key}="{value}"' for key, value in attrs)
    return tag[:-2] + additions + " />" if tag.endswith("/>") else tag[:-1] + additions + ">"


def url_path_to_file(site_dir: Path, url: str) -> Path | None:
    parsed = urlparse(url)
    if parsed.scheme or parsed.netloc or url.startswith("data:"):
        return None
    path = unquote(parsed.path)
    if not path:
        return None
    if path.startswith("/"):
        candidate = site_dir / path.lstrip("/")
    else:
        candidate = site_dir / path
    return candidate


def resolve_relative_asset(site_dir: Path, html_file: Path, url: str) -> Path | None:
    parsed = urlparse(url)
    if parsed.scheme or parsed.netloc or url.startswith(("data:", "#")):
        return None
    clean = unquote(parsed.path)
    if clean.startswith("/"):
        return site_dir / clean.lstrip("/")
    return (html_file.parent / clean).resolve()


def find_reference_html(site_dir: Path) -> Path | None:
    preferred = [site_dir / "index.html"]
    preferred.extend(sorted(site_dir.rglob("*.html")))
    for path in preferred:
        if path.exists():
            text = read_text(path)
            if LOCAL_CSS_RE.search(text) or LOCAL_JS_RE.search(text):
                return path
    return None


def ordered_asset_paths(site_dir: Path, html: str, regex: re.Pattern[str], group: str) -> list[Path]:
    paths: list[Path] = []
    seen: set[Path] = set()
    for match in regex.finditer(html):
        candidate = url_path_to_file(site_dir, match.group(group).split("?", 1)[0])
        if candidate and candidate.exists() and candidate not in seen:
            paths.append(candidate)
            seen.add(candidate)
    return paths


def bundle_assets(site_dir: Path, report: Report) -> tuple[str | None, str | None]:
    reference = find_reference_html(site_dir)
    if not reference:
        return None, None

    ref_html = read_text(reference)
    assets_dir = site_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    css_paths = ordered_asset_paths(site_dir, ref_html, LOCAL_CSS_RE, "href")
    for extra in sorted((site_dir / "_styles").rglob("*.css")) if (site_dir / "_styles").exists() else []:
        if extra not in css_paths and not extra.name.endswith(".map"):
            css_paths.append(extra)

    css_href: str | None = None
    if css_paths:
        chunks: list[str] = []
        for path in css_paths:
            content = read_text(path)
            report.css_bytes_before += path.stat().st_size
            chunks.append(f"\n{content.rstrip()}\n")
        bundle_text = "".join(chunks).lstrip()
        data = bundle_text.encode("utf-8")
        filename = f"site-bundle.{sha12(data)}.css"
        target = assets_dir / filename
        target.write_bytes(data)
        report.css_files_bundled = len(css_paths)
        report.css_bytes_after = len(data)
        css_href = f"/assets/{filename}"

    js_paths = ordered_asset_paths(site_dir, ref_html, LOCAL_JS_RE, "src")
    for extra in sorted((site_dir / "_scripts").rglob("*.js")) if (site_dir / "_scripts").exists() else []:
        if extra not in js_paths:
            js_paths.append(extra)

    js_href: str | None = None
    if js_paths:
        chunks = []
        for path in js_paths:
            content = read_text(path)
            report.js_bytes_before += path.stat().st_size
            # Preserve source order and isolate accidental source-map directives.
            content = re.sub(r"^\s*//# sourceMappingURL=.*$", "", content, flags=re.MULTILINE)
            chunks.append(f"\n;\n{content.rstrip()}\n")
        bundle_text = "".join(chunks).lstrip()
        data = bundle_text.encode("utf-8")
        filename = f"site-bundle.{sha12(data)}.js"
        target = assets_dir / filename
        target.write_bytes(data)
        report.js_files_bundled = len(js_paths)
        report.js_bytes_after = len(data)
        js_href = f"/assets/{filename}"

    return css_href, js_href


def infer_base_prefix(html: str) -> str:
    for regex, group in ((LOCAL_CSS_RE, "href"), (LOCAL_JS_RE, "src")):
        match = regex.search(html)
        if match:
            value = match.group(group).split("?", 1)[0]
            marker = "/_styles/" if group == "href" else "/_scripts/"
            if marker in value:
                return value.split(marker, 1)[0]
    return ""


def replace_local_asset_tags(html: str, css_href: str | None, js_href: str | None) -> str:
    prefix = infer_base_prefix(html)

    if css_href:
        final_css_href = f"{prefix}{css_href}" if prefix and css_href.startswith("/") else css_href
        replacement = f'<link href="{final_css_href}" rel="stylesheet">'
        matches = list(LOCAL_CSS_RE.finditer(html))
        if matches:
            first = matches[0]
            html = html[: first.start()] + replacement + html[first.end() :]
            html = LOCAL_CSS_RE.sub("", html)

    if js_href:
        final_js_href = f"{prefix}{js_href}" if prefix and js_href.startswith("/") else js_href
        replacement = f'<script src="{final_js_href}" defer></script>'
        matches = list(LOCAL_JS_RE.finditer(html))
        if matches:
            first = matches[0]
            html = html[: first.start()] + replacement + html[first.end() :]
            html = LOCAL_JS_RE.sub("", html)

    return html


def image_save_kwargs(image: Image.Image, quality: int) -> dict[str, object]:
    return {
        "format": "WEBP",
        "quality": quality,
        "method": 6,
        "lossless": False,
        "exact": True,
        "icc_profile": image.info.get("icc_profile"),
        "exif": image.info.get("exif", b""),
    }


def save_webp_candidate(source: Path, target: Path, quality: int) -> tuple[int, int] | None:
    try:
        with Image.open(source) as raw:
            image = ImageOps.exif_transpose(raw)
            if image.mode not in {"RGB", "RGBA"}:
                image = image.convert("RGBA" if "A" in image.getbands() else "RGB")
            target.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(suffix=".webp", delete=False, dir=target.parent) as temp:
                temp_path = Path(temp.name)
            try:
                kwargs = {k: v for k, v in image_save_kwargs(image, quality).items() if v not in {None, b""}}
                image.save(temp_path, **kwargs)
                old_size = source.stat().st_size
                new_size = temp_path.stat().st_size
                if new_size < old_size * 0.88:
                    shutil.move(temp_path, target)
                    return old_size, new_size
            finally:
                temp_path.unlink(missing_ok=True)
    except (OSError, ValueError) as exc:
        print(f"Warning: could not optimize {source}: {exc}", file=sys.stderr)
    return None


def optimize_existing_webp(path: Path, quality: int) -> tuple[int, int] | None:
    try:
        with Image.open(path) as raw:
            image = ImageOps.exif_transpose(raw)
            if image.mode not in {"RGB", "RGBA"}:
                image = image.convert("RGBA" if "A" in image.getbands() else "RGB")
            with tempfile.NamedTemporaryFile(suffix=".webp", delete=False, dir=path.parent) as temp:
                temp_path = Path(temp.name)
            try:
                kwargs = {k: v for k, v in image_save_kwargs(image, quality).items() if v not in {None, b""}}
                image.save(temp_path, **kwargs)
                old_size = path.stat().st_size
                new_size = temp_path.stat().st_size
                if new_size < old_size * 0.92:
                    shutil.move(temp_path, path)
                    return old_size, new_size
            finally:
                temp_path.unlink(missing_ok=True)
    except (OSError, ValueError) as exc:
        print(f"Warning: could not recompress {path}: {exc}", file=sys.stderr)
    return None


def replace_asset_references(site_dir: Path, mapping: dict[str, str]) -> None:
    if not mapping:
        return
    variants: list[tuple[str, str]] = []
    for old_rel, new_rel in mapping.items():
        variants.extend(
            [
                (old_rel, new_rel),
                (f"/{old_rel}", f"/{new_rel}"),
                (old_rel.replace("/", "%2F"), new_rel.replace("/", "%2F")),
            ]
        )
    variants.sort(key=lambda item: len(item[0]), reverse=True)

    for path in site_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = read_text(path)
        updated = text
        for old, new in variants:
            updated = updated.replace(old, new)
        if updated != text:
            write_text(path, updated)


def should_skip_lossy_image(path: Path, images_root: Path) -> bool:
    try:
        parts = {part.lower() for part in path.relative_to(images_root).parts[:-1]}
    except ValueError:
        return False
    return bool(parts & {"brand", "funders", "infographics"})


def optimize_images(site_dir: Path, report: Report, threshold: int, quality: int) -> dict[str, str]:
    images_root = site_dir / "images"
    if not images_root.exists():
        return {}

    mapping: dict[str, str] = {}
    candidates = sorted(path for path in images_root.rglob("*") if path.is_file())
    for path in candidates:
        if should_skip_lossy_image(path, images_root):
            continue
        suffix = path.suffix.lower()
        size = path.stat().st_size
        if size < threshold:
            continue
        if suffix in RASTER_SUFFIXES:
            target = path.with_suffix(".webp")
            result = save_webp_candidate(path, target, quality)
            if result:
                old_size, new_size = result
                old_rel = path.relative_to(site_dir).as_posix()
                new_rel = target.relative_to(site_dir).as_posix()
                mapping[old_rel] = new_rel
                report.images_converted += 1
                report.image_bytes_before += old_size
                report.image_bytes_after += new_size
        elif suffix == ".webp":
            result = optimize_existing_webp(path, quality)
            if result:
                old_size, new_size = result
                report.webp_images_recompressed += 1
                report.image_bytes_before += old_size
                report.image_bytes_after += new_size

    replace_asset_references(site_dir, mapping)
    # Converted originals are removed only from the generated deploy artifact.
    # The repository source images remain untouched and continue to be editable.
    for old_rel in mapping:
        (site_dir / old_rel).unlink(missing_ok=True)
    return mapping


def should_eager_load(tag: str, index_on_page: int) -> bool:
    value = tag.lower()
    important_tokens = (
        "logo",
        "home-hero",
        "hero-image",
        "site-header",
        "nsf-logo",
        "nih-logo",
        "funding",
    )
    return index_on_page < 1 or any(token in value for token in important_tokens)


def update_img_tag(site_dir: Path, html_file: Path, tag: str, index_on_page: int, report: Report) -> str:
    src = extract_attr(tag, "src")
    attrs: list[tuple[str, str]] = []

    if not should_eager_load(tag, index_on_page):
        if not has_attr(tag, "loading"):
            attrs.append(("loading", "lazy"))
            report.image_tags_lazy_loaded += 1
    elif not has_attr(tag, "fetchpriority") and ("hero" in tag.lower() or index_on_page == 0):
        attrs.append(("fetchpriority", "high"))

    if not has_attr(tag, "decoding"):
        attrs.append(("decoding", "async"))

    if src and (not has_attr(tag, "width") or not has_attr(tag, "height")):
        asset = resolve_relative_asset(site_dir, html_file, src)
        if asset and asset.exists() and asset.suffix.lower() in RASTER_SUFFIXES | {".webp", ".gif"}:
            try:
                with Image.open(asset) as image:
                    width, height = image.size
                if not has_attr(tag, "width"):
                    attrs.append(("width", str(width)))
                if not has_attr(tag, "height"):
                    attrs.append(("height", str(height)))
                report.image_dimensions_added += 1
            except OSError:
                pass

    return add_attrs(tag, attrs) if attrs else tag


def add_connection_hints(html: str) -> str:
    hints: list[str] = []
    if "https://fonts.googleapis.com" in html and 'href="https://fonts.googleapis.com"' not in html:
        hints.append('<link rel="preconnect" href="https://fonts.googleapis.com">')
    if "https://fonts.gstatic.com" in html and 'href="https://fonts.gstatic.com" crossorigin' not in html:
        hints.append('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
    if not hints or "</head>" not in html:
        return html
    return html.replace("</head>", "\n".join(hints) + "\n</head>", 1)


def add_homepage_preloads(site_dir: Path, html: str) -> str:
    if "</head>" not in html:
        return html
    preloads: list[str] = []
    skyline_match = re.search(
        r"(?P<url>(?:/|[.]{0,2}/)?images/brand/nyc-skyline-licensed\.webp)", html
    )
    if skyline_match and 'rel="preload"' not in html:
        preloads.append(
            f'<link rel="preload" as="image" href="{skyline_match.group("url")}" fetchpriority="high">'
        )
    if not preloads:
        return html
    return html.replace("</head>", "\n".join(preloads) + "\n</head>", 1)


def update_html_files(site_dir: Path, css_href: str | None, js_href: str | None, report: Report) -> None:
    for html_file in sorted(site_dir.rglob("*.html")):
        original = read_text(html_file)
        updated = replace_local_asset_tags(original, css_href, js_href)
        updated = add_connection_hints(updated)

        counter = {"value": 0}

        def replace_img(match: re.Match[str]) -> str:
            index = counter["value"]
            counter["value"] += 1
            return update_img_tag(site_dir, html_file, match.group(0), index, report)

        updated = IMG_TAG_RE.sub(replace_img, updated)
        if html_file == site_dir / "index.html":
            updated = add_homepage_preloads(site_dir, updated)

        if updated != original:
            write_text(html_file, updated)
            report.html_files_updated += 1


def remove_unreferenced_local_asset_files(site_dir: Path) -> None:
    """Remove only generated per-file CSS/JS from the deploy artifact.

    Source files in the repository are unaffected. This reduces artifact size and
    prevents browsers or crawlers from fetching redundant generated assets.
    """
    for folder, suffix in ((site_dir / "_styles", ".css"), (site_dir / "_scripts", ".js")):
        if not folder.exists():
            continue
        for path in folder.rglob(f"*{suffix}"):
            path.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", default="_site", help="Generated Jekyll site directory")
    parser.add_argument(
        "--image-threshold-kb",
        type=int,
        default=220,
        help="Only optimize raster images at or above this size",
    )
    parser.add_argument(
        "--webp-quality",
        type=int,
        default=86,
        help="WebP quality used for generated deploy assets",
    )
    args = parser.parse_args()

    site_dir = Path(args.site_dir).resolve()
    if not site_dir.is_dir():
        print(f"Generated site directory not found: {site_dir}", file=sys.stderr)
        return 2

    report = Report()
    css_href, js_href = bundle_assets(site_dir, report)
    optimize_images(
        site_dir,
        report,
        threshold=max(1, args.image_threshold_kb) * 1024,
        quality=max(1, min(args.webp_quality, 100)),
    )
    update_html_files(site_dir, css_href, js_href, report)
    remove_unreferenced_local_asset_files(site_dir)

    report_path = site_dir / "assets" / "performance-report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(asdict(report), indent=2) + "\n", encoding="utf-8")

    print("\nBukhari Lab generated-site optimization complete")
    print(f"  CSS: {report.css_files_bundled} requests -> 1")
    print(f"  JavaScript: {report.js_files_bundled} requests -> 1")
    print(
        "  Images: "
        f"{report.images_converted} converted, "
        f"{report.webp_images_recompressed} WebP files recompressed"
    )
    if report.image_bytes_before:
        saved = report.image_bytes_before - report.image_bytes_after
        percent = saved / report.image_bytes_before * 100
        print(f"  Image bytes saved: {saved:,} ({percent:.1f}%)")
    print(f"  HTML files updated: {report.html_files_updated}")
    print(f"  Report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
