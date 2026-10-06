---
title: "Archived: vulnerability-tab narrative (Struts / Equifax example)"
archived: 2026-10-06
note: Replaced on the research page by the July 2026 OpenAI / libheif case. Kept here for reuse; _drafts is not published.
---

<p class="page-narrative">
  Under coordinated vulnerability disclosure, a vulnerability is typically <em>silently fixed</em> on the public repository weeks before its CVE is published &mdash; and attackers can infer the vulnerability from those silent commits long before defenders hear about it. In the <strong>CVE-2018-11776</strong> Apache Struts remote-code-execution case, a silent fix sat in the public repo for about <strong>two months</strong> before public disclosure; this is the same class of exposure window that contributed to the 2017 <strong>Equifax breach</strong> (~147.9M records). Starting from our ASE'21 <em>VulFixMiner</em> paper, our research line has pioneered <strong>proactive vulnerability sensing</strong> &mdash; modeling silent fix commits as the first public, inevitable signal of a hidden vulnerability, covering <strong>65%</strong> of silent fixes <strong>1&ndash;2 weeks</strong> ahead of CVE disclosure.
</p>
