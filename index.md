---
title: Home
nav:
  order: 0
  tooltip: Home
---

<div class="home-hero home-hero--revised" style="--hero-image: url('{{ 'images/brand/nyc-skyline-licensed.webp' | relative_url }}')">
  <div class="home-hero__inner">
    <div class="home-hero__content">
      <p class="home-hero__eyebrow">Auditability · Explainability · Trustworthiness</p>
      <h1>Advancing Biomedical Data Science through Transparent, Explainable, and Trustworthy AI</h1>
      <p class="home-hero__formula home-hero__formula--trust" aria-label="Better Health is a function of Trustworthy AI"><strong>BetterHealth = f(TrustWorthyAI)</strong></p>

      <div class="home-hero__actions">
        {% include button.html link="research" text="Explore our research" %}
        {% include button.html link="team" text="Meet the team" style="bare" %}
        {% include button.html link="contact" text="Join us" style="bare" %}
      </div>

      <div class="home-hero__funding-row" aria-label="Research funding and fellowship acknowledgments">
        <span class="home-hero__funding-label">Funding &amp; fellowship support</span>
        <a class="home-hero__funder" href="https://www.stjohns.edu/news-media/news/2024-09-17/st-johns-professor-awarded-grant-study-use-ai-medical-coding" target="_blank" rel="noopener noreferrer">
          <span class="home-hero__funder-logo"><img src="{{ 'images/funders/nsf-logo.png' | relative_url }}" alt="National Science Foundation logo"></span>
          <span>National Science Foundation</span>
        </a>
        <a class="home-hero__funder" href="https://www.stjohns.edu/academics/faculty/syed-ahmad-chan-bukhari" target="_blank" rel="noopener noreferrer">
          <span class="home-hero__funder-logo home-hero__funder-logo--nih"><img src="{{ 'images/funders/nih-logo.png' | relative_url }}" alt="National Institutes of Health logo"></span>
          <span>NIH–NCBI Fellowship</span>
        </a>
      </div>
    </div>
  </div>

  <p class="home-hero__credit">
    Skyline: <a href="https://commons.wikimedia.org/wiki/File:Lower_Manhattan_from_Jersey_City_November_2014_panorama_1.jpg">King of Hearts / Wikimedia Commons</a>,
    <a href="https://creativecommons.org/licenses/by-sa/3.0/">CC BY-SA 3.0</a>. Cropped and resized.
  </p>
</div>

{% include section.html %}

<section class="homepage-content-block" aria-labelledby="active-projects-heading">
  <div class="section-intro section-intro--split trust-section-heading">
    <div>
      <p class="trust-section-heading__eyebrow">Current research</p>
      <h2 id="active-projects-heading">Active Projects</h2>
      <p>Selected initiatives that demonstrate the lab's focus on auditable, explainable, and trustworthy biomedical AI.</p>
    </div>
    {% include button.html link="research" text="Explore full portfolio" style="bare" %}
  </div>

  <div class="trust-project-grid">
    {% for project in site.data.homepage.active_projects %}
      {% assign project_url = project.link %}
      {% unless project.external %}{% assign project_url = project.link | relative_url %}{% endunless %}
      <article class="trust-project-card{% if project.featured %} trust-project-card--featured{% endif %}">
        <a href="{{ project_url }}"{% if project.external %} target="_blank" rel="noopener noreferrer"{% endif %}>
          {% if project.featured %}<span class="trust-card-badge">Featured</span>{% endif %}
          <span class="trust-project-card__icon" aria-hidden="true"><i class="{{ project.icon }}"></i></span>
          <span class="trust-project-card__label">{{ project.label }}</span>
          <h3>{{ project.title }}</h3>
          <p>{{ project.description }}</p>
          <span class="trust-card-link">Explore <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></span>
        </a>
      </article>
    {% endfor %}
  </div>
</section>

{% include section.html %}

<section class="homepage-content-block trust-benchmark" aria-labelledby="benchmark-heading">
  <div class="trust-benchmark__intro">
    <p class="trust-section-heading__eyebrow">A defining research pillar</p>
    <h2 id="benchmark-heading">Benchmarking &amp; Evaluation</h2>
    <p>We develop rigorous evaluation frameworks that make biomedical AI and data infrastructure more measurable, comparable, auditable, and trustworthy.</p>
  </div>

  <div class="trust-benchmark__grid">
    {% for benchmark in site.data.homepage.benchmarking %}
      {% assign benchmark_url = benchmark.link %}
      {% unless benchmark.external %}{% assign benchmark_url = benchmark.link | relative_url %}{% endunless %}
      <a class="trust-benchmark-card" href="{{ benchmark_url }}"{% if benchmark.external %} target="_blank" rel="noopener noreferrer"{% endif %}>
        <span class="trust-benchmark-card__status">{{ benchmark.status }}</span>
        <span class="trust-benchmark-card__icon" aria-hidden="true"><i class="fa-solid fa-gauge-high"></i></span>
        <span>
          <strong>{{ benchmark.title }}</strong>
          <small>{{ benchmark.description }}</small>
        </span>
        <i class="fa-solid fa-arrow-right" aria-hidden="true"></i>
      </a>
    {% endfor %}
  </div>
</section>

{% include section.html %}

<section class="homepage-content-block" aria-labelledby="featured-papers-heading">
  <div class="section-intro section-intro--split trust-section-heading">
    <div>
      <p class="trust-section-heading__eyebrow">Selected scholarship</p>
      <h2 id="featured-papers-heading">Featured Papers</h2>
      <p>Recent work spanning trustworthy clinical AI, interoperability, biomedical knowledge engineering, and rigorous evaluation.</p>
    </div>
    {% include button.html link="papers" text="View all papers" style="bare" %}
  </div>

  <div class="trust-paper-grid">
    {% for paper in site.data.homepage.featured_papers %}
      <article class="trust-paper-card">
        <span class="trust-paper-card__icon" aria-hidden="true"><i class="fa-regular fa-file-lines"></i></span>
        <div>
          <p class="trust-paper-card__venue">{{ paper.venue }}</p>
          <h3><a href="{{ paper.link }}" target="_blank" rel="noopener noreferrer">{{ paper.title }}</a></h3>
          <p>{{ paper.description }}</p>
          <a class="trust-card-link" href="{{ paper.link }}" target="_blank" rel="noopener noreferrer">Read paper <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
        </div>
      </article>
    {% endfor %}
  </div>
</section>

{% include section.html %}

<section class="homepage-content-block" aria-labelledby="software-heading">
  <div class="section-intro section-intro--split trust-section-heading">
    <div>
      <p class="trust-section-heading__eyebrow">Open research infrastructure</p>
      <h2 id="software-heading">Software &amp; Resources</h2>
      <p>A curated selection from the lab's broader portfolio of research software, standards, and knowledge-engineering tools.</p>
    </div>
    {% include button.html link="software" text="Explore all software" style="bare" %}
  </div>

  <div class="trust-resource-grid">
    {% for resource in site.data.homepage.software_resources %}
      <article class="trust-resource-card{% if resource.featured %} trust-resource-card--featured{% endif %}">
        <a href="{{ resource.link }}" target="_blank" rel="noopener noreferrer">
          {% if resource.featured %}<span class="trust-card-badge">Highlighted</span>{% endif %}
          <span class="trust-resource-card__icon" aria-hidden="true"><i class="{{ resource.icon }}"></i></span>
          <div>
            <p class="trust-resource-card__type">{{ resource.type }}</p>
            <h3>{{ resource.title }}</h3>
            <p>{{ resource.description }}</p>
            <span class="trust-card-link">View resource <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></span>
          </div>
        </a>
      </article>
    {% endfor %}
  </div>
</section>

{% include section.html %}

<section class="homepage-content-block homepage-content-block--news" aria-labelledby="news-heading">
  <div class="section-intro section-intro--split trust-section-heading">
    <div>
      <p class="trust-section-heading__eyebrow">From the lab</p>
      <h2 id="news-heading">News</h2>
    </div>
    {% include button.html link="blog" text="Read latest updates" style="bare" %}
  </div>

  <div class="news-grid news-grid--home">
    {% assign latest_posts = site.posts | slice: 0, 3 %}
    {% for post in latest_posts %}
      {% include post-excerpt.html lookup=post.slug %}
    {% endfor %}
  </div>
</section>
