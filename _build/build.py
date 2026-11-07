# -*- coding: utf-8 -*-
"""EditPDF site generator.
Edit config.json, then run:   python build.py
Regenerates every page, sitemap.xml, robots.txt, ads.txt, manifest and the IndexNow key file in the site root."""
import json, os, re, sys, html
from content import *

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
CFG = json.load(open(os.path.join(HERE, 'config.json'), encoding='utf8'))
DOMAIN = CFG['domain'].rstrip('/')
EMAIL = CFG.get('contact_email', '').strip()
GSC = CFG.get('google_site_verification', '').strip()
ADS = CFG.get('adsense_publisher_id', '').strip().replace('ca-pub-', 'pub-')
IKEY = CFG.get('indexnow_key', '').strip()
LASTMOD = CFG['last_modified']
V = LASTMOD.replace('-', '')
BRAND = 'EditPDF'
e = lambda s: html.escape(s, quote=True)

LIBS = {
 'pdflib': 'https://cdnjs.cloudflare.com/ajax/libs/pdf-lib/1.17.1/pdf-lib.min.js',
 'jspdf': 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js',
 'pdfjs': 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js',
}
MARK = ('<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M8 3.5h10l7 7V27a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 7 27V5a1.5 1.5 0 0 1 1-1.5Z" fill="none" stroke="currentColor" stroke-width="2"/>'
        '<path d="M18 4v7h7M11 17h10M11 21h10" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>')
BRAND_HTML = f'<span class="brand-mark">{MARK}</span><span>Edit<span class="brand-accent">PDF</span></span>'

written = []   # (url path, priority, changefreq) for sitemap
def url(path): return DOMAIN + path

def ldjson(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>'

def head(path, title, desc, graph=None, robots=True, og_type='website'):
    canon = url(path)
    rb = 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1' if robots else 'noindex, follow'
    h = ['<!DOCTYPE html>', '<html lang="en">', '<head>', '<meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1">',
         f'<title>{e(title)}</title>', f'<meta name="description" content="{e(desc)}">']
    if GSC: h.append(f'<meta name="google-site-verification" content="{e(GSC)}">')
    h += [f'<meta name="robots" content="{rb}">', f'<link rel="canonical" href="{canon}">', '<link rel="sitemap" type="application/xml" href="/sitemap.xml">', '<meta name="theme-color" content="#6857e8">',
          f'<meta property="og:type" content="{og_type}">', f'<meta property="og:site_name" content="{BRAND}">',
          f'<meta property="og:title" content="{e(title)}">', f'<meta property="og:description" content="{e(desc)}">',
          f'<meta property="og:url" content="{canon}">', f'<meta property="og:image" content="{url("/img/og-image.png")}">',
          '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">',
          f'<meta property="og:image:alt" content="{BRAND} — free online PDF tools">', '<meta property="og:locale" content="en_US">',
          '<meta name="twitter:card" content="summary_large_image">', f'<meta name="twitter:title" content="{e(title)}">',
          f'<meta name="twitter:description" content="{e(desc)}">', f'<meta name="twitter:image" content="{url("/img/og-image.png")}">',
          '<link rel="icon" href="/favicon.svg" type="image/svg+xml">', '<link rel="icon" href="/favicon.ico" sizes="any">',
          '<link rel="icon" href="/img/icon-192.png" type="image/png" sizes="192x192">',
          '<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">', '<link rel="manifest" href="/site.webmanifest">',
          '<link rel="preconnect" href="https://fonts.googleapis.com">', '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
          '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap" media="print" onload="this.media=\'all\'">',
          '<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap"></noscript>',
          f'<link rel="stylesheet" href="/css/style.css?v={V}">']
    if ADS: h.append(f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-{ADS}" crossorigin="anonymous"></script>')
    if graph: h.append(ldjson({'@context': 'https://schema.org', '@graph': graph}))
    h.append('</head>')
    return '\n'.join(h)

NAV = [('merge-pdf', 'Merge PDF'), ('split-pdf', 'Split PDF'), ('compress-pdf', 'Compress PDF'), ('image-to-pdf', 'Image to PDF')]
def header(current=None):
    cur = ' aria-current="page"'
    links = ''.join('<a href="/%s/"%s>%s</a>' % (s, cur if s == current else '', n) for s, n in NAV)
    about_cur = cur if current == 'about' else ''
    return (f'<a class="skip" href="#main">Skip to content</a>\n<header class="topbar"><a class="brand" href="/" aria-label="{BRAND} home">{BRAND_HTML}</a>'
            f'<nav class="nav-links" aria-label="Main">{links}<a href="/about/"{about_cur}>About</a></nav>'
            f'<div class="header-actions"><a class="header-cta" href="/#tools">All tools <span>↗</span></a></div></header>')

def footer():
    tools = ''.join(f'<a href="/{t["slug"]}/">{t["name"]}</a>' for t in TOOLS)
    guides = ''.join(f'<a href="/{g["slug"]}/">{g["h1"].replace("How to ","How to ")}</a>' for g in GUIDES)
    return (f'<footer class="site-footer"><div class="footer-inner"><div class="footer-col"><a class="brand footer-brand" href="/" aria-label="{BRAND} home">{BRAND_HTML}</a>'
            f'<p class="footer-about">Free online PDF tools that run in your browser. Merge, split, compress and rotate PDFs, or turn images into PDF — no account needed.</p></div>'
            f'<nav class="footer-col" aria-label="PDF tools"><h2>PDF tools</h2>{tools}</nav>'
            f'<nav class="footer-col" aria-label="Guides"><h2>Guides</h2>{guides}</nav>'
            f'<nav class="footer-col" aria-label="Company"><h2>{BRAND}</h2><a href="/about/">About</a><a href="/contact/">Contact</a><a href="/privacy/">Privacy Policy</a><a href="/terms/">Terms of Use</a></nav></div>'
            f'<div class="footer-bottom"><span>© <span id="year">{LASTMOD[:4]}</span> {BRAND}. All rights reserved.</span><span>{BRAND} is an independent tool and is not affiliated with Adobe.</span></div></footer>')

def scripts(libs=(), extra=()):
    s = ''.join(f'<script defer src="{LIBS[l]}"></script>\n' for l in libs)
    s += f'<script defer src="/js/app.js?v={V}"></script>\n'
    for x in extra: s += f'<script defer src="{x}?v={V}"></script>\n'
    return s

def relativize(path, content):
    # Make local links relative so CSS/JS work from any folder, from file://, and on subfolder hosting.
    depth = 0 if path == '/' else path.strip('/').count('/') + 1
    prefix = './' if depth == 0 else '../' * depth
    return re.sub(r'(href|src)="/(?!/)', lambda m: '%s="%s' % (m.group(1), prefix), content)

def write(path, content):
    content = relativize(path, content)
    fp = os.path.join(ROOT, path.strip('/'), 'index.html') if path != '/' else os.path.join(ROOT, 'index.html')
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'w', encoding='utf8').write(content)

def crumbs_html(items):
    out = '<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a>'
    for i, (name, p) in enumerate(items):
        out += '<span>/</span>' + (f'<a href="{p}">{e(name)}</a>' if i < len(items) - 1 else f'<span style="margin:0">{e(name)}</span>')
    return out + '</nav>'

def crumbs_ld(items):
    el = [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': url('/')}]
    for i, (name, p) in enumerate(items): el.append({'@type': 'ListItem', 'position': i + 2, 'name': name, 'item': url(p)})
    return {'@type': 'BreadcrumbList', 'itemListElement': el}

ORG = {'@type': 'Organization', '@id': url('/#organization'), 'name': BRAND, 'url': url('/'), 'logo': {'@type': 'ImageObject', 'url': url('/img/icon-512.png'), 'width': 512, 'height': 512}}
WEBSITE = {'@type': 'WebSite', '@id': url('/#website'), 'url': url('/'), 'name': BRAND, 'description': 'Free online PDF tools that run in your browser.', 'inLanguage': 'en', 'publisher': {'@id': url('/#organization')}}

def faq_html(faq):
    return ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq)
def faq_ld(faq):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]}

def tool_card(t):
    return (f'<a class="tool-card" href="/{t["slug"]}/" data-category="{t["cat"]}"><span class="tool-icon {t["color"]}"><svg viewBox="0 0 24 24" aria-hidden="true">{t["icon"]}</svg></span>'
            f'<span class="tool-card-text"><b>{t["name"]}</b><small>{t["card"]}</small><span class="tool-link">{t["cta"]} →</span></span><span class="tool-arrow" aria-hidden="true">↗</span></a>')

def link_cards(slugs, guide=None):
    cards = ''
    for s in slugs:
        t = next(x for x in TOOLS if x['slug'] == s)
        cards += f'<a class="link-card" href="/{s}/"><b>{t["name"]}</b><span>{t["card"]}</span></a>'
    if guide:
        g = next(x for x in GUIDES if x['slug'] == guide)
        cards += f'<a class="link-card" href="/{g["slug"]}/"><b>Guide: {g["h1"]}</b><span>{g["card"]}</span></a>'
    return f'<div class="link-cards">{cards}</div>'

# ------------------------------------------------------------------ home
def build_home():
    title = 'EditPDF: Free Online PDF Tools – Merge, Split, Compress'
    desc = 'Free online PDF tools: merge, split, compress and rotate PDF files, or convert images to PDF. Fast, private and right in your browser — no account needed.'
    graph = [ORG, WEBSITE, {'@type': 'WebPage', '@id': url('/#webpage'), 'url': url('/'), 'name': title, 'description': desc, 'isPartOf': {'@id': url('/#website')}, 'inLanguage': 'en'},
             {'@type': 'ItemList', 'name': 'EditPDF tools', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': url(f'/{t["slug"]}/'), 'name': t['name']} for i, t in enumerate(TOOLS)]},
             faq_ld(HOME_FAQ)]
    cats = ['All tools', 'Organize PDF', 'Convert & Compress', 'PDF Info']
    pills = ''.join(f'<button type="button" class="category-pill{" active" if i == 0 else ""}">{c}</button>' for i, c in enumerate(cats))
    cards = ''.join(tool_card(t) for t in TOOLS)
    guides = ''.join(f'<a class="link-card" href="/{g["slug"]}/"><b>{g["h1"]}</b><span>{g["card"]}</span></a>' for g in GUIDES)
    body = f'''<body>
{header()}
<main id="main">
<section class="hero"><h1>{e(HERO_LINE)}</h1></section>
<section class="tool-section" id="tools" aria-label="PDF tools">
<h2 class="sr-only">All PDF tools</h2>
<div class="tool-bar"><div class="category-row" role="group" aria-label="Filter tools">{pills}</div><div class="search-box"><span aria-hidden="true">⌕</span><input id="toolSearch" type="search" placeholder="Search tools..." aria-label="Search tools"></div></div>
<div class="tool-grid" id="toolGrid">{cards}</div>
<div class="empty-search" id="emptySearch" hidden>No tools found. Try another search.</div>
</section>
<section class="section" id="how"><div class="how-title"><div class="eyebrow">No complicated steps</div><h2>Work with PDFs in 3 steps</h2><p>Spend less time managing files and more time getting things done.</p></div>
<ol class="steps"><li class="step"><div class="step-number">01</div><h3>Choose your file</h3><p>Pick a tool, then select a PDF or image from your device. Your files are not uploaded to our server.</p></li><li class="step"><div class="step-number">02</div><h3>Use your tool</h3><p>Set the options you need and let the tool process your document in your browser.</p></li><li class="step"><div class="step-number">03</div><h3>Download the result</h3><p>Save your finished file. No sign-up, no waiting for an email, no watermark.</p></li></ol></section>
<section class="privacy-section" id="privacy"><div class="privacy-icon" aria-hidden="true">♧</div><div><h2>Your files are your business.</h2><p>Files are processed locally in your browser with open-source document libraries. They are not sent to an {BRAND} server. Avoid using public devices for sensitive documents, and keep your downloads secure.</p></div><div class="privacy-checks"><span>✓ No account</span><span>✓ Local processing</span><span>✓ Free tools</span></div></section>
<section class="section"><div class="eyebrow">Learn more</div><h2>PDF guides</h2><p class="sub">Short, practical how-tos for everyday PDF jobs.</p><div class="link-cards">{guides}</div></section>
<section class="section faq" id="faq"><div class="eyebrow">Good to know</div><h2>Frequently asked questions</h2>{faq_html(HOME_FAQ)}</section>
</main>
{footer()}
{scripts()}</body></html>'''
    write('/', head('/', title, desc, graph) + '\n' + body)
    written.append(('/', '1.0', 'weekly'))

# ------------------------------------------------------------------ tool pages
def build_tool(t):
    path = f'/{t["slug"]}/'; name = t['name']
    steps_ld = [{'@type': 'HowToStep', 'position': i + 1, 'name': s[0], 'text': s[1]} for i, s in enumerate(t['steps'])]
    crumbs = [(name, path)]
    graph = [ORG, WEBSITE,
      {'@type': 'WebApplication', '@id': url(path) + '#app', 'name': f'{BRAND} {name}', 'url': url(path), 'description': t['desc'], 'applicationCategory': 'UtilitiesApplication',
       'operatingSystem': 'Any (web browser)', 'browserRequirements': 'Requires JavaScript', 'isAccessibleForFree': True, 'inLanguage': 'en',
       'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'}, 'publisher': {'@id': url('/#organization')}},
      crumbs_ld(crumbs),
      {'@type': 'HowTo', 'name': f'How to use the {name} tool', 'step': steps_ld},
      faq_ld(t['faq'])]
    steps = ''.join(f'<li><strong>{e(a)}.</strong> {e(b)}</li>' for a, b in t['steps'])
    feats = ''.join(f'<div class="feature"><h3>{e(a)}</h3><p>{e(b)}</p></div>' for a, b in t['feats'])
    body = f'''<body>
{header(t['slug'])}
<main id="main">
{crumbs_html(crumbs)}
<section class="page-hero"><h1>{e(t['h1'])}</h1><p>{e(t['lead'])}</p></section>
<div class="tool-panel-wrap"><section class="tool-panel" id="toolPanel" data-tool="{t['key']}" aria-label="{e(name)} tool">
<div id="toolFields"></div>
<div class="status-message" id="statusMessage" role="status" aria-live="polite"></div>
<div class="panel-actions"><a class="result-link" id="resultLink" href="#">Download</a><button class="primary-btn" id="runTool" type="button">{e(name)} <span>→</span></button></div>
<noscript><div class="noscript-msg">This tool needs JavaScript. Please enable JavaScript in your browser to use it.</div></noscript>
<p class="panel-footnote">🔒 Your files stay on your device — they are processed in your browser and never uploaded. Processing may take a moment for large documents.</p>
</section></div>
<section class="prose-section"><h2>How to use {e(name)}</h2><ol>{steps}</ol></section>
<section class="prose-section"><h2>About {e(name)}</h2><p>{e(t['about'])}</p><div class="note">{t['limits']}</div></section>
<section class="section"><h2>Why use {BRAND} for this?</h2><div class="feature-grid">{feats}</div></section>
<section class="section faq"><h2>{e(name)} — frequently asked questions</h2>{faq_html(t['faq'])}</section>
<section class="section"><h2>More PDF tools</h2>{link_cards(t['related'], t['guide'])}</section>
</main>
{footer()}
{scripts(t['libs'])}</body></html>'''
    write(path, head(path, t['title'], t['desc'], graph) + '\n' + body)
    written.append((path, '0.9', 'monthly'))

# ------------------------------------------------------------------ guides
def build_guide(g):
    path = f'/{g["slug"]}/'; crumbs = [(g['h1'], path)]
    graph = [ORG, WEBSITE, crumbs_ld(crumbs),
      {'@type': 'Article', '@id': url(path) + '#article', 'headline': g['h1'], 'description': g['desc'], 'mainEntityOfPage': url(path), 'image': url('/img/og-image.png'),
       'datePublished': LASTMOD, 'dateModified': LASTMOD, 'inLanguage': 'en', 'author': {'@id': url('/#organization')}, 'publisher': {'@id': url('/#organization')}}]
    t = next(x for x in TOOLS if x['slug'] == g['tool'])
    body = f'''<body>
{header()}
<main id="main" class="legal-main">
{crumbs_html(crumbs)}
<article><header class="legal-hero"><div class="eyebrow">{BRAND} guide</div><h1>{e(g['h1'])}</h1><p>{e(g['lead'])}</p><div class="legal-meta">Last updated: {LASTMOD}</div></header>
<div class="legal-content">{g['body']}
<div class="article-cta"><div><b>{e(t['name'])}</b><span>{e(t['card'])} Free, private, no account.</span></div><a class="primary-btn" href="/{t['slug']}/">{e(g['tool_cta'])} <span>→</span></a></div>
<h2>Related tools</h2>{link_cards([x for x in ['merge-pdf','split-pdf','compress-pdf','image-to-pdf','rotate-pdf'] if x != g['tool']][:3])}
</div></article>
</main>
{footer()}
{scripts()}</body></html>'''
    write(path, head(path, g['title'], g['desc'], graph, og_type='article') + '\n' + body)
    written.append((path, '0.7', 'monthly'))

# ------------------------------------------------------------------ info pages
def info_page(path, title, desc, eyebrow, h1, lead, inner, prio, freq, current=None, extra_scripts=(), meta=True):
    graph = [ORG, WEBSITE, crumbs_ld([(h1, path)])]
    body = f'''<body>
{header(current)}
<main id="main" class="legal-main">
{crumbs_html([(h1, path)])}
<section class="legal-hero"><div class="eyebrow">{e(eyebrow)}</div><h1>{e(h1)}</h1><p>{e(lead)}</p>{f'<div class="legal-meta">Last updated: {LASTMOD}</div>' if meta else ''}</section>
{inner}
</main>
{footer()}
{scripts(extra=extra_scripts)}</body></html>'''
    write(path, head(path, title, desc, graph) + '\n' + body)
    written.append((path, prio, freq))

def build_about():
    inner = f'''<div class="legal-content"><h2>What we do</h2><p>{BRAND} brings everyday PDF tasks together on one fast website. Depending on the tool, you can combine PDFs, extract pages, rotate pages, inspect PDF properties, compress a PDF, or turn images into a PDF.</p>
<div class="legal-card-grid"><article class="legal-card"><div class="legal-card-icon" aria-hidden="true">⌁</div><h3>Simple by design</h3><p>Clear tools and practical instructions, built to work on desktop and mobile browsers.</p></article><article class="legal-card"><div class="legal-card-icon" aria-hidden="true">♧</div><h3>Local processing</h3><p>Supported file operations run in your browser; files are not intentionally uploaded to an {BRAND} server.</p></article><article class="legal-card"><div class="legal-card-icon" aria-hidden="true">✦</div><h3>Free access</h3><p>The current tools are free to use. Features and availability may change as the site develops.</p></article></div>
<h2>How the tools work</h2><p>{BRAND} uses open-source JavaScript libraries (pdf-lib, PDF.js and jsPDF) to process documents on your device. An internet connection is needed to load these libraries and fonts from public content delivery networks. Performance depends on your device, browser and document size.</p>
<h2>Honest limitations</h2><p>Compression can turn text into images, which means the resulting PDF may no longer have selectable or searchable text, and it does not guarantee a smaller output. {BRAND} does not currently include PDF-to-Word conversion, OCR or every advanced feature offered by desktop software. Always review important output files before relying on them.</p>
<h2>Explore the tools</h2>{link_cards(['merge-pdf','split-pdf','compress-pdf'])}
<h2>Questions or feedback?</h2><p>We welcome reports about errors, accessibility issues and suggestions for useful tools. Visit our <a href="/contact/">Contact page</a> to get in touch.</p>
<div class="legal-callout"><strong>Independence notice:</strong> {BRAND} is an independent tool website and is not affiliated with or endorsed by Adobe or any PDF software vendor.</div></div>'''
    info_page('/about/', f'About {BRAND} – Free Browser-Based PDF Tools', f'Learn about {BRAND}, a simple collection of free PDF tools that run in your browser: merge, split, compress, rotate and convert.',
              f'About {BRAND}', 'Useful PDF tools. Without the fuss.', f'{BRAND} is a small, practical toolkit that makes everyday PDF tasks simpler. Our goal is to help people manage documents quickly, without an account or a desktop application.', inner, '0.4', 'yearly', 'about')

def build_contact():
    mailbox = f'<a class="contact-email" href="mailto:{e(EMAIL)}">{e(EMAIL)}</a>' if EMAIL else ''
    inner = f'''<div class="contact-layout"><section class="contact-panel"><h2>Send a message</h2><p>This form opens your device's default email app with a prepared message. Nothing is sent automatically; you can review and send the email yourself.</p>
<form class="contact-form" id="contactForm" data-email="{e(EMAIL)}"><label for="contactName">Your name (optional)</label><input id="contactName" name="name" autocomplete="name" maxlength="100" placeholder="Name"><label for="contactEmail">Your email address</label><input id="contactEmail" name="email" type="email" autocomplete="email" required maxlength="200" placeholder="you@example.com"><label for="contactTopic">What is your message about?</label><select id="contactTopic" name="topic"><option>General feedback</option><option>Tool not working</option><option>Privacy question</option><option>Accessibility issue</option><option>Business or advertising</option><option>Other</option></select><label for="contactMessage">Message</label><textarea id="contactMessage" name="message" required maxlength="5000" placeholder="Tell us how we can help..."></textarea><button class="primary-btn" type="submit">Prepare email <span>→</span></button><p class="form-note">Please do not include passwords, financial details or sensitive documents in your message.</p><p id="contactStatus" class="form-note" role="status" aria-live="polite"></p></form></section>
<aside class="contact-panel"><h2>Before you contact us</h2><p>For the fastest help, mention which tool you used, what you expected to happen and what happened instead. If you see an error, include the exact message and your browser name.</p>{('<h3>Email</h3>' + mailbox) if EMAIL else ''}<h3>Privacy requests</h3><p>For a privacy-related request, choose “Privacy question” and describe the request without including sensitive personal information.</p><p>{BRAND} does not currently offer live chat or a guaranteed response time.</p></aside></div>'''
    info_page('/contact/', f'Contact {BRAND} – Help and Feedback', f'Contact {BRAND} with questions, feedback or reports about our free PDF tools.', "We'd like to hear from you", f'Contact {BRAND}',
              'Found a problem, have a suggestion, or need to report an accessibility or privacy concern? Send us a message using the form below.', inner, '0.3', 'yearly', 'contact', extra_scripts=['/js/contact.js'], meta=False)

def build_privacy():
    ads_para = ('<p>This website uses Google AdSense to show ads. Google and its partners may use cookies and similar technologies to serve and measure ads, including ads based on your previous visits to this or other websites. Google’s use of advertising cookies enables it and its partners to serve ads to you based on your visit to this site and/or other sites on the Internet. You can opt out of personalized advertising by visiting <a href="https://www.google.com/settings/ads" rel="noopener">Google Ads Settings</a>, and you can learn how Google uses information from sites that use its services at <a href="https://policies.google.com/technologies/partner-sites" rel="noopener">policies.google.com/technologies/partner-sites</a>. Where required by law (for example for visitors in the European Economic Area, the United Kingdom and Switzerland), ads and cookies are shown only according to your consent choices.</p>'
                if ADS else
                '<p>If an advertising service such as Google AdSense is added in the future, that provider may use cookies or similar technologies to deliver, measure and personalize ads, subject to your settings, applicable law and the provider’s policies. This policy will be updated before such services are enabled.</p>')
    inner = f'''<div class="legal-content"><div class="legal-callout"><strong>In brief:</strong> The tools process your selected documents locally in your browser. {BRAND} does not intentionally upload your selected files to an {BRAND} server. The website uses third-party services to load fonts and JavaScript libraries, and the hosting provider may process routine connection logs.</div>
<h2>1. Information we process</h2><h3>Files you choose</h3><p>PDFs and images selected for the tools are processed locally in your browser using JavaScript libraries. The tool code does not intentionally transmit the contents of those files to an {BRAND}-operated server. Your browser and device remain responsible for the local processing and downloaded results. Do not use a shared or untrusted device for confidential documents.</p>
<h3>Routine technical information</h3><p>When you visit a website, its hosting provider and network infrastructure may automatically receive technical data such as your IP address, browser and device details, requested URLs, timestamps and error information in server or security logs. The precise data retained depends on the hosting provider and its settings.</p>
<h3>Messages you send us</h3><p>If you contact us by email, we receive the information you include, such as your email address and the contents of your message. We use it to respond and handle follow-up questions.</p>
<h2>2. Cookies, analytics and advertising</h2><p>{BRAND} does not set its own analytics cookies. Hosting services and third-party scripts may use their own technical mechanisms according to their policies.</p>{ads_para}
<h2>3. Third-party libraries and fonts</h2><p>The website loads PDF processing libraries from cdnjs (Cloudflare) and fonts from Google Fonts. Your browser requests these resources from the respective providers, which may receive technical connection data such as your IP address. Your selected document files are not sent with these requests. Please review the providers’ own privacy information for their practices.</p>
<h2>4. Why information may be used</h2><p>Technical information may be processed by hosting or security providers to deliver the website, prevent abuse, diagnose errors and maintain reliability. Contact information is used to respond to messages. We do not sell the contents of your documents.</p>
<h2>5. Retention and security</h2><p>Document processing takes place in your browser; files you download or keep are under your control. Routine hosting logs and correspondence may be retained by the relevant providers or by us for periods determined by operational needs, security, legal obligations and provider settings. No website or transmission method can be guaranteed completely secure.</p>
<h2>6. Children’s privacy</h2><p>{BRAND} is a general-purpose utility website and is not directed to children. If you believe a child has provided personal information to us through a contact message, please contact us so we can address the request.</p>
<h2>7. Your choices and privacy rights</h2><p>Depending on where you live, you may have rights to request access to, correction of, deletion of, or information about personal data. You can control cookies through your browser settings and choose not to send us personal information in a message. Some technical data is handled directly by the hosting provider; contact that provider where appropriate.</p>
<h2>8. International visitors</h2><p>Your technical information may be processed in countries where our hosting or third-party providers operate. Data protection laws vary by location.</p>
<h2>9. Changes to this policy</h2><p>We may update this policy when tools, hosting, analytics, advertising or legal requirements change. The date at the top shows when this version was published.</p>
<h2>10. Contact</h2><p>For privacy questions or requests, use our <a href="/contact/">Contact page</a>{f' or email <a href="mailto:{e(EMAIL)}">{e(EMAIL)}</a>' if EMAIL else ''}.</p></div>'''
    info_page('/privacy/', f'Privacy Policy | {BRAND}', f'How {BRAND} handles information. Files you select are processed in your browser and are not uploaded to our servers.', 'Privacy & transparency', 'Privacy Policy',
              f'This policy explains how {BRAND} handles information when you visit the website and use its browser-based document tools.', inner, '0.3', 'yearly')

def build_terms():
    inner = f'''<div class="legal-content"><h2>1. Acceptance of terms</h2><p>By using {BRAND} you agree to these terms. If you do not agree, please do not use the website.</p>
<h2>2. What the service provides</h2><p>{BRAND} offers free, browser-based tools for working with PDF files and images. The tools run in your browser on your device. Features may change, be limited or be removed at any time.</p>
<h2>3. Your responsibility for your files</h2><p>You are responsible for the files you process and for having the right to use them. Do not use {BRAND} for unlawful content or to infringe the rights of others. Keep copies of your original files: always review the output before relying on it.</p>
<h2>4. No warranty</h2><p>The service is provided “as is” and “as available”, without warranties of any kind. Results can vary by file and device, and we do not guarantee that output files will be smaller, error-free or suitable for a particular purpose.</p>
<h2>5. Limitation of liability</h2><p>To the extent permitted by law, {BRAND} and its operator are not liable for any loss or damage arising from use of, or inability to use, the website or its tools, including loss of data.</p>
<h2>6. Acceptable use</h2><p>Do not attempt to disrupt the website, scrape it at a rate that harms its availability, or use automated means to bypass its normal operation.</p>
<h2>7. Third-party services and advertising</h2><p>The website relies on third-party libraries, fonts and hosting, and may display third-party advertising. Those services are governed by their own terms and privacy policies. See our <a href="/privacy/">Privacy Policy</a>.</p>
<h2>8. Intellectual property</h2><p>The {BRAND} name, design and original content belong to the site operator. Open-source libraries used by the tools remain under their respective licenses.</p>
<h2>9. Changes</h2><p>We may update these terms from time to time. Continued use after a change means you accept the updated terms.</p>
<h2>10. Contact</h2><p>Questions about these terms? Visit our <a href="/contact/">Contact page</a>.</p></div>'''
    info_page('/terms/', f'Terms of Use | {BRAND}', f'The terms for using {BRAND} free online PDF tools.', 'Legal', 'Terms of Use', f'Please read these terms before using {BRAND}.', inner, '0.3', 'yearly')

def build_404():
    body = f'''<body>
{header()}
<main id="main"><div class="not-found"><h1>Page not found</h1><p>The page you wanted does not exist or has moved. Try one of our PDF tools instead.</p><a class="primary-btn" href="/">Go to all PDF tools <span>→</span></a></div>
<section class="section"><h2>Popular tools</h2>{link_cards(['merge-pdf','compress-pdf','split-pdf'])}</section></main>
{footer()}
{scripts()}</body></html>'''
    html404 = head('/404.html', f'Page not found | {BRAND}', 'This page does not exist. Return to the EditPDF free online PDF tools.', robots=False) + '\n' + body
    open(os.path.join(ROOT, '404.html'), 'w', encoding='utf8').write(html404)

# ------------------------------------------------------------------ seo + config files
def build_files():
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p, pr, fr in written:
        sm.append(f'  <url>\n    <loc>{url(p)}</loc>\n    <lastmod>{LASTMOD}</lastmod>\n    <changefreq>{fr}</changefreq>\n    <priority>{pr}</priority>\n  </url>')
    sm.append('</urlset>\n')
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf8').write('\n'.join(sm))
    open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf8').write(f'# Allow search engines to crawl all public pages and assets.\nUser-agent: *\nAllow: /\nDisallow: /_build/\n\nSitemap: {url("/sitemap.xml")}\n')
    if ADS: open(os.path.join(ROOT, 'ads.txt'), 'w', encoding='utf8').write(f'google.com, {ADS}, DIRECT, f08c47fec0942fa0\n')
    elif os.path.exists(os.path.join(ROOT, 'ads.txt')): os.remove(os.path.join(ROOT, 'ads.txt'))
    if IKEY: open(os.path.join(ROOT, f'{IKEY}.txt'), 'w', encoding='utf8').write(IKEY)
    manifest = {'name': BRAND, 'short_name': BRAND, 'description': 'Free online PDF tools that run in your browser.', 'start_url': '/', 'scope': '/', 'display': 'standalone',
                'background_color': '#f7f8fc', 'theme_color': '#6857e8',
                'icons': [{'src': '/img/icon-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': '/img/icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]}
    open(os.path.join(ROOT, 'site.webmanifest'), 'w', encoding='utf8').write(json.dumps(manifest, indent=2))

build_home()
for t in TOOLS: build_tool(t)
for g in GUIDES: build_guide(g)
build_about(); build_contact(); build_privacy(); build_terms(); build_404(); build_files()
print(f'Built {len(written)} pages for {DOMAIN}')
if 'your-domain' in DOMAIN: print('\n!! WARNING: domain in _build/config.json is still the placeholder. Set your real domain, then run build.py again.\n')
if not GSC: print('Note: google_site_verification is empty (fine if you verify with the HTML-file or DNS method).')
if not ADS: print('Note: adsense_publisher_id is empty — AdSense code and ads.txt are not added yet.')
