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
    <h3><a href="<%- item.pdf || item.path %>"<% if (item.pdf) { %> title="Open paper PDF"<% } %>><%- item.title %></a></h3>
    <p class="publication-authors"><%- item.byline %></p>
    <p class="publication-venue"><%- item.publication %></p>
    <div class="publication-links">
      <a href="<%- item.path %>"><%- item.abstract ? 'Abstract & details' : 'Details' %></a>
    </div>
  </div>
</article>
<% } %>
</div>
```
