#!/usr/bin/env python3
"""Copy the project pages from ~/WorkSpace/Presentation into this site and
re-apply the homepage-only edits (public titles, BibTeX, links).

Run from the repo root:  python3 bin/sync_project_pages.py
"""
import re
import shutil
from pathlib import Path

PRES = Path.home() / "WorkSpace" / "Presentation"
SITE = Path(__file__).resolve().parent.parent
OUT = SITE / "blog"   # pages are published under /blog/<name>/

PAGES = {
    "lingxi": PRES / "ISSTA26-Lingxi" / "project-page",
    "stair": PRES / "Traj-exp paper" / "project-page",
    "testgrad": PRES / "TestGrad paper" / "project-page",
}

STAIR_ARXIV_TITLE = "Reusing Past Repairs Through Hierarchical Trajectory Abstraction for Coding Agents"
STAIR_SUBMITTED_TITLE = "Too Specific or Too Vague? Reusing Repair Recipes at Multiple Granularities"
STAIR_BIBTEX = """<pre><code>@misc{xu2026reusingpastrepairshierarchical,
  title         = {Reusing Past Repairs Through Hierarchical Trajectory
                   Abstraction for Coding Agents},
  author        = {Yisen Xu and Jiayuan Zhou and Ruiqi Pan and Tse-Hsun Chen},
  year          = {2026},
  eprint        = {2607.29658},
  archivePrefix = {arXiv},
  primaryClass  = {cs.SE},
  url           = {https://arxiv.org/abs/2607.29658}
}</code></pre>"""

TESTGRAD_SUBMITTED_TITLE = "Evolving Test Suites via Failure Pattern Momentum for SWE-Agent Ensemble"
TESTGRAD_PUBLIC_TITLE = "Evolving the test suite until it tells candidate patches apart"
TESTGRAD_PUBLIC_SHORT = "Test-based patch selection for SWE-agent ensembles"
TESTGRAD_PUBLIC_TITLE_ZH = "演化测试套件，直到它能区分候选补丁"
TESTGRAD_PUBLIC_SHORT_ZH = "面向 SWE 智能体集成、基于测试的补丁选择"

ADVISOR = "https://github.com/spine-se-lab/Lingxi-advisor"


def replace_once(s, old, new, page):
    if new in s and old not in s:
        return s  # already applied
    if s.count(old) != 1:
        raise SystemExit(f"[{page}] expected exactly one match for: {old[:70]!r}")
    return s.replace(old, new)


def replace_if_present(s, old, new):
    """For pages whose source may already carry the homepage wording."""
    return s.replace(old, new) if old in s else s


def patch_lingxi(s, lang):
    s = replace_if_present(s, '''          <a class="btn" href="#method">How it works</a>
        </div>
        <p class="hnote">Code · not yet public · Slides · after the talk</p>''', f'''          <a class="btn" href="{ADVISOR}" target="_blank" rel="noopener">Lingxi Advisor · code</a>
          <a class="btn" href="#method">How it works</a>
        </div>
        <p class="hnote">Slides · after the talk</p>''')
    s = replace_if_present(s, "In practice · Task Pattern Advisor</span>", "In practice · Lingxi Advisor</span>")
    s = replace_if_present(s, "Task Pattern Advisor (working name) brings the same idea into",
                     f'<a href="{ADVISOR}" target="_blank" rel="noopener">Lingxi Advisor</a> brings the same idea into')
    s = replace_if_present(s, "everyday coding agents. Works with iCode and OpenCode · in development.</p>",
                     'everyday coding agents. Works with <a href="https://github.com/openJiuwen-ai/iCode" target="_blank" rel="noopener">iCode</a> and OpenCode.</p>')
    s = replace_if_present(s, "<b>Disclaimer.</b> The plugin is driven by the paper's core idea but is <b>not the system evaluated in the",
                     "<b>Disclaimer.</b> Lingxi Advisor is a simplified reimplementation of the paper's method; it is <b>not the system evaluated in the")
    s = replace_if_present(s, "      paper. Repository and release details will be posted here.</p>",
                     f'''      paper. Installation, supported platforms and the differences from the research implementation are in the
      <a href="{ADVISOR}" target="_blank" rel="noopener">repository README</a>.</p>''')
    s = s.replace('<a href="mailto:jiayuan.zhou1@huawei.com">jiayuan.zhou1@huawei.com</a>',
                  '<a href="mailto:jiayuan.zjy@gmail.com">jiayuan.zjy@gmail.com</a>')
    return s


def patch_stair(s, lang):
    if lang == "en":
        s = re.sub(r"<title>STAIR · [^<]*</title>", f"<title>STAIR · {STAIR_ARXIV_TITLE}</title>", s)
    s = s.replace(STAIR_SUBMITTED_TITLE, STAIR_ARXIV_TITLE)
    s = re.sub(r"<pre><code>@misc\{xu2026[a-z]*,.*?\}</code></pre>", lambda m: STAIR_BIBTEX, s, flags=re.S)
    if STAIR_ARXIV_TITLE not in s or "primaryClass" not in s:
        raise SystemExit("[stair] title or BibTeX patch did not apply")
    return s


def patch_testgrad(s, lang):
    title, short = (TESTGRAD_PUBLIC_TITLE, TESTGRAD_PUBLIC_SHORT) if lang == "en" else (TESTGRAD_PUBLIC_TITLE_ZH, TESTGRAD_PUBLIC_SHORT_ZH)
    if lang == "en":
        s = re.sub(r"<title>TestGRAD · [^<]*</title>", f"<title>TestGRAD · {short}</title>", s)
    s = s.replace(f'content="TestGRAD: {TESTGRAD_SUBMITTED_TITLE}"', f'content="TestGRAD · {short}"')
    s = s.replace(f'<p class="ptitle">{TESTGRAD_SUBMITTED_TITLE}</p>', f'<p class="ptitle">{title}</p>')
    s = s.replace(f"<b>TestGRAD</b> · {TESTGRAD_SUBMITTED_TITLE}.", f"<b>TestGRAD</b> · {short}.")
    # The paper is under review with no public version: no BibTeX with its title.
    s = re.sub(r'<div class="prose"><p>[^<]*</p></div>\s*</div>\s*<div class="bib reveal">.*?</code></pre>\s*</div>',
               '<div class="prose"><p>' + ('The paper is under review. Citation details will be added when it is public.' if lang == 'en' else '论文正在审稿中，公开后补充引用信息。') + '</p></div>\n    </div>',
               s, flags=re.S)
    if "Failure Pattern Momentum for SWE" in s or "@misc{testgrad" in s:
        raise SystemExit("[testgrad] submitted title or BibTeX still present")
    return s


PATCHES = {"lingxi": patch_lingxi, "stair": patch_stair, "testgrad": patch_testgrad}

for name, src in PAGES.items():
    dst = OUT / name
    dst.mkdir(parents=True, exist_ok=True)
    if (dst / "assets").exists():
        shutil.rmtree(dst / "assets")
    shutil.copytree(src / "assets", dst / "assets")
    for fname, lang in (("index.html", "en"), ("index.zh.html", "zh")):
        if (src / fname).exists():
            (dst / fname).write_text(PATCHES[name]((src / fname).read_text(), lang))
    print(f"synced {name} <- {src}")
