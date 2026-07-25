#!/usr/bin/env python3
"""Validate factual source mappings, internal assets, and known public links."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


DENIED_URLS = {
    "https://github.com/bukharilab/Semantically",
    "https://github.com/bukharilab/deepflaim",
    "https://github.com/bukharilab/linkedimm",
    "https://github.com/bukharilab/diseasepredictionmodels",
    "https://github.com/bukharilab/annotatia",
    "https://github.com/bukharilab/LymeDetector",
    "https://github.com/bukharilab/CEDAROnDemand",
}
EXPECTED_FEATURED_SOFTWARE = [
    "mediloom",
    "semantically",
    "gosemantically",
    "airr_standards",
]
BLOCKED_CITATION_IDS = {"doi:10.32473/flairs.36"}


def load_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"Could not parse {path}: {exc}") from exc


def normalize_title(value: Any) -> str:
    text = re.sub(r"[^a-z0-9]+", " ", str(value or "").lower())
    return " ".join(text.split())


def parse_front_matter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data = yaml.safe_load(parts[1]) or {}
    return data if isinstance(data, dict) else {}


def collect_urls(value: Any) -> set[str]:
    urls: set[str] = set()
    if isinstance(value, dict):
        for item in value.values():
            urls.update(collect_urls(item))
    elif isinstance(value, list):
        for item in value:
            urls.update(collect_urls(item))
    elif isinstance(value, str) and value.startswith(("http://", "https://")):
        urls.add(value)
    return urls


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", nargs="?", default=".")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    errors: list[str] = []

    required = [
        "_config.yaml",
        "_data/homepage.yaml",
        "_data/software_catalog.yaml",
        "_data/lab_portfolio.yaml",
        "_data/projects.yaml",
        "_data/papers.yaml",
        "_data/citations.yaml",
    ]
    for relative in required:
        if not (repo / relative).is_file():
            errors.append(f"Missing required file: {relative}")
    if errors:
        print("Content-integrity audit failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    config = load_yaml(repo / "_config.yaml") or {}
    homepage = load_yaml(repo / "_data/homepage.yaml") or {}
    software = load_yaml(repo / "_data/software_catalog.yaml") or {}
    portfolio = load_yaml(repo / "_data/lab_portfolio.yaml") or {}
    projects = load_yaml(repo / "_data/projects.yaml") or []
    papers = load_yaml(repo / "_data/papers.yaml") or {}
    citations = load_yaml(repo / "_data/citations.yaml") or []

    if config.get("hugging_face_url") != "https://huggingface.co/BukhariLab":
        errors.append("Hugging Face URL is not the canonical BukhariLab organization URL.")

    featured_ids = homepage.get("featured_software_ids", [])
    if featured_ids != EXPECTED_FEATURED_SOFTWARE:
        errors.append(
            "Homepage featured software IDs must be: "
            + ", ".join(EXPECTED_FEATURED_SOFTWARE)
        )

    all_structured_urls = set()
    for data in (config, homepage, software, portfolio, projects, papers, citations):
        all_structured_urls.update(collect_urls(data))

    for url in sorted(DENIED_URLS & all_structured_urls):
        errors.append(f"Known broken, empty, or misleading destination remains: {url}")

    featured = software.get("featured", [])
    if not isinstance(featured, list):
        errors.append("_data/software_catalog.yaml featured must be a list.")
        featured = []
    by_id = {
        item.get("id"): item
        for item in featured
        if isinstance(item, dict) and item.get("id")
    }
    for software_id in EXPECTED_FEATURED_SOFTWARE:
        if software_id not in by_id:
            errors.append(f"Canonical featured software record is missing: {software_id}")

    semantically = by_id.get("semantically", {})
    if semantically:
        if semantically.get("link") != "https://ceur-ws.org/Vol-2980/paper367.pdf":
            errors.append("Semantically must link to its verified CEUR-WS paper.")
        description = str(semantically.get("description", "")).lower()
        for phrase in ("open-source", "biomedical", "authoring", "publishing"):
            if phrase not in description:
                errors.append(f"Semantically description is missing factual concept: {phrase}")

    if "deep_flaim" in by_id:
        errors.append("Deep-FLAIM is a published research model, not a verified public software repository.")

    documented = portfolio.get("documented", [])
    portfolio_by_slug = {
        item.get("slug"): item
        for item in documented
        if isinstance(item, dict) and item.get("slug")
    }
    deep_flaim = portfolio_by_slug.get("deep-flaim")
    if deep_flaim:
        if deep_flaim.get("link") != "https://pubmed.ncbi.nlm.nih.gov/32773672/":
            errors.append("Deep-FLAIM must link to its verified PubMed record.")
        if deep_flaim.get("software") is not False:
            errors.append("Deep-FLAIM must be classified as a research model, not public software.")
    else:
        errors.append("Deep-FLAIM research record is missing from the lab portfolio.")

    forbidden_portfolio_slugs = {
        "cedar-ondemand",
        "linked-im",
        "disease-prediction-model",
        "ghost-semanticly",
        "anaplasia",
    }
    present_slugs = {
        item.get("slug")
        for section in ("documented", "additional_repositories", "additional_initiatives")
        for item in portfolio.get(section, [])
        if isinstance(item, dict)
    }
    for slug in sorted(forbidden_portfolio_slugs & present_slugs):
        errors.append(f"Unsupported or intentionally removed portfolio entry remains: {slug}")

    project_permalinks: set[str] = set()
    for path in (repo / "_projects").glob("*.md"):
        permalink = parse_front_matter(path).get("permalink")
        if permalink:
            project_permalinks.add(str(permalink))

    if not isinstance(projects, list):
        errors.append("_data/projects.yaml must contain a list.")
        projects = []
    for project in projects:
        if not isinstance(project, dict):
            errors.append("Project entry is not a mapping.")
            continue
        title = str(project.get("title", "[untitled]"))
        image = str(project.get("image", ""))
        detail = str(project.get("detail", ""))
        link = str(project.get("link", ""))
        publication = str(project.get("publication", ""))
        if not image or not (repo / image.lstrip("/")).is_file():
            errors.append(f"Project image is missing for {title}: {image}")
        if detail not in project_permalinks:
            errors.append(f"Project detail route has no matching page for {title}: {detail}")
        if not link.startswith("https://"):
            errors.append(f"Project link must use HTTPS for {title}: {link}")
        if publication != link:
            errors.append(f"Project publication and primary link disagree for {title}.")

    benchmark_titles = {
        str(item.get("title", ""))
        for item in papers.get("benchmarking", [])
        if isinstance(item, dict)
    }
    if not any(title.startswith("SynTrustBench") for title in benchmark_titles):
        errors.append("SynTrustBench is missing from _data/papers.yaml.")

    seen_titles: dict[str, int] = {}
    if not isinstance(citations, list):
        errors.append("_data/citations.yaml must contain a list.")
        citations = []
    for index, citation in enumerate(citations):
        if not isinstance(citation, dict):
            errors.append(f"Citation {index + 1} is not a mapping.")
            continue
        title = str(citation.get("title", "")).strip()
        citation_id = str(citation.get("id", "")).strip()
        link = str(citation.get("link", "")).strip()
        if not title:
            errors.append(f"Citation {index + 1} has no title.")
            continue
        normalized = normalize_title(title)
        if normalized in seen_titles:
            errors.append(
                f"Duplicate citation title: {title!r} "
                f"(entries {seen_titles[normalized] + 1} and {index + 1})"
            )
        else:
            seen_titles[normalized] = index
        if citation_id.lower() in BLOCKED_CITATION_IDS:
            errors.append(f"Proceedings/container DOI remains: {citation_id}")
        if citation_id.lower().startswith("doi:"):
            expected = "https://doi.org/" + citation_id[4:].strip()
            if link != expected:
                errors.append(f"DOI citation does not use canonical DOI link: {citation_id}")
        elif citation_id.lower().startswith("arxiv:"):
            expected = "https://arxiv.org/abs/" + citation_id[6:].strip()
            if link != expected:
                errors.append(f"arXiv citation does not use canonical abstract link: {citation_id}")
        elif link and not link.startswith("https://"):
            errors.append(f"Citation link must use HTTPS: {link}")

    image_owners: dict[str, str] = {}
    for member_path in (repo / "_members").glob("*.md"):
        front = parse_front_matter(member_path)
        image = str(front.get("image", "")).strip()
        if not image:
            continue
        if image in image_owners:
            errors.append(
                f"Team image is assigned to more than one person: {image} "
                f"({image_owners[image]} and {member_path.name})"
            )
        else:
            image_owners[image] = member_path.name
        if not (repo / image.lstrip("/")).is_file():
            errors.append(f"Member image does not exist: {member_path.name} -> {image}")

    for source_path in repo.rglob("*"):
        if not source_path.is_file():
            continue
        if any(part in {".git", "_site", "vendor", ".jekyll-cache"} for part in source_path.parts):
            continue
        if source_path.suffix.lower() not in {".md", ".html", ".yaml", ".yml"}:
            continue
        try:
            text = source_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for match in re.findall(r'http://[^\s"\'<>]+', text):
            if match.startswith(("http://localhost", "http://127.0.0.1")):
                continue
            errors.append(f"Insecure HTTP URL in {source_path.relative_to(repo)}: {match}")

    if errors:
        print("Content-integrity audit failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Content-integrity audit passed.")
    print(
        "Verified software/resource mappings, project routes and images, "
        "citation destinations, team images, and HTTPS source links."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
