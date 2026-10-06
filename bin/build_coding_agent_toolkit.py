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

SRC = Path.home() / "WorkSpace/Presentation/ISSTA26-Lingxi/decks/lingxi-issta2026-rev10-iCode-detailed.html"
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
]

MEDAL = ('<span class="award" title="ISSTA 2026 · ACM SIGSOFT Distinguished Paper Award">'
         '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 2h4l1.6 4.2L14.2 2h4l-3.4 8.1" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
         '<circle cx="12" cy="15.5" r="6" fill="currentColor"/><path d="M12 12.4l.95 1.95 2.15.31-1.55 1.51.37 2.13L12 17.3l-1.92 1 .37-2.13-1.55-1.51 2.15-.31z" fill="#fff"/></svg>'
         "<span>ISSTA'26<br>Distinguished Paper</span></span>")


def remap(t):
    for a, b in COLOR_MAP:
        t = t.replace(a, b).replace(a.lower(), b)
    return t


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
    body = body.replace("</main>\n</div>", "</main>\n</div>\n</div>", 1)

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
.elinks .plug, .elinks .lk {{ height: 44px; min-height: 44px; box-sizing: border-box; }}
html[lang="zh-Hans"] .slide {{ font-family: var(--font-display), "PingFang SC", "Hiragino Sans GB", "Noto Sans SC", "Microsoft YaHei", sans-serif; }}
html[lang="zh-Hans"] .tag, html[lang="zh-Hans"] .ec .src, html[lang="zh-Hans"] .flowpill, html[lang="zh-Hans"] .egh {{ text-transform: none; letter-spacing: .04em; }}
</style>
<script>
(function () {{
  var vp = document.querySelector('.deck-viewport'), st = document.getElementById('deckStage');
  function fit() {{ var s = vp.clientWidth / {VIEW_W}; st.style.transform = 'scale(' + s + ') translate(-{CROP_X}px, -{CROP_Y}px)'; }}
  window.addEventListener('resize', fit); fit();
}})();
</script>
'''
    body = body.replace("</body>", extra + "</body>", 1)
    return head + body


OUT.mkdir(parents=True, exist_ok=True)
(OUT / "index.html").write_text(build("en"))
(OUT / "index.zh.html").write_text(build("zh"))
print("built", OUT)
