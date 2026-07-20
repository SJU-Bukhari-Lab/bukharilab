---
title: News
nav:
  order: 5
  tooltip: Lab news
---

<div class="interior-hero interior-hero--news">
  <p class="interior-hero__eyebrow">From the lab</p>
  <h1>News</h1>
  <p>Publications, presentations, grants, project milestones, and other developments from the Bukhari Lab.</p>
  <div class="interior-hero__actions">
    {% include button.html link="research" text="Explore research" %}
    {% include button.html link="contact" text="Connect with the lab" style="bare" %}
  </div>
</div>

{% include section.html %}

<div class="news-flow">
  <div class="news-flow__toolbar">
    <div class="news-flow__intro">
      <p class="interior-heading__eyebrow">Browse the archive</p>
      <h2>Latest from the Lab</h2>
      <p>Search updates or filter by topic to find publications, grants, presentations, and project milestones.</p>
    </div>
    <div class="filter-panel news-filter-panel">
      {% include search-box.html %}
      {% include tags.html tags=site.tags %}
      {% include search-info.html %}
    </div>
  </div>

  <div class="news-editorial-grid">
    {% for post in site.posts %}
      {% if forloop.first %}{% include post-excerpt.html lookup=post.slug style="lead" %}
      {% else %}{% include post-excerpt.html lookup=post.slug style="card" %}{% endif %}
    {% endfor %}
  </div>
</div>
