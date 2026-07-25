"""Canonicalize, validate, and deduplicate generated publication records."""

from __future__ import annotations

import re
from typing import Any

BLOCKED_CITATION_IDS = {"doi:10.32473/flairs.36"}
LINK_OVERRIDES = {
    "leveraging the cedar workbench for ontology linked submission of adaptive immune receptor repertoire data to the sequence read archive sra":
        "https://doi.org/10.6084/m9.figshare.4244126",
    "biomedical image ontology on bioportal":
        "https://bioportal.bioontology.org/ontologies/BIM",
    "the center for expanded data annotation and retrieval":
        "https://doi.org/10.1093/jamia/ocv048",
    "bim an open ontology for the annotation of biomedical images":
        "https://ceur-ws.org/Vol-1515/regular8.pdf",
    "icyrus a semantic framework for biomedical image discovery":
        "https://ceur-ws.org/Vol-1546/paper_30.pdf",
    "sebi an architecture for biomedical image discovery interoperability and reusability based on semantic enrichment":
        "https://ceur-ws.org/Vol-1320/paper_8.pdf",
    "ho2iev heavyweight ontology based web information extraction technique for visionless users":
        "https://ieeexplore.ieee.org/document/5967523/",
}


def normalize_title(value: Any) -> str:
    return " ".join(re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).split())


def citation_quality(citation: dict[str, Any]) -> int:
    score = 0
    score += 8 if citation.get("id") else 0
    score += 5 if citation.get("authors") else 0
    score += 4 if citation.get("link") else 0
    score += 2 if citation.get("date") else 0
    score += 1 if citation.get("publisher") or citation.get("journal") else 0
    return score


def normalize_generated_citation(
    citation: dict[str, Any],
    source_id: str = "",
) -> dict[str, Any] | None:
    citation = dict(citation)
    title = str(citation.get("title", "")).strip()
    raw_id = str(source_id or citation.get("id", "")).strip()
    normalized_id = raw_id.lower()

    if not title or normalized_id in BLOCKED_CITATION_IDS:
        return None

    if normalized_id.startswith("doi:"):
        citation["link"] = "https://doi.org/" + raw_id[4:].strip()
    elif normalized_id.startswith("arxiv:"):
        citation["link"] = "https://arxiv.org/abs/" + raw_id[6:].strip()
    else:
        override = LINK_OVERRIDES.get(normalize_title(title))
        if override:
            citation["link"] = override
        elif isinstance(citation.get("link"), str):
            citation["link"] = citation["link"].replace(
                "http://www.scopus.com/",
                "https://www.scopus.com/",
            )

    return citation


def deduplicate_generated_citations(
    citations: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    selected: dict[str, dict[str, Any]] = {}
    order: list[str] = []

    for citation in citations:
        key = normalize_title(citation.get("title"))
        if not key:
            continue

        if key not in selected:
            selected[key] = citation
            order.append(key)
            continue

        current = selected[key]
        if citation_quality(citation) > citation_quality(current):
            better, other = citation, current
        else:
            better, other = current, citation

        for field, value in other.items():
            if not better.get(field) and value:
                better[field] = value
        selected[key] = better

    return [selected[key] for key in order]
