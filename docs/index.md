---
title: lojban machine translation
---
## The project

The project: [olpa/lojban-mt](https://github.com/olpa/lojban-mt)

Subscribe to the news: [RSS](/feed.xml)

## Posts

<ul>
  {% for post in site.posts %}
    <li>
      {{ post.date | date: "%-d %B %Y" }}, <a href="{{ post.url | prepend:site.baseurl }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>

