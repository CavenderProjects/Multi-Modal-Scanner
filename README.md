# AI-Augmented Pen Test Triage: Claude Code Skill

> A Claude Code skill that augments penetration testing and vulnerability assessment workflows in regulated environments. Built and maintained by a senior information security professional with 20 years of GRC and security management experience across financial services, healthcare, and real estate.

---

## What This Does

Security assessments generate noise. Regulated environments generate liability. This skill bridges both.

It provides **four assessment workflows** covering the full spectrum of security analysis:

- **Website Vulnerability Assessment** — Evaluates web applications against OWASP Top 10 2021 and 63 controls across 13 families, producing interactive dark-theme reports with severity-filtered findings, expandable remediation cards, and exportable artifacts
- **Skill Vulnerability Assessment** — Applies the same rigorous analysis to Claude Code skills and AI-integrated tooling, identifying security risks specific to AI-augmented workflows
- **Source Code Review** — Static analysis of codebases against 51 controls across 12 families covering security flaws, complexity risks, and development practice gaps
- **API Vulnerability Assessment** — Tests APIs against OWASP API Security Top 10 (2023) and 53 controls across 17 families, covering authentication, authorization, rate limiting, data exposure, and more

All four workflows produce **interactive HTML reports** with severity toggles, expandable finding cards, radio-button mitigation selection, code artifacts, CIA Triad analysis, and a Review & Export modal for generating markdown summaries.

---

## Compliance Framework Coverage

Every finding is cross-referenced against **12+ compliance and regulatory frameworks**:

| Framework | Coverage |
|-----------|----------|
| OWASP Top 10 2021 | Website, Skill, Code Review |
| OWASP API Security Top 10 (2023) | API |
| NIST SP 800-53 Rev 5 | All workflows |
| ISO/IEC 27001:2022 | All workflows |
| CMMC 2.0 | All workflows |
| DoD SRG | All workflows |
| EU AI Act | All workflows |
| EU DORA | All workflows |
| FedRAMP 20x | All workflows |
| HIPAA Security Rule | All workflows |
| PCI-DSS v4.0 | All workflows |
| SEC/FINRA | All workflows |
| SOC 2 Type II | All workflows |

Reports include a **multi-select framework filter** allowing users to narrow findings to the frameworks relevant to their regulatory environment.

---

## Why It Exists

Standard pen test reports are written for engineers. They get handed to compliance teams, business leaders, and auditors who need to make risk decisions, fast, in language they can act on.

After 11 years managing GRC programs across industries where a misclassified finding can mean a HIPAA violation or a PCI audit failure, I built this skill to do what I was doing manually: translate technical security findings into business risk language without losing the technical accuracy that makes the translation credible.

It also addresses a gap I kept hitting in regulated environments: **most AI-assisted security tools have no concept of chain-of-custody**. When a finding is used in an audit response, a board presentation, or a regulatory submission, the trail from raw scanner output to final risk position needs to be defensible. This skill documents that trail.

---

## Regulated Environment Considerations

This skill was designed with three regulated-environment constraints that most security tooling ignores:

### 1. False-Positive Risk
In regulated environments, a false positive isn't just wasted time. It can trigger unnecessary remediation spend, create misleading audit artifacts, or generate erroneous risk exceptions that become permanent record. The skill prompts explicit false-positive evaluation before any finding is documented as confirmed.

### 2. Chain-of-Custody Documentation
Any finding that may surface in an audit response, regulatory submission, or board-level risk report needs a clear record of: who assessed it, what context was applied, what compensating controls were considered, and what the final risk position is. The skill produces output structured for this trail.

### 3. Business-Constraint Remediation
Many findings in production regulated environments **cannot be remediated in isolation.** A vulnerability in a critical-care device, a legacy system under a multi-year vendor contract, or an integration that a business unit depends on for revenue falls into this category. The skill handles the risk-acceptance workflow, not just the remediation workflow.

---

## Repository Structure

```
pen-test-triage/
├── README.md
├── pen-tester/
│   ├── SKILL.md                                    # Core skill definition (4 workflows)
│   ├── assets/
│   │   ├── report-template.html                    # Website & Skill report template
│   │   ├── api-report-template.html                # API vulnerability report template
│   │   └── code-review-report-template.html        # Source code review report template
│   └── references/
│       ├── controls-library.md                     # 63 controls, 13 families (Website/Skill)
│       ├── code-review-controls.md                 # 51 controls, 12 families (Code Review)
│       └── api-controls-library.md                 # 53 controls, 17 families (API)
├── sample-reports/
│   ├── Sample Website Vulnerability Report.html
│   ├── Sample Skill Vulnerability Report.html
│   ├── Sample Code Review Report.html
│   └── Sample API Vulnerability Report.html
└── test-targets/
    ├── sample-website/                             # Test target for website assessments
    └── vulnerable-skill/                           # Test target for skill assessments
```

---

## How to Use

### Prerequisites
- [Claude Code](https://docs.claude.ai/en/docs/claude-code/getting-started) installed
- Basic familiarity with running skills in Claude Code

### Installation

```bash
# Clone the repository
git clone https://github.com/CavenderProjects/pen-test-triage.git

# Copy the skill into your Claude Code skills directory
cp -r pen-test-triage/pen-tester ~/.claude/skills/pen-tester/
```

### Target Type Detection

The skill automatically detects the assessment type based on what you provide:

| Target | Workflow | Controls |
|--------|----------|----------|
| URL or web application | Website Vulnerability Assessment | 63 controls, 13 families |
| Claude Code skill (SKILL.md) | Skill Vulnerability Assessment | 63 controls, 13 families |
| Source code / repository | Source Code Review | 51 controls, 12 families |
| API endpoint or spec | API Vulnerability Assessment | 53 controls, 17 families |

### Example Input

```
Assess this API for security vulnerabilities: https://api.example.com/v2
Regulatory environment: HIPAA, PCI-DSS v4.0, SOC 2 Type II
```

### Report Features

Every report includes:
- **Severity toggle filters** (Critical / High / Medium / Low / Info)
- **Family and framework filter dropdowns** with multi-select
- **CIA Triad impact analysis** per finding
- **Expandable finding cards** with detailed descriptions, evidence, and remediation options
- **Radio-button mitigation selection** for choosing remediation approaches
- **Code artifacts** with copy/export functionality
- **Review & Export modal** for generating markdown assessment summaries
- **Dark theme** optimized for extended security review sessions

---

## Limitations and Honest Caveats

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
| **Pen Test Triage Skill** (this repo) | Live | Claude Code skill for regulated-environment security assessment augmentation |
| **AI Risk Assessment Template** | In progress | Maps NIST AI RMF + ISO 42001 controls to GRC framework language enterprises already use |
| **AI Vendor Risk Questionnaire** | In progress | 25-question due diligence framework for evaluating third-party AI vendors; fills the gap left by pre-2023 contracts with no AI clause |

The larger project addresses a specific gap: most AI governance content is written for either AI engineers (too technical for GRC teams) or compliance audiences (too theoretical for practitioners). These tools are built for the people who have to operationalize AI governance inside real organizations with real regulatory exposure.

---

## Background

**Christopher Cavender, CISSP, CCSP | IAPP AIGP (in progress)**

20 years in information security and GRC. Former Business Information Security Officer at Anywhere Real Estate (Fortune 500); 11 years managing security programs across financial services, healthcare, and real estate. Currently Information Systems Security Manager at Tripoint Solutions. NJ/NYC.

This skill emerged from a practical problem encountered repeatedly across regulated environments: AI tools being adopted into security workflows with no framework for evaluating false-positive risk, chain-of-custody implications, or regulatory exposure. Rather than write another policy about it, I built the tool.

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
