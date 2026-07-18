---
title: Team
nav:
  order: 4
  tooltip: Meet our team
---

# Team

<div class="team-directory">
  <div class="team-block team-block--pi">
    <div class="team-block__heading">
      <h2>Principal Investigator</h2>
    </div>

    <div class="team-pi">
      {% assign principal_investigators = site.members | where: "group", "pi" | sort: "name" %}
      {% for member in principal_investigators %}
        {% include team-profile.html member=member variant="pi" %}
      {% endfor %}
    </div>
  </div>

  <div class="team-block team-block--current">
    <div class="team-block__heading">
      <h2>Current Members</h2>
    </div>

    <div class="team-grid team-grid--current">
      {% assign current_members = site.members | where: "group", "current" | sort: "name" %}
      {% for member in current_members %}
        {% include team-profile.html member=member variant="current" %}
      {% endfor %}
    </div>
  </div>

  <details class="team-block team-alumni" open>
    <summary class="team-block__heading team-alumni__summary">
      <h2>Previous Members</h2>
      <span class="team-alumni__toggle" aria-hidden="true"></span>
    </summary>

    <div class="team-grid team-grid--previous">
      {% assign previous_members = site.members | where: "group", "previous" | sort: "name" %}
      {% for member in previous_members %}
        {% include team-profile.html member=member variant="previous" %}
      {% endfor %}
    </div>
  </details>
</div>
