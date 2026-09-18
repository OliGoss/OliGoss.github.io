```{=html}
<div class="publication-list">
<% for (const item of items) {
  if (!item['paper-record']) continue;
  const mode = templateParams.mode;
  if (mode === 'selected' && !item.featured) continue;
  if (mode === 'sinfonia' && !item.sinfonia) continue;
  if (mode !== 'selected' && mode !== 'sinfonia' && item.status !== mode) continue;
%>
<article class="publication-row">
  <div class="publication-year"><%- item.year %></div>
  <div class="publication-content">
    <h3><a href="<%- item.path %>"><%- item.title %></a></h3>
    <p class="publication-authors"><%- item.byline %></p>
    <p class="publication-venue"><%- item.publication %></p>
    <div class="publication-links">
      <% if (item.pdf) { %><a href="<%- item.pdf %>"><%- item['pdf-label'] || 'Paper PDF' %></a><% } %>
      <% if (item['arxiv-url']) { %><a href="<%- item['arxiv-url'] %>">arXiv</a><% } %>
      <% if (item['publisher-url']) { %><a href="<%- item['publisher-url'] %>">Published version</a><% } %>
      <% if (item['record-url']) { %><a href="<%- item['record-url'] %>">Archive record</a><% } %>
      <a href="<%- item.path %>"><%- item.abstract ? 'Abstract & details' : 'Details' %></a>
    </div>
  </div>
</article>
<% } %>
</div>
```
