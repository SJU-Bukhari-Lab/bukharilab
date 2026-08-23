---
title: Research
nav:
  order: 1
  tooltip: Research areas and initiatives
---

<div class="interior-hero interior-hero--research">
  <p class="interior-hero__eyebrow">Auditability · Explainability · Trustworthiness</p>
  <h1>Research</h1>
  <p>We develop biomedical and healthcare AI that can be inspected, explained, evaluated, and responsibly integrated into scientific and clinical workflows.</p>
  <div class="interior-hero__actions">
    {% include button.html link="papers" text="Explore papers" %}
    {% include button.html link="software" text="Explore software" style="bare" %}
  </div>
</div>

{% include section.html %}

<div class="interior-section">
  <div class="interior-heading">
    <p class="interior-heading__eyebrow">Research identity</p>
    <h2>Core Research Pillars</h2>
    <p>Our portfolio connects foundational AI methods with biomedical data, clinical systems, knowledge engineering, and rigorous evaluation.</p>
  </div>

  <div class="pillar-grid">
    <article class="pillar-card"><i class="fa-solid fa-shield-halved" aria-hidden="true"></i><h3>Trustworthy &amp; Auditable AI</h3><p>Systems whose evidence, limitations, decisions, and human oversight can be examined throughout the AI lifecycle.</p></article>
    <article class="pillar-card"><i class="fa-solid fa-eye" aria-hidden="true"></i><h3>Explainable Clinical AI</h3><p>Models and interfaces designed to help clinicians and other stakeholders understand how recommendations are produced.</p></article>
    <article class="pillar-card"><i class="fa-solid fa-diagram-project" aria-hidden="true"></i><h3>Biomedical Knowledge Engineering</h3><p>Ontologies, linked data, semantic technologies, knowledge graphs, and structured scientific metadata.</p></article>
    <article class="pillar-card"><i class="fa-solid fa-gauge-high" aria-hidden="true"></i><h3>Data and Benchmarking</h3><p>Frameworks that make biomedical AI and data infrastructure measurable, comparable, and reproducible.</p></article>
  </div>
</div>

{% include section.html %}

<div class="interior-section">
  <div class="interior-heading">
    <p class="interior-heading__eyebrow">Research portfolio</p>
    <h2>Projects, Platforms &amp; Initiatives</h2>
    <p>Explore research projects, software platforms, standards, and initiatives spanning trustworthy AI, biomedical informatics, and healthcare data science.</p>
  </div>

  <div class="portfolio-grid">
    {% for item in site.data.lab_portfolio.documented %}
      <article class="portfolio-card{% if item.featured %} portfolio-card--featured{% endif %}">
        <a href="{{ item.link }}" target="_blank" rel="noopener noreferrer">
          {% if item.featured %}<span class="portfolio-card__badge">Prominent highlight</span>{% endif %}
          <span class="portfolio-card__icon"><i class="{{ item.icon }}" aria-hidden="true"></i></span>
          <p class="portfolio-card__status">{{ item.status }}</p>
          <h3>{{ item.title }}</h3>
          <p>{{ item.description }}</p>
          {% include github-stats.html link=item.link %}
          <span class="portfolio-card__link">View source <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></span>
        </a>
      </article>
    {% endfor %}

    {% for item in site.data.lab_portfolio.additional_repositories %}
      <article class="portfolio-card portfolio-card--minimal">
        <a href="{{ item.link }}" target="_blank" rel="noopener noreferrer">
          <span class="portfolio-card__icon"><i class="{{ item.icon }}" aria-hidden="true"></i></span>
          <p class="portfolio-card__status">{{ item.status }}</p>
          <h3>{{ item.title }}</h3>
          <span class="portfolio-card__link">Open repository <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></span>
        </a>
      </article>
    {% endfor %}

    {% for item in site.data.lab_portfolio.additional_initiatives %}
      <article class="portfolio-card portfolio-card--initiative">
        <div class="portfolio-card__static">
          <span class="portfolio-card__icon"><i class="{{ item.icon }}" aria-hidden="true"></i></span>
          <p class="portfolio-card__status">{{ item.status }}</p>
          <h3>{{ item.title }}</h3>
        </div>
      </article>
    {% endfor %}
  </div>
</div>

{% include section.html %}

<div class="interior-section benchmark-panel">
  <div class="interior-heading">
    <p class="interior-heading__eyebrow">A defining research pillar</p>
    <h2>Data and Benchmarking</h2>
    <p>The lab’s benchmark-oriented portfolio includes three completed works spanning clinical AI readiness, synthetic clinical data trustworthiness, and RDF data infrastructure.</p>
  </div>

  <div class="benchmark-grid">
    {% for benchmark in site.data.homepage.benchmarking %}
      {% assign benchmark_url = benchmark.link %}
      {% unless benchmark.external %}{% assign benchmark_url = benchmark.link | relative_url %}{% endunless %}
      <a class="benchmark-card" href="{{ benchmark_url }}"{% if benchmark.external %} target="_blank" rel="noopener noreferrer"{% endif %}>
        <span class="benchmark-card__status">{{ benchmark.status }}</span>
        <i class="fa-solid fa-gauge-high" aria-hidden="true"></i>
        <strong>{{ benchmark.title }}</strong>
        <small>{{ benchmark.description }}</small>
      </a>
    {% endfor %}
  </div>
</div>

{% include section.html %}

<div class="interior-section">
  <div class="interior-heading interior-heading--split">
    <div>
      <p class="interior-heading__eyebrow">Foundational portfolio</p>
      <h2>Project Archive</h2>
      <p>Browse the lab's existing archive of publications, models, semantic technologies, and biomedical informatics projects.</p>
    </div>
    {% include button.html link="projects" text="Open project archive" style="bare" %}
  </div>

  <div class="archive-grid">
    {% for project in site.data.projects %}
      {% if project.detail %}
        {% assign project_url = project.detail | relative_url %}
        {% assign project_external = false %}
      {% else %}
        {% assign project_url = project.link %}
        {% assign project_external = true %}
      {% endif %}
      <article class="archive-card">
        <p class="archive-card__tag">{% if project.tags and project.tags.size > 0 %}{{ project.tags | first }}{% else %}Research project{% endif %}</p>
        <h3><a href="{{ project_url }}"{% if project_external %} target="_blank" rel="noopener noreferrer"{% endif %}>{{ project.title }}</a></h3>
        <p>{{ project.description | strip_html | truncate: 175 }}</p>
        <a class="archive-card__link" href="{{ project_url }}"{% if project_external %} target="_blank" rel="noopener noreferrer"{% endif %}>View project <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
      </article>
    {% endfor %}
  </div>
</div>
