---
title: Software
nav:
  order: 3
  tooltip: Research software, standards, and tools
---

<div class="interior-hero interior-hero--software">
  <p class="interior-hero__eyebrow">Tools, platforms &amp; repositories</p>
  <h1>Software</h1>
  <p>Explore the lab’s research software, semantic technologies, standards resources, biomedical data infrastructure, and supporting repositories.</p>
  <div class="interior-hero__actions">
    {% include button.html link="https://github.com/bukharilab" text="Bukhari Lab GitHub" icon="fa-brands fa-github" %}
    {% include button.html link="research" text="Related research" style="bare" %}
  </div>
</div>

{% include section.html %}

{% assign featured_software = site.data.software_catalog.featured | where: "id", "semantically" | first %}
<div class="software-spotlight">
  <div class="software-spotlight__icon"><i class="{{ featured_software.icon }}" aria-hidden="true"></i></div>
  <div class="software-spotlight__content">
    <p class="interior-heading__eyebrow">Featured software</p>
    <h2>{{ featured_software.title }}</h2>
    <p>{{ featured_software.description }}</p>
    <div class="software-spotlight__meta"><span>{{ featured_software.category }}</span><span>{{ featured_software.status }}</span></div>
    {% include github-stats.html link=featured_software.link %}
    <a class="software-spotlight__link" href="{{ featured_software.link }}" target="_blank" rel="noopener noreferrer">View repository <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
  </div>
</div>

{% include section.html %}

<div class="interior-section">
  <div class="interior-heading">
    <p class="interior-heading__eyebrow">Primary portfolio</p>
    <h2>Research Software &amp; Platforms</h2>
    <p>Core tools, platforms, standards, and research code associated with the lab’s current public portfolio.</p>
  </div>

  <div class="software-grid">
    {% for item in site.data.software_catalog.featured %}
      {% unless item.id == "semantically" %}
        <article class="software-card">
          <a href="{{ item.link }}" target="_blank" rel="noopener noreferrer">
            <span class="software-card__icon"><i class="{{ item.icon }}" aria-hidden="true"></i></span>
            <p class="software-card__status">{{ item.status }}</p>
            <h3>{{ item.title }}</h3>
            <p class="software-card__category">{{ item.category }}</p>
            <p>{{ item.description }}</p>
            {% include github-stats.html link=item.link %}
            <span class="software-card__link">View resource <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></span>
          </a>
        </article>
      {% endunless %}
    {% endfor %}
  </div>
</div>

{% include section.html %}

<div class="interior-section">
  <div class="interior-heading interior-heading--split">
    <div>
      <p class="interior-heading__eyebrow">Full directory</p>
      <h2>All Repositories</h2>
      <p>Every public repository in the lab’s GitHub account, refreshed automatically with live stars, languages, and activity.</p>
    </div>
    <a class="catalog-count" href="https://github.com/bukharilab?tab=repositories" target="_blank" rel="noopener noreferrer">
      View on GitHub <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i>
    </a>
  </div>

  <div class="software-directory">
    {% assign all_repos = site.data.github_repos | sort: "updated" | reverse %}
    {% for item in all_repos %}
      <a class="software-directory__item" href="{{ item.link }}" target="_blank" rel="noopener noreferrer">
        <span class="software-directory__icon"><i class="fa-brands fa-github" aria-hidden="true"></i></span>
        <span class="software-directory__body">
          <strong>{{ item.name }}</strong>
          <small>{{ item.description | default: "No description provided" }}</small>
          {% include github-stats.html link=item.link %}
        </span>
        <i class="fa-solid fa-arrow-up-right-from-square software-directory__arrow" aria-hidden="true"></i>
      </a>
    {% endfor %}
  </div>
</div>
