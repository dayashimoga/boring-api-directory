# Technical Architecture

## System Overview

QuickUtils API Directory is a **Programmatic SEO** static site generator. It fetches data from public API sources, generates thousands of static HTML pages, and deploys them to a CDN for fast, free hosting.

```
┌─────────────────────────────────────────────────────────────────┐
│                    GitHub Actions (CI/CD)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Weekly Sync   │  │ Daily Social │  │ CI Tests (on push)   │  │
│  │ (data-sync)   │  │ (social-bot) │  │ pytest + build smoke │  │
│  └──────┬───────┘  └──────────────┘  └──────────────────────┘  │
│         │ git push (triggers Netlify rebuild)                    │
└─────────┼───────────────────────────────────────────────────────┘
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Build Pipeline                              │
│                                                                  │
│  fetch_data.py ──▶ database.json ──▶ build_directory.py         │
│                                          │                       │
│                                          ├──▶ 30 item pages      │
│                                          ├──▶ 14 category pages  │
│                                          ├──▶ index.html         │
│                                          └──▶ 404.html           │
│                                                                  │
│  generate_sitemap.py ──▶ sitemap.xml + robots.txt               │
│                                                                  │
│  Static assets (CSS, JS, ads.txt) ──▶ dist/                     │
└─────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────┐     ┌─────────────────┐
│   Netlify CDN   │────▶│   End Users     │
│   (free tier)   │     │   + Googlebot   │
└─────────────────┘     └─────────────────┘
```

---

## Code Tree

```
h:\boring\
│
├── .github/workflows/
│   ├── ci.yml                 # Runs on push: pytest + coverage + smoke build
│   ├── data-sync.yml          # Weekly (Sun 3AM UTC): fetch → commit → push
│   └── social-bot.yml         # Daily (noon UTC): pick random API → post
│
├── data/
│   └── database.json          # JSON array of API entries (auto-updated)
│
├── docs/
│   ├── ARCHITECTURE.md        # This file
│   ├── SETUP_GUIDE.md         # Deployment & configuration guide
│   └── TESTING.md             # Test suite documentation
│
├── scripts/
│   ├── __init__.py            # Makes scripts a Python package
│   ├── utils.py               # Shared constants (paths, slugify, DB I/O)
│   ├── fetch_data.py          # Fetches from primary & fallback APIs
│   ├── build_directory.py     # SSG engine: Jinja2 → minified HTML
│   ├── generate_sitemap.py    # Generates XML sitemap + robots.txt
│   ├── post_social.py         # Mastodon auto-poster
│   ├── run_tests.ps1          # PowerShell test runner (Docker)
│   └── run_tests.sh           # Bash test runner (Docker)
│
├── src/
│   ├── templates/
│   │   ├── base.html          # Master layout (head, header, footer)
│   │   ├── index.html         # Homepage (hero, categories, featured)
│   │   ├── item.html          # Individual API detail page
│   │   ├── category.html      # Category listing with filter
│   │   └── 404.html           # Custom error page
│   ├── css/
│   │   └── styles.css         # Full design system (~1200 lines)
│   ├── js/
│   │   └── main.js            # Theme toggle, mobile nav, smooth scroll
│   ├── ads.txt                # AdSense authorized sellers
│   └── robots.txt             # Bot directives
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Shared fixtures (sample data, tmp dirs)
│   ├── test_utils.py          # slugify, DB I/O, categories, truncate
│   ├── test_fetch_data.py     # normalize, deduplicate, fetch pipeline
│   ├── test_build_directory.py# Jinja env, page gen, static copy, full build
│   ├── test_generate_sitemap.py # pages, priority, XML, robots, pipeline
│   ├── test_post_social.py    # daily seed, format, Mastodon API, main()
│   └── test_templates.py      # Template rendering, meta tags, JSON-LD
│
├── .dockerignore              # Excludes dist, venv, caches from Docker
├── .gitignore                 # Comprehensive ignore rules
├── Dockerfile                 # Python 3.11-slim base image
├── docker-compose.yml         # test / build / serve services
├── netlify.toml               # Netlify build config + security headers
├── requirements.txt           # Python dependencies
└── README.md                  # Project overview and quickstart
```

---

## Module Descriptions

### `scripts/utils.py`
**Purpose**: Shared constants and utility functions used by all other scripts.

| Function | Description |
|---|---|
| `slugify(text)` | Converts text to URL-safe slug (`"Hello World!"` → `"hello-world"`) |
| `load_database(path)` | Reads `data/database.json` into a list of dicts |
| `save_database(items, path)` | Writes sorted JSON with 2-space indent |
| `ensure_dir(path)` | Creates directory and parents if missing |
| `get_categories(items)` | Groups items by category, sorted alphabetically |
| `truncate(text, max_length)` | Truncates text with ellipsis for meta descriptions |

### `scripts/fetch_data.py`
**Purpose**: Fetches API data from public sources with primary + fallback strategy.

- **Primary**: `https://api.publicapis.org/entries` (JSON with `entries` key)
- **Fallback**: `https://raw.githubusercontent.com/public-apis/public-apis/master/json/entries.min.json` (flat JSON array)
- Normalizes fields (`API` → `title`, `Description` → `description`, etc.)
- Deduplicates by title (case-insensitive)
- Saves to `data/database.json`

### `scripts/build_directory.py`
**Purpose**: Static Site Generator using Jinja2 templates.

- Loads database → groups by category
- Generates individual item pages with related items + book recommendations
- Generates category listing pages with filter functionality
- Generates homepage with hero, category cards, and featured APIs
- Generates custom 404 page
- Copies static assets (CSS, JS, ads.txt, robots.txt)
- Minifies HTML output via `htmlmin`

### `scripts/generate_sitemap.py`
**Purpose**: Generates `sitemap.xml` and `robots.txt` for search engine crawling.

- Collects all `.html` files from `dist/`
- Assigns priority (`1.0` index, `0.8` categories, `0.6` items)
- Assigns changefreq (`weekly` index/category, `monthly` items)
- Generates valid XML sitemap with `lastmod`, `priority`, `changefreq`
- Creates `robots.txt` with sitemap reference

### `scripts/post_social.py`
**Purpose**: Automated social media posting to Mastodon.

- Uses date-seeded random selection (same API each day)
- Formats post with title, description, URL, hashtags
- Posts via Mastodon API (`/api/v1/statuses`)
- Keeps posts under 500 character limit

---

## Data Flow

```
1. FETCH PHASE (weekly via GitHub Actions)
   ├── GET primary API → normalize entries → deduplicate
   ├── If primary fails → GET fallback API → normalize → deduplicate
   └── Save to data/database.json → git commit → git push

2. BUILD PHASE (triggered by push to main)
   ├── Load database.json
   ├── Group by category
   ├── For each item:
   │   ├── Find related items (same category, max 6)
   │   ├── Get book recommendations for category
   │   └── Render item.html → minify → save to dist/api/{slug}.html
   ├── For each category:
   │   └── Render category.html → minify → save to dist/category/{slug}.html
   ├── Render index.html → minify → save to dist/index.html
   ├── Render 404.html → minify → save to dist/404.html
   ├── Copy CSS, JS, ads.txt, robots.txt → dist/
   └── Generate sitemap.xml + robots.txt → dist/

3. DEPLOY PHASE (Netlify auto-deploy)
   └── Netlify detects push → runs build → deploys dist/ to CDN

4. SOCIAL PHASE (daily via GitHub Actions)
   └── Pick random API → format post → POST to Mastodon API
```

---

## SEO Architecture

| Feature | Implementation |
|---|---|
| **Title tags** | Unique per page: `{Title} - Free API \| QuickUtils API Directory` |
| **Meta descriptions** | Auto-truncated to 160 chars from API description |
| **Canonical URLs** | Absolute URLs on every page |
| **Open Graph** | `og:title`, `og:description`, `og:url`, `og:type`, `og:site_name` |
| **Twitter Cards** | `summary_large_image` with title + description |
| **JSON-LD** | `WebSite` (index), `SoftwareApplication` (item), `CollectionPage` (category), `BreadcrumbList` (item + category) |
| **Sitemap** | Auto-generated XML with priority + changefreq per page type |
| **robots.txt** | Auto-generated with sitemap reference |
| **Breadcrumbs** | Visual breadcrumbs + JSON-LD structured data |
| **Semantic HTML** | `<nav>`, `<main>`, `<article>`, `<aside>`, `<footer>` |
| **Favicon** | SVG emoji (⚡) via data URI — zero additional requests |
| **CSS Preload** | `<link rel="preload">` for critical stylesheet |
| **Font Preconnect** | Google Fonts with `preconnect` hints |

---

## Monetization Architecture

| Channel | Implementation |
|---|---|
| **Google AdSense** | Auto ad units on item pages (in-content + sidebar) and index (below featured). Conditional loading — only loads when real publisher ID is configured. |
| **Amazon Affiliates** | Curated book recommendations per API category in item page sidebar. Uses affiliate tag from env var. FTC disclosure included. |
| **Gumroad** | "Submit a Tool" CTA in header and CTA section. Paid listing submissions. |
| **Google Analytics** | GA4 tracking on all pages. Conditional — only loads with real measurement ID. |
