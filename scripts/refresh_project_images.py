#!/usr/bin/env python3
"""Safely point every project page at a matching generated infographic.

The script is transactional: it changes nothing unless each project can be mapped
unambiguously to an existing file under images/projects/infographics.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

IMAGE_FIELDS = (
    "image",
    "thumbnail",
    "card_image",
    "featured_image",
    "infographic",
    "cover",
    "banner",
)
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".svg"}

PROJECT_ALIASES = {
    "clinician burnout": ["burnout surveillance", "narrative driven ai", "burnout"],
    "drug repurposing": ["neuro symbolic ai", "drug repurposing ai", "repurposing"],
    "medical coding": ["extreme multi label", "trustworthy medical coding", "clinical coding"],
    "biomedical content": ["content authoring publishing", "biomedical publishing", "socio technical"],
    "kg4bio": ["kg 4 bio", "knowledge graph bio", "knowledge graph for bio"],
    "mediloom": ["medi loom"],
    "care escalators": ["semanticly care escalators", "care escalation"],
    "ghost": ["ghost semanticly linked im", "semanticly linked im"],
    "deepflame": ["deep flame", "deepflaim", "semantically deepflame"],
    "ai standards": ["air ai standards", "air standards"],
    "disease prediction": ["disease prediction model"],
    "lyme": ["lyme detector", "lyme disease"],
    "anaplasia": ["anaplasmosis", "anaplasia detector"],
    "cedar": ["cedar ondemand", "cedar on demand"],
    "fhirtrustbench": ["fhir trust bench", "fhir benchmark"],
    "sparql": ["rdf triplestore benchmark", "sparql benchmark"],
}

STOPWORDS = {
    "a", "an", "and", "the", "of", "for", "to", "in", "on", "with",
    "using", "based", "project", "framework", "system", "approach",
}


@dataclass
class Project:
    path: Path
    text: str
    front_matter: str
    body: str
    fields: dict[str, str]
    title: str
    slug: str


def normalize(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    tokens = [token for token in value.split() if token not in STOPWORDS]
    return " ".join(tokens)


def compact(value: str) -> str:
    return normalize(value).replace(" ", "")


def tokens(value: str) -> set[str]:
    return set(normalize(value).split())


def parse_project(path: Path) -> Project:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n?", text, flags=re.S)
    if not match:
        raise ValueError(f"Missing YAML front matter: {path}")
    front = match.group(1)
    body = text[match.end():]
    fields: dict[str, str] = {}
    for line in front.splitlines():
        field_match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*?)\s*$", line)
        if field_match:
            value = field_match.group(2).strip().strip('"\'')
            fields[field_match.group(1)] = value
    title = fields.get("title", path.stem.replace("-", " "))
    slug = fields.get("slug", path.stem)
    return Project(path, text, front, body, fields, title, slug)


def candidate_score(project: Project, candidate: Path) -> float:
    stem = candidate.stem
    aliases = [project.slug, project.path.stem, project.title]
    project_identity = normalize(" ".join((project.slug, project.path.stem, project.title)))
    for key, values in PROJECT_ALIASES.items():
        if key in project_identity:
            aliases.extend(values)
    current_names = []
    for key in IMAGE_FIELDS:
        value = project.fields.get(key)
        if value:
            current_names.append(Path(value).stem)
    aliases.extend(current_names)

    candidate_compact = compact(stem)
    candidate_tokens = tokens(stem)
    best = 0.0
    for alias in aliases:
        alias_compact = compact(alias)
        alias_tokens = tokens(alias)
        if not alias_compact:
            continue
        if candidate_compact == alias_compact:
            best = max(best, 100.0)
        elif candidate_compact in alias_compact or alias_compact in candidate_compact:
            ratio = min(len(candidate_compact), len(alias_compact)) / max(len(candidate_compact), len(alias_compact))
            best = max(best, 76.0 + 18.0 * ratio)
        if alias_tokens and candidate_tokens:
            intersection = len(alias_tokens & candidate_tokens)
            union = len(alias_tokens | candidate_tokens)
            jaccard = intersection / union
            coverage = intersection / min(len(alias_tokens), len(candidate_tokens))
            best = max(best, 58.0 * jaccard + 34.0 * coverage)
    return best


def relative_asset(repo: Path, path: Path) -> str:
    return "/" + path.relative_to(repo).as_posix()


def replace_or_add_fields(project: Project, asset: str) -> str:
    front = project.front_matter
    present = [key for key in IMAGE_FIELDS if re.search(rf"(?m)^{re.escape(key)}\s*:", front)]
    fields_to_write = present or ["image", "infographic"]
    for key in fields_to_write:
        pattern = rf"(?m)^({re.escape(key)}\s*:)\s*.*$"
        replacement = rf'\1 "{asset}"'
        if re.search(pattern, front):
            front = re.sub(pattern, replacement, front)
        else:
            front = front.rstrip() + f'\n{key}: "{asset}"'
    return f"---\n{front}\n---\n{project.body}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", type=Path)
    parser.add_argument("--apply", action="store_true", help="Write the verified mappings")
    args = parser.parse_args()

    repo = args.repo.expanduser().resolve()
    project_dir = repo / "_projects"
    infographic_dir = repo / "images" / "projects" / "infographics"

    if not project_dir.is_dir():
        print("Project image update skipped: _projects was not found.")
        return 2
    if not infographic_dir.is_dir():
        print("Project image update skipped: images/projects/infographics was not found.")
        return 2

    project_paths = sorted(
        path for path in project_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".markdown", ".html"}
    )
    candidates = sorted(
        path for path in infographic_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    )
    if not project_paths or not candidates:
        print("Project image update skipped: project pages or infographic assets are missing.")
        return 2

    projects: list[Project] = []
    errors: list[str] = []
    for path in project_paths:
        try:
            projects.append(parse_project(path))
        except ValueError as exc:
            errors.append(str(exc))

    mappings: dict[Path, Path] = {}
    for project in projects:
        ranked = sorted(
            ((candidate_score(project, candidate), candidate) for candidate in candidates),
            key=lambda item: (-item[0], item[1].as_posix()),
        )
        top_score, top_candidate = ranked[0]
        second_score = ranked[1][0] if len(ranked) > 1 else 0.0

        current_new = None
        for key in IMAGE_FIELDS:
            value = project.fields.get(key, "")
            if "images/projects/infographics/" in value:
                possible = repo / value.lstrip("/")
                if possible.is_file():
                    current_new = possible
                    break
        if current_new:
            mappings[project.path] = current_new
            continue

        if top_score < 62.0 or (second_score >= 62.0 and top_score - second_score < 8.0):
            suggestions = ", ".join(f"{candidate.name} ({score:.1f})" for score, candidate in ranked[:3])
            errors.append(f"{project.path.relative_to(repo)}: no unique match; candidates: {suggestions}")
            continue
        mappings[project.path] = top_candidate

    if errors:
        print("Project images were not changed because every project could not be mapped safely:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(f"Verified {len(mappings)} project-to-infographic mappings:")
    for project_path, asset_path in mappings.items():
        print(f"  {project_path.relative_to(repo)} -> {asset_path.relative_to(repo)}")

    if not args.apply:
        print("Dry run only. Run again with --apply to write these mappings.")
        return 0

    replacements = {
        project.path: replace_or_add_fields(project, relative_asset(repo, mappings[project.path]))
        for project in projects
    }
    for path, text in replacements.items():
        path.write_text(text, encoding="utf-8")

    print(f"Updated project image fields for {len(replacements)} project pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
