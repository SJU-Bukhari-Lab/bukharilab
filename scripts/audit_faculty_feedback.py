#!/usr/bin/env python3
"""Audit the final Bukhari Lab faculty-feedback implementation.

Uses only the repository source. Exits nonzero when a requested item is missing.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

STYLE_FILE = "_styles/zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz-faculty-feedback.scss"
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
SOFTWARE_TITLES = [
    "DeepFLAME Semantically",
    "CEDAR OnDemand",
    "GoSemantically",
    "AI Standards",
]
IMAGE_FIELDS = (
    "image", "thumbnail", "card_image", "featured_image", "infographic", "cover", "banner"
)


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def section(text: str, start: str, end: str | None = None) -> str:
    begin = text.find(start)
    if begin < 0:
        return ""
    if end is None:
        return text[begin:]
    finish = text.find(end, begin)
    return text[begin:] if finish < 0 else text[begin:finish]


def audit_project_images(repo: Path, errors: list[str]) -> None:
    project_dir = repo / "_projects"
    if not project_dir.is_dir():
        errors.append("_projects directory is missing; project-image references could not be audited.")
        return

    projects = sorted(
        path for path in project_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".markdown", ".html"}
    )
    if not projects:
        errors.append("No project pages were found under _projects.")
        return

    for path in projects:
        text = path.read_text(encoding="utf-8")
        front_match = re.match(r"\A---\s*\n(.*?)\n---", text, flags=re.S)
        if not front_match:
            errors.append(f"{path.relative_to(repo)} has no readable YAML front matter.")
            continue
        front = front_match.group(1)
        refs: list[str] = []
        for field in IMAGE_FIELDS:
            match = re.search(rf"(?m)^{re.escape(field)}\s*:\s*[\"']?([^\"'\n]+)", front)
            if match:
                refs.append(match.group(1).strip())
        if not refs:
            errors.append(f"{path.relative_to(repo)} has no project image field.")
            continue
        for ref in refs:
            normalized = ref.split("?", 1)[0]
            if "images/projects/infographics/" not in normalized:
                errors.append(
                    f"{path.relative_to(repo)} still references a non-infographic image: {ref}"
                )
                continue
            target = repo / normalized.lstrip("/")
            if not target.is_file():
                errors.append(
                    f"{path.relative_to(repo)} references a missing infographic: {ref}"
                )


def main() -> int:
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else ".").expanduser().resolve()
    errors: list[str] = []

    index_path = repo / "index.md"
    data_path = repo / "_data/homepage.yaml"
    footer_path = repo / "_includes/footer.html"
    style_path = repo / STYLE_FILE

    for path in (index_path, data_path, footer_path, style_path):
        require(path.is_file(), f"Required file is missing: {path.relative_to(repo)}", errors)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    index = index_path.read_text(encoding="utf-8")
    data = data_path.read_text(encoding="utf-8")
    footer = footer_path.read_text(encoding="utf-8")
    style = style_path.read_text(encoding="utf-8")

    # Navigation is intentionally not rewritten by this revision.
    require("Our work is proudly funded by" in index, "Funding acknowledgment text is missing.", errors)
    require("Funding & Fellowship" not in index + data, "Old Funding & Fellowship wording remains.", errors)
    require("images/funders/nsf-logo.svg" in index, "Homepage is not using the crisp NSF SVG.", errors)
    require("images/funders/nih-logo.png" in index, "Homepage is not using the crisp NIH SVG.", errors)
    require("images/funders/nsf-logo.png" not in index, "Homepage still references the old NSF PNG.", errors)
    require("images/funders/nih-logo.png" not in index, "Homepage still references the old NIH PNG.", errors)
    require("border-radius: 16px" in style, "Rounded funder-logo image edges are missing.", errors)
    require("home-hero__funder--logo-only:hover" in style, "Funder-logo hover behavior is missing.", errors)

    active = section(data, "active_projects:", "benchmarking:")
    for title in PROJECT_TITLES:
        require(title in active, f"Featured project is missing: {title}", errors)
    require(active.count("  - title:") == 4, "Active Projects must contain exactly four featured projects.", errors)

    benchmarking = section(data, "benchmarking:", "featured_papers:")
    require(benchmarking.count("  - title:") == 2, "Benchmarking must show exactly two completed benchmark items.", errors)
    require("A third benchmarking study is currently in development." in data, "Third benchmark development note is missing.", errors)
    require("Data and Benchmarking" in index, "Data and Benchmarking heading is missing.", errors)

    papers = section(data, "featured_papers:", "software_resources:")
    for title in PAPER_TITLES:
        require(title in papers, f"Featured paper is missing: {title}", errors)
    require(papers.count("  - title:") == 4, "Featured Papers must contain exactly four balanced selections.", errors)
    require("citrus" not in papers.lower(), "The citrus-fruit paper is still featured.", errors)

    software = section(data, "software_resources:")
    for title in SOFTWARE_TITLES:
        require(title in software, f"Featured software/resource is missing: {title}", errors)
    require(software.count("  - title:") == 4, "Software & Resources must contain exactly four featured entries.", errors)
    require("DeepLime" not in software, "DeepLime still appears in featured software.", errors)

    news = section(index, '<section class="homepage-content-block homepage-content-block--news"')
    require("<h2 id=\"news-heading\">News</h2>" in news, "News section is missing or was renamed.", errors)
    require("news-grid news-grid--home" in news, "Approved News layout is not intact.", errors)

    require("images/brand/bukharilab-logo.png" in footer, "Lab logo is missing from the footer.", errors)
    require("<span>Bukhari Lab</span>" not in footer, "Redundant plain Bukhari Lab identity text remains in the footer.", errors)
    for label in ("Google Scholar", "GitHub", "Website", "LinkedIn", "Hugging Face"):
        require(f"<span>{label}</span>" in footer, f"Footer link is missing: {label}", errors)
    require("https://huggingface.co/bukharilab" in (repo / "_config.yaml").read_text(encoding="utf-8"), "Hugging Face URL is missing from _config.yaml.", errors)
    require("grid-template-columns: repeat(2, minmax(0, 1fr));" in style, "Two-column footer Explore layout is missing.", errors)
    require("Health AI as our primary application domain" in footer, "Lab distinction statement is missing from the footer.", errors)

    audit_project_images(repo, errors)

    if errors:
        print("Faculty-feedback audit failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print("Faculty-feedback audit passed.")
    print("Verified homepage funding, four active projects, benchmark status, balanced papers,")
    print("four software/resources, unchanged News structure, expanded footer links, and project infographics.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
