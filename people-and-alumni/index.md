---
title: People & Alumni
nav:
  order: 4
  tooltip: Meet our people
---

<div class="interior-hero interior-hero--team">
  <p class="interior-hero__eyebrow">Our people</p>
  <h1>People &amp; Alumni</h1>
  <p>Researchers, students, and collaborators advancing auditable, explainable, and trustworthy AI for healthcare and biomedical discovery.</p>
  <div class="interior-hero__actions">
    {% include button.html link="contact" text="Join the lab" %}
    {% include button.html link="research" text="Explore research" style="bare" %}
  </div>
</div>

{% include section.html %}

<div class="team-context">
  <span><i class="fa-solid fa-shield-halved" aria-hidden="true"></i> Trustworthy AI</span>
  <span><i class="fa-solid fa-diagram-project" aria-hidden="true"></i> Knowledge Engineering</span>
  <span><i class="fa-solid fa-heart-pulse" aria-hidden="true"></i> Healthcare Informatics</span>
</div>

<div class="team-directory">
  <div class="team-block team-block--pi">
    <div class="team-block__heading">
      <p class="interior-heading__eyebrow">Lab leadership</p>
      <h2>Principal Investigator</h2>
    </div>
    <div class="team-pi">
      {% assign principal_investigators = site.members | where: "group", "pi" | sort: "name" %}
      {% for member in principal_investigators %}{% include team-profile.html member=member variant="pi" %}{% endfor %}
    </div>
  </div>

  <hr class="people-divider">

  <div class="team-block team-block--members">
    <div class="team-block__heading">
      <p class="interior-heading__eyebrow">Students &amp; researchers</p>
      <h2>Lab Members</h2>
    </div>
    <div class="people-panel">
      {% for group in site.data.people %}
        {% assign group_size = group.people | size %}
        <div class="people-row">
          <div class="people-row__label">
            <h3 id="people-group-{{ forloop.index }}">{{ group.category }}</h3>
            <p>{{ group_size }} {% if group_size == 1 %}member{% else %}members{% endif %}</p>
          </div>
          <ul class="people-list" aria-labelledby="people-group-{{ forloop.index }}">
            {% for person in group.people %}
              {% assign name_parts = person.name | split: " " %}
              <li class="people-person">
                <span class="people-person__initials" aria-hidden="true">{{ name_parts.first | slice: 0 }}{{ name_parts.last | slice: 0 }}</span>
                <span class="people-person__text">
                  <span class="people-person__name">{{ person.name }}</span>
                  {% if person.affiliation %}<span class="people-person__affiliation">{{ person.affiliation }}</span>{% endif %}
                </span>
              </li>
            {% endfor %}
          </ul>
        </div>
      {% endfor %}
    </div>
  </div>
</div>
