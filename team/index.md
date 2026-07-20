---
title: Team
nav:
  order: 4
  tooltip: Meet our team
---

<div class="interior-hero interior-hero--team">
  <p class="interior-hero__eyebrow">Our people</p>
  <h1>Team</h1>
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

  <div class="team-block team-block--current">
    <div class="team-block__heading">
      <p class="interior-heading__eyebrow">Students &amp; researchers</p>
      <h2>Current Members</h2>
    </div>
    <div class="team-grid team-grid--current">
      {% assign current_members = site.members | where: "group", "current" | sort: "name" %}
      {% for member in current_members %}{% include team-profile.html member=member variant="current" %}{% endfor %}
    </div>
  </div>

  <details class="team-block team-alumni">
    <summary class="team-block__heading team-alumni__summary">
      <div>
        <p class="interior-heading__eyebrow">Lab history</p>
        <h2>Previous Members</h2>
      </div>
      <span class="team-alumni__toggle" aria-hidden="true"></span>
    </summary>
    <div class="team-grid team-grid--previous">
      {% assign previous_members = site.members | where: "group", "previous" | sort: "name" %}
      {% for member in previous_members %}{% include team-profile.html member=member variant="previous" %}{% endfor %}
    </div>
  </details>
</div>
