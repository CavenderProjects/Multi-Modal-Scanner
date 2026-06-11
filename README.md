# Multi-Modal Vulnerability Scanner

> A regulated-environment security assessment platform built and maintained by a senior information security professional with 20 years of GRC and security management experience across financial services, healthcare, and real estate.

---

## Two Versions

| Version | Repo | What It Is |
|---------|------|------------|
| **Claude Code Skill** | [Multi-Modal-Scanner](https://github.com/CavenderProjects/Multi-Modal-Scanner) | AI-augmented assessment workflows inside Claude Code — install once, runs wherever Claude Code runs |
| **Standalone App** | [Multi-Modal-Scanner_Standalone](https://github.com/CavenderProjects/Multi-Modal-Scanner_Standalone) | Full PyQt6 desktop application — runs independently, no Claude Code required, persistent scan history, offline capable |

Both versions share the core controls libraries (website/agent, API, code review, interconnected), compliance framework mappings, and report format. The standalone app is the production-ready version of the scanner with a full GUI, database-backed scan history, and an interactive report review interface.

---

## What This Does

Across both versions the platform provides **seven assessment workflows**:

- **Website Vulnerability Assessment** — Evaluates web applications against 67 controls across 13 families
- **AI Agent Assessment** — Evaluates Claude skills, OpenAI GPTs, MCP servers, LangChain/LangGraph apps, Bedrock agents, and other AI agents against the same controls library, identifying risks specific to AI-augmented workflows *(both versions)*
- **API Vulnerability Assessment** — Tests APIs against OWASP API Security Top 10 and 53 controls across 17 families, covering authentication, authorization, rate limiting, data exposure, and SSRF
- **Source Code Review** — Static analysis of codebases against 51 controls across 12 families covering security flaws, complexity risks, and development practice gaps
- **STIG Compliance Assessment** — Imports DISA STIG XCCDF files, parses rules into a structured controls library, and produces a compliance checklist report *(both versions)*
- **OS & Software Assessment** — Scans Windows/Linux hosts for patch compliance, EOL software, insecure services, and CVE exposure *(Standalone only)*
- **Connected Systems Assessment** — Correlates findings from two or more completed assessments to detect multi-step attack chains spanning connected systems, with CVSS re-scoring and reachability promotion analysis

Vulnerability assessment workflows (Website, AI Agent, API, Source Code, Connected Systems) produce **interactive HTML reports** with:
- CVSS v3.1 scoring and vector strings
- Severity pill filters (multi-select: Critical / High / Medium / Low)
- Status filters (Compliant / Needs Review / Suppressed)
- Expandable finding cards with evidence, remediation, and review procedures
- Per-control triage actions: Confirm / Mark Compliant / Suppress as False Positive
- Expandable **Review Procedure** for every Needs Review finding — specific numbered steps tailored to the control
- Report save with original filename + timestamp preserved

The **STIG Compliance Assessment** produces a separate checklist report in CAT I/II/III severity format. The **Standalone App** supports prior report import to carry forward false positive decisions and notes across reassessments.

---

## Compliance Framework Coverage

Every finding is cross-referenced against **12+ compliance and regulatory frameworks**:

| Framework | Coverage |
|-----------|----------|
| OWASP Top 10 (2025) | All workflows |
| NIST SP 800-53 Rev 5 | All workflows |
| ISO/IEC 27001:2022 | All workflows |
| PCI-DSS v4.0.1 | All workflows |
| SOC 2 Type II | All workflows |
| HIPAA Security Rule | All workflows |
| CMMC v2.0 Level 2 | All workflows |
| DoD Cloud SRG | All workflows |
| FedRAMP Moderate | All workflows |
| SEC/FINRA | All workflows |
| EU DORA | All workflows |
| EU AI Act | All workflows |

---

## Why It Exists

Security assessments generate noise. Regulated environments generate liability. After 11 years managing GRC programs across financial services, healthcare, and real estate, I built this to structure what I was doing manually: running findings against compliance frameworks, flagging ambiguous results for explicit review, and producing reports that hold up when they surface in an audit or board-level discussion.

---

## Regulated Environment Considerations

### 1. False-Positive Risk
In regulated environments, a false positive isn't just wasted time — it can trigger unnecessary remediation spend, create misleading audit artifacts, or generate erroneous risk exceptions that become permanent record. Every finding with ambiguous scanner output is flagged for explicit manual review before being documented as confirmed.

### 2. Assessment Documentation
Any finding that may surface in an audit response, regulatory submission, or board-level risk report needs a clear record of: who assessed it, what context was applied, what compensating controls were considered, and what the final risk position is. Reports are structured for this and carry decisions forward across reassessment cycles.

### 3. Business-Constraint Remediation
Many findings in production regulated environments **cannot be remediated in isolation.** A vulnerability in a critical-care device, a legacy system under a multi-year vendor contract, or an integration a business unit depends on for revenue falls into this category. The tool supports suppression and false-positive documentation for findings where remediation isn't viable.

---

## Repository Structure

```
Multi-Modal-Scanner/
├── README.md
├── pen-tester/
│   ├── SKILL.md                                    # Claude Code skill definition
│   ├── assets/
│   │   ├── report-template.html                    # Website & AI Agent report template
│   │   ├── api-report-template.html                # API vulnerability report template
│   │   ├── code-review-report-template.html        # Source code review report template
│   │   ├── interconnected-report-template.html     # Connected systems report template
│   │   └── stig-report-template.html               # STIG checklist report template
│   ├── references/
│   │   ├── controls-library.md                     # 67 controls, 13 families (Website/Agent)
│   │   ├── api-controls-library.md                 # 53 controls, 17 families (API)
│   │   ├── code-review-controls.md                 # 51 controls, 12 families (Code Review)
│   │   ├── interconnected-controls.md              # 27 controls, 9 families (Connected)
│   │   └── os-software-controls.md                 # OS & software security controls
│   └── test-reports/                               # Sample generated reports
└── Multi-Modal-Scanner_Standalone/                 # → See standalone repo
    # Full PyQt6 desktop app — lives at:
    # https://github.com/CavenderProjects/Multi-Modal-Scanner_Standalone
```

---

## Standalone App

The standalone desktop application is maintained in a separate repository:
**[github.com/CavenderProjects/Multi-Modal-Scanner_Standalone](https://github.com/CavenderProjects/Multi-Modal-Scanner_Standalone)**

It is the full, independently deployable version of this scanner — no Claude Code, no API dependency. Designed for use in air-gapped or restricted environments where a Claude API connection is not available or not permitted.

Key differences from the Claude Code skill:

| Feature | Claude Code Skill | Standalone App |
|---------|-------------------|----------------|
| Runtime | Claude Code | Python + PyQt6 (desktop) |
| Internet required | Yes (Claude API) | No (local scan engine) |
| Scan history | Per session | SQLite database, persistent |
| Report triage | In report (browser) | In-app triage interface |
| AI Agent assessment | Yes | Yes |
| STIG import | Yes (XCCDF) | Yes (XCCDF) |
| OS & Software assessment | No | Yes |
| Prior report import | No | Yes (FP + notes carryover) |

---

## Limitations and Honest Caveats

This is a **workflow augmentation tool**, not an autonomous security assessment engine.

- It does not perform active network scanning, probing, or discovery against live systems
- Output requires review by a qualified security professional before use in any regulatory or audit context
- False-positive evaluation is only as good as the context provided
- It does not replace legal review for risk acceptance decisions with significant regulatory exposure

---

## Part of a Broader AI Governance Practice Portfolio

| Artifact | Status | Description |
|----------|--------|-------------|
| **Multi-Modal Vulnerability Scanner** (this repo) | Live | Regulated-environment security assessment platform — Claude Code skill + standalone app |
| **AI Risk Assessment Template** | In progress | Maps NIST AI RMF + ISO 42001 controls to GRC language enterprises already use |
| **AI Vendor Risk Questionnaire** | In progress | 25-question due diligence framework for evaluating third-party AI vendors |

---

## Background

**Christopher Cavender, CISSP, CCSP | IAPP AIGP (in progress)**

20 years in information security and GRC. Former Business Information Security Officer at Anywhere Real Estate (Fortune 500); 11 years managing security programs across financial services, healthcare, and real estate. Currently Information Systems Security Manager at Tripoint Solutions. NJ/NYC.

**Connect:** [LinkedIn](https://linkedin.com/in/christopher-cavender-cissp)

---

## Contributing

Contributions welcome, especially from practitioners working in regulated environments with specific HIPAA, NYDFS, PCI, EU AI Act, or other framework-specific context to add. Open an issue or submit a PR.

---

## License

MIT License. Use freely. Attribution appreciated but not required.

---

*Built 2026 · Part of an active AI governance practice portfolio*
