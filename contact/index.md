---
title: Contact
nav:
  order: 6
  tooltip: St. John's University address
---

# Contact

<div class="contact-campus">
  <img
    src="{{ 'images/contact/st-johns-campus.jpg' | relative_url }}"
    alt="St. John's University campus"
    loading="lazy"
    onerror="this.src='{{ 'images/contact/st-johns-campus-placeholder.svg' | relative_url }}'; this.onerror=null;"
  >
</div>

<div class="contact-layout">
  <article class="contact-card">
    <h2>Address</h2>

    <p><strong></strong></p>
    <p>St. John's University<br>8000 Utopia Parkway<br>Queens, NY 11439</p>
    <p></p>
    <p>GPS: 40.721378, -73.790375</p>

    <div class="contact-actions">
      {% include button.html type="address" text="St. John's University, 8000 Utopia Parkway, Queens, NY 11439" tooltip="St. John's University on Google Maps" link="https://www.google.com/maps/search/?api=1&query=40.721378,-73.790375" %}
      {% include button.html type="phone" text="718-990-2000" link="+1-718-990-2000" %}
    </div>
  </article>

  <div class="contact-map">
    <iframe
      title="St. John's University location"
      src="https://www.google.com/maps?q=40.721378,-73.790375&z=16&output=embed"
      loading="lazy"
      referrerpolicy="no-referrer-when-downgrade"
      allowfullscreen
    ></iframe>
  </div>
</div>
