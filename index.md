---
title: Home
nav:
  order: 0
  tooltip: Welcome to the Bukhari Lab
---

<div class="home-hero home-hero--revised" style="--hero-image: url('{{ 'images/brand/nyc-skyline-licensed.webp' | relative_url }}')">
  <div class="home-hero__inner">
    <div class="home-hero__content">
      <p class="home-hero__eyebrow">Bukhari Lab · Biomedical Data Science &amp; Healthcare AI</p>
      <h1>Advancing Biomedical Data Science through Transparent, Explainable, and Trustworthy AI</h1>
      <p class="home-hero__formula"><strong>HUMAN + AI &gt; HUMAN</strong></p>

      <div class="home-hero__actions">
        {% include button.html link="research" text="Explore our research" %}
        {% include button.html link="team" text="Meet the team" style="bare" %}
        {% include button.html link="https://www.linkedin.com/company/bukharilab" text="Join us on LinkedIn" style="bare" %}
      </div>

      <a class="home-hero__funding" href="https://www.nsf.gov/awardsearch/showAward?AWD_ID=2101350">
        <i class="fa-solid fa-award" aria-hidden="true"></i>
        Our work is proudly supported by the National Science Foundation (NSF).
      </a>
    </div>
  </div>

  <p class="home-hero__credit">
    Skyline: <a href="https://commons.wikimedia.org/wiki/File:Lower_Manhattan_from_Jersey_City_November_2014_panorama_1.jpg">King of Hearts / Wikimedia Commons</a>,
    <a href="https://creativecommons.org/licenses/by-sa/3.0/">CC BY-SA 3.0</a>. Cropped and resized.
  </p>
</div>

{% include section.html %}

<div class="section-intro section-intro--split homepage-section-heading">
  <div>
    <p class="homepage-section-heading__eyebrow">Current research</p>
    <h2>Active Projects</h2>
    <p>Recent initiatives spanning trustworthy clinical AI, interoperability, predictive analytics, and biomedical discovery.</p>
  </div>
  {% include button.html link="projects" text="View all projects" style="bare" %}
</div>

<div class="homepage-project-grid">
  {% for project in site.data.homepage.active_projects %}
    <article class="homepage-project-card">
      <a href="{{ project.link }}" target="_blank" rel="noopener noreferrer" aria-label="Read more about {{ project.title | escape }}">
        <span class="homepage-project-card__icon" aria-hidden="true"><i class="{{ project.icon }}"></i></span>
        <span class="homepage-project-card__label">{{ project.label }}</span>
        <h3>{{ project.title }}</h3>
        <p>{{ project.description }}</p>
        <span class="homepage-card-link">Explore project <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></span>
      </a>
    </article>
  {% endfor %}
</div>

{% include section.html %}

<div class="section-intro section-intro--split homepage-section-heading">
  <div>
    <p class="homepage-section-heading__eyebrow">Recent scholarship</p>
    <h2>Featured Papers</h2>
    <p>Selected recent publications and preprints from the lab's current research program.</p>
  </div>
  {% include button.html link="https://scholar.google.com/citations?hl=en&user=JhWJ5PEAAAAJ" text="View all papers" style="bare" %}
</div>

<div class="homepage-paper-grid">
  {% for paper in site.data.homepage.featured_papers %}
    <article class="homepage-paper-card">
      <span class="homepage-paper-card__icon" aria-hidden="true"><i class="fa-regular fa-file-lines"></i></span>
      <div>
        <p class="homepage-paper-card__venue">{{ paper.venue }}</p>
        <h3><a href="{{ paper.link }}" target="_blank" rel="noopener noreferrer">{{ paper.title }}</a></h3>
        <p>{{ paper.description }}</p>
        <a class="homepage-card-link" href="{{ paper.link }}" target="_blank" rel="noopener noreferrer">Read paper <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
      </div>
    </article>
  {% endfor %}
</div>

{% include section.html %}

<div class="section-intro section-intro--split homepage-section-heading">
  <div>
    <p class="homepage-section-heading__eyebrow">Open research infrastructure</p>
    <h2>Software &amp; Resources</h2>
    <p>Public tools and repositories supporting reproducible biomedical informatics research.</p>
  </div>
  {% include button.html link="https://github.com/bukharilab" text="Explore all software" style="bare" %}
</div>

<div class="homepage-resource-grid">
  {% for resource in site.data.homepage.software_resources %}
    <article class="homepage-resource-card">
      <a href="{{ resource.link }}" target="_blank" rel="noopener noreferrer">
        <span class="homepage-resource-card__icon" aria-hidden="true"><i class="{{ resource.icon }}"></i></span>
        <div>
          <p class="homepage-resource-card__type">{{ resource.type }}</p>
          <h3>{{ resource.title }}</h3>
          <p>{{ resource.description }}</p>
          <span class="homepage-card-link">View on GitHub <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></span>
        </div>
      </a>
    </article>
  {% endfor %}
</div>

{% include section.html %}

<div class="section-intro section-intro--split">
  <h2>News &amp; Updates</h2>
  {% include button.html link="blog" text="Read lab news" style="bare" %}
</div>

<div class="news-grid news-grid--home">
  {% assign latest_posts = site.posts | slice: 0, 3 %}
  {% for post in latest_posts %}
    {% include post-excerpt.html lookup=post.slug %}
  {% endfor %}
</div>
