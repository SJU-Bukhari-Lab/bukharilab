---
title: News
nav:
  order: 5
  tooltip: Lab news and updates
---

# News

<div class="filter-panel news-filter-panel">
  {% include search-box.html %}
  {% include tags.html tags=site.tags %}
  {% include search-info.html %}
</div>

{% include section.html %}

<div class="news-editorial-grid">
  {% for post in site.posts %}
    {% if forloop.first %}
      {% include post-excerpt.html lookup=post.slug style="lead" %}
    {% else %}
      {% include post-excerpt.html lookup=post.slug style="card" %}
    {% endif %}
  {% endfor %}
</div>
