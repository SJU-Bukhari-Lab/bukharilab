#!/usr/bin/env python3
"""Apply the approved project-to-infographic mappings safely.

The script parses YAML front matter with PyYAML, verifies every target image,
and updates only recognized image fields. It is transactional: source files are
written only after all mappings and front matter validate successfully.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "PyYAML is required. Install dependencies with "
        "python3 -m pip install -r _cite/requirements.txt"
    ) from exc

MAPPINGS = {
    "a-deep-learning-approach-for-covid-19-8-viral-pneumonia-screening-with-x-ray-images.md":
        "images/projects/infographics/covid-xray-screening-infographic.webp",
    "a-linked-data-graph-approach-to-integration-of-immunological-data.md":
        "images/projects/infographics/linked-immunology-data-infographic.webp",
    "classification-of-positive-covid-19-ct-scans-using-deep-learning.md":
        "images/projects/infographics/covid-ct-classification-infographic.webp",
    "formal-representation-of-immunology-related-data-with-ontologies.md":
        "images/projects/infographics/formal-immunology-ontologies-infographic.webp",
    "how-representative-is-a-sparql-benchmark-an-analysis-of-rdf-triplestore-benchmarks.md":
        "images/projects/infographics/sparql-benchmark-infographic.webp",
    "lda-ga-svm-improved-hepatocellular-carcinoma-prediction-through-dimensionality-reduction-and-genetically-optimized-support-vector-machine.md":
        "images/projects/infographics/lda-ga-svm-infographic.webp",
    "multimodal-brain-tumor-classification-using-deep-learning-and-robust-feature-selection-a-machine-learning-application-for-radiologists.md":
        "images/projects/infographics/brain-tumor-classification-infographic.webp",
    "ontology-based-scientific-metadata-generation.md":
        "images/projects/infographics/ontology-metadata-generation-infographic.webp",
    "our-socio-technical-approach-for-biomedical-content-authoring-and-structured-web-publishing.md":
        "images/projects/infographics/our-socio-technical-approach-infographic.webp",
    "predicting-30-days-all-cause-hospital-readmissions-considering-discharge-to-alternate-care-facilities.md":
        "images/projects/infographics/hospital-readmissions-infographic.webp",
    "reporting-and-connecting-cell-type-names-and-gating-definitions-through-ontologies.md":
        "images/projects/infographics/cell-type-gating-ontologies-infographic.webp",
    "statistically-rigorous-deep-neural-network-approach-to-predict-mortality-in-trauma-patients-admitted-to-the-intensive-care-unit.md":
        "images/projects/infographics/trauma-mortality-infographic.webp",
    "the-adc-api-a-web-api-for-the-programmatic-query-of-the-airr-data-commons.md":
        "images/projects/infographics/adc-api-infographic.webp",
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

FRONT_MATTER_RE = re.compile(r"\A---\s*\n(?P<front>.*?)\n---(?P<body>.*)\Z", re.S)


def replace_front_matter_image_fields(front_text: str, target: str) -> str:
    """Preserve formatting while replacing existing top-level image fields."""
    updated = front_text
    matched = False

    for field in IMAGE_FIELDS:
        pattern = re.compile(
            rf"(?m)^(?P<indent>[ \t]*){re.escape(field)}\s*:\s*.*$"
        )
        if pattern.search(updated):
            updated = pattern.sub(rf"\g<indent>{field}: {target}", updated)
            matched = True

    if not matched:
        suffix = "" if updated.endswith("\n") else "\n"
        updated = f"{updated}{suffix}image: {target}"

    return updated


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", nargs="?", default=".")
    parser.add_argument("--check", action="store_true", help="Validate without writing files.")
    args = parser.parse_args()

    repo = Path(args.repo).expanduser().resolve()
    projects_dir = repo / "_projects"
    errors: list[str] = []
    pending: dict[Path, str] = {}

    if not projects_dir.is_dir():
        raise SystemExit(f"Project directory not found: {projects_dir}")

    for filename, target in MAPPINGS.items():
        project_path = projects_dir / filename
        image_path = repo / target

        if not project_path.is_file():
            errors.append(f"Missing project file: {project_path.relative_to(repo)}")
            continue
        if not image_path.is_file():
            errors.append(f"Missing infographic: {target}")
            continue

        text = project_path.read_text(encoding="utf-8")
        match = FRONT_MATTER_RE.match(text)
        if not match:
            errors.append(f"Unreadable YAML front matter: {project_path.relative_to(repo)}")
            continue

        front_text = match.group("front")
        try:
            front = yaml.safe_load(front_text) or {}
        except yaml.YAMLError as exc:
            errors.append(f"Invalid YAML in {project_path.relative_to(repo)}: {exc}")
            continue

        if not isinstance(front, dict):
            errors.append(f"Front matter is not a mapping: {project_path.relative_to(repo)}")
            continue

        updated_front = replace_front_matter_image_fields(front_text, target)
        try:
            parsed_updated = yaml.safe_load(updated_front) or {}
        except yaml.YAMLError as exc:
            errors.append(f"Updated YAML would be invalid in {project_path.relative_to(repo)}: {exc}")
            continue

        refs = [parsed_updated.get(field) for field in IMAGE_FIELDS if parsed_updated.get(field)]
        if not refs or any(ref != target for ref in refs):
            errors.append(f"Could not normalize image fields in {project_path.relative_to(repo)}")
            continue

        pending[project_path] = f"---\n{updated_front}\n---{match.group('body')}"

    if errors:
        print("Project-image refresh failed; no files were changed:", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    if args.check:
        for path, updated in pending.items():
            current = path.read_text(encoding="utf-8")
            if current != updated:
                print(f"NEEDS UPDATE: {path.relative_to(repo)}")
                return 1
        print(f"Project-image mappings are current for {len(pending)} project files.")
        return 0

    changed = 0
    for path, updated in pending.items():
        if path.read_text(encoding="utf-8") != updated:
            path.write_text(updated, encoding="utf-8")
            changed += 1

    print(f"Verified {len(pending)} project-to-infographic mappings; updated {changed} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
