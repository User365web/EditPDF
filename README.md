# EditPDF — Free Online PDF Tools

A fast, static website (no backend, no database). All PDF processing happens in the visitor's browser.

**Tools:** Merge PDF · Split PDF · Compress PDF · Rotate PDF · Image to PDF · PDF Page Counter · PDF Info
**Guides:** how to merge PDFs · how to compress a PDF · how to convert images to PDF
**Pages:** Home, About, Contact, Privacy Policy, Terms of Use, custom 404

---

## 1. Run it on your computer

1. Install Python 3 from https://www.python.org/downloads/ (tick **Add Python to PATH**).
2. Double-click **start.bat** → your browser opens http://localhost:8000
   (or run `python -m http.server 8000` in this folder).

> You can also double-click index.html to see the styled home page, but page links and tools work best through start.bat (a local web server).

## 2. Before you publish (2 minutes) — set your domain

1. Open `_build/config.json` and set:
   - `"domain"` → your real address, e.g. `"https://www.editpdf.com"` (no trailing slash; use exactly the version — www or non-www — you will open in the browser)
   - `"contact_email"` → the email shown on the Contact page (currently `DocufreePDF223@gmail.com`, taken from your old site — change it if you want)
   - `"google_site_verification"` → the code from Google Search Console (see step 4), or leave empty if you verify another way
   - `"adsense_publisher_id"` → e.g. `"pub-1234567890123456"` once AdSense gives it to you (leave empty until then)
   - `"last_modified"` → update this date only when you really change content
2. Double-click **build.bat** (or run `python _build/build.py`). This regenerates every page, `sitemap.xml`, `robots.txt`, `ads.txt` and the manifest with your domain.
3. Upload the whole folder contents to your host (you can skip `README.md`, `start.bat`, `build.bat` and the `_build` folder).

Any time you edit text in `_build/content.py` or `_build/build.py`, run build.bat again.

## 3. Hosting

Works on any static host: Cloudflare Pages, Netlify, GitHub Pages, Vercel, InfinityFree / cPanel (Apache).
- Cloudflare Pages / Netlify read `_headers` automatically. Apache hosts read `.htaccess`.
- Use HTTPS (free on all of the above). Pick **one** address (www or non-www) and redirect the other to it.
- Pages use clean folder URLs such as `/merge-pdf/`, and all work on every host without extra setup.

## 4. Google Search Console — step by step

1. Go to https://search.google.com/search-console → **Add property**.
   - Choose **URL prefix** and enter exactly the same address as `"domain"` in config.json (e.g. `https://www.editpdf.com/`). *(Or choose **Domain** and verify by DNS; then you don't need a meta tag.)*
2. Verify ownership — easiest options:
   - **HTML tag**: copy the code from `content="..."` into `google_site_verification` in config.json, run build.bat, upload, then click Verify.
   - **HTML file**: download the file Google gives you and upload it to the site root.
3. **Sitemaps** (left menu) → type `sitemap.xml` → **Submit**. Status should become **Success**. (On a brand-new site it can say "Couldn't fetch" for a few hours; wait and resubmit — also confirm https://YOUR-DOMAIN/sitemap.xml opens in a browser.)
4. **URL Inspection** (top bar) → paste your home page URL → **Request indexing**. Repeat for your most important pages (merge-pdf, compress-pdf, image-to-pdf…). Google limits these requests, so do a few per day.
5. Check **Pages** and **Core Web Vitals** reports after a few days to see what is indexed.
6. Optional but useful: Bing Webmaster Tools (https://www.bing.com/webmasters) → import from Google Search Console. A ready IndexNow key file is included (`e7d3a91c5b2f4086a1c9d4e8f2b70635.txt`); it speeds up Bing/Yandex discovery.

## 5. What was built in for SEO

- `sitemap.xml` with every page, absolute URLs, `lastmod`
- `robots.txt` allowing all crawlers and pointing to the sitemap
- A **separate landing page for every tool** (each one can rank for its own keyword) with unique title, meta description, how-to steps, FAQ and internal links
- 3 guide articles, internal links in header, footer and "More tools" blocks
- Canonical URLs, Open Graph + Twitter cards, 1200×630 share image
- Structured data (JSON-LD): Organization, WebSite, WebApplication, HowTo, FAQPage, BreadcrumbList, Article
- Mobile-friendly responsive layout, non-blocking fonts, scripts loaded with `defer` and only the libraries each page needs
- Favicon set, web manifest, custom 404 (noindex)

## 6. Google AdSense — what to know

- AdSense reviews sites manually. Approval and traffic can't be guaranteed. Helpful for approval: a real domain, Privacy Policy, About, Contact and Terms pages (all included), and original content.
- When you have your publisher ID: put it in config.json, run build.bat, upload. This adds the AdSense script to every page, creates `ads.txt`, and switches the Privacy Policy to the AdSense wording. Then enable **Auto ads** in your AdSense account.
- If you expect visitors from the EU/UK, set up Google's consent message (AdSense → Privacy & messaging) — it is required there.
- Never click your own ads or ask others to.
- Traffic grows slowly: publish more helpful pages over time (new guides and tools), and get a few genuine links from other sites.

## 7. File map

| Path | Purpose |
|---|---|
| `index.html`, `*/index.html` | Generated pages |
| `css/style.css`, `js/app.js`, `js/contact.js` | Styles and tool logic |
| `_build/config.json` | **Your settings** |
| `_build/content.py` | All page text (tools, FAQs, guides) |
| `_build/build.py` | Page + sitemap generator |
| `_headers`, `.htaccess` | Hosting config (security, cache, redirects) |
| `start.bat`, `build.bat` | Windows helpers |

PDF libraries used (loaded from cdnjs): pdf-lib, PDF.js, jsPDF.
