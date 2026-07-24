# Bukhari Lab Website

The Bukhari Lab website is a Jekyll site deployed through GitHub Pages. It presents the lab's work in trustworthy, auditable, and explainable artificial intelligence, with Health AI as the primary application domain.

## Requirements

- Ruby 3.2
- Bundler
- Python 3.12 or a compatible Python 3 release

Install dependencies from the repository root:

```bash
bundle install
python3 -m pip install -r _cite/requirements.txt Pillow==11.3.0
```

## Local development

```bash
bundle exec jekyll serve --livereload
```

Open `http://127.0.0.1:4000/`. Restart Jekyll after changing `_config.yaml`.

## Complete local validation

Run the same core checks used by pull-request CI:

```bash
./scripts/validate_site.sh
```

The validation command:

1. rebuilds the site from a clean `_site` directory;
2. runs the public-release audit;
3. runs the faculty-feedback and data-consistency audit;
4. confirms every project uses an approved infographic;
5. validates generated internal links and images with HTMLProofer;
6. checks for whitespace errors.

## Production build

GitHub Pages deploys committed source and publication data from `main`. Production deployment does not refresh external publication records, which keeps builds reproducible.

To test the optimized artifact locally:

```bash
rm -rf _site .jekyll-cache
bundle exec jekyll build
python3 scripts/optimize_built_site.py --site-dir _site
python3 scripts/public_release_audit.py . --include-built
```

## Content locations

| Content | Location |
|---|---|
| Homepage layout | `index.md` |
| Homepage selections | `_data/homepage.yaml` |
| Canonical software catalog | `_data/software_catalog.yaml` |
| Publications | `_data/papers.yaml`, `_data/citations.yaml` |
| Projects | `_projects/` and `_data/projects.yaml` |
| Team members | `_members/` |
| News | `_posts/` |
| Site navigation and social links | `_config.yaml` |
| Images | `images/` |

## Featured software

The homepage stores only canonical software IDs in `_data/homepage.yaml` under `featured_software_ids`. Titles, descriptions, icons, and URLs come from `_data/software_catalog.yaml`.

When adding or changing featured software:

1. Add or update the canonical record in `_data/software_catalog.yaml`.
2. Give the record a unique `id`.
3. Add that ID to `_data/homepage.yaml`.
4. Run `./scripts/validate_site.sh`.

This prevents the homepage and Software page from drifting apart.

## Adding a publication

Publication data is committed to the repository. To refresh records from the configured sources:

```bash
./scripts/refresh_publications.sh
```

Review the generated diff before committing. A normal website deployment does not call external publication services.

## Adding a project

1. Add a Markdown file under `_projects/` with valid YAML front matter.
2. Add an approved image under `images/projects/infographics/`.
3. Set the project's image field to that infographic.
4. Run:

```bash
python3 scripts/refresh_project_images.py . --check
```

The approved project-image mappings are maintained in `scripts/refresh_project_images.py`.

## Adding news

Create a file under `_posts/` using the name format:

```text
YYYY-MM-DD-title.md
```

Include valid front matter and a licensed or lab-owned image. Record external image attribution in `IMAGE_CREDITS.md` when required.

## Branch and pull-request workflow

```bash
git switch main
git pull --ff-only origin main
git switch -c descriptive-branch-name
```

After making changes:

```bash
./scripts/validate_site.sh
git status
git add .
git commit -m "Describe the website change"
git push -u origin descriptive-branch-name
```

Open a pull request into `main`. The `Validate website` workflow must pass before merging. The production Pages workflow runs only after changes reach `main`.

## Deployment

- `.github/workflows/validate.yml` validates pull requests.
- `.github/workflows/pages.yml` builds, audits, optimizes, and deploys `main`.
- `.github/workflows/refresh-publications.yml` refreshes citation data monthly and opens a reviewable pull request when records change.
- Dependabot checks Bundler and GitHub Actions dependencies monthly.
- Third-party browser libraries, MathJax, and GitHub Actions are pinned to exact versions for reproducible builds.

Do not force-push `main` or bypass failed validation checks.
