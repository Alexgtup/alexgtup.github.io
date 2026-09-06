# Stage 18 deploy hotfix

Fixes false canonical validation failures in GitHub Actions.

The previous validator required the literal attribute order `<link rel="canonical" ...>`.
HTML formatters may legitimately serialize the same link as `<link href="..." rel="canonical"/>`.
The new check scans link tags for `rel="canonical"` regardless of attribute order.

Local clean-build validation after the fix:
- 58 sitemap URLs found
- 62 HTML files validated
- canonical validation passes
- image dimension/budget checks pass
- root and English RSS feeds parse
