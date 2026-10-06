---
layout: page
permalink: /blog/
title: blog
description: Project pages for our recent work.
nav: true
nav_order: 3
---

<style>
  .proj-list { list-style: none; padding: 0; margin: 0; }
  .proj-item {
    display: grid;
    grid-template-columns: 220px minmax(0, 1fr);
    gap: 1.4rem;
    align-items: center;
    padding: 1.2rem 0;
    border-bottom: 1px solid var(--global-divider-color);
  }
  .proj-item:last-child { border-bottom: none; }
  .proj-thumb {
    display: block;
    background: #fff;
    border: 1px solid var(--global-divider-color);
    border-radius: 6px;
    padding: 6px;
  }
  .proj-thumb img { display: block; width: 100%; height: 130px; object-fit: contain; }
  .proj-item h3 { font-size: 1.1rem; margin: 0 0 0.35rem 0; line-height: 1.4; }
  .proj-item p { font-size: 0.92rem; margin: 0 0 0.35rem 0; color: var(--global-text-color); }
  .proj-item .meta { font-size: 0.8rem; color: var(--global-text-color-light); }
  @media (max-width: 640px) {
    .proj-item { grid-template-columns: 1fr; gap: 0.7rem; }
  }
</style>

<ul class="proj-list">
{% for post in site.posts %}
  {% assign link = post.redirect | default: post.url %}
  <li class="proj-item">
    <a class="proj-thumb" href="{{ link | relative_url }}">
      {% if post.thumbnail %}<img src="{{ post.thumbnail | relative_url }}" alt="{{ post.title }}" loading="lazy">{% endif %}
    </a>
    <div>
      <h3><a href="{{ link | relative_url }}">{{ post.title }}</a></h3>
      <p>{{ post.description }}</p>
      <div class="meta">{{ post.date | date: '%B %Y' }}</div>
    </div>
  </li>
{% endfor %}
</ul>
