#!/usr/bin/env python3
"""Audit the Bukhari Lab faculty-feedback implementation and review fixes."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "PyYAML is required. Install repository Python dependencies with "
        "python3 -m pip install -r _cite/requirements.txt"
    ) from exc

PROJECT_TITLES = [
    "Neuro-Symbolic AI for Drug Repurposing",
    "Narrative-Driven AI for Clinician Burnout Surveillance",
    "Trustworthy Algorithms for Extreme Multi-Label Medical Coding",
    "A Socio-Technical Approach to Biomedical Content Authoring and Publishing",
]

PAPER_TITLES = [
    "Fish-Pak: Fish species dataset from Pakistan for visual features based classification",
    "Adaptive Immune Receptor Repertoire Community recommendations for sharing immune-repertoire sequencing data",
    "Knowledge Graph Based Trustworthy Medical Code Recommendations",
    "FHIRTrustBench: A Benchmark for Interoperability-Driven Clinical AI Readiness and Trustworthiness",
]

FEATURED_SOFTWARE_IDS = [
    "deep_flaim",
    "cedar_ondemand",
    "gosemantically",
    "airr_standards",
]

EXPECTED_SOFTWARE = {
    "deep_flaim": {
        "title": "Deep-FLAIM",
        "link": "https://github.com/bukharilab/deepflaim",
    },
    "cedar_ondemand": {
        "title": "CEDAR OnDemand",
        "link": "https://github.com/bukharilab/CEDAROnDemand",
    },
    "gosemantically": {
        "title": "goSemantically",
        "link": "https://github.com/bukharilab/gosemantically",
    },
    "airr_standards": {
        "title": "AIRR Standards",
        "link": "https://github.com/bukharilab/airr-standards",
    },
}

IMAGE_FIELDS = (
    "image",
    "thumbnail",
    "card_image",
    "featured_image",
    "infographic",
    "cover",
    "banner",
)


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def load_yaml(path: Path, errors: list[str]) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        errors.append(f"Could not parse {path}: {exc}")
        return {}


def parse_front_matter(path: Path, errors: list[str]) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append(f"{path} has no readable YAML front matter.")
        return {}

    closing = text.find("\n---", 4)
    if closing < 0:
        errors.append(f"{path} has unterminated YAML front matter.")
        return {}

    try:
        return yaml.safe_load(text[4:closing]) or {}
    except yaml.YAMLError as exc:
        errors.append(f"Could not parse front matter in {path}: {exc}")
        return {}


def audit_project_images(repo: Path, errors: list[str]) -> None:
    project_dir = repo / "_projects"
    require(project_dir.is_dir(), "_projects directory is missing.", errors)
    if not project_dir.is_dir():
        return

    projects = sorted(project_dir.glob("*.md"))
    require(bool(projects), "No project pages were found under _projects.", errors)

    for path in projects:
        front = parse_front_matter(path, errors)
        refs = [front[field] for field in IMAGE_FIELDS if isinstance(front.get(field), str)]
        if not refs:
            errors.append(f"{path.relative_to(repo)} has no project image field.")
            continue

        for ref in refs:
            clean_ref = ref.split("?", 1)[0]
            if "images/projects/infographics/" not in clean_ref:
                errors.append(
                    f"{path.relative_to(repo)} still references a non-infographic image: {ref}"
                )
                continue
            target = repo / clean_ref.lstrip("/")
            if not target.is_file():
                errors.append(
                    f"{path.relative_to(repo)} references a missing infographic: {ref}"
                )


def main() -> int:
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else ".").expanduser().resolve()
    errors: list[str] = []

    required = {
        "index": repo / "index.md",
        "homepage": repo / "_data/homepage.yaml",
        "software": repo / "_data/software_catalog.yaml",
        "footer": repo / "_includes/footer.html",
        "meta": repo / "_includes/meta.html",
        "config": repo / "_config.yaml",
        "style": repo
        / "_styles/zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz-faculty-feedback.scss",
        "workflow": repo / ".github/workflows/validate.yml",
    }

    for label, path in required.items():
        require(path.is_file(), f"Required {label} file is missing: {path.relative_to(repo)}", errors)

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    index = required["index"].read_text(encoding="utf-8")
    footer = required["footer"].read_text(encoding="utf-8")
    meta = required["meta"].read_text(encoding="utf-8")
    config_text = required["config"].read_text(encoding="utf-8")
    style = required["style"].read_text(encoding="utf-8")
    homepage = load_yaml(required["homepage"], errors)
    software_catalog = load_yaml(required["software"], errors)
    config = load_yaml(required["config"], errors)

    require("Our work is proudly funded by" in index, "Funding acknowledgment is missing.", errors)
    require("Funding & Fellowship" not in index, "Old funding wording remains.", errors)
    require("images/funders/nsf-logo.svg" in index, "Homepage is not using the NSF SVG.", errors)
    require("images/funders/nih-logo.png" in index, "Homepage is not using the approved NIH PNG.", errors)
    require("images/funders/nih-logo.svg" not in index, "Homepage still references the unused NIH SVG.", errors)
    funding_start = index.find("home-hero__funding-row")
    funding_end = index.find("home-hero__credit", funding_start)
    funding_section = index[funding_start:funding_end if funding_end >= 0 else None]
    require("tabindex=\"0\"" not in funding_section, "Noninteractive funder logos are keyboard-focusable.", errors)
    require("home-hero__funder--logo-only:hover" in style, "Funder hover styling is missing.", errors)
    require(
        bool(re.search(r"home-hero__funder[^}]*border-radius\s*:", style, re.S)),
        "Rounded funding-logo edges are missing.",
        errors,
    )

    active_projects = homepage.get("active_projects", [])
    require(len(active_projects) == 4, "Exactly four active projects must be featured.", errors)
    active_titles = {item.get("title") for item in active_projects if isinstance(item, dict)}
    for title in PROJECT_TITLES:
        require(title in active_titles, f"Featured project is missing: {title}", errors)

    benchmarks = homepage.get("benchmarking", [])
    require(len(benchmarks) == 2, "Exactly two completed benchmarks must be displayed.", errors)
    require(
        homepage.get("benchmarking_note") == "A third benchmarking study is currently in development.",
        "The third-benchmark development note is missing or changed.",
        errors,
    )
    require("Data and Benchmarking" in index, "Data and Benchmarking heading is missing.", errors)

    papers = homepage.get("featured_papers", [])
    require(len(papers) == 4, "Exactly four featured papers must be selected.", errors)
    paper_titles = {item.get("title") for item in papers if isinstance(item, dict)}
    for title in PAPER_TITLES:
        require(title in paper_titles, f"Featured paper is missing: {title}", errors)
    require(
        not any("citrus" in str(title).lower() for title in paper_titles),
        "The citrus-fruit paper is still featured.",
        errors,
    )

    selected_ids = homepage.get("featured_software_ids", [])
    require(selected_ids == FEATURED_SOFTWARE_IDS, "Featured software IDs are missing or out of order.", errors)

    featured_records = software_catalog.get("featured", [])
    by_id = {
        item.get("id"): item
        for item in featured_records
        if isinstance(item, dict) and item.get("id")
    }
    for software_id, expected in EXPECTED_SOFTWARE.items():
        record = by_id.get(software_id)
        require(record is not None, f"Canonical software record is missing: {software_id}", errors)
        if record:
            require(record.get("title") == expected["title"], f"Incorrect title for {software_id}.", errors)
            require(record.get("link") == expected["link"], f"Incorrect link for {software_id}.", errors)
            require(bool(record.get("description")), f"Missing description for {software_id}.", errors)

    require("site.data.homepage.featured_software_ids" in index, "Homepage is not using canonical software IDs.", errors)
    require("site.data.software_catalog.featured" in index, "Homepage is not reading the canonical software catalog.", errors)

    links = config.get("links", {}) if isinstance(config, dict) else {}
    require(links.get("website") == "https://bukharilab.org", "Website configuration is incorrect.", errors)
    require(links.get("linkedin") == "https://www.linkedin.com/company/bukharilab", "LinkedIn configuration is incorrect.", errors)
    require("site.links.linkedin" in footer, "Footer does not use the LinkedIn configuration key.", errors)
    require("site.links.website" not in footer, "Footer still misuses the Website key for LinkedIn.", errors)
    website_label = footer.find("<span>Website</span>")
    website_anchor_start = footer.rfind("<a", 0, website_label) if website_label >= 0 else -1
    website_anchor = footer[website_anchor_start:website_label] if website_anchor_start >= 0 else ""
    require("target=\"_blank\"" not in website_anchor, "Internal Website link opens a new tab.", errors)
    for label in ("Google Scholar", "GitHub", "Website", "LinkedIn", "Hugging Face"):
        require(label in footer, f"Footer link is missing: {label}", errors)
    require("https://huggingface.co/bukharilab" in config_text, "Hugging Face URL is missing.", errors)
    require("mathjax@4.1.3/tex-mml-chtml.js" in config_text, "MathJax is not pinned to version 4.1.3.", errors)

    require("rel=\"canonical\"" in meta, "Canonical URL metadata is missing.", errors)
    require("page.url | absolute_url" in meta, "Metadata is not page-specific.", errors)
    require("og:site_name" in meta, "Open Graph site_name is missing.", errors)
    require("og:site_title" not in meta, "Invalid og:site_title property remains.", errors)
    require("| jsonify" in meta, "JSON-LD values are not serialized with jsonify.", errors)
    require("page.author | default: site.title" in meta, "JSON-LD author fallback is incorrect.", errors)

    require((repo / "_scripts/site-search.js").read_text(encoding="utf-8").find("URLSearchParams") >= 0, "Site search does not encode queries.", errors)
    dark_mode = (repo / "_scripts/dark-mode.js").read_text(encoding="utf-8")
    require("instanceof HTMLInputElement" in dark_mode, "Dark-mode toggle has no null/type guard.", errors)
    require("try" in dark_mode and "localStorage" in dark_mode, "Dark-mode storage access is not guarded.", errors)

    validate_workflow = required["workflow"].read_text(encoding="utf-8")
    require("pull_request:" in validate_workflow, "Pull-request validation is not configured.", errors)
    require("htmlproofer" in validate_workflow, "HTMLProofer is not run in pull-request CI.", errors)
    require("audit_faculty_feedback.py" in validate_workflow, "Faculty-feedback audit is not run in CI.", errors)
    for action in (
        "actions/checkout@v7.0.1",
        "actions/setup-python@v6.3.0",
        "ruby/setup-ruby@v1.321.0",
    ):
        require(action in validate_workflow, f"Validation workflow is not pinned to {action}.", errors)

    pages_workflow = (repo / ".github/workflows/pages.yml").read_text(encoding="utf-8")
    require("cancel-in-progress: true" in pages_workflow, "Obsolete Pages builds are not cancelled.", errors)
    require("Refresh publication record" not in pages_workflow, "Production deployment still refreshes external publication data.", errors)
    for action in (
        "actions/upload-pages-artifact@v5.0.0",
        "actions/deploy-pages@v5.0.0",
    ):
        require(action in pages_workflow, f"Pages workflow is not pinned to {action}.", errors)

    scripts_include = (repo / "_includes/scripts.html").read_text(encoding="utf-8")
    for version in ("@popperjs/core@2.11.8", "tippy.js@6.3.7", "mark.js@8.11.1"):
        require(version in scripts_include, f"Third-party script is not pinned: {version}", errors)

    optimizer = (repo / "scripts/optimize_built_site.py").read_text(encoding="utf-8")
    require("should_skip_lossy_image" in optimizer, "Optimizer does not protect logos and infographics from lossy conversion.", errors)
    require('chunks.append(f"\\n;\\n{content.rstrip()}\\n")' in optimizer, "Bundled JavaScript files are not separated safely.", errors)

    audit_project_images(repo, errors)

    if errors:
        print("Faculty-feedback audit failed:", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    print("Faculty-feedback and code-review audit passed.")
    print("Verified content, canonical software data, metadata, footer links, CI, JavaScript, and project infographics.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
