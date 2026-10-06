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
  /* Narrow the profile column slightly and widen the gap between the photo
     and the body text so the two columns breathe. */
  @media (min-width: 576px) {
    .post > article > .profile { width: 26%; }
    .post > article > .profile.float-left { margin-right: 2rem; }
  }
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
  /* Keep the two research-line bullets in the text column beside the photo,
     even where a bullet runs past the bottom of the floated image. */
  .post > article > .clearfix > ul { overflow: hidden; font-size: 0.95rem; line-height: 1.6; padding-left: 1.2rem; }
  .post > article > .clearfix > ul > li { margin-bottom: 0.7rem; }
  .post > article > .clearfix > ul > li > p { margin-bottom: 0.4rem; }
  /* The three experience sources: a compact, quieter sub-list. */
  .post > article > .clearfix > ul ul {
    list-style: none;
    padding-left: 0.9rem;
    margin: 0.3rem 0 0.5rem 0;
    border-left: 2px solid var(--global-divider-color);
    font-size: 0.9rem;
    line-height: 1.55;
  }
  .post > article > .clearfix > ul ul li { margin: 0.1rem 0; }
  .post > article > .clearfix .src { color: var(--global-text-color-light); }
  /* Tagline sits beside the name in the page header. */
  .post-header .name-row { display: flex; align-items: flex-end; flex-wrap: wrap; gap: 0.4rem 1.6rem; }
  .post-header .name-row .post-title { margin-bottom: 0; }
  .post-header .name-tagline {
    flex: 1 1 22rem; max-width: 34rem; margin: 0 0 0.45rem 0;
    font-style: italic; font-size: 1rem; line-height: 1.4; color: var(--global-text-color-light);
    padding-left: 0.8rem; border-left: 3px solid var(--global-divider-color);
  }
  .post > article .more { white-space: nowrap; font-size: 0.9em; font-weight: 500; }
  /* First paragraph of the bio starts level with the top of the photo. */
  .post > article > .clearfix > p:first-of-type { margin-top: 0; }
  /* Drop the photo by the line's top leading so its edge meets the cap height of the first line. */
  @media (min-width: 576px) { .post > article > .profile { margin-top: 6px; } }
</style>

I am a **Technical Expert** at the **Waterloo Research Center, Huawei Canada**. Every software artifact (e.g., commits, issues, agent trajectories) records what was done, but rarely why. My team learns the why and puts it to work:

- **[Process intelligence for coding agents](/research/#lingxi).** We mine historical issues, agent trajectories and test outcomes into constraints and guidance for the next run. Our work [Lingxi](/blog/lingxi/) received an ISSTA'26 *Distinguished Paper* award. <a class="more" href="/research/#lingxi">More details →</a>
- **[OSS vulnerability management](/research/#vuln).** **Proactive sensing**: detecting silent fix commits **1–2 weeks before public disclosure**, a window that LLM-built exploits now close in days. <a class="more" href="/research/#vuln">More details →</a>

<div class="clear-float"></div>

I received my Ph.D. in Computer Science from the [SAIL lab](https://sailresearch.github.io/sail-website), Queen's University, under the supervision of [Prof. Ahmed E. Hassan](https://scholar.google.com/citations?user=9hwXx34AAAAJ) and [Prof. Shaowei Wang](https://sites.google.com/view/mambalab). My dissertation studied extrinsic incentives in open source communities through mining GitHub, Stack Overflow, and Bountysource data. Before grad school, I was the founding engineer of 1688's One-Click Dropshipping (一键代销) system at **Alibaba Group** — a full-stack platform connecting B2B suppliers with millions of Taobao/Tmall merchants.

**Research interests:** AI agents for software engineering, experience and procedural knowledge mining, agent trajectory analysis, test-time scaling, agent evaluation, vulnerability detection and management, mining software repositories.

**Publications:** papers at **ICSE**, **FSE**, **ASE**, **ISSTA**, **IEEE TSE**, **ACM TOSEM**, and **EMSE** — see [publications](/publications/) and [google scholar](https://scholar.google.com/citations?hl=zh-CN&user=ySQkd5nCb0cC). I hold **12 patents** in software engineering and AI applications.

