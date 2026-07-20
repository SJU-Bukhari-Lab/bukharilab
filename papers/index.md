---
title: Papers
nav:
  order: 2
  tooltip: Publications and benchmarking research
---

<div class="interior-hero interior-hero--papers">
  <p class="interior-hero__eyebrow">Publications &amp; scholarship</p>
  <h1>Papers</h1>
  <p>Explore the lab’s publications across benchmarking, trustworthy clinical AI, biomedical knowledge engineering, predictive analytics, and semantic interoperability.</p>
  <div class="interior-hero__actions">
    {% include button.html type="google-scholar" text="Google Scholar" link="https://scholar.google.com/citations?hl=en&user=JhWJ5PEAAAAJ" %}
    {% include button.html link="research" text="Related research" style="bare" %}
  </div>
</div>

{% include section.html %}

<div class="interior-section">
  <div class="interior-heading">
    <p class="interior-heading__eyebrow">Benchmarking</p>
    <h2>Benchmarking &amp; Evaluation</h2>
    <p>Benchmark-oriented scholarship evaluating clinical AI readiness, interoperability, and biomedical data infrastructure.</p>
  </div>

  <div class="publication-grid publication-grid--benchmark">
    {% for paper in site.data.papers.benchmarking %}
      <article class="publication-card publication-card--benchmark">
        <span class="publication-card__badge">Benchmarking</span>
        <p class="publication-card__meta">{{ paper.venue }} · {{ paper.year }}</p>
        <h3><a href="{{ paper.link }}" target="_blank" rel="noopener noreferrer">{{ paper.title }}</a></h3>
        <p>{{ paper.description }}</p>
        <a class="publication-card__link" href="{{ paper.link }}" target="_blank" rel="noopener noreferrer">
          Read paper <i class="fa-solid fa-arrow-right" aria-hidden="true"></i>
        </a>
      </article>
    {% endfor %}
  </div>

  <div class="development-note development-note--light">
    <i class="fa-solid fa-flask" aria-hidden="true"></i>
    <div>
      <strong>Benchmarking research in progress</strong>
      <p>The lab continues to expand its benchmarking portfolio across clinical AI and biomedical data infrastructure.</p>
    </div>
  </div>
</div>

{% include section.html %}

<div class="interior-section">
  <div class="interior-heading">
    <p class="interior-heading__eyebrow">Research highlights</p>
    <h2>Selected Recent Work</h2>
    <p></p>
  </div>

  <div class="publication-grid">
    {% for paper in site.data.papers.selected %}
      <article class="publication-card">
        <span class="publication-card__badge">{{ paper.area }}</span>
        <p class="publication-card__meta">{{ paper.venue }} · {{ paper.year }}</p>
        <h3><a href="{{ paper.link }}" target="_blank" rel="noopener noreferrer">{{ paper.title }}</a></h3>
        <p>{{ paper.description }}</p>
        <a class="publication-card__link" href="{{ paper.link }}" target="_blank" rel="noopener noreferrer">
          Read paper <i class="fa-solid fa-arrow-right" aria-hidden="true"></i>
        </a>
      </article>
    {% endfor %}
  </div>
</div>

{% include section.html %}

<div class="interior-section publications-browser">
  <div class="interior-heading interior-heading--split">
    <div>
      <p class="interior-heading__eyebrow">Publication record</p>
      <h2>All Publications</h2>
      <p></p>
    </div>
    <a
      class="catalog-count"
      href="https://scholar.google.com/citations?hl=en&user=JhWJ5PEAAAAJ"
      target="_blank"
      rel="noopener noreferrer"
    >
      Google Scholar profile
      <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i>
    </a>
  </div>

  {% assign all_citations = site.data.citations | sort: "date" | reverse %}

  {% if all_citations and all_citations.size > 0 %}
    <div class="publication-toolbar" aria-label="Publication filters">
      <div class="publication-toolbar__search">
        <label for="publication-search">Search publications</label>
        <div class="publication-search-field">
          <i class="fa-solid fa-magnifying-glass" aria-hidden="true"></i>
          <input
            id="publication-search"
            type="search"
            placeholder="Search by title, author, journal, or keyword"
            autocomplete="off"
          >
        </div>
      </div>

      <div class="publication-toolbar__select">
        <label for="publication-year">Year</label>
        <select id="publication-year">
          <option value="">All years</option>
        </select>
      </div>

      <div class="publication-toolbar__select">
        <label for="publication-category">Research area</label>
        <select id="publication-category">
          <option value="">All areas</option>
        </select>
      </div>

      <button class="publication-toolbar__reset" id="publication-reset" type="button">
        Clear filters
      </button>
    </div>

    <div class="publication-results-summary" aria-live="polite">
      <span id="publication-results-count">{{ all_citations.size }} publications</span>
      <span>Newest first</span>
    </div>

    <div class="publication-catalog-grid" id="publication-catalog">
      {% for citation in all_citations %}
        {% include publication-grid-card.html citation=citation %}
      {% endfor %}
    </div>

    <div class="publication-empty-state" id="publication-empty-state" hidden>
      <i class="fa-solid fa-file-circle-question" aria-hidden="true"></i>
      <h3>No publications match these filters</h3>
      <p>Try a broader search term or clear the selected filters.</p>
    </div>
  {% else %}
    <div class="publication-catalog-grid">
      {% for paper in site.data.projects %}
        {% assign paper_url = paper.publication | default: paper.link %}
        <article class="publication-grid-card" data-year="" data-category="Research publication">
          <div class="publication-grid-card__top">
            <span class="publication-grid-card__icon">
              <i class="fa-solid fa-file-lines" aria-hidden="true"></i>
            </span>
            <span class="publication-grid-card__category">Research publication</span>
          </div>
          <h3>
            <a href="{{ paper_url }}" target="_blank" rel="noopener noreferrer">{{ paper.title }}</a>
          </h3>
          <p class="publication-grid-card__authors">{{ paper.description | strip_html | truncate: 150 }}</p>
          <a class="publication-grid-card__action" href="{{ paper_url }}" target="_blank" rel="noopener noreferrer">
            Read publication <i class="fa-solid fa-arrow-right" aria-hidden="true"></i>
          </a>
        </article>
      {% endfor %}
    </div>
  {% endif %}
</div>

{% include section.html %}

<div class="continuation-panel">
  <div>
    <p class="interior-heading__eyebrow">Connected portfolio</p>
    <h2>From Publications to Research Infrastructure</h2>
    <p>Explore the projects, repositories, standards, and tools connected to the lab’s scholarly work.</p>
  </div>
  <div class="continuation-panel__actions">
    {% include button.html link="research" text="Explore research" %}
    {% include button.html link="software" text="Explore software" style="bare" %}
  </div>
</div>
