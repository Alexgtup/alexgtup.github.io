Google Search Console sitemap fix

1) Deploy this patch over the repository.
2) Wait for GitHub Pages deployment success.
3) Open https://alexgtup.github.io/sitemap.xml directly in the browser. It must show XML, not a 404 page.
4) In Search Console delete the old sitemap.txt submission and the old sitemap.xml row if desired.
5) Submit only: sitemap.xml

The XML was intentionally simplified to the core sitemap protocol: loc + lastmod only.
