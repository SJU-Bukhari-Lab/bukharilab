---
title: Projects
nav:
  order: 3
  tooltip: Research projects and tools
---

# Projects

<div class="filter-panel project-filter-panel">
  {% include search-box.html %}
  {% include tags.html tags="semantic web, data integration, clinical prediction, medical imaging" %}
  {% include search-info.html %}
</div>

{% include section.html %}

<h2>Featured</h2>

<div class="projects-featured-grid">
  {% assign featured_projects = site.data.projects | where: "group", "featured" %}
  {% for project in featured_projects %}
    <article class="card project-card project-card--featured" data-search="{{ project.title | xml_escape }} {{ project.description | xml_escape }}">
      <a class="project-card__image" href="{{ project.detail | relative_url }}" aria-label="View details for {{ project.title | xml_escape }}">
        <img
          src="{{ project.image | relative_url | uri_escape }}"
          alt=""
          loading="lazy"
          decoding="async"
          {% include fallback.html %}
        >
      </a>

      <div class="project-card__content">
        {% if project.subtitle %}<p class="project-card__eyebrow">{{ project.subtitle }}</p>{% endif %}
        <h3 class="project-card__title"><a href="{{ project.detail | relative_url }}">{{ project.title }}</a></h3>
        {% if project.description %}<div class="project-card__description">{{ project.description | markdownify }}</div>{% endif %}
        <div class="project-card__footer">
          {% include tags.html tags=project.tags repo=project.repo %}
          <a class="project-card__detail-link" href="{{ project.detail | relative_url }}">View project →</a>
        </div>
      </div>
    </article>
  {% endfor %}
</div>

{% include section.html %}

<h2>More</h2>

<div class="projects-directory-grid">
  {% for project in site.data.projects %}
    {% if project.group != "featured" %}
      <article class="card project-card project-card--directory" data-search="{{ project.title | xml_escape }} {{ project.description | xml_escape }}">
        <a class="project-card__thumb" href="{{ project.detail | relative_url }}" aria-label="View details for {{ project.title | xml_escape }}">
          <img
            src="{{ project.image | relative_url | uri_escape }}"
            alt=""
            loading="lazy"
            decoding="async"
            {% include fallback.html %}
          >
        </a>

        <div class="project-card__content">
          <h3 class="project-card__title"><a href="{{ project.detail | relative_url }}">{{ project.title }}</a></h3>
          {% if project.description %}<div class="project-card__description">{{ project.description | markdownify }}</div>{% endif %}
          <div class="project-card__footer">
            {% include tags.html tags=project.tags repo=project.repo %}
            <a class="project-card__detail-link" href="{{ project.detail | relative_url }}">View project →</a>
          </div>
        </div>
      </article>
    {% endif %}
  {% endfor %}
</div>
