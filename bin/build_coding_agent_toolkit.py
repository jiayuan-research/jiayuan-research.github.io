#!/usr/bin/env python3
"""Build blog/coding-agent-toolkit/{index.html,index.zh.html} from the ISSTA deck slide.

Takes the single-slide deck, re-skins it light, drops the slide title and the
presenter tooling, crops the empty stage margins, adds the Distinguished Paper
badge, points links at their published URLs, and writes an English and a
Chinese page with an EN / 中文 switch (same convention as the project pages).

Run from the repo root:  python3 bin/build_beyond_the_paper.py
"""
import re
from pathlib import Path

SRC = Path.home() / "WorkSpace/Presentation/ISSTA26-Lingxi/decks/lingxi-issta2026-rev15-iCode-detailed.html"
OUT = Path(__file__).resolve().parent.parent / "blog" / "coding-agent-toolkit"
SITE = "https://www.jiayuanzhou.com"

TITLE = {"en": "Beyond the paper: mine knowledge, evaluate it, run it on iCode",
         "zh": "论文之外：挖掘知识、评估知识，并在 iCode 上运行"}

# visible stage region (stage px): the content spans x 120..1800, y 250..1002
CROP_X, CROP_Y, VIEW_W, VIEW_H = 96, 226, 1728, 800

COLOR_MAP = [
    ("rgba(236,229,214,", "rgba(28,32,30,"), ("rgba(12,16,15,", "rgba(255,255,255,"),
    ("rgba(8,10,9,", "rgba(255,255,255,"), ("rgba(141,197,174,", "rgba(46,139,110,"),
    ("rgba(233,213,138,", "rgba(166,124,30,"), ("rgba(242,84,45,", "rgba(217,68,31,"),
    ("rgba(255,214,170,", "rgba(194,87,26,"), ("rgba(255,200,140,", "rgba(194,87,26,"),
    ("rgba(248,206,204,", "rgba(192,57,43,"), ("rgba(242,150,150,", "rgba(192,57,43,"),
    ("#0C100F", "#FBF9F4"), ("#060807", "#F3EFE6"), ("#0A0D0C", "#F2EEE5"), ("#121614", "#F5F1E8"),
    ("#ECE5D6", "#1C201E"), ("#8DC5AE", "#2E8B6E"), ("#E9D58A", "#A67C1E"), ("#D9B88F", "#9A6B2F"),
    ("#F2B98A", "#C2571A"), ("#EFA3A0", "#C0392B"), ("#1d1a10", "#F6EFDC"), ("#F2542D", "#D9441F"),
]

ZH = [  # (exact HTML fragment, Chinese replacement); longer fragments first
    (">iCode · our coding agent<", ">iCode · 我们的 coding agent<"),
    ("iCode on GitHub</a>", "iCode · GitHub</a>"),
    (">Each agent profile picks its own plugins.<", ">每个 agent profile 自行选择插件。<"),
    ("A one-stop pipeline for <span>agent research</span>.", "面向 <span>agent 研究</span>的一站式流水线。"),
    ("<b>Agents as configuration</b><span>tools, skills, MCP, memory</span>", "<b>Agent 即配置</b><span>工具、技能、MCP、记忆</span>"),
    ("<b>Mix models and agents</b><span>swap mid-session to compare</span>", "<b>混用模型与 agent</b><span>会话中途切换，直接对比</span>"),
    ("<b>Programmable workflows</b><span>agent + code nodes, loops</span>", "<b>可编程工作流</b><span>agent 与代码节点、循环</span>"),
    ("<b>Parallel analysis</b><span>fan out, then merge findings</span>", "<b>并行分析</b><span>多路展开，再合并发现</span>"),
    ("<b>Headless batch runs</b><span>scripted, repeatable runs</span>", "<b>无界面批量运行</b><span>脚本化、可重复</span>"),
    ("<b>Trajectory analytics</b><span>time, tokens, findings</span>", "<b>轨迹分析</b><span>耗时、token、发现</span>"),
    ("<b>Your data is yours.</b><span>No tracking · no data collection<br>telemetry off by default</span>",
     "<b>你的数据归你所有。</b><span>不追踪 · 不收集数据<br>遥测默认关闭</span>"),
    (">Lingxi Advisor · procedural knowledge, mined three ways<", ">Lingxi Advisor · 过程性知识，三种来源<"),
    (">from issue + patch<", ">来自 issue + patch<"),
    (">from trajectories<", ">来自执行轨迹<"),
    (">from test outcomes<", ">来自测试结果<"),
    ("<span>ISSTA'26<br>Distinguished Paper</span>", "<span>ISSTA'26<br>杰出论文奖</span>"),
    ("<i>(ensemble)</i>", "<i>（多 agent 集成）</i>"),
    ("↗ Plugin · available<br>for common agent harness", "↗ 插件 · 已发布<br>适配常见 agent 框架"),
    (">Plugin · coming soon<", ">插件 · 即将发布<"),
    (">↗ Project page<", ">↗ 项目主页<"),
    (">Evaluation Kit<", ">评估套件<"),
    (">Benchmarks<", ">基准<"),
    (">Techniques<", ">技术<"),
    (">Parallel deep analysis<", ">并行深度分析<"),
    (">Knowledge integration<", ">知识集成<"),
    (">supported<", ">已支持<"),
    (">integrated<", ">已集成<"),
    (">coming soon<", ">即将支持<"),
    (">↗ Plugin<", ">↗ 插件<"),
    (">plugs into<", ">接入<"),
    (">runs on<", ">运行于<"),
    # phone overview (mobile_view)
    (">procedural knowledge, mined three ways<", ">过程性知识，三种来源<"),
    ("<b>Your data is yours.</b></span>", "<b>你的数据归你所有。</b></span>"),
    (">Tap for details<", ">点击查看详情<"),
    (">available<", ">已可用<"),
    (">✕ Close<", ">✕ 关闭<"),
]

MEDAL = ('<span class="award" title="ISSTA 2026 · ACM SIGSOFT Distinguished Paper Award">'
         '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 2h4l1.6 4.2L14.2 2h4l-3.4 8.1" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
         '<circle cx="12" cy="15.5" r="6" fill="currentColor"/><path d="M12 12.4l.95 1.95 2.15.31-1.55 1.51.37 2.13L12 17.3l-1.92 1 .37-2.13-1.55-1.51 2.15-.31z" fill="#fff"/></svg>'
         "<span>ISSTA'26<br>Distinguished Paper</span></span>")


def remap(t):
    for a, b in COLOR_MAP:
        t = t.replace(a, b).replace(a.lower(), b)
    return t



def _line(body, prefix):
    """The single source line of the slide that starts with `prefix` (stripped)."""
    hits = [ln.strip() for ln in body.splitlines() if ln.strip().startswith(prefix)]
    assert len(hits) == 1, (prefix, len(hits))
    return hits[0]


def _inner(line):
    return line[line.index(">") + 1: line.rindex("</div>")]


def mobile_view(body):
    """Phone layout: an overview map of the slide, each box expandable.

    Overview keeps the slide's arrangement in portrait: Lingxi Advisor (top
    left) and Evaluation Kit (top right) both point down into iCode. Each tile
    shows a summary; tapping it opens a full-screen sheet with the complete
    box. Built from the slide's own fragments so the ZH map translates it too.
    """
    gh = _line(body, '<a class="ghlink r"')
    gh = re.sub(r'class="ghlink r" style="[^"]*"', 'class="ghlink"', gh)
    shot = _inner(_line(body, '<div class="shot2 r"'))
    anote = _inner(_line(body, '<div class="anote r"'))
    onestop = _inner(_line(body, '<div class="onestop r"'))
    ifeat_ln = _line(body, '<div class="ifeat xs r"')
    ifeat = ifeat_ln[ifeat_ln.index(">") + 1: -len("</div>")]
    privacy = _inner(_line(body, '<div class="privacy r"'))
    lock = re.search(r"<svg.*?</svg>", privacy).group(0)
    icode_tag = _line(body, '<div class="tag">iCode')
    adv_tag = _line(body, '<div class="tag hot">Lingxi Advisor')
    m = re.match(r'<div class="ecards"[^>]*>(.*)</div><div class="efoot">(.*?)</div>$', _line(body, '<div class="ecards"'))
    cards, efoot = m.group(1), m.group(2)
    kit_tag = _line(body, '<div class="tag">Evaluation Kit')
    kit_ln = _line(body, '<div class="egrid"')
    kit = re.sub(r' style="[^"]*"', '', kit_ln)
    medal = re.search(r"<svg.*?</svg>", MEDAL).group(0)
    ghmark = re.search(r"<svg.*?</svg>", gh).group(0)
    url_icode = re.search(r'href="([^"]+)"', gh).group(1)
    url_adv = re.search(r'<a class="plug"[^>]*href="([^"]+)"', cards).group(1)
    url_kit = re.search(r'<a class="lk" href="([^"]+)"[^>]*>↗ Plugin</a>', kit).group(1)
    assert 'github.com' in url_icode + url_adv + url_kit

    def ghchip(url, label):
        return f'<a class="mt-gh" href="{url}" target="_blank" rel="noopener">{ghmark}<span>{label}</span></a>'

    def ghicon(url, what):  # icon-only link that sits inline next to a name
        return f'<a class="mt-ghi" href="{url}" target="_blank" rel="noopener" aria-label="{what} on GitHub" title="{what} on GitHub">{ghmark}</a>'

    scores = re.findall(r'<b>([^<]+)</b>(?:<span class="award".*?</span></span>)?<div class="num">([^<]+)<i>', cards)
    assert [n for n, _ in scores] == ["Lingxi", "STAIR", "TestGRAD"], scores
    adv_rows = "".join(
        f'<span class="mt-row{" hot" if i == 0 else ""}"><b>{n}{f"<span class=mt-medal>{medal}</span>" + ghicon(url_adv, "Lingxi Advisor plugin") if i == 0 else ""}</b><i>{v}</i></span>'
        for i, (n, v) in enumerate(scores))
    kit_items = re.findall(r'<div class="er sm"><span>([^<]+)</span><em class="(ok|soon|wip)">', kit)
    assert len(kit_items) == 4, kit_items
    kit_rows = "".join(f'<span class="mt-row kit"><span>{n}{ghicon(url_kit, "SWE-bench Pro evaluation plugin") if n == "SWE-bench Pro" else ""}</span><em class="dot {c}"></em></span>'
                       for n, c in kit_items)
    more = '<span class="mt-more">Tap for details</span>'

    def sheet(sid, inner):
        return (f'<div class="msheet" id="{sid}" role="dialog" aria-modal="true">'
                f'<div class="msheet-bar"><button class="msheet-x" type="button">✕ Close</button></div>{inner}</div>')

    return f'''<div class="mview">
<div class="mmap">
<div class="mt mt-adv" role="button" tabindex="0" data-sheet="ms-adv"><span class="mt-name hot">Lingxi Advisor</span><span class="mt-sub">procedural knowledge, mined three ways</span><span class="mt-rows">{adv_rows}</span><span class="mt-foot">{efoot}</span>{more}</div>
<div class="mt mt-kit" role="button" tabindex="0" data-sheet="ms-kit"><span class="mt-name sand">Evaluation Kit</span><span class="mt-rows">{kit_rows}</span><span class="mt-legend"><span><em class="dot ok"></em>available</span><span><em class="dot soon"></em>coming soon</span></span>{more}</div>
<div class="mflow down hot"><span class="flowpill hot">plugs into</span></div>
<div class="mflow down"><span class="flowpill">runs on</span></div>
<div class="mt mt-icode" role="button" tabindex="0" data-sheet="ms-icode"><span class="mt-head"><span class="mt-name jade">iCode · our coding agent</span>{ghchip(url_icode, "GitHub")}</span><span class="mt-shot">{shot}</span><span class="mt-one">{onestop}</span><span class="mt-priv">{lock}<b>Your data is yours.</b></span>{more}</div>
</div>
{sheet("ms-adv", f'<section class="mcard m-adv">{adv_tag}<div class="m-ecards">{cards}</div><div class="m-foot">{efoot}</div></section>')}
{sheet("ms-kit", f'<section class="mcard m-kit">{kit_tag}{kit}</section>')}
{sheet("ms-icode", f'<section class="mcard m-icode"><div class="m-head">{icode_tag}{gh}</div><div class="m-shot">{shot}</div><div class="anote">{anote}</div><div class="onestop">{onestop}</div><div class="ifeat">{ifeat}</div><div class="privacy">{privacy}</div></section>')}
</div><!--/mview-->'''


def build(lang):
    s = SRC.read_text()
    head_end = s.index("</head>")
    head, body = remap(s[:head_end]), remap(s[head_end:])
    head = head.replace('<html lang="en">', '<html lang="zh-Hans">') if lang == "zh" else head
    head = re.sub(r"<title>[^<]*</title>", f"<title>{TITLE[lang]}</title>", head, count=1)
    alt = ('<link rel="alternate" hreflang="en" href="index.html">\n'
           '<link rel="alternate" hreflang="zh-Hans" href="index.zh.html">\n')
    head = head.replace("</title>", "</title>\n" + alt, 1)
    s = s  # noqa

    # drop slide title, chrome overlay, presenter/edit UI, deck script
    body = re.sub(r'\s*<div class="hd">\s*<h2 class="h2 one r"[^>]*>.*?</h2>\s*</div>', '', body, count=1, flags=re.S)
    body = re.sub(r'<!-- =+\s*DECK CHROME.*?</div>\s*\n\s*</main>', '</main>', body, count=1, flags=re.S)
    body = re.sub(r'<!-- Presenter aids.*?</script>', '', body, count=1, flags=re.S)
    assert 'class="chrome' not in body and '<script' not in body
    body = body.replace('<section class="slide"', '<section class="slide active visible"', 1)

    # Distinguished Paper badge, to the right of the Lingxi title
    key = '<div class="src">from issue + patch</div><b>Lingxi</b>'
    assert body.count(key) == 1
    body = body.replace(key, key + MEDAL, 1)

    # published URLs
    ph = '<a class="lk ph" href="#" title="link to be added" onclick="event.stopPropagation()">↗ Project page</a>'
    assert body.count(ph) == 2
    body = body.replace(ph, f'<a class="lk" href="{SITE}/blog/stair/" target="_blank" rel="noopener">↗ Project page</a>', 1)
    body = body.replace(ph, f'<a class="lk" href="{SITE}/blog/testgrad/" target="_blank" rel="noopener">↗ Project page</a>', 1)
    body = body.replace(f'href="{SITE}/lingxi/"', f'href="{SITE}/blog/lingxi/"')
    php = '<a class="lk ph" href="#" title="link to be added" onclick="event.stopPropagation()">↗ Plugin</a>'
    assert body.count(php) == 1
    body = body.replace(php, '<a class="lk" href="https://github.com/spine-se-lab/eval-kit-swe-pro" target="_blank" rel="noopener">↗ Plugin</a>')
    body = body.replace(' onclick="event.stopPropagation()"', '')
    body = body.replace("</main>\n</div>", "</main>\n</div>\n" + mobile_view(body), 1)
    if lang == "zh":
        sub = "index.zh.html"
        body = body.replace(f'{SITE}/blog/stair/', f'{SITE}/blog/stair/{sub}').replace(f'{SITE}/blog/testgrad/', f'{SITE}/blog/testgrad/{sub}').replace(f'{SITE}/blog/lingxi/', f'{SITE}/blog/lingxi/{sub}')
        for a, b in ZH:
            assert a in body, a
            body = body.replace(a, b)

    # language switch, page wrapper
    cur = ' aria-current="page"'
    en_cur, zh_cur = (cur, "") if lang == "en" else ("", cur)
    switch = ('<nav class="lang" aria-label="Language">'
              f'<a href="index.html" hreflang="en" lang="en"{en_cur}>EN</a>'
              f'<a href="index.zh.html" hreflang="zh-Hans" lang="zh-Hans"{zh_cur}>中文</a></nav>')
    body = body.replace('<div class="deck-viewport">', f'<div class="page">\n{switch}\n<div class="deck-viewport">', 1)
    body = body.replace("<!--/mview-->", "<!--/mview-->\n</div>", 1)

    extra = f'''
<style>
/* ===== blog page: light, one static slide, cropped and scaled to the column ===== */
:root {{ --page-bg: #E9E4DA; --card-bg: #FBF9F4; --bone-faint: rgba(28,32,30,.16); --sand: #9A6B2F; }}
html, body {{ width: auto; height: auto; overflow: auto; background: var(--page-bg); }}
body {{ padding: 20px 16px 40px 16px; }}
.page {{ max-width: 1440px; margin: 0 auto; }}
.lang {{ display: flex; justify-content: flex-end; margin: 0 0 10px auto; width: max-content; border: 1px solid #CFC7B6; background: var(--card-bg); font: 500 12px/1 'JetBrains Mono', monospace; letter-spacing: .08em; }}
.lang a {{ padding: 7px 11px; color: #5b6158; text-decoration: none; }}
.lang a + a {{ border-left: 1px solid #CFC7B6; }}
.lang a[aria-current="page"] {{ background: #1C201E; color: #fff; }}
.deck-viewport {{ position: relative; inset: auto; width: 100%; overflow: hidden; background: var(--card-bg);
  aspect-ratio: {VIEW_W} / {VIEW_H}; border: 1px solid #CFC7B6; border-radius: 10px; }}
.deck-stage {{ background: var(--card-bg); }}
.slide {{ background: radial-gradient(900px 600px at 26% 24%, rgba(217,68,31,.05), transparent 62%), radial-gradient(1100px 800px at 94% 78%, rgba(46,139,110,.05), transparent 66%), var(--card-bg); }}
.slide::after {{ opacity: .035; }}
.slide aside.notes {{ display: none; }}
.shot2 {{ box-shadow: 0 18px 40px -22px rgba(28,32,30,.45); border: 1px solid rgba(28,32,30,.12); }}
.ec .plug {{ color: #fff; }}
.ecards > .ec.hot {{ flex: 1.4; }}
.award {{ position: absolute; top: 35px; right: 16px; display: inline-flex; align-items: center; gap: 7px; padding: 4px 10px 4px 7px;
  border: 1.5px solid #B8860B; border-radius: 8px; background: #FFF7E0; color: #8A5E06; font: 700 12px/1.15 var(--font-mono); letter-spacing: -.01em; white-space: nowrap; }}
.award svg {{ width: 20px; height: 20px; flex: none; color: #C9961A; }}
/* privacy strip: keep it inside the iCode card (card bottom = 1002, feature grid bottom = 937) */
.privacy {{ top: 945px !important; padding: 6px 16px; }}
.privacy b {{ font-size: 22px; }}
.privacy span {{ font-size: 13px; line-height: 1.25; }}
.elinks .plug, .elinks .lk {{ height: 44px; min-height: 44px; box-sizing: border-box; }}
html[lang="zh-Hans"] .slide {{ font-family: var(--font-display), "PingFang SC", "Hiragino Sans GB", "Noto Sans SC", "Microsoft YaHei", sans-serif; }}
html[lang="zh-Hans"] .tag, html[lang="zh-Hans"] .ec .src, html[lang="zh-Hans"] .flowpill, html[lang="zh-Hans"] .egh {{ text-transform: none; letter-spacing: .04em; }}
/* ===== phone / narrow tablet: hide the scaled slide, show the re-flowed stack ===== */
.mview {{ display: none; }}
@media (max-width: 900px) {{
  body {{ padding: 14px 16px 32px; }}
  .deck-viewport {{ display: none; }}
  .mview {{ display: block; max-width: 640px; margin: 0 auto; }}
  .mcard {{ position: relative; padding: 18px 16px; border: 1px solid #CFC7B6; border-radius: 10px; background: var(--card-bg); }}
  .mcard .tag {{ font-size: 12px; line-height: 1.35; letter-spacing: .12em; }}
  .m-adv {{ border-color: rgba(217,68,31,.45); }}
  .m-icode {{ border-color: rgba(46,139,110,.45); }}
  .m-kit {{ border-color: rgba(154,107,47,.45); }}
  /* Advisor: one card per source */
  .m-ecards {{ display: grid; gap: 10px; margin-top: 14px; }}
  .m-ecards .ec {{ height: auto !important; padding: 14px; }}
  .m-ecards .ec .src {{ font-size: 11px; }}
  .m-ecards .ec b {{ margin-top: 6px; font-size: 24px; }}
  .m-ecards .ec .num {{ margin-top: 8px; font-size: 30px; }}
  .m-ecards .ec .num i {{ font-size: 12px; }}
  .m-ecards .ec.hot b {{ display: inline-block; vertical-align: middle; }}
  .m-ecards .award {{ position: static; vertical-align: middle; margin: 6px 0 0 10px; font-size: 11px; }}
  .m-ecards .elinks {{ position: static; display: grid; grid-template-columns: 1fr; gap: 8px; margin-top: 12px; }}
  .m-ecards .elinks .lk, .m-ecards .elinks .plug {{ position: static; height: auto; min-height: 38px; display: inline-flex; align-items: center; justify-content: center;
    padding: 7px 10px; font-size: 12px !important; line-height: 1.25; text-align: center; }}
  .m-foot {{ margin-top: 12px; font: 500 12px/1.3 var(--font-mono); letter-spacing: .06em; color: var(--bone-dim); }}
  /* connectors */
  .mflow {{ position: relative; display: flex; justify-content: center; height: 64px; }}
  .mflow::before {{ content: ""; position: absolute; left: 50%; top: 0; bottom: 0; width: 2px; margin-left: -1px; background: var(--sand); }}
  .mflow.hot::before {{ background: var(--cinnabar); }}
  .mflow::after {{ content: ""; position: absolute; left: 50%; margin-left: -6px; border: 6px solid transparent; }}
  .mflow.down::after {{ bottom: -2px; border-top: 9px solid var(--cinnabar); border-bottom: 0; }}
  .mflow .flowpill {{ position: relative; transform: none; z-index: 1; align-self: center; left: auto; top: auto; padding: 5px 10px; font-size: 12px; background: var(--page-bg); }}
  .mflow:not(.hot) .flowpill {{ color: var(--sand); border: 2px solid var(--sand); }}
  /* iCode */
  .m-head {{ display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 8px; }}
  .m-head .ghlink {{ position: static; font-size: 12px; }}
  .m-shot {{ margin-top: 12px; }}
  .m-shot img {{ display: block; width: 100%; height: auto; border-radius: 6px; border: 1px solid rgba(28,32,30,.12); box-shadow: 0 12px 28px -18px rgba(28,32,30,.45); }}
  .m-icode .anote {{ position: static; margin-top: 10px; font-size: 12px; color: var(--jade); }}
  .m-icode .onestop {{ position: static; margin-top: 10px; font-size: 20px !important; line-height: 1.25; }}
  .m-icode .ifeat {{ position: static; display: grid; grid-template-columns: 1fr 1fr; gap: 10px 14px; margin-top: 12px; }}
  .m-icode .ifeat b {{ font-size: 15px; }}
  .m-icode .ifeat span {{ font-size: 12.5px; }}
  .m-icode .privacy {{ position: static; display: flex; flex-wrap: wrap; align-items: center; gap: 6px 12px; margin-top: 14px; padding: 10px 14px; }}
  .m-icode .privacy b {{ font-size: 17px; }}
  .m-icode .privacy span {{ font-size: 12px; white-space: normal; }}
  /* Evaluation Kit */
  .m-kit > .tag {{ color: var(--sand); }}
  .m-kit .egrid {{ display: grid; grid-template-columns: 1fr; gap: 14px; margin-top: 12px; }}
  .m-kit .eg {{ margin-top: 0; }}
  .m-kit .egh {{ font-size: 11px; }}
  .m-kit .er {{ font-size: 16px; margin-top: 10px; }}
  .m-kit .er em {{ font-size: 11px; padding: 4px 8px; }}
  .m-kit .lk {{ display: inline-flex; margin-top: 14px; font-size: 12px; }}
  /* overview map: Advisor | Kit on top, both feeding iCode below */
  .mmap {{ display: grid; grid-template-columns: 1fr 1fr; column-gap: 10px; }}
  .mt {{ display: flex; flex-direction: column; align-items: stretch; gap: 6px; width: 100%; margin: 0; padding: 12px; text-align: left; cursor: pointer;
    font: inherit; color: var(--bone); border: 1px solid #CFC7B6; border-radius: 10px; background: var(--card-bg); -webkit-tap-highlight-color: transparent;
    box-shadow: 0 10px 24px -20px rgba(28,32,30,.5); transition: transform .15s, box-shadow .15s; }}
  .mt:active {{ transform: scale(.98); }}
  .mt:focus-visible {{ outline: 2px solid var(--bone); outline-offset: 2px; }}
  .mt-head {{ display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 6px; }}
  .mt-gh {{ display: inline-flex; align-items: center; justify-self: start; align-self: flex-start; gap: 5px; padding: 5px 9px; border: 1px solid rgba(28,32,30,.35);
    border-radius: 999px; background: rgba(255,255,255,.7); font: 600 11px/1 var(--font-mono); color: var(--bone); text-decoration: none; }}
  .mt-gh svg {{ width: 13px; height: 13px; flex: none; fill: var(--bone); }}
  .mt-ghi {{ display: inline-flex; align-items: center; justify-content: center; flex: none; width: 20px; height: 20px; margin-left: 1px;
    border: 1px solid rgba(28,32,30,.3); border-radius: 50%; background: rgba(255,255,255,.75); }}
  .mt-ghi svg {{ width: 12px; height: 12px; fill: var(--bone); }}
  .mt-row.kit > span {{ display: inline-flex; align-items: center; gap: 3px; }}
  .mt-row.kit {{ gap: 4px; }}
  .mt-adv {{ border-color: rgba(217,68,31,.5); background: linear-gradient(160deg, rgba(217,68,31,.08), rgba(217,68,31,.015)), var(--card-bg); }}
  .mt-kit {{ border-color: rgba(154,107,47,.45); }}
  .mt-icode {{ grid-column: 1 / -1; border-color: rgba(46,139,110,.5); background: linear-gradient(160deg, rgba(46,139,110,.07), rgba(46,139,110,.01)), var(--card-bg); }}
  .mt-name {{ font: 600 12px/1.3 var(--font-mono); letter-spacing: .1em; text-transform: uppercase; color: var(--bone); }}
  .mt-name.hot {{ color: var(--cinnabar); }} .mt-name.sand {{ color: var(--sand); }} .mt-name.jade {{ color: var(--jade); }}
  .mt-sub {{ font: 400 12px/1.3 var(--font-display); color: var(--bone-dim); }}
  .mt-rows {{ display: grid; gap: 4px; margin-top: 2px; }}
  .mt-row {{ display: flex; align-items: center; justify-content: space-between; gap: 6px; }}
  .mt-row b {{ display: inline-flex; align-items: center; gap: 4px; font: 700 15px/1.2 var(--font-display); }}
  .mt-row i {{ font: 700 15px/1.2 var(--font-display); font-style: normal; color: var(--jade); }}
  .mt-row.hot i {{ color: var(--bone); }}
  .mt-medal svg {{ width: 15px; height: 15px; color: #C9961A; display: block; }}
  .mt-row.kit span {{ font: 500 12.5px/1.25 var(--font-display); }}
  .mt-row .dot {{ flex: none; width: 9px; height: 9px; border-radius: 50%; }}
  .mt-row .dot.ok {{ background: var(--jade); }}
  .mt-row .dot.soon, .mt-row .dot.wip {{ border: 1.5px dashed rgba(28,32,30,.5); }}
  .mt-legend {{ display: flex; flex-wrap: wrap; align-items: center; gap: 3px 10px; font: 500 10.5px/1.3 var(--font-mono); color: var(--bone-dim); }}
  .mt-legend .dot {{ display: inline-block; width: 8px; height: 8px; border-radius: 50%; }}
  .mt-legend .dot.ok {{ background: var(--jade); }} .mt-legend .dot.soon {{ border: 1.5px dashed rgba(28,32,30,.5); }}
  .mt-legend > span {{ display: inline-flex; align-items: center; gap: 5px; white-space: nowrap; }}
  .mt-foot {{ font: 500 10.5px/1.3 var(--font-mono); color: var(--bone-dim); }}
  .mt-more {{ margin-top: auto; padding-top: 6px; font: 600 11px/1 var(--font-mono); letter-spacing: .04em; color: var(--bone-dim); }}
  .mt-more::after {{ content: " →"; }}
  .mt-shot img {{ display: block; width: 100%; height: auto; border-radius: 6px; border: 1px solid rgba(28,32,30,.12); }}
  .mt-one {{ font: 700 17px/1.25 var(--font-display); }}
  .mt-one span {{ color: var(--jade); }}
  .mt-priv {{ display: inline-flex; align-self: flex-start; align-items: center; gap: 8px; padding: 6px 10px; border-radius: 6px; background: var(--jade); color: #FBF9F4; }}
  .mt-priv svg {{ width: 15px; height: 15px; fill: #FBF9F4; }}
  .mt-priv b {{ font: 800 13px/1 var(--font-display); }}
  .mmap .mflow {{ height: 46px; }}
  .mmap .mflow.down:not(.hot)::after {{ border-top-color: var(--sand); }}
  /* full-screen detail sheets */
  .msheet {{ position: fixed; inset: 0; z-index: 50; overflow-y: auto; padding: 0 16px 28px; background: var(--page-bg);
    transform: translateY(100%); visibility: hidden; transition: transform .28s ease, visibility 0s linear .28s; -webkit-overflow-scrolling: touch; }}
  .msheet.open {{ transform: none; visibility: visible; transition: transform .28s ease; }}
  .msheet > .mcard {{ max-width: 640px; margin: 0 auto; }}
  .msheet-bar {{ position: sticky; top: 0; z-index: 1; display: flex; justify-content: flex-end; max-width: 640px; margin: 0 auto; padding: 12px 0; background: var(--page-bg); }}
  .msheet-x {{ padding: 8px 12px; border: 1px solid #CFC7B6; border-radius: 6px; background: var(--card-bg); font: 600 12px/1 var(--font-mono); color: var(--bone); cursor: pointer; }}
  html.m-lock, html.m-lock body {{ overflow: hidden; }}
}}
@media (max-width: 400px) {{ .m-icode .ifeat {{ grid-template-columns: 1fr; }} }}
@media (max-width: 900px) and (prefers-reduced-motion: reduce) {{ .msheet, .msheet.open {{ transition: none; }} }}
</style>
<script>
(function () {{
  var vp = document.querySelector('.deck-viewport'), st = document.getElementById('deckStage');
  function fit() {{ var s = vp.clientWidth / {VIEW_W}; st.style.transform = 'scale(' + s + ') translate(-{CROP_X}px, -{CROP_Y}px)'; }}
  window.addEventListener('resize', fit); fit();
  // phone overview: tap a tile to open its full-screen sheet; Close / Esc / Back closes it
  var openSheet = null;
  function show(id, push) {{
    var el = document.getElementById(id); if (!el) return;
    openSheet = el; el.classList.add('open'); el.scrollTop = 0; document.documentElement.classList.add('m-lock');
    el.querySelector('.msheet-x').focus({{ preventScroll: true }});
    if (push) history.pushState({{ sheet: id }}, '');
  }}
  function hide() {{
    if (!openSheet) return;
    var id = openSheet.id; openSheet.classList.remove('open'); openSheet = null;
    document.documentElement.classList.remove('m-lock');
    var t = document.querySelector('.mt[data-sheet="' + id + '"]'); if (t) t.focus({{ preventScroll: true }});
  }}
  document.querySelectorAll('.mt[data-sheet]').forEach(function (t) {{
    t.addEventListener('click', function (e) {{ if (e.target.closest('a')) return; show(t.getAttribute('data-sheet'), true); }});
    t.addEventListener('keydown', function (e) {{
      if (e.target !== t || (e.key !== 'Enter' && e.key !== ' ')) return;
      e.preventDefault(); show(t.getAttribute('data-sheet'), true);
    }});
  }});
  document.querySelectorAll('.msheet-x').forEach(function (b) {{
    b.addEventListener('click', function () {{ if (history.state && history.state.sheet) history.back(); else hide(); }});
  }});
  window.addEventListener('popstate', hide);
  document.addEventListener('keydown', function (e) {{ if (e.key === 'Escape' && openSheet) {{ if (history.state && history.state.sheet) history.back(); else hide(); }} }});
}})();
</script>
'''
    body = body.replace("</body>", extra + "</body>", 1)
    return head + body


OUT.mkdir(parents=True, exist_ok=True)
(OUT / "index.html").write_text(build("en"))
(OUT / "index.zh.html").write_text(build("zh"))
print("built", OUT)
