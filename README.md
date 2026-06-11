# Multi-Modal-Scanner: Claude Code Skill

> A Claude Code skill that augments penetration testing and vulnerability assessment workflows in regulated environments. Built and maintained by a senior information security professional with 20 years of GRC and security management experience across financial services, healthcare, and real estate.

---

## What This Does

Security assessments generate noise. Regulated environments generate liability. This skill bridges both.

It provides **six assessment workflows**:

- **Website Vulnerability Assessment** — Evaluates web applications against 67 controls across 13 families, producing interactive dark-theme reports with severity-filtered findings, expandable remediation cards, and exportable artifacts
- **AI Agent Assessment** — Evaluates Claude skills, OpenAI GPTs, MCP servers, LangChain/LangGraph apps, CrewAI/AutoGen agents, Bedrock agents, Hugging Face Spaces, and Gemini Gems against the same controls library, identifying security risks specific to AI-augmented workflows
- **API Vulnerability Assessment** — Tests APIs against OWASP API Security Top 10 and 53 controls across 17 families, covering authentication, authorization, rate limiting, data exposure, and SSRF
- **Source Code Review** — Static analysis of codebases against 51 controls across 12 families covering security flaws, complexity risks, and development practice gaps
- **STIG Compliance Assessment** — Imports DISA STIG XCCDF files via `tools/stig_parser.py`, parses rules into a structured controls library, and produces a compliance checklist report
- **Connected Systems Assessment** — Correlates findings from two or more completed assessments to detect multi-step attack chains spanning connected systems, with CVSS re-scoring and reachability promotion analysis (27 controls across 9 families)

Vulnerability assessment workflows (Website, AI Agent, API, Source Code, Connected Systems) produce **interactive HTML reports** with CVSS v3.1 scoring, reachability ratings, severity toggles, compliance framework filters, expandable finding cards, radio-button mitigation selection, code artifacts, CIA Triad analysis, and a Review & Export modal for generating markdown/JSON remediation bundles. The **STIG Compliance Assessment** produces a separate checklist report in CAT I/II/III severity format.

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

Reports include a **multi-select framework filter** allowing users to narrow findings to the frameworks relevant to their regulatory environment.

---

## Why It Exists

Security assessments generate noise. Regulated environments generate liability. After 11 years managing GRC programs across financial services, healthcare, and real estate, I built this to structure what I was doing manually: running findings against compliance frameworks, flagging ambiguous results for explicit review, and producing reports that hold up when they surface in an audit or board-level discussion.

---

## Regulated Environment Considerations

This skill was designed with three regulated-environment constraints that most security tooling ignores:

### 1. False-Positive Risk
In regulated environments, a false positive isn't just wasted time. It can trigger unnecessary remediation spend, create misleading audit artifacts, or generate erroneous risk exceptions that become permanent record. The skill prompts explicit false-positive evaluation before any finding is documented as confirmed.

### 2. Assessment Documentation
Any finding that may surface in an audit response, regulatory submission, or board-level risk report needs a clear record of: who assessed it, what context was applied, what compensating controls were considered, and what the final risk position is. The skill produces output structured for this.

### 3. Business-Constraint Remediation
Many findings in production regulated environments **cannot be remediated in isolation.** A vulnerability in a critical-care device, a legacy system under a multi-year vendor contract, or an integration that a business unit depends on for revenue falls into this category. The skill supports suppression and false-positive documentation for findings where remediation isn't viable.

---

## Repository Structure

```
Multi-Modal-Scanner/
├── README.md
├── pen-tester/
│   ├── SKILL.md                                    # Core skill definition (6 workflows)
│   ├── assets/
│   │   ├── report-template.html                    # Website & AI Agent report template
│   │   ├── api-report-template.html                # API vulnerability report template
│   │   ├── code-review-report-template.html        # Source code review report template
│   │   ├── interconnected-report-template.html     # Connected systems correlation report
│   │   └── stig-report-template.html               # STIG compliance checklist report
│   ├── references/
│   │   ├── controls-library.md                     # 67 controls, 13 families (Website/Agent)
│   │   ├── api-controls-library.md                 # 53 controls, 17 families (API)
│   │   ├── code-review-controls.md                 # 51 controls, 12 families (Code Review)
│   │   └── interconnected-controls.md              # 27 controls, 9 families (Connected Systems)
│   └── tools/
│       └── stig_parser.py                          # STIG XCCDF parser
└── test-targets/
    ├── sample-website/                             # Test target for website assessments
    └── vulnerable-skill/                           # Test target for AI agent assessments
```

---

## How to Use

### Prerequisites
- [Claude Code](https://docs.claude.ai/en/docs/claude-code/getting-started) installed
- Basic familiarity with running skills in Claude Code

### Installation

```bash
# Clone the repository
git clone https://github.com/CavenderProjects/Multi-Modal-Scanner.git

# Copy the skill into your Claude Code skills directory
cp -r Multi-Modal-Scanner/pen-tester ~/.claude/skills/pen-tester/
```

### Target Type Detection

The skill automatically detects the assessment type based on what you provide:

| Target | Workflow | Controls |
|--------|----------|----------|
| URL or web application | Website Vulnerability Assessment | 67 controls, 13 families |
| AI agent (Claude skill, GPT, MCP server, etc.) | AI Agent Assessment | 67 controls, 13 families |
| API endpoint or spec | API Vulnerability Assessment | 53 controls, 17 families |
| Source code / repository | Source Code Review | 51 controls, 12 families |
| STIG XCCDF XML file | STIG Compliance Assessment | Auto-generated from STIG rules |
| 2+ completed assessments | Connected Systems Assessment | 27 controls, 9 families |

### Example Input

```
Assess this API for security vulnerabilities: https://api.example.com/v2
Regulatory environment: HIPAA, PCI-DSS v4.0, SOC 2 Type II
```

### Report Features

Every report includes:
- **CVSS v3.1 scoring** with numeric score, severity label, vector string, and progress bar per finding
- **Reachability ratings** (Direct, One Hop, Multi-Step, Internal) with toggle filters
- **Severity toggle filters** (Critical / High / Medium / Low / Info)
- **12 compliance framework filter** with multi-select dropdown
- **CIA Triad impact analysis** per finding
- **Expandable finding cards** with detailed descriptions, evidence, and remediation options
- **Radio-button mitigation selection** for choosing remediation approaches
- **Code artifacts** with preview, copy, and export functionality
- **Review & Export modal** for generating Markdown or JSON remediation bundles
- **Dark theme** optimized for extended security review sessions

The Connected Systems report adds:
- **Chained Vulnerabilities** — multi-step attack chains with step-by-step flow visualization and system badges
- **Compounded Risk** — re-scored findings with original vs. new CVSS side by side
- **Collapsible section headings** with live counts that update with filters

---

## Limitations and Caveats

This is a **workflow augmentation tool**, not an autonomous security assessment engine.

- It does not perform scanning, probing, or discovery. It assists with the triage and documentation of findings already identified by the assessor
- Output requires review by a qualified security professional before use in any regulatory or audit context
- False-positive evaluation is only as good as the context provided (garbage in, garbage out)
- It does not replace legal review for risk acceptance decisions with significant regulatory exposure

---

## Part of a Broader AI Governance Practice Portfolio

This skill is the first published artifact in a broader AI governance project portfolio being built in 2026.

| Artifact | Status | Description |
|----------|--------|-------------|
| **Multi-Modal-Scanner** (this repo) | Live | Claude Code skill for regulated-environment security assessment augmentation |
| **AI Risk Assessment Template** | In progress | Maps NIST AI RMF + ISO 42001 controls to GRC framework language enterprises already use |
| **AI Vendor Risk Questionnaire** | In progress | 25-question due diligence framework for evaluating third-party AI vendors; fills the gap left by pre-2023 contracts with no AI clause |

The larger project addresses a specific gap: most AI governance content is written for either AI engineers (too technical for GRC teams) or compliance audiences (too theoretical for practitioners). These tools are built for the people who have to operationalize AI governance inside real organizations with real regulatory exposure.

---

## Background

**Christopher Cavender, CISSP, CCSP | IAPP AIGP (in progress)**

20 years in information security and GRC. Former Business Information Security Officer at Anywhere Real Estate (Fortune 500); 11 years managing security programs across financial services, healthcare, and real estate. Currently Information Systems Security Manager at Tripoint Solutions. NJ/NYC.

This skill emerged from a practical problem encountered repeatedly across regulated environments: AI tools being adopted into security workflows with no framework for evaluating false-positive risk, defensible documentation, or regulatory exposure. Rather than write another policy about it, I built the tool.

**Connect:** [LinkedIn](https://linkedin.com/in/christopher-cavender-cissp) · [AI Risk Assessment Template repo](https://github.com/CavenderProjects/ai-risk-assessment-template) *(coming)*

---

## Contributing

Contributions welcome, especially from practitioners working in regulated environments with specific HIPAA, NYDFS, PCI, EU AI Act, or other framework-specific context to add. Open an issue or submit a PR.

---

## License

MIT License. Use freely. Attribution appreciated but not required.

If you use this in a regulated environment and find something that needs fixing, please open an issue; that feedback directly improves the tool.

---

*Built May 2026 · Part of an active AI governance practice portfolio*
