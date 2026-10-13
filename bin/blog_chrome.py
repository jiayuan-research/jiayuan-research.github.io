"""Homepage-only chrome shared by the standalone blog pages under /blog/.

add_sitebar() puts the same header as the al-folio pages (name on the left,
site links on the right, collapsing to a menu on phones) at the top of a page.

Used by bin/sync_project_pages.py and bin/build_coding_agent_toolkit.py.
"""

SITE_LINKS = [("about", "/"), ("research", "/research/"), ("blog", "/blog/"),
              ("publications", "/publications/"), ("services", "/services/")]

SITEBAR_HEAD = """
<!-- site header (homepage-only; injected by bin/blog_chrome.py) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap">
<style>
  :root { --site-h: 56px; }
  .sitebar { position: fixed; z-index: 150; top: 0; left: 0; right: 0; height: var(--site-h); background: #fff;
    border-bottom: 1px solid rgba(0,0,0,.1); font: 300 16px/1.5 Roboto, sans-serif; letter-spacing: normal; text-transform: none; }
  .sitebar-in { position: relative; display: flex; align-items: center; justify-content: space-between; gap: 16px;
    max-width: 930px; height: 100%; margin: 0 auto; padding: 0 16px; box-sizing: border-box; }
  .sitebar a { color: #000; text-decoration: none; }
  .sb-brand { font-size: 20px; font-weight: 300; white-space: nowrap; }
  .sb-brand b { font-weight: 700; }
  .sb-links { display: flex; gap: 6px; margin: 0; padding: 0; list-style: none; }
  .sb-links a { display: block; padding: 8px 6px; }
  .sb-links a:hover, .sb-links a[aria-current="page"] { color: #b509ac; }
  .sb-links a[aria-current="page"] { font-weight: 400; }
  .sb-toggle { display: none; width: 40px; height: 40px; margin-right: -8px; padding: 0; border: 0; background: none; cursor: pointer; }
  .sb-toggle span { display: block; width: 22px; height: 2px; margin: 5px auto; background: #000; transition: transform .2s, opacity .2s; }
  .sitebar.open .sb-toggle span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
  .sitebar.open .sb-toggle span:nth-child(2) { opacity: 0; }
  .sitebar.open .sb-toggle span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }
  @media (max-width: 640px) {
    .sb-toggle { display: block; }
    .sb-links { display: none; position: absolute; top: 100%; left: 0; right: 0; flex-direction: column; gap: 0; padding: 6px 16px 10px;
      background: #fff; border-bottom: 1px solid rgba(0,0,0,.1); text-align: right; }
    .sitebar.open .sb-links { display: flex; }
  }
  @media print { .sitebar { display: none; } }
</style>
"""

SITEBAR_SCRIPT = """<script>
  (function () {
    var bar = document.querySelector('.sitebar'), btn = bar && bar.querySelector('.sb-toggle');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var open = bar.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  })();
</script>"""


def sitebar_html():
    current = ' aria-current="page"'
    links = "".join(
        f'<li><a href="{href}"{current if name == "blog" else ""}>{name}</a></li>'
        for name, href in SITE_LINKS)
    return f"""<header class="sitebar">
  <div class="sitebar-in">
    <a class="sb-brand" href="/"><b>Jiayuan</b> Zhou</a>
    <nav aria-label="Site"><ul class="sb-links" id="sb-links">{links}</ul></nav>
    <button class="sb-toggle" type="button" aria-expanded="false" aria-controls="sb-links" aria-label="Site menu"><span></span><span></span><span></span></button>
  </div>
</header>
{SITEBAR_SCRIPT}"""


def add_sitebar(html, page_css=""):
    """Insert the site header right after <body> and its CSS (plus page_css,
    the page-specific offsets) at the end of <head>."""
    if 'class="sitebar"' in html:
        return html
    if html.count("</head>") != 1 or html.count("<body>") != 1:
        raise SystemExit("add_sitebar: expected exactly one </head> and one <body>")
    css = SITEBAR_HEAD + (f"<style>\n{page_css}\n</style>\n" if page_css else "")
    html = html.replace("</head>", css + "</head>", 1)
    return html.replace("<body>", "<body>\n" + sitebar_html(), 1)
