# Link and Content Audit

Last researched: July 24, 2026.

This repository separates three different validation concerns:

1. **Internal site integrity**: Jekyll build and HTMLProofer verify internal routes, anchors, scripts, and image assets.
2. **External-link integrity**: `scripts/audit_external_links.py` checks every rendered external `href` and `src`, follows redirects, and fails on confirmed permanent failures such as HTTP 404 or 410.
3. **Content integrity**: `scripts/audit_content_integrity.py` verifies canonical software mappings, project routes and infographics, publication destinations, team-image ownership, HTTPS links, and known removed or misleading records.

## Source decisions

The cleanup uses public primary or authoritative sources wherever available:

- **Semantically** is represented by its peer-reviewed CEUR-WS system paper, which describes an open-source framework for structured, ontology-enriched biomedical content authoring and Web publishing. The former GitHub destination does not resolve publicly.
- **Deep-FLAIM** is represented as a published research model and links to its PubMed record. It is not presented as downloadable public software because the former GitHub destination does not resolve publicly.
- **MediLoom**, **Burnout Surveillance AI**, **KG-4Bio**, **AIRR Standards**, **goSemantically**, and **SynTrustBench** retain their verified public GitHub repositories.
- Empty or undocumented repository cards were removed from the public catalog rather than given unsupported descriptions.
- DOI-based publications use canonical `https://doi.org/...` destinations; arXiv records use canonical abstract pages.
- The principal-investigator biography was reduced to facts supported by the official St. John’s University faculty profile.

## Automated policy

The scheduled workflow runs weekly and on pull requests. A permanent 404 or 410 fails the audit. Some sites deliberately block automated clients with 401, 403, 429, or 451 responses; those are reported separately and require manual review rather than being mislabeled as broken.

No external URL can be guaranteed to remain available forever. The weekly audit is the safeguard against future link rot.
