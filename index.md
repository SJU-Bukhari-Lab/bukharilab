---
title: Home
nav:
  order: 0
  tooltip: Welcome to the Bukhari Lab
---

<div class="home-hero" style="--hero-image: url('{{ 'images/brand/nyc-banner.jpg' | relative_url }}')">
  <div class="home-hero__inner">
    <div class="home-hero__content">
      <p class="home-hero__eyebrow">Biomedical Data Science &amp; Healthcare AI</p>
      <h1>Bukhari Lab</h1>
      <p class="home-hero__mission"><strong>Advancing Biomedical Data Science through Transparent, Explainable, and Trustworthy AI</strong></p>
      <p class="home-hero__formula"><strong>HUMAN + AI &gt; HUMAN</strong></p>
      <div class="home-hero__actions">
        {% include button.html link="research" text="Explore our research" %}
        {% include button.html link="team" text="Meet the team" style="bare" %}
      </div>
      <a class="home-hero__funding" href="https://www.nsf.gov/awardsearch/showAward?AWD_ID=2101350">Our work is proudly supported by the National Science Foundation (NSF).</a>
    </div>
  </div>
</div>

{% include section.html %}

<div class="section-intro">
  <h2>Expertise</h2>
</div>

{% capture text %}
Balancing the speed and accuracy in structured biomedical content authoring

{% include button.html link="https://www.nsf.gov/awardsearch/showAward?AWD_ID=2101350" text="Our Socio-technical Approach for Biomedical Content Authoring and Structured Web Publishing" style="bare" %}
{% endcapture %}

{% include feature.html image="images/projects/semantic-biomedical-ai.png" link="https://www.nsf.gov/awardsearch/showAward?AWD_ID=2101350" title="Semantically" text=text %}

{% capture text %}
Knowledge Engineering & Prediction Solutions

{% include button.html link="projects" text="Check our Completed Research Projects" style="bare" %}
{% endcapture %}

{% include feature.html image="images/projects/medical-knowledge-engineering.png" link="projects" title="Medical" flip=true text=text %}

{% capture text %}
Research, Analytics & Prediction

{% include button.html link="research" text="Our Expertise" style="bare" %}
{% endcapture %}

{% include feature.html image="images/projects/clinical-decision-support.png" link="research" title="Clinical Decision Support System" text=text %}

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
