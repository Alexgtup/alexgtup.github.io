# Stage 99 - persistent light/dark theme

Date: 2026-09-10

## Goal

Add an optional light theme without breaking the existing dark visual identity, and make the preference persist across the entire portfolio journey.

## What changed

- Added `/assets/theme-system.js` as the shared theme controller.
- Added `/assets/theme-system.css` as the global light-theme layer.
- Dark remains the default for first-time visitors.
- The selected theme is persisted in `localStorage` and restored on later pages/visits.
- The theme preference synchronizes between open tabs.
- Browser `color-scheme` and `theme-color` metadata update together with the selected mode.
- Desktop receives a compact theme switch in the shared header.
- Mobile receives a labelled theme switch inside the shared navigation menu.
- Russian and English labels are selected from the document language.
- Theme changes are exposed to the existing consent-based analytics as `theme_toggle` without sending user-entered content.

## Light theme coverage

The light layer defines both the Stage 98 design-system variables and older legacy variable names so that page families built at different stages follow the same mode.

Explicit light-theme treatment covers:

- page and homepage atmospheric backgrounds;
- sticky shared header;
- desktop and mobile navigation;
- project/case/service cards;
- filters and filter buttons;
- forms, inputs, textareas and selects;
- primary and secondary CTAs;
- editorial separators and disclosure panels;
- footer and analytics-consent surfaces;
- empty media wells while leaving real screenshots visually intact.

## Build safety

`scripts/stage24_layout_system.py` now injects the theme CSS and JS into every full HTML document and validates `theme-system.js` with `node --check` during the normal deploy pipeline.

GitHub Pages workflow run `34450555674` completed successfully, including build validation, deployment and search-engine notification.

## Next UX work

Use real interaction data to compare dark/light preference and CTA placement rather than choosing one theme globally. Continue improving the path from project/service browsing to a contextual Telegram or email enquiry, especially on mobile.
