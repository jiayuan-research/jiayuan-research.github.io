---
layout: about
title: about
permalink: /
subtitle: 

  <p>jiayuan.zjy[at]gmail.com</p>

profile:
  align: left
  image: resume_photo.jpeg
  image_circular: false # crops the image to make it circular
  more_info: >
    <p>Toronto, Canada</p>

news: true # includes a list of news items
publications: true
selected_papers: false # includes a list of papers marked as "selected={true}"
social: false # includes social icons at the bottom of the page
---

<style>
  /* Tighten the top of the body column so the tagline sits aligned with the
     profile image's top edge. */
  .post > article > .clearfix > .tagline {
    margin-top: 0;
    margin-bottom: 0.75rem;
    font-style: italic;
    color: var(--global-text-color-light);
    font-size: 1rem;
    line-height: 1.4;
    padding-left: 0.8rem;
    border-left: 3px solid var(--global-divider-color);
  }
  /* After the "lines I lead" intro + bullets, break out of the float so the
     synthesis/background paragraphs go full-width under the profile, not in
     a narrow column beside empty space. */
  .post > article > .clearfix > .clear-float { clear: left; height: 0; }
</style>

<p class="tagline">Principal Researcher on AI agents for software engineering and vulnerability management.</p>

I am a **Principal Researcher** at **Huawei Canada**, leading a team across two complementary lines:

- **[AI agents for software engineering](/research/#lingxi).** Our **[Lingxi](https://github.com/lingxi-agent/Lingxi)** agent framework — **#1 on SWE-bench Verified** — mines knowledge from development data and agent trajectories to guide the agent harness and evolve the underlying models. Deployed across internal product lines at Huawei.
- **[OSS vulnerability management](/research/#vuln).** We pushed vulnerability defense from reactive CVE response to **proactive sensing** — detecting silent fix commits **1–2 weeks ahead of public disclosure** through large-scale code-change modeling.

<div class="clear-float"></div>

A common thread runs through both: **turning implicit, hard-to-observe signals in software development events into explicit systems that can act on them.**

I received my Ph.D. in Computer Science from the [SAIL lab](https://sailresearch.github.io/sail-website), Queen's University, under the supervision of [Prof. Ahmed E. Hassan](https://scholar.google.com/citations?user=9hwXx34AAAAJ) and [Prof. Shaowei Wang](https://sites.google.com/view/mambalab). My dissertation studied extrinsic incentives in open source communities through mining GitHub, Stack Overflow, and Bountysource data. Before grad school, I was the founding engineer of 1688's **One-Click Dropshipping (一件代发/一键代销)** system at **Alibaba Group** — a full-stack platform connecting B2B suppliers with millions of Taobao/Tmall merchants.

See [Research Highlights](/research/) for a deeper look at these research lines.

**Research interests:** AI agents for software engineering, procedural knowledge mining, agent memory, development-process knowledge, LLM-based code generation, vulnerability detection and management, mining software repositories.

**Publications:** 22 papers at **ICSE**, **FSE**, **ASE**, **ISSTA**, **IEEE TSE**, **ACM TOSEM**, and **EMSE** — see [google scholar](https://scholar.google.com/citations?hl=zh-CN&user=ySQkd5nCb0cC). I hold **12 patents** in software engineering and AI applications.

