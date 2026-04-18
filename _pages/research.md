---
layout: page
permalink: /research/
title: research
description: Research map organized around the questions I am asking, not the papers I have written.
nav: true
nav_order: 1
---

<!-- _pages/research.md -->

<style>
  /* ============================================
     Layout
     ============================================ */
  .research-area {
    max-width: 980px;
    margin: 0 auto 3.5rem auto;
  }
  .page-narrative {
    max-width: 760px;
    margin: 0 auto 2.2rem auto;
    line-height: 1.65;
    color: var(--global-text-color);
  }

  /* ============================================
     Main box (thick border; title + questions + toggle)
     ============================================ */
  .main-box {
    border: 3px solid #7da0c4;
    border-radius: 8px;
    padding: 1rem 1.4rem 1.1rem 1.4rem;
    background: #f7fafd;
    max-width: 760px;
    margin: 0 auto;
    text-align: center;
  }
  .main-box h2 {
    margin: 0 0 0.6rem 0;
    font-size: 1.35rem;
    font-weight: 700;
    color: #1c2e4a;
  }
  .main-box .q {
    margin: 0.3rem auto;
    font-size: 1rem;
    color: #2c3e50;
    line-height: 1.45;
    max-width: 620px;
    text-align: left;
    padding-left: 1.9rem;
    text-indent: -1.9rem;
  }
  .main-box .q-num {
    font-weight: 700;
    color: #1c2e4a;
    margin-right: 0.35rem;
  }
  .main-box .toggle {
    display: inline-block;
    margin-top: 0.7rem;
    color: #1f5eb3;
    font-weight: 500;
    cursor: pointer;
  }
  .main-box .toggle:hover { text-decoration: underline; }

  /* ============================================
     Vertical arrow between boxes (arrowhead tip flush with bottom)
     ============================================ */
  .v-arrow {
    position: relative;
    width: 12px;
    height: 1.6rem;
    margin: 0 auto;
  }
  .v-arrow::before {
    content: '';
    position: absolute;
    top: 0;
    bottom: 6px;
    left: 50%;
    transform: translateX(-50%);
    width: 2px;
    background: #7da0c4;
  }
  .v-arrow::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 7px solid #7da0c4;
  }
  /* Variant: plain shaft (no arrowhead) — used when a v-arrow terminates at a
     trunk/line rather than a box. The real arrowheads live at the tick-to-box
     junctions below, one per sub-box. */
  .v-arrow.shaft {
    /* height stays 1.6rem; shaft fills full height, no head */
  }
  .v-arrow.shaft::before { bottom: 0; }
  .v-arrow.shaft::after { display: none; }

  /* ============================================
     Mid box (thin border; Empirical Understanding — horizontal expansion)
     ============================================ */
  .mid-box {
    border: 1px solid #9ab4cc;
    border-radius: 6px;
    padding: 0.7rem 1rem 0.85rem 1rem;
    background: #fff;
    max-width: 760px;
    margin: 0 auto;
    text-align: center;
  }
  .mid-box > b {
    color: #1c2e4a;
    font-size: 1rem;
  }
  .mid-box ul.content {
    list-style: none;
    padding: 0;
    margin: 0.55rem 0 0 0;
    display: none;
    font-size: 0.9rem;
    text-align: center;
  }
  .mid-box ul.content li {
    display: inline-block;
    margin: 0.25rem 0.8rem;
    vertical-align: top;
    line-height: 1.4;
    max-width: 320px;
    min-width: 240px;
  }

  /* ============================================
     Sub-boxes row with T-trunk
     ============================================ */
  .subs-row {
    display: grid;
    gap: 1.4rem;
    margin: 0 auto;
    padding-top: 1.2rem;   /* room for T-ticks above each sub-box */
    position: relative;
    max-width: 980px;
  }
  .subs-row.cols-3 { grid-template-columns: repeat(3, 1fr); }
  .subs-row.cols-4 { grid-template-columns: repeat(4, 1fr); }

  /* Horizontal trunk — computed so ends line up exactly with outer sub-box centers.
     top: 0 keeps trunk flush at the subs-row top edge, so v-arrow above lands on it. */
  .subs-row.cols-3::before {
    content: '';
    position: absolute;
    top: 0;
    left: calc((100% - 2 * 1.4rem) / 6);
    right: calc((100% - 2 * 1.4rem) / 6);
    height: 2px;
    background: #7da0c4;
  }
  .subs-row.cols-4::before {
    content: '';
    position: absolute;
    top: 0;
    left: calc((100% - 3 * 1.4rem) / 8);
    right: calc((100% - 3 * 1.4rem) / 8);
    height: 2px;
    background: #7da0c4;
  }

  /* Sub-box (thin border column) */
  .sub-box {
    position: relative;
    border: 1px solid #9ab4cc;
    border-radius: 6px;
    padding: 0.7rem 0.9rem 0.9rem 0.9rem;
    background: #fff;
  }
  .sub-box > b {
    color: #1c2e4a;
    font-size: 1rem;
    display: block;
  }

  /* Vertical tick from trunk down toward sub-box top */
  .sub-box::before {
    content: '';
    position: absolute;
    top: -1.2rem;
    left: calc(50% - 1px);
    width: 2px;
    height: 1.2rem;
    background: #7da0c4;
  }
  /* Arrowhead at the tick-to-box junction — every sub-box gets an arrow
     pointing into its top border (line-to-box intersection). */
  .sub-box::after {
    content: '';
    position: absolute;
    top: -7px;
    left: calc(50% - 5px);
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 7px solid #7da0c4;
  }

  /* Paper list (vertical, hidden by default) */
  .sub-box ul.content {
    list-style: none;
    padding-left: 0;
    margin: 0.55rem 0 0 0;
    font-size: 0.9rem;
    line-height: 1.5;
    display: none;
  }
  .sub-box ul.content li {
    margin: 0.45rem 0;
  }

  /* Code-name link + subtitle */
  a.proj, span.proj-na {
    color: #1f5eb3;
    text-decoration: none;
    font-weight: 600;
    white-space: nowrap;
  }
  a.proj:hover { text-decoration: underline; }
  span.proj-na {
    color: #666;
  }
  .proj-sub {
    display: block;
    color: #5b6775;
    font-size: 0.78rem;
    font-weight: 400;
    margin-top: 1px;
    line-height: 1.35;
    font-style: italic;
    white-space: normal;
  }

  /* ============================================
     Horizontal flow arrow (orange) — shaft + triangle tip as SVG
     sits exactly in the gap between two consecutive sub-boxes
     ============================================ */
  .flow-arrow {
    position: absolute;
    top: 1.05rem;          /* aligned with title baseline */
    right: -1.4rem;        /* right edge of span = left edge of next sub-box */
    width: 1.4rem;         /* spans the full gap */
    height: 10px;
    pointer-events: none;
    z-index: 2;
    display: block;
  }
  .flow-arrow svg {
    width: 100%;
    height: 100%;
    display: block;
  }

  /* "Coming soon" tag — results forthcoming, not a status flag on siblings */
  .tag-soon {
    display: inline-block;
    font-size: 0.72rem;
    padding: 1px 6px;
    border-radius: 3px;
    background: #ffe8d6;
    color: #8a3d00;
    margin-left: 4px;
    vertical-align: middle;
    font-weight: 500;
    font-style: italic;
  }

  /* Feedback-loop visual: wide curved arrow under the 3 sub-boxes, going from
     the rightmost box (Model & Loop Evolution) back to the leftmost box (Dev
     Implicit Knowledge Mining) — the literal data flywheel. */
  .feedback-loop {
    max-width: 980px;
    margin: 0 auto;
  }
  .feedback-loop > svg {
    display: block;
    width: 100%;
    height: 58px;
  }
  /* Loop-back note (text caption below the arrow) */
  .loop-note {
    text-align: center;
    font-size: 0.88rem;
    color: #e06b2a;
    font-style: italic;
    margin: 0.15rem 0 0 0;
  }

  /* ============================================
     Tabs (top-level: Vulnerability / AI Agent)
     ============================================ */
  .research-tabs { max-width: 980px; margin: 0 auto 2rem auto; }
  .tabs-nav {
    display: flex;
    gap: 0;
    border-bottom: 2px solid #c5d4e3;
    margin-bottom: 2rem;
  }
  .tab-btn {
    flex: 1;
    background: transparent;
    border: none;
    border-bottom: 3px solid transparent;
    margin-bottom: -2px;
    padding: 0.85rem 1.2rem;
    font-size: 1.02rem;
    font-weight: 600;
    color: var(--global-text-color-light);
    cursor: pointer;
    transition: color 0.15s, border-color 0.15s;
    text-align: center;
  }
  .tab-btn:hover { color: var(--global-theme-color); }
  .tab-btn.active {
    color: var(--global-theme-color);
    border-bottom-color: var(--global-theme-color);
  }
  .tab-panel { display: none; }
  .tab-panel.active { display: block; }

  /* ============================================
     Hero figure above the vuln narrative
     ============================================ */
  .vuln-hero {
    max-width: 760px;
    margin: 0 auto 1.6rem auto;
    text-align: center;
  }
  .vuln-hero img {
    width: 100%;
    height: auto;
    border-radius: 6px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.12);
  }
  .vuln-hero figcaption {
    font-style: italic;
    color: var(--global-text-color-light);
    font-size: 0.92rem;
    margin-top: 0.55rem;
    line-height: 1.4;
  }
  .vuln-hero .img-credit {
    display: block;
    font-size: 0.72rem;
    color: var(--global-text-color-light);
    opacity: 0.7;
    font-style: normal;
    margin-top: 0.2rem;
  }

  /* Mobile fallback: collapse to single column, drop all connectors */
  @media (max-width: 780px) {
    .subs-row.cols-4, .subs-row.cols-3 { grid-template-columns: 1fr; }
    .subs-row::before { display: none; }
    .sub-box::before { display: none; }
    .sub-box::after { display: none; }
    .flow-arrow { display: none; }
    .v-arrow { display: none; }
    .mid-box ul.content li { display: block; margin: 0.35rem 0; }
    .tabs-nav { flex-direction: column; }
    .tab-btn { text-align: left; }
  }
</style>

<!-- ================================================================== -->
<!-- Tabs: Vulnerability Management  |  AI Agents for SE                  -->
<!-- ================================================================== -->

<div class="research-tabs">
  <div class="tabs-nav">
    <button class="tab-btn active" data-tab="vuln" type="button">OSS Vulnerability Management</button>
    <button class="tab-btn" data-tab="lingxi" type="button">AI Agents for Software Engineering</button>
  </div>

<!-- ================================================================== -->
<!-- Tab 1: OSS Vulnerability Management                                  -->
<!-- ================================================================== -->

<div class="tab-panel active" id="tab-vuln">

<figure class="vuln-hero">
  <img src="/assets/img/VulnDisclosureLifecycle.png" alt="Conventional vs. proposed pre-emptive vulnerability patch cycles" />
  <figcaption><strong>My research focus:</strong> close the pre-disclosure window — act before the attacker.<span class="img-credit">Diagram generated with Gemini.</span></figcaption>
</figure>

<p class="page-narrative">
  Under coordinated vulnerability disclosure, a vulnerability is typically <em>silently fixed</em> on the public repository weeks before its CVE is published &mdash; and attackers can infer the vulnerability from those silent commits long before defenders hear about it. In the <strong>CVE-2018-11776</strong> Apache Struts remote-code-execution case, a silent fix sat in the public repo for about <strong>two months</strong> before public disclosure; this is the same class of exposure window that contributed to the 2017 <strong>Equifax breach</strong> (~147.9M records). Starting from our ASE'21 <em>VulFixMiner</em> paper, our research line has pioneered <strong>proactive vulnerability sensing</strong> &mdash; modeling silent fix commits as the first public, inevitable signal of a hidden vulnerability, covering <strong>65%</strong> of silent fixes <strong>1&ndash;2 weeks</strong> ahead of CVE disclosure.
</p>

<div class="research-area" id="vuln-area">

  <!-- Main box -->
  <div class="main-box">
    <h2>OSS Vulnerability Management</h2>
    <p class="q"><span class="q-num">Q1.</span> How can we detect a vulnerability <strong><em>before</em></strong> it is publicly disclosed?</p>
    <p class="q"><span class="q-num">Q2.</span> How do we manage that vulnerability with one hand tied behind our back &mdash; no public CVEs or advisories to draw on?</p>
    <a class="toggle" href="javascript:$('#vuln-area ul.content').slideToggle();">Show/Hide Work on Vulnerability Management</a>
  </div>

  <!-- Vertical arrow: OSS main box -> Empirical Understanding -->
  <div class="v-arrow"></div>

  <!-- Empirical Understanding (mid-box, horizontal paper expansion) -->
  <div class="mid-box" id="empirical-box">
    <b>Empirical Understanding</b>
    <ul class="content">
      <li>
        <a class="proj" href="/publications/#liu2025disclosure">[OSS Disclosure Management]</a>
        <span class="proj-sub">how OSS projects coordinate the private-to-public disclosure window</span>
      </li>
      <li>
        <a class="proj" href="/publications/#liu2025industrial2academia">[Industry to Academia]</a>
        <span class="proj-sub">mapping the gap between industrial vulnerability-management practice and academic research</span>
      </li>
    </ul>
  </div>

  <!-- Connector from Empirical down to the T-trunk (plain shaft — arrowheads live at the
       tick-to-box junctions below, one per sub-box). -->
  <div class="v-arrow shaft"></div>

  <!-- T-branch down to 3 lifecycle sub-boxes -->
  <div class="subs-row cols-3">

    <div class="sub-box">
      <b>Proactive Sensing</b>
      <ul class="content">
        <li>
          <a class="proj" href="/publications/#zhou2021finding">[VulFixMiner]</a>
          <span class="proj-sub">commit-only sensing, language-agnostic</span>
        </li>
        <li>
          <a class="proj" href="/publications/#zhou2023colefunda">[CoLeFunDa]</a>
          <span class="proj-sub">contrastive learning + data augmentation</span>
        </li>
        <li>
          <a class="proj" href="/publications/#wen2024taintfix">[TaintFix]</a>
          <span class="proj-sub">taint-propagation analysis</span>
        </li>
        <li>
          <a class="proj" href="/publications/#nguyen2023multi">[MGD]</a>
          <span class="proj-sub">multi-granularity hierarchical detector</span>
        </li>
        <li>
          <a class="proj" href="/publications/#xu2025llm4vulfix">[LLM4VulFix]</a>
          <span class="proj-sub">intention + dev artifacts + history</span>
        </li>
        <li>
          <a class="proj" href="/publications/#xu2025moe">[MoE-VulDet]</a>
          <span class="proj-sub">mixture-of-experts detection</span>
        </li>
        <li>
          <a class="proj" href="/publications/#sridharkumar2026protracted">[Lingering-Vul]</a>
          <span class="proj-sub">long-unfixed vulnerability detection</span>
        </li>
        <li>
          <a class="proj" href="/publications/#pan2022automated">[DIR]</a>
          <span class="proj-sub">dangerous issue-report mining</span>
        </li>
      </ul>
      <span class="flow-arrow" aria-hidden="true">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 22 10" preserveAspectRatio="xMidYMid meet">
          <line x1="0" y1="5" x2="14" y2="5" stroke="#e06b2a" stroke-width="2"/>
          <polygon points="14,1 22,5 14,9" fill="#e06b2a"/>
        </svg>
      </span>
    </div>

    <div class="sub-box">
      <b>Assessment</b>
      <ul class="content">
        <li>
          <a class="proj" href="/publications/#pan2024towards">[Auto-CVSS]</a>
          <span class="proj-sub">LLM-based CVSS scoring</span>
        </li>
        <li>
          <a class="proj" href="/publications/#pan2026eava">[EAVA]</a>
          <span class="proj-sub">evidence-augmented assessment</span>
        </li>
        <li>
          <a class="proj" href="/publications/#pan2024unveil">[CritVul]</a>
          <span class="proj-sub">criticality estimation</span>
        </li>
      </ul>
      <span class="flow-arrow" aria-hidden="true">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 22 10" preserveAspectRatio="xMidYMid meet">
          <line x1="0" y1="5" x2="14" y2="5" stroke="#e06b2a" stroke-width="2"/>
          <polygon points="14,1 22,5 14,9" fill="#e06b2a"/>
        </svg>
      </span>
    </div>

    <div class="sub-box">
      <b>Fix &amp; Validation</b>
      <ul class="content">
        <li>
          <a class="proj" href="/publications/#chen2026diffploit">[Diffploit]</a>
          <span class="proj-sub">cross-version exploit migration</span>
        </li>
        <li>
          <a class="proj" href="/publications/#pan2026mip">[PatchPort]</a>
          <span class="proj-sub">implicit-inconsistency-aware porting</span>
        </li>
        <li>
          <a class="proj" href="/publications/#tan2025similar">[SimPatch]</a>
          <span class="proj-sub">similar-but-patched code removal</span>
        </li>
        <li>
          <a class="proj" href="/publications/#Zhu2024APRInject">[APR-Inject]</a>
          <span class="proj-sub">automated repair for injections</span>
        </li>
      </ul>
    </div>

  </div>

</div>


</div> <!-- /#tab-vuln -->


<!-- ================================================================== -->
<!-- Tab 2: AI Agents for Software Engineering                            -->
<!-- ================================================================== -->

<div class="tab-panel" id="tab-lingxi">

<p class="page-narrative">
  A software-engineering agent is only as good as the <em>procedural knowledge</em> it can bring to bear &mdash; how this repository is structured, how its tests fail, how past developers navigated change. Our <strong>Lingxi</strong> agent framework mines that knowledge from historical development data and from its own trajectories, guiding the agent harness and feeding back into the underlying model. <strong>#1 on SWE-bench Verified (81.2%)</strong>, deployed across Huawei's internal product lines.
</p>

<div class="research-area" id="lingxi-area">

  <div class="main-box">
    <h2>AI Agents for Software Engineering</h2>
    <p class="q"><span class="q-num">Q1.</span> How do we build a software-engineering agent that handles real, repository-scale tasks?</p>
    <p class="q"><span class="q-num">Q2.</span> How does such an agent keep getting better &mdash; by mining knowledge from development history and its own trajectories?</p>
    <a class="toggle" href="javascript:$('#lingxi-area ul.content').slideToggle();">Show/Hide Work on Lingxi</a>
  </div>

  <!-- Connector from Lingxi main box down to the T-trunk (plain shaft — arrowheads
       live at each tick-to-box junction below). -->
  <div class="v-arrow shaft"></div>

  <div class="subs-row cols-3">

    <div class="sub-box">
      <b>Dev Implicit Knowledge Mining</b>
      <ul class="content">
        <li>
          <a class="proj" href="/publications/#yang2026lingxi">[Lingxi-Miner]</a>
          <span class="proj-sub">procedural knowledge from historical dev data</span>
        </li>
      </ul>
      <span class="flow-arrow" aria-hidden="true">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 22 10" preserveAspectRatio="xMidYMid meet">
          <line x1="0" y1="5" x2="14" y2="5" stroke="#e06b2a" stroke-width="2"/>
          <polygon points="14,1 22,5 14,9" fill="#e06b2a"/>
        </svg>
      </span>
    </div>

    <div class="sub-box">
      <b>Code Agent Harness</b>
      <ul class="content">
        <li>
          <a class="proj" href="https://github.com/lingxi-agent/Lingxi">[Lingxi-GH]</a>
          <span class="proj-sub">#1 on SWE-bench Verified (81.2%)</span>
        </li>
        <li>
          <a class="proj" href="https://github.com/lingxi-agent/Lingxi/blob/master/docs/Lingxi%20v2.0%20Technical%20Report%202026.pdf">[Lingxi-v2.0]</a>
          <span class="proj-sub">agent architecture technical report</span>
        </li>
      </ul>
      <span class="flow-arrow" aria-hidden="true">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 22 10" preserveAspectRatio="xMidYMid meet">
          <line x1="0" y1="5" x2="14" y2="5" stroke="#e06b2a" stroke-width="2"/>
          <polygon points="14,1 22,5 14,9" fill="#e06b2a"/>
        </svg>
      </span>
    </div>

    <div class="sub-box">
      <b>Model &amp; Loop Evolution <span class="tag-soon">results coming soon</span></b>
      <ul class="content">
        <li>
          <span class="proj-na">[Traj-Evolver]</span>
          <span class="proj-sub">trajectories &rarr; harness + model updates</span>
        </li>
      </ul>
    </div>

  </div>

  <div class="feedback-loop">
    <svg viewBox="0 0 1000 70" preserveAspectRatio="none" aria-hidden="true">
      <!-- Curve from bottom-center of the rightmost sub-box, dipping down, up to
           bottom-center of the leftmost sub-box -->
      <path d="M 833 4 C 833 68 167 68 167 17"
            stroke="#e06b2a" stroke-width="2.5" fill="none" stroke-linecap="round" />
      <!-- Arrowhead tip pointing up, into the bottom border of the leftmost sub-box -->
      <polygon points="159,17 167,2 175,17" fill="#e06b2a" />
    </svg>
    <p class="loop-note">
      evolved knowledge feeds back into Dev Implicit Knowledge Mining &mdash; closing the data flywheel.
    </p>
  </div>

</div> <!-- /#lingxi-area -->

</div> <!-- /#tab-lingxi -->

</div> <!-- /.research-tabs -->

<script>
  document.addEventListener('DOMContentLoaded', function() {
    function activateTab(tabId) {
      var btn = document.querySelector('.tab-btn[data-tab="' + tabId + '"]');
      var panel = document.getElementById('tab-' + tabId);
      if (!btn || !panel) return false;
      document.querySelectorAll('.tab-btn').forEach(function(b) { b.classList.remove('active'); });
      document.querySelectorAll('.tab-panel').forEach(function(p) { p.classList.remove('active'); });
      btn.classList.add('active');
      panel.classList.add('active');
      return true;
    }

    // Click: switch tab + update URL hash so the state is shareable / back-button-navigable
    document.querySelectorAll('.tab-btn').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var tabId = this.dataset.tab;
        if (activateTab(tabId)) {
          history.replaceState(null, '', '#' + tabId);
        }
      });
    });

    // On load and on hashchange: sync tab state from URL (#vuln or #lingxi)
    function syncFromHash() {
      var hash = window.location.hash.substring(1);
      if (hash) activateTab(hash);
    }
    syncFromHash();
    window.addEventListener('hashchange', syncFromHash);
  });
</script>
