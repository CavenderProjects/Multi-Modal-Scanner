# API Security Controls Library

## Overview

This library contains 53 security controls organized into 17 control families, purpose-built for API vulnerability assessment. Each control includes a unique ID, control name, family, CIA triad classification, framework mappings, control statement, default severity if non-compliant, and a test approach.

Controls are derived from the OWASP API Security Top 10 (2023), NIST SP 800-53 Rev 5, ISO/IEC 27001:2022, and industry best practices from 42Crunch, Salt Security, and PortSwigger research.

## Framework References

| Abbreviation | Framework | Version | Scope |
|---|---|---|---|
| OWASP-API | OWASP API Security Top 10 | 2023 | API-specific security risks |
| OWASP | OWASP Top 10 | 2021 | Web application security — universal |
| NIST-800 | NIST SP 800-53 | Rev 5 | Federal/enterprise security controls |
| ISO-27001 | ISO/IEC 27001 | 2022 | Information security management |
| CMMC | CMMC 2.0 | Level 2 (2023) | DoD cybersecurity maturity — 110 practices from NIST 800-171 |
| DoD-SRG | DoD Cloud Computing SRG | v1r4 (2024) | Department of Defense cloud security requirements |
| EU-AI | EU AI Act | Reg (EU) 2024/1689 | Risk-based regulation for AI systems |
| EU-DORA | EU DORA | Reg (EU) 2022/2554 | Digital operational resilience for financial entities |
| FedRAMP | FedRAMP | Rev 5 Baselines (2024) | Federal cloud security — NIST 800-53 baselines |
| HIPAA | HIPAA Security Rule | 45 CFR §164 | Healthcare data protection requirements |
| PCI-DSS | PCI-DSS | v4.0.1 (2024) | Payment card industry data security standard |
| SEC-FINRA | SEC/FINRA | Reg S-P, Cyber Rule (2023) | Securities industry cybersecurity requirements |
| SOC2 | SOC 2 Type II | TSC 2022 | AICPA Trust Services Criteria |

### OWASP API Security Top 10 (2023) — Quick Reference
- API1:2023 — Broken Object Level Authorization (BOLA)
- API2:2023 — Broken Authentication
- API3:2023 — Broken Object Property Level Authorization (BOPLA)
- API4:2023 — Unrestricted Resource Consumption
- API5:2023 — Broken Function Level Authorization
- API6:2023 — Unrestricted Access to Sensitive Business Flows
- API7:2023 — Server-Side Request Forgery (SSRF)
- API8:2023 — Security Misconfiguration
- API9:2023 — Improper Inventory Management
- API10:2023 — Unsafe Consumption of APIs

---

## BOLA — Broken Object Level Authorization

### BOLA-001
- **Name**: Object-Level Access Control
- **CIA**: C (Confidentiality)
- **Secondary**: I
- **OWASP-API**: API1:2023
- **NIST-800**: AC-3, AC-6
- **ISO-27001**: A.9.4.1
- **CMMC**: AC.L2-3.1.1, AC.L2-3.1.2; AC.L2-3.1.5, AC.L2-3.1.6
- **DoD-SRG**: SRG-APP-000033, SRG-APP-000340; SRG-APP-000062, SRG-APP-000063
- **FedRAMP**: AC-3 (Moderate); AC-6 (Moderate)
- **HIPAA**: §164.312(a)(1) — Access Control
- **PCI-DSS**: Req 7.2 — Restrict access by need-to-know; Req 7.2.1 — Least privilege access
- **SOC2**: CC6.1 — Logical and physical access; CC6.3 — Least privilege access
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(c) — Access control policies; Art. 9(4)(c) — Least privilege
- **EU-AI**: Art. 15(4) — Cybersecurity (access control); Art. 15(4) — Cybersecurity (access restriction)
- **Severity**: CRITICAL
- **Statement**: Every API endpoint that receives an object ID shall verify that the authenticated user has permission to access that specific object before returning data or performing actions.
- **Test**: Authenticate as User A, capture a request containing an object ID (e.g., /api/orders/123). Replace the ID with an object belonging to User B (e.g., /api/orders/456). If User A can access User B's object, the control fails.

### BOLA-002
- **Name**: Predictable Identifier Enumeration
- **CIA**: C
- **OWASP-API**: API1:2023
- **NIST-800**: AC-3
- **ISO-27001**: A.9.4.1
- **CMMC**: AC.L2-3.1.1, AC.L2-3.1.2
- **DoD-SRG**: SRG-APP-000033, SRG-APP-000340
- **FedRAMP**: AC-3 (Moderate)
- **HIPAA**: §164.312(a)(1) — Access Control
- **PCI-DSS**: Req 7.2 — Restrict access by need-to-know
- **SOC2**: CC6.1 — Logical and physical access
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(c) — Access control policies
- **EU-AI**: Art. 15(4) — Cybersecurity (access control)
- **Severity**: HIGH
- **Statement**: APIs shall use non-predictable identifiers (UUIDs, hashes) instead of sequential integers for resource references, or shall enforce strict authorization checks regardless of identifier format.
- **Test**: Examine API responses for sequential or predictable IDs (e.g., /api/users/1, /api/users/2). Attempt to enumerate resources by incrementing IDs. If resources are returned without authorization checks, the control fails.

### BOLA-003
- **Name**: Batch/Bulk Endpoint Authorization
- **CIA**: C, I
- **OWASP-API**: API1:2023
- **NIST-800**: AC-3
- **ISO-27001**: A.9.4.1
- **CMMC**: AC.L2-3.1.1, AC.L2-3.1.2
- **DoD-SRG**: SRG-APP-000033, SRG-APP-000340
- **FedRAMP**: AC-3 (Moderate)
- **HIPAA**: §164.312(a)(1) — Access Control
- **PCI-DSS**: Req 7.2 — Restrict access by need-to-know
- **SOC2**: CC6.1 — Logical and physical access
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(c) — Access control policies
- **EU-AI**: Art. 15(4) — Cybersecurity (access control)
- **Severity**: HIGH
- **Statement**: Batch or bulk API endpoints (e.g., /api/users?ids=1,2,3) shall apply the same object-level authorization checks as single-object endpoints.
- **Test**: Send a batch request containing IDs from multiple users. Verify that only objects belonging to the authenticated user are returned.

---

## AUTH — API Authentication

### AUTH-001
- **Name**: Authentication Enforcement
- **CIA**: A (Accessibility)
- **Secondary**: C
- **OWASP-API**: API2:2023
- **NIST-800**: IA-2
- **ISO-27001**: A.9.4.2
- **CMMC**: IA.L2-3.5.1, IA.L2-3.5.2
- **DoD-SRG**: SRG-APP-000148, SRG-APP-000149
- **FedRAMP**: IA-2 (Low)
- **HIPAA**: §164.312(d) — Person or Entity Authentication
- **PCI-DSS**: Req 8.3 — Strong authentication for access
- **SOC2**: CC6.1 — Logical and physical access
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(c) — Authentication mechanisms
- **EU-AI**: Art. 15(4) — Cybersecurity (authentication)
- **Severity**: CRITICAL
- **Statement**: All API endpoints that access or modify protected resources shall require valid authentication credentials. Public endpoints shall be explicitly documented and minimized.
- **Test**: Send requests to all documented API endpoints without any authentication headers or tokens. Any endpoint that returns data or performs actions without credentials (and is not explicitly documented as public) represents a failure.

### AUTH-002
- **Name**: Token Security (JWT/OAuth)
- **CIA**: C
- **OWASP-API**: API2:2023
- **NIST-800**: IA-5, SC-12
- **ISO-27001**: A.9.2.4
- **CMMC**: IA.L2-3.5.7, IA.L2-3.5.8, IA.L2-3.5.9; SC.L2-3.13.10
- **DoD-SRG**: SRG-APP-000164, SRG-APP-000165; SRG-APP-000231
- **FedRAMP**: IA-5 (Low); SC-12 (Low)
- **HIPAA**: §164.312(d) — Person or Entity Authentication; §164.312(e)(2)(ii) — Encryption
- **PCI-DSS**: Req 8.3.6 — Password complexity requirements; Req 3.6 — Cryptographic key management
- **SOC2**: CC6.1 — Logical and physical access
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(c) — Authentication mechanisms; Art. 9(4)(d) — Cryptographic key management
- **EU-AI**: Art. 15(4) — Cybersecurity (credential security); Art. 15(4) — Cybersecurity (key management)
- **Severity**: CRITICAL
- **Statement**: API tokens (JWT, OAuth bearer tokens) shall use strong signing algorithms (RS256, ES256), shall have appropriate expiration times, and shall not store sensitive data in the payload. JWTs shall not accept "none" algorithm.
- **Test**: Decode JWT tokens and inspect the header (algorithm) and payload (expiration, claims). Attempt to forge a token with alg:none or HS256 using a known secret. Verify tokens are rejected after expiration.

### AUTH-003
- **Name**: Credential Stuffing Protection
- **CIA**: C, A
- **OWASP-API**: API2:2023
- **NIST-800**: AC-7, SI-4
- **ISO-27001**: A.9.4.2
- **CMMC**: AC.L2-3.1.8; SI.L2-3.14.6, SI.L2-3.14.7
- **DoD-SRG**: SRG-APP-000065; SRG-APP-000516
- **FedRAMP**: AC-7 (Low); SI-4 (Low)
- **HIPAA**: §164.312(a)(1) — Access Control; §164.308(a)(1)(ii)(D) — Information System Activity Review
- **PCI-DSS**: Req 8.3.4 — Lock-out after invalid attempts; Req 10.4 — Audit log monitoring and review
- **SOC2**: CC6.1 — Logical and physical access; CC7.2 — System monitoring
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule; SEC Cyber Rule §229.106 — Incident Disclosure
- **EU-DORA**: Art. 9(4)(c) — Access control policies; Art. 10(1) — Detection of anomalous activities
- **EU-AI**: Art. 15(4) — Cybersecurity (access control); Art. 9(9) — Ongoing monitoring
- **Severity**: HIGH
- **Statement**: Authentication endpoints shall implement rate limiting, account lockout, or CAPTCHA to prevent credential stuffing and brute-force attacks.
- **Test**: Send 50+ rapid authentication requests with incorrect credentials to the login/token endpoint. Verify that rate limiting, progressive delays, or account lockout is enforced.

### AUTH-004
- **Name**: API Key Management
- **CIA**: C
- **OWASP-API**: API2:2023
- **NIST-800**: IA-5
- **ISO-27001**: A.9.2.4
- **CMMC**: IA.L2-3.5.7, IA.L2-3.5.8, IA.L2-3.5.9
- **DoD-SRG**: SRG-APP-000164, SRG-APP-000165
- **FedRAMP**: IA-5 (Low)
- **HIPAA**: §164.312(d) — Person or Entity Authentication
- **PCI-DSS**: Req 8.3.6 — Password complexity requirements
- **SOC2**: CC6.1 — Logical and physical access
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(c) — Authentication mechanisms
- **EU-AI**: Art. 15(4) — Cybersecurity (credential security)
- **Severity**: HIGH
- **Statement**: API keys shall not be transmitted in URL query parameters. Keys shall be sent via headers (Authorization, X-API-Key) and shall be rotatable without service disruption.
- **Test**: Check if any API key is passed as a URL query parameter (e.g., ?api_key=xxx). Verify keys are transmitted in headers. Check if key rotation is supported.

---

## BOPLA — Broken Object Property Level Authorization

### BOPLA-001
- **Name**: Excessive Data Exposure
- **CIA**: C
- **OWASP-API**: API3:2023
- **NIST-800**: AC-3, SC-8
- **ISO-27001**: A.14.1.2
- **CMMC**: AC.L2-3.1.1, AC.L2-3.1.2; SC.L2-3.13.8
- **DoD-SRG**: SRG-APP-000033, SRG-APP-000340; SRG-APP-000219, SRG-APP-000224
- **FedRAMP**: AC-3 (Moderate); SC-8 (Moderate)
- **HIPAA**: §164.312(a)(1) — Access Control; §164.312(e)(1) — Transmission Security
- **PCI-DSS**: Req 7.2 — Restrict access by need-to-know; Req 4.2.1 — Strong cryptography for transmission
- **SOC2**: CC6.1 — Logical and physical access; CC6.7 — Encryption in transit
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(c) — Access control policies; Art. 9(4)(d) — Cryptographic controls
- **EU-AI**: Art. 15(4) — Cybersecurity (access control); Art. 15(4) — Cybersecurity (data in transit)
- **Severity**: HIGH
- **Statement**: API responses shall return only the minimum set of object properties required by the client. Internal fields (internal IDs, password hashes, audit timestamps, admin flags) shall never be exposed.
- **Test**: Inspect API responses for each endpoint. Look for fields that are not consumed by the client UI, especially: internal database IDs, password hashes, email addresses not displayed, role/privilege fields, internal timestamps, debug information.

### BOPLA-002
- **Name**: Mass Assignment Prevention
- **CIA**: I
- **OWASP-API**: API3:2023
- **NIST-800**: AC-3
- **ISO-27001**: A.14.2.5
- **CMMC**: AC.L2-3.1.1, AC.L2-3.1.2
- **DoD-SRG**: SRG-APP-000033, SRG-APP-000340
- **FedRAMP**: AC-3 (Moderate)
- **HIPAA**: §164.312(a)(1) — Access Control
- **PCI-DSS**: Req 7.2 — Restrict access by need-to-know
- **SOC2**: CC6.1 — Logical and physical access
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(c) — Access control policies
- **EU-AI**: Art. 15(4) — Cybersecurity (access control)
- **Severity**: CRITICAL
- **Statement**: API endpoints that accept object updates (PUT, PATCH, POST) shall explicitly whitelist the properties that can be modified. Clients shall not be able to set properties like role, isAdmin, balance, or internal flags by including them in the request body.
- **Test**: Send a PUT/PATCH request with additional properties not exposed in the normal UI (e.g., "role": "admin", "isAdmin": true, "balance": 99999). If any of these properties are accepted and persisted, the control fails.

### BOPLA-003
- **Name**: Response Schema Validation
- **CIA**: C
- **OWASP-API**: API3:2023
- **NIST-800**: SI-10
- **ISO-27001**: A.14.2.5
- **CMMC**: SI.L2-3.14.2
- **DoD-SRG**: SRG-APP-000251
- **FedRAMP**: SI-10 (Moderate)
- **HIPAA**: §164.312(c)(1) — Integrity
- **PCI-DSS**: Req 6.2.4 — Input validation
- **SOC2**: CC7.1 — Vulnerability management
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(a) — ICT systems integrity
- **EU-AI**: Art. 10(3) — Data governance (validation)
- **Severity**: MEDIUM
- **Statement**: API responses shall conform to a documented schema (OpenAPI/Swagger). Responses shall not contain undocumented fields, and schema validation shall be enforced.
- **Test**: Compare actual API responses against the documented OpenAPI schema. Identify any fields present in responses that are not documented in the schema.

---

## RATE — Resource Consumption & Rate Limiting

### RATE-001
- **Name**: Request Rate Limiting
- **CIA**: A
- **OWASP-API**: API4:2023
- **NIST-800**: SC-5
- **ISO-27001**: A.12.1.3
- **CMMC**: SC.L2-3.13.1
- **DoD-SRG**: SRG-APP-000246
- **FedRAMP**: SC-5 (Low)
- **HIPAA**: §164.308(a)(7) — Contingency Plan
- **PCI-DSS**: Req 11.5 — Network intrusion detection
- **SOC2**: A1.2 — Environmental protections
- **SEC-FINRA**: FINRA Rule 4370 — Business Continuity
- **EU-DORA**: Art. 9(2) — Continuity and availability
- **EU-AI**: Art. 15(3) — Robustness (availability)
- **Severity**: HIGH
- **Statement**: All API endpoints shall enforce rate limits (requests per second/minute per client/IP). Rate limit headers (X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset) should be returned to clients.
- **Test**: Send requests at increasing rates to various endpoints. Verify that 429 Too Many Requests is returned when limits are exceeded. Check for rate limit headers in responses.

### RATE-002
- **Name**: Payload Size Limits
- **CIA**: A
- **OWASP-API**: API4:2023
- **NIST-800**: SC-5
- **ISO-27001**: A.12.1.3
- **CMMC**: SC.L2-3.13.1
- **DoD-SRG**: SRG-APP-000246
- **FedRAMP**: SC-5 (Low)
- **HIPAA**: §164.308(a)(7) — Contingency Plan
- **PCI-DSS**: Req 11.5 — Network intrusion detection
- **SOC2**: A1.2 — Environmental protections
- **SEC-FINRA**: FINRA Rule 4370 — Business Continuity
- **EU-DORA**: Art. 9(2) — Continuity and availability
- **EU-AI**: Art. 15(3) — Robustness (availability)
- **Severity**: MEDIUM
- **Statement**: APIs shall enforce maximum request body size limits. Upload endpoints shall have file size limits. JSON body depth and array length shall be bounded.
- **Test**: Send requests with oversized payloads (e.g., 100MB JSON body, deeply nested JSON with 100+ levels, arrays with 100,000+ items). Verify the server rejects them with 413 or 400 status codes.

### RATE-003
- **Name**: Query Complexity Limits (GraphQL)
- **CIA**: A
- **OWASP-API**: API4:2023
- **NIST-800**: SC-5
- **ISO-27001**: A.12.1.3
- **CMMC**: SC.L2-3.13.1
- **DoD-SRG**: SRG-APP-000246
- **FedRAMP**: SC-5 (Low)
- **HIPAA**: §164.308(a)(7) — Contingency Plan
- **PCI-DSS**: Req 11.5 — Network intrusion detection
- **SOC2**: A1.2 — Environmental protections
- **SEC-FINRA**: FINRA Rule 4370 — Business Continuity
- **EU-DORA**: Art. 9(2) — Continuity and availability
- **EU-AI**: Art. 15(3) — Robustness (availability)
- **Severity**: HIGH
- **Statement**: GraphQL APIs shall enforce query depth limits, complexity scoring, and field count limits to prevent denial-of-service via deeply nested or expensive queries.
- **Test**: If the API uses GraphQL, send deeply nested queries (10+ levels), queries requesting all fields on all types, and introspection queries. Verify complexity limits are enforced.

### RATE-004
- **Name**: Pagination Enforcement
- **CIA**: A, C
- **OWASP-API**: API4:2023
- **NIST-800**: SC-5
- **ISO-27001**: A.12.1.3
- **CMMC**: SC.L2-3.13.1
- **DoD-SRG**: SRG-APP-000246
- **FedRAMP**: SC-5 (Low)
- **HIPAA**: §164.308(a)(7) — Contingency Plan
- **PCI-DSS**: Req 11.5 — Network intrusion detection
- **SOC2**: A1.2 — Environmental protections
- **SEC-FINRA**: FINRA Rule 4370 — Business Continuity
- **EU-DORA**: Art. 9(2) — Continuity and availability
- **EU-AI**: Art. 15(3) — Robustness (availability)
- **Severity**: MEDIUM
- **Statement**: List endpoints shall enforce pagination with a maximum page size. Clients shall not be able to request unbounded result sets (e.g., ?limit=999999).
- **Test**: Send requests with excessively large page sizes (e.g., ?limit=100000 or ?per_page=999999). Verify the server caps the result set to a maximum page size.

---

## FUNC — Function Level Authorization

### FUNC-001
- **Name**: Admin Function Isolation
- **CIA**: C, I, A
- **OWASP-API**: API5:2023
- **NIST-800**: AC-6
- **ISO-27001**: A.9.2.3
- **CMMC**: AC.L2-3.1.5, AC.L2-3.1.6
- **DoD-SRG**: SRG-APP-000062, SRG-APP-000063
- **FedRAMP**: AC-6 (Moderate)
- **HIPAA**: §164.312(a)(1) — Access Control
- **PCI-DSS**: Req 7.2.1 — Least privilege access
- **SOC2**: CC6.3 — Least privilege access
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(c) — Least privilege
- **EU-AI**: Art. 15(4) — Cybersecurity (access restriction)
- **Severity**: CRITICAL
- **Statement**: Administrative API functions (user management, configuration, data export) shall be accessible only to users with appropriate roles. Regular users shall receive 403 Forbidden when attempting to access admin endpoints.
- **Test**: Authenticate as a regular user. Attempt to call administrative endpoints (e.g., /api/admin/users, /api/admin/config, DELETE /api/users/{id}). All should return 403 Forbidden.

### FUNC-002
- **Name**: HTTP Method Restriction
- **CIA**: I
- **OWASP-API**: API5:2023
- **NIST-800**: AC-3
- **ISO-27001**: A.14.1.2
- **CMMC**: AC.L2-3.1.1, AC.L2-3.1.2
- **DoD-SRG**: SRG-APP-000033, SRG-APP-000340
- **FedRAMP**: AC-3 (Moderate)
- **HIPAA**: §164.312(a)(1) — Access Control
- **PCI-DSS**: Req 7.2 — Restrict access by need-to-know
- **SOC2**: CC6.1 — Logical and physical access
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(c) — Access control policies
- **EU-AI**: Art. 15(4) — Cybersecurity (access control)
- **Severity**: MEDIUM
- **Statement**: API endpoints shall only accept the HTTP methods they are designed for. Unsupported methods (e.g., DELETE on a read-only endpoint) shall return 405 Method Not Allowed.
- **Test**: Send OPTIONS requests to all endpoints and note allowed methods. Then send disallowed methods (e.g., DELETE to a GET-only endpoint). Verify 405 responses.

### FUNC-003
- **Name**: Role Escalation Prevention
- **CIA**: C, I
- **OWASP-API**: API5:2023
- **NIST-800**: AC-6(2)
- **ISO-27001**: A.9.2.3
- **CMMC**: AC.L2-3.1.5
- **DoD-SRG**: SRG-APP-000063
- **FedRAMP**: AC-6(2) (Moderate)
- **HIPAA**: §164.312(a)(1) — Access Control
- **PCI-DSS**: Req 7.2.1 — Least privilege access
- **SOC2**: CC6.3 — Least privilege access
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(c) — Least privilege
- **EU-AI**: Art. 15(4) — Cybersecurity (access restriction)
- **Severity**: CRITICAL
- **Statement**: No API endpoint shall allow a user to modify their own role or privilege level. Role changes shall require administrative authorization from a separate, higher-privileged account.
- **Test**: Authenticate as a regular user. Attempt to change your own role via user profile update endpoints (e.g., PATCH /api/users/me with {"role": "admin"}). The request should be rejected.

---

## FLOW — Sensitive Business Flow Protection

### FLOW-001
- **Name**: Business Logic Abuse Prevention
- **CIA**: I, A
- **OWASP-API**: API6:2023
- **NIST-800**: SI-10
- **ISO-27001**: A.14.2.5
- **CMMC**: SI.L2-3.14.2
- **DoD-SRG**: SRG-APP-000251
- **FedRAMP**: SI-10 (Moderate)
- **HIPAA**: §164.312(c)(1) — Integrity
- **PCI-DSS**: Req 6.2.4 — Input validation
- **SOC2**: CC7.1 — Vulnerability management
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(a) — ICT systems integrity
- **EU-AI**: Art. 10(3) — Data governance (validation)
- **Severity**: HIGH
- **Statement**: APIs exposing sensitive business flows (checkout, transfer, registration, coupon redemption) shall implement anti-automation controls (CAPTCHA, device fingerprinting, rate limiting) to prevent abuse at scale.
- **Test**: Automate rapid sequential calls to business-critical endpoints (e.g., coupon application, account creation, purchase flow). Verify that anti-automation controls activate.

### FLOW-002
- **Name**: Transaction Integrity
- **CIA**: I
- **OWASP-API**: API6:2023
- **NIST-800**: SI-7
- **ISO-27001**: A.14.2.5
- **CMMC**: SI.L2-3.14.4
- **DoD-SRG**: SRG-APP-000357
- **FedRAMP**: SI-7 (Moderate)
- **HIPAA**: §164.312(c)(1) — Integrity
- **PCI-DSS**: Req 11.5 — File integrity monitoring
- **SOC2**: CC7.1 — Vulnerability management
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(a) — ICT systems integrity
- **EU-AI**: Art. 15(3) — Robustness (integrity)
- **Severity**: HIGH
- **Statement**: Multi-step transaction flows (e.g., add-to-cart → checkout → payment) shall validate the integrity of each step. Clients shall not be able to skip steps, replay steps, or modify prices/quantities between steps.
- **Test**: Capture a multi-step flow. Attempt to skip steps (e.g., go directly from cart to payment confirmation), modify amounts between steps, or replay a completed transaction.

---

## SSRF — Server-Side Request Forgery

### SSRF-001
- **Name**: URL Input Validation
- **CIA**: C, I
- **OWASP-API**: API7:2023
- **NIST-800**: SI-10
- **ISO-27001**: A.14.2.5
- **CMMC**: SI.L2-3.14.2
- **DoD-SRG**: SRG-APP-000251
- **FedRAMP**: SI-10 (Moderate)
- **HIPAA**: §164.312(c)(1) — Integrity
- **PCI-DSS**: Req 6.2.4 — Input validation
- **SOC2**: CC7.1 — Vulnerability management
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(a) — ICT systems integrity
- **EU-AI**: Art. 10(3) — Data governance (validation)
- **Severity**: CRITICAL
- **Statement**: API endpoints that accept URLs as input (webhooks, callbacks, image URLs, import URLs) shall validate and restrict the target to allowed domains and protocols. Internal/private IP ranges (10.x, 172.16-31.x, 192.168.x, 127.x, ::1) shall be blocked.
- **Test**: Submit URLs pointing to internal resources: http://127.0.0.1, http://169.254.169.254 (cloud metadata), http://10.0.0.1, file:///etc/passwd. All should be rejected.

### SSRF-002
- **Name**: Webhook Security
- **CIA**: C, I
- **OWASP-API**: API7:2023
- **NIST-800**: SI-10
- **ISO-27001**: A.14.2.5
- **CMMC**: SI.L2-3.14.2
- **DoD-SRG**: SRG-APP-000251
- **FedRAMP**: SI-10 (Moderate)
- **HIPAA**: §164.312(c)(1) — Integrity
- **PCI-DSS**: Req 6.2.4 — Input validation
- **SOC2**: CC7.1 — Vulnerability management
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(a) — ICT systems integrity
- **EU-AI**: Art. 10(3) — Data governance (validation)
- **Severity**: HIGH
- **Statement**: Webhook registration endpoints shall validate callback URLs against an allowlist, shall use HMAC signature verification for webhook payloads, and shall not follow HTTP redirects to internal addresses.
- **Test**: Register a webhook with an internal URL (http://127.0.0.1:8080). Verify it is rejected. Register a webhook with a URL that returns a 302 redirect to an internal address. Verify the redirect is not followed.

---

## CONFIG — Security Misconfiguration

### CONFIG-001
- **Name**: CORS Policy
- **CIA**: C, I
- **OWASP-API**: API8:2023
- **NIST-800**: SC-8
- **ISO-27001**: A.13.1.1
- **CMMC**: SC.L2-3.13.8
- **DoD-SRG**: SRG-APP-000219, SRG-APP-000224
- **FedRAMP**: SC-8 (Moderate)
- **HIPAA**: §164.312(e)(1) — Transmission Security
- **PCI-DSS**: Req 4.2.1 — Strong cryptography for transmission
- **SOC2**: CC6.7 — Encryption in transit
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(d) — Cryptographic controls
- **EU-AI**: Art. 15(4) — Cybersecurity (data in transit)
- **Severity**: HIGH
- **Statement**: Cross-Origin Resource Sharing (CORS) headers shall not use wildcard (*) for Access-Control-Allow-Origin on authenticated endpoints. Allowed origins shall be explicitly listed.
- **Test**: Send a request with Origin: https://evil.com. Check if the API reflects it in Access-Control-Allow-Origin. Check if wildcard (*) is used. Verify credentials mode restrictions.

### CONFIG-002
- **Name**: Error Response Sanitization
- **CIA**: C
- **OWASP-API**: API8:2023
- **NIST-800**: SI-11
- **ISO-27001**: A.14.1.2
- **CMMC**: SI.L2-3.14.1
- **DoD-SRG**: SRG-APP-000266
- **FedRAMP**: SI-11 (Moderate)
- **HIPAA**: §164.312(c)(1) — Integrity
- **PCI-DSS**: Req 6.2.6 — Error handling
- **SOC2**: CC7.1 — Vulnerability management
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(a) — ICT systems integrity
- **EU-AI**: Art. 13(1) — Transparency (error handling)
- **Severity**: MEDIUM
- **Statement**: API error responses shall use generic messages. Stack traces, internal file paths, database queries, framework versions, and debug information shall not be exposed in any environment accessible to clients.
- **Test**: Trigger errors by sending malformed requests, invalid JSON, missing required fields, and type mismatches. Inspect error responses for stack traces, file paths, SQL queries, or framework identifiers.

### CONFIG-003
- **Name**: HTTP Security Headers
- **CIA**: C, I
- **OWASP-API**: API8:2023
- **NIST-800**: SC-8
- **ISO-27001**: A.13.1.1
- **CMMC**: SC.L2-3.13.8
- **DoD-SRG**: SRG-APP-000219, SRG-APP-000224
- **FedRAMP**: SC-8 (Moderate)
- **HIPAA**: §164.312(e)(1) — Transmission Security
- **PCI-DSS**: Req 4.2.1 — Strong cryptography for transmission
- **SOC2**: CC6.7 — Encryption in transit
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(d) — Cryptographic controls
- **EU-AI**: Art. 15(4) — Cybersecurity (data in transit)
- **Severity**: MEDIUM
- **Statement**: API responses shall include security headers: Strict-Transport-Security, X-Content-Type-Options: nosniff, Cache-Control: no-store for sensitive data, and X-Frame-Options (if serving HTML).
- **Test**: Inspect response headers on all API endpoints. Verify the presence of required security headers. Check for missing or misconfigured headers.

### CONFIG-004
- **Name**: Debug/Development Endpoint Exposure
- **CIA**: C
- **OWASP-API**: API8:2023
- **NIST-800**: CM-7
- **ISO-27001**: A.12.1.4
- **CMMC**: CM.L2-3.4.6, CM.L2-3.4.7
- **DoD-SRG**: SRG-APP-000141, SRG-APP-000142
- **FedRAMP**: CM-7 (Low)
- **HIPAA**: §164.308(a)(8) — Evaluation
- **PCI-DSS**: Req 2.2.4 — Disable unnecessary services
- **SOC2**: CC6.8 — Prevent unauthorized software
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(e) — Configuration management
- **EU-AI**: Art. 15(3) — Robustness (minimization)
- **Severity**: HIGH
- **Statement**: Debug, profiling, and development endpoints (e.g., /debug, /metrics, /swagger, /graphql/playground, /actuator) shall be disabled or access-restricted in production.
- **Test**: Probe for common debug/admin endpoints: /debug, /metrics, /health, /swagger, /swagger-ui, /api-docs, /graphql, /graphql/playground, /.env, /actuator, /phpinfo. Any that return data without authentication fail.

### CONFIG-005
- **Name**: TLS Enforcement
- **CIA**: C
- **OWASP-API**: API8:2023
- **NIST-800**: SC-8
- **ISO-27001**: A.10.1.1
- **CMMC**: SC.L2-3.13.8
- **DoD-SRG**: SRG-APP-000219, SRG-APP-000224
- **FedRAMP**: SC-8 (Moderate)
- **HIPAA**: §164.312(e)(1) — Transmission Security
- **PCI-DSS**: Req 4.2.1 — Strong cryptography for transmission
- **SOC2**: CC6.7 — Encryption in transit
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(d) — Cryptographic controls
- **EU-AI**: Art. 15(4) — Cybersecurity (data in transit)
- **Severity**: HIGH
- **Statement**: All API endpoints shall be accessible only over HTTPS (TLS 1.2+). HTTP requests shall be redirected to HTTPS or rejected entirely. TLS 1.0 and 1.1 shall be disabled.
- **Test**: Attempt to connect to the API over plain HTTP. Verify it redirects to HTTPS or returns an error. Check TLS version support — verify TLS 1.0/1.1 connections are rejected.

---

## INPUT — API Input Validation

### INPUT-001
- **Name**: Request Schema Validation
- **CIA**: I, A
- **OWASP-API**: API8:2023
- **NIST-800**: SI-10
- **ISO-27001**: A.14.2.5
- **CMMC**: SI.L2-3.14.2
- **DoD-SRG**: SRG-APP-000251
- **FedRAMP**: SI-10 (Moderate)
- **HIPAA**: §164.312(c)(1) — Integrity
- **PCI-DSS**: Req 6.2.4 — Input validation
- **SOC2**: CC7.1 — Vulnerability management
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(a) — ICT systems integrity
- **EU-AI**: Art. 10(3) — Data governance (validation)
- **Severity**: HIGH
- **Statement**: All API request bodies shall be validated against a defined schema (JSON Schema, OpenAPI spec). Requests with unexpected fields, wrong types, or missing required fields shall be rejected with 400 Bad Request.
- **Test**: Send requests with: missing required fields, extra undocumented fields, wrong data types (string where integer expected), null values in non-nullable fields. Verify 400 responses with descriptive error codes.

### INPUT-002
- **Name**: SQL/NoSQL Injection Prevention
- **CIA**: C, I
- **OWASP-API**: API8:2023
- **NIST-800**: SI-10
- **ISO-27001**: A.14.2.5
- **CMMC**: SI.L2-3.14.2
- **DoD-SRG**: SRG-APP-000251
- **FedRAMP**: SI-10 (Moderate)
- **HIPAA**: §164.312(c)(1) — Integrity
- **PCI-DSS**: Req 6.2.4 — Input validation
- **SOC2**: CC7.1 — Vulnerability management
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(a) — ICT systems integrity
- **EU-AI**: Art. 10(3) — Data governance (validation)
- **Severity**: CRITICAL
- **Statement**: All API parameters used in database queries shall use parameterized queries or ORM abstractions. No user input shall be concatenated directly into SQL or NoSQL query strings.
- **Test**: Inject SQL payloads (' OR 1=1 --, '; DROP TABLE--, UNION SELECT) and NoSQL payloads ({"$gt": ""}, {"$ne": null}) into query parameters, body fields, and headers. Verify all are rejected or safely handled.

### INPUT-003
- **Name**: Content-Type Validation
- **CIA**: I
- **OWASP-API**: API8:2023
- **NIST-800**: SI-10
- **ISO-27001**: A.14.2.5
- **CMMC**: SI.L2-3.14.2
- **DoD-SRG**: SRG-APP-000251
- **FedRAMP**: SI-10 (Moderate)
- **HIPAA**: §164.312(c)(1) — Integrity
- **PCI-DSS**: Req 6.2.4 — Input validation
- **SOC2**: CC7.1 — Vulnerability management
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(a) — ICT systems integrity
- **EU-AI**: Art. 10(3) — Data governance (validation)
- **Severity**: MEDIUM
- **Statement**: APIs shall validate the Content-Type header on all requests that include a body. Requests with unexpected content types shall be rejected with 415 Unsupported Media Type.
- **Test**: Send a POST/PUT request with Content-Type: text/xml to an endpoint expecting application/json. Verify it returns 415. Try sending form-encoded data to a JSON endpoint.

### INPUT-004
- **Name**: Path Traversal Prevention
- **CIA**: C
- **OWASP-API**: API8:2023
- **NIST-800**: SI-10
- **ISO-27001**: A.14.2.5
- **CMMC**: SI.L2-3.14.2
- **DoD-SRG**: SRG-APP-000251
- **FedRAMP**: SI-10 (Moderate)
- **HIPAA**: §164.312(c)(1) — Integrity
- **PCI-DSS**: Req 6.2.4 — Input validation
- **SOC2**: CC7.1 — Vulnerability management
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(a) — ICT systems integrity
- **EU-AI**: Art. 10(3) — Data governance (validation)
- **Severity**: HIGH
- **Statement**: API endpoints that accept file paths or resource identifiers shall sanitize input to prevent path traversal attacks (../, ..\, %2e%2e%2f).
- **Test**: Include path traversal sequences in URL parameters and body fields: ../../etc/passwd, ..%2f..%2fetc%2fpasswd, ....//....//etc/passwd. Verify all are rejected.

---

## INVENTORY — API Inventory & Versioning

### INVENTORY-001
- **Name**: API Documentation Accuracy
- **CIA**: C, I
- **OWASP-API**: API9:2023
- **NIST-800**: PL-8
- **ISO-27001**: A.8.1.1
- **CMMC**: CA.L2-3.12.4
- **DoD-SRG**: SRG-APP-000516
- **FedRAMP**: PL-8 (Moderate)
- **HIPAA**: §164.308(a)(1)(i) — Security Management Process
- **PCI-DSS**: Req 12.1 — Information security policy
- **SOC2**: CC3.1 — Risk assessment
- **SEC-FINRA**: FINRA Rule 3110 — Supervisory Systems
- **EU-DORA**: Art. 6(1) — ICT risk management framework
- **EU-AI**: Art. 9(1) — Risk management system
- **Severity**: MEDIUM
- **Statement**: A complete, up-to-date API inventory shall exist documenting all endpoints, methods, parameters, authentication requirements, and data classifications. Shadow APIs (undocumented endpoints) shall not exist.
- **Test**: Compare the documented API specification (OpenAPI/Swagger) against actual API behavior. Probe for undocumented endpoints using wordlists and path fuzzing. Any endpoint that responds but is not documented fails.

### INVENTORY-002
- **Name**: API Version Management
- **CIA**: C, I
- **OWASP-API**: API9:2023
- **NIST-800**: CM-3
- **ISO-27001**: A.14.2.2
- **CMMC**: CM.L2-3.4.3
- **DoD-SRG**: SRG-APP-000380
- **FedRAMP**: CM-3 (Moderate)
- **HIPAA**: §164.308(a)(8) — Evaluation
- **PCI-DSS**: Req 6.5.1 — Change management procedures
- **SOC2**: CC8.1 — Change management
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(e) — Change management
- **EU-AI**: Art. 9(9) — Risk management (change control)
- **Severity**: MEDIUM
- **Statement**: Deprecated API versions shall be decommissioned within a defined timeline. Old API versions shall not bypass security controls that exist in current versions.
- **Test**: Check for older API version endpoints (e.g., /v1/, /v2/ when current is /v3/). Verify deprecated versions are disabled or apply the same security controls as current versions.

### INVENTORY-003
- **Name**: API Gateway / Proxy Coverage
- **CIA**: C, I, A
- **OWASP-API**: API9:2023
- **NIST-800**: SC-7
- **ISO-27001**: A.13.1.1
- **CMMC**: SC.L2-3.13.1, SC.L2-3.13.5
- **DoD-SRG**: SRG-APP-000001, SRG-APP-000002
- **FedRAMP**: SC-7 (Low)
- **HIPAA**: §164.312(e)(1) — Transmission Security
- **PCI-DSS**: Req 1.2 — Network security controls
- **SOC2**: CC6.6 — Boundary protection
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(b) — Network security management
- **EU-AI**: Art. 15(4) — Cybersecurity (network protection)
- **Severity**: HIGH
- **Statement**: All API traffic shall route through a centralized API gateway or reverse proxy that enforces authentication, rate limiting, and logging. Direct access to backend API services shall be blocked.
- **Test**: Attempt to access backend API services directly (bypassing the gateway). Check if internal service ports are exposed. Verify all traffic flows through the gateway.

---

## CONSUME — Unsafe API Consumption

### CONSUME-001
- **Name**: Third-Party API Input Validation
- **CIA**: C, I
- **OWASP-API**: API10:2023
- **NIST-800**: SA-9, SI-10
- **ISO-27001**: A.15.1.1
- **CMMC**: SA.L2-3.13.1; SI.L2-3.14.2
- **DoD-SRG**: SRG-APP-000516; SRG-APP-000251
- **FedRAMP**: SA-9 (Low); SI-10 (Moderate)
- **HIPAA**: §164.308(b)(1) — Business Associate Contracts; §164.312(c)(1) — Integrity
- **PCI-DSS**: Req 12.8 — Third-party service providers; Req 6.2.4 — Input validation
- **SOC2**: CC9.2 — Vendor management; CC7.1 — Vulnerability management
- **SEC-FINRA**: FINRA Rule 3110 — Supervisory Systems; Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 28(1)(a) — Third-party ICT risk; Art. 9(4)(a) — ICT systems integrity
- **EU-AI**: Art. 25 — Responsibilities along the AI value chain; Art. 10(3) — Data governance (validation)
- **Severity**: HIGH
- **Statement**: Data received from third-party APIs shall be validated and sanitized with the same rigor as user input. The API shall not trust data from external services implicitly.
- **Test**: If the API integrates with third-party services, examine how their responses are handled. Check if third-party data is validated before being stored, displayed, or used in queries.

### CONSUME-002
- **Name**: Third-Party API Transport Security
- **CIA**: C
- **OWASP-API**: API10:2023
- **NIST-800**: SC-8
- **ISO-27001**: A.10.1.1
- **CMMC**: SC.L2-3.13.8
- **DoD-SRG**: SRG-APP-000219, SRG-APP-000224
- **FedRAMP**: SC-8 (Moderate)
- **HIPAA**: §164.312(e)(1) — Transmission Security
- **PCI-DSS**: Req 4.2.1 — Strong cryptography for transmission
- **SOC2**: CC6.7 — Encryption in transit
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(d) — Cryptographic controls
- **EU-AI**: Art. 15(4) — Cybersecurity (data in transit)
- **Severity**: MEDIUM
- **Statement**: All communications with third-party APIs shall use TLS. Certificate validation shall not be disabled. Redirects from third-party APIs shall be validated.
- **Test**: Review the API's outbound connections to third-party services. Verify TLS is enforced, certificate validation is enabled, and HTTP redirects are handled safely.

### CONSUME-003
- **Name**: Third-Party API Failure Handling
- **CIA**: A
- **OWASP-API**: API10:2023
- **NIST-800**: SI-17
- **ISO-27001**: A.17.1.1
- **CMMC**: SI.L2-3.14.1
- **DoD-SRG**: SRG-APP-000516
- **FedRAMP**: SI-17 (Moderate)
- **HIPAA**: §164.312(c)(1) — Integrity
- **PCI-DSS**: Req 6.2.4 — Input validation
- **SOC2**: CC7.1 — Vulnerability management
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(a) — ICT systems integrity
- **EU-AI**: Art. 10(3) — Data governance (validation)
- **Severity**: MEDIUM
- **Statement**: The API shall handle third-party API failures gracefully with circuit breakers, timeouts, and fallback responses. A third-party outage shall not cascade into a full API outage.
- **Test**: Simulate third-party API failures (timeout, 500 error, malformed response). Verify the API returns graceful error responses and does not crash or hang.

---

## DATA — API Data Protection

### DATA-001
- **Name**: Sensitive Data Classification
- **CIA**: C
- **NIST-800**: RA-2
- **ISO-27001**: A.8.2.1
- **CMMC**: RA.L2-3.11.1
- **DoD-SRG**: SRG-APP-000381
- **FedRAMP**: RA-2 (Low)
- **HIPAA**: §164.308(a)(1)(ii)(A) — Risk Analysis
- **PCI-DSS**: Req 12.3.1 — Targeted risk analysis
- **SOC2**: CC3.1 — Risk assessment
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 6(1) — ICT risk management framework
- **EU-AI**: Art. 9(2) — Risk identification and analysis
- **Severity**: MEDIUM
- **Statement**: All API data fields shall be classified by sensitivity level. PII, financial data, health data, and authentication credentials shall be identified and treated with appropriate protection levels.
- **Test**: Review API responses for data classification. Identify fields containing PII (email, phone, SSN, DOB), financial data, or credentials. Verify appropriate handling (masking, encryption, access controls).

### DATA-002
- **Name**: Data Minimization in Responses
- **CIA**: C
- **OWASP-API**: API3:2023
- **NIST-800**: SA-8
- **ISO-27001**: A.18.1.4
- **CMMC**: SA.L2-3.13.2
- **DoD-SRG**: SRG-APP-000516
- **FedRAMP**: SA-8 (Moderate)
- **HIPAA**: §164.308(a)(1)(i) — Security Management Process
- **PCI-DSS**: Req 6.2.1 — Secure development practices
- **SOC2**: CC8.1 — Change management
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 8(1) — ICT systems resilience
- **EU-AI**: Art. 15(1) — Accuracy, robustness, cybersecurity
- **Severity**: MEDIUM
- **Statement**: API responses shall return only fields required by the requesting client. Endpoints shall support field selection (sparse fieldsets, GraphQL field selection) to minimize unnecessary data exposure.
- **Test**: Compare API response fields against what the client UI actually uses. Identify any fields returned but not consumed. Check if field selection parameters are supported.

### DATA-003
- **Name**: Sensitive Data in Logs
- **CIA**: C
- **NIST-800**: AU-3
- **ISO-27001**: A.12.4.1
- **CMMC**: AU.L2-3.3.1, AU.L2-3.3.2
- **DoD-SRG**: SRG-APP-000095, SRG-APP-000096
- **FedRAMP**: AU-3 (Low)
- **HIPAA**: §164.312(b) — Audit Controls
- **PCI-DSS**: Req 10.2.1 — Log entry detail
- **SOC2**: CC7.2 — System monitoring
- **SEC-FINRA**: SEC Cyber Rule §229.106 — Incident Disclosure
- **EU-DORA**: Art. 10(1) — Detection of anomalous activities
- **EU-AI**: Art. 12(1) — Record-keeping (logging)
- **Severity**: MEDIUM
- **Statement**: API request/response logs shall not contain sensitive data (passwords, tokens, PII, payment data). Sensitive fields shall be masked or redacted in all log outputs.
- **Test**: Review API logging configuration. Check if request bodies containing passwords or tokens are logged in plaintext. Verify PII masking in log output.

### DATA-004
- **Name**: Data Encryption in Transit
- **CIA**: C
- **NIST-800**: SC-8
- **ISO-27001**: A.10.1.1
- **CMMC**: SC.L2-3.13.8
- **DoD-SRG**: SRG-APP-000219, SRG-APP-000224
- **FedRAMP**: SC-8 (Moderate)
- **HIPAA**: §164.312(e)(1) — Transmission Security
- **PCI-DSS**: Req 4.2.1 — Strong cryptography for transmission
- **SOC2**: CC6.7 — Encryption in transit
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(d) — Cryptographic controls
- **EU-AI**: Art. 15(4) — Cybersecurity (data in transit)
- **Severity**: HIGH
- **Statement**: All sensitive data transmitted via API shall be encrypted using TLS 1.2+. Sensitive fields shall additionally be encrypted at the application layer where appropriate (e.g., payment card data).
- **Test**: Verify TLS enforcement on all API endpoints. Check for sensitive data transmitted over unencrypted channels. Review application-layer encryption for high-sensitivity fields.

---

## SECRETS — API Secrets Management

### SECRETS-001
- **Name**: API Key Exposure
- **CIA**: C
- **OWASP-API**: API2:2023
- **NIST-800**: IA-5
- **ISO-27001**: A.9.2.4
- **CMMC**: IA.L2-3.5.7, IA.L2-3.5.8, IA.L2-3.5.9
- **DoD-SRG**: SRG-APP-000164, SRG-APP-000165
- **FedRAMP**: IA-5 (Low)
- **HIPAA**: §164.312(d) — Person or Entity Authentication
- **PCI-DSS**: Req 8.3.6 — Password complexity requirements
- **SOC2**: CC6.1 — Logical and physical access
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(c) — Authentication mechanisms
- **EU-AI**: Art. 15(4) — Cybersecurity (credential security)
- **Severity**: CRITICAL
- **Statement**: API keys, tokens, and secrets shall not be exposed in client-side code, URL parameters, API responses, error messages, or public repositories.
- **Test**: Search client-side JavaScript bundles for API keys (patterns: sk_, pk_, api_key, secret). Check API responses and error messages for leaked tokens. Check URL query parameters for key exposure.

### SECRETS-002
- **Name**: Token Expiration & Rotation
- **CIA**: C
- **OWASP-API**: API2:2023
- **NIST-800**: IA-5(1)
- **ISO-27001**: A.9.2.4
- **CMMC**: IA.L2-3.5.7
- **DoD-SRG**: SRG-APP-000166, SRG-APP-000167
- **FedRAMP**: IA-5(1) (Low)
- **HIPAA**: §164.312(d) — Person or Entity Authentication
- **PCI-DSS**: Req 8.3.6 — Password complexity requirements
- **SOC2**: CC6.1 — Logical and physical access
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(c) — Authentication mechanisms
- **EU-AI**: Art. 15(4) — Cybersecurity (credential security)
- **Severity**: HIGH
- **Statement**: API tokens shall have finite expiration times. Access tokens shall expire within 1 hour. Refresh tokens shall expire within 30 days. API keys shall support rotation without service disruption.
- **Test**: Inspect token expiration claims (exp in JWT). Verify expired tokens are rejected. Check if token rotation/revocation endpoints exist and function correctly.

### SECRETS-003
- **Name**: OAuth Scope Enforcement
- **CIA**: C, I
- **OWASP-API**: API2:2023
- **NIST-800**: AC-6
- **ISO-27001**: A.9.4.1
- **CMMC**: AC.L2-3.1.5, AC.L2-3.1.6
- **DoD-SRG**: SRG-APP-000062, SRG-APP-000063
- **FedRAMP**: AC-6 (Moderate)
- **HIPAA**: §164.312(a)(1) — Access Control
- **PCI-DSS**: Req 7.2.1 — Least privilege access
- **SOC2**: CC6.3 — Least privilege access
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(c) — Least privilege
- **EU-AI**: Art. 15(4) — Cybersecurity (access restriction)
- **Severity**: HIGH
- **Statement**: OAuth tokens shall be scoped to the minimum permissions required. The API shall reject requests that exceed the token's granted scopes.
- **Test**: Obtain a token with limited scopes (e.g., read:users). Attempt to call endpoints requiring broader scopes (e.g., write:users, admin:config). Verify 403 Forbidden is returned.

---

## AUDIT — API Logging & Monitoring

### AUDIT-001
- **Name**: API Request Logging
- **CIA**: I, A
- **NIST-800**: AU-2, AU-3
- **ISO-27001**: A.12.4.1
- **CMMC**: AU.L2-3.3.1; AU.L2-3.3.1, AU.L2-3.3.2
- **DoD-SRG**: SRG-APP-000089, SRG-APP-000091; SRG-APP-000095, SRG-APP-000096
- **FedRAMP**: AU-2 (Low); AU-3 (Low)
- **HIPAA**: §164.312(b) — Audit Controls
- **PCI-DSS**: Req 10.2 — Audit log implementation; Req 10.2.1 — Log entry detail
- **SOC2**: CC7.2 — System monitoring
- **SEC-FINRA**: SEC Cyber Rule §229.106 — Incident Disclosure
- **EU-DORA**: Art. 10(1) — Detection of anomalous activities
- **EU-AI**: Art. 12(1) — Record-keeping (logging)
- **Severity**: MEDIUM
- **Statement**: All API requests shall be logged with: timestamp, client IP, authenticated user, HTTP method, endpoint path, response status code, and response time. Logs shall be retained for a minimum of 90 days.
- **Test**: Make authenticated API requests. Verify that logs capture all required fields. Check log retention policies and storage.

### AUDIT-002
- **Name**: Security Event Alerting
- **CIA**: I, A
- **NIST-800**: SI-4, IR-4
- **ISO-27001**: A.12.4.1
- **CMMC**: SI.L2-3.14.6, SI.L2-3.14.7; IR.L2-3.6.1, IR.L2-3.6.2
- **DoD-SRG**: SRG-APP-000516
- **FedRAMP**: SI-4 (Low); IR-4 (Low)
- **HIPAA**: §164.308(a)(1)(ii)(D) — Information System Activity Review; §164.308(a)(6) — Security Incident Procedures
- **PCI-DSS**: Req 10.4 — Audit log monitoring and review; Req 12.10 — Incident response plan
- **SOC2**: CC7.2 — System monitoring; CC7.3 — Incident identification
- **SEC-FINRA**: SEC Cyber Rule §229.106 — Incident Disclosure
- **EU-DORA**: Art. 10(1) — Detection of anomalous activities; Art. 17(1) — ICT-related incident management
- **EU-AI**: Art. 9(9) — Ongoing monitoring; Art. 62 — Reporting of serious incidents
- **Severity**: HIGH
- **Statement**: The API shall generate alerts for security-relevant events: authentication failures exceeding threshold, authorization failures, rate limit violations, and anomalous request patterns.
- **Test**: Trigger security events (multiple auth failures, rate limit hits, unauthorized access attempts). Verify alerts are generated and routed to the appropriate monitoring system.

### AUDIT-003
- **Name**: Audit Trail Integrity
- **CIA**: I
- **NIST-800**: AU-10
- **ISO-27001**: A.12.4.2
- **CMMC**: AU.L2-3.3.8
- **DoD-SRG**: SRG-APP-000080
- **FedRAMP**: AU-10 (Moderate)
- **HIPAA**: §164.312(b) — Audit Controls
- **PCI-DSS**: Req 10.3 — Protect audit logs
- **SOC2**: CC7.2 — System monitoring
- **SEC-FINRA**: SEC Cyber Rule §229.106 — Incident Disclosure
- **EU-DORA**: Art. 10(1) — Detection of anomalous activities
- **EU-AI**: Art. 12(1) — Record-keeping (non-repudiation)
- **Severity**: MEDIUM
- **Statement**: API audit logs shall be immutable and tamper-evident. Log entries shall not be modifiable by API users or application-level code.
- **Test**: Verify logs are written to a separate, append-only log store. Check if the API application has write access to modify existing log entries. Verify log integrity mechanisms.

---

## DOCS — API Documentation & Specification

### DOCS-001
- **Name**: OpenAPI/Swagger Specification
- **CIA**: I
- **OWASP-API**: API9:2023
- **NIST-800**: PL-8
- **ISO-27001**: A.14.2.1
- **CMMC**: CA.L2-3.12.4
- **DoD-SRG**: SRG-APP-000516
- **FedRAMP**: PL-8 (Moderate)
- **HIPAA**: §164.308(a)(1)(i) — Security Management Process
- **PCI-DSS**: Req 12.1 — Information security policy
- **SOC2**: CC3.1 — Risk assessment
- **SEC-FINRA**: FINRA Rule 3110 — Supervisory Systems
- **EU-DORA**: Art. 6(1) — ICT risk management framework
- **EU-AI**: Art. 9(1) — Risk management system
- **Severity**: LOW
- **Statement**: The API shall maintain a machine-readable specification (OpenAPI 3.0+, AsyncAPI) that accurately describes all endpoints, parameters, request/response schemas, authentication requirements, and error codes.
- **Test**: Request the OpenAPI specification (/openapi.json, /swagger.json). Verify it exists, is valid, and accurately describes the API's behavior. Cross-reference with actual endpoint behavior.

### DOCS-002
- **Name**: Authentication Documentation
- **CIA**: C
- **OWASP-API**: API9:2023
- **NIST-800**: PL-8
- **ISO-27001**: A.14.2.1
- **CMMC**: CA.L2-3.12.4
- **DoD-SRG**: SRG-APP-000516
- **FedRAMP**: PL-8 (Moderate)
- **HIPAA**: §164.308(a)(1)(i) — Security Management Process
- **PCI-DSS**: Req 12.1 — Information security policy
- **SOC2**: CC3.1 — Risk assessment
- **SEC-FINRA**: FINRA Rule 3110 — Supervisory Systems
- **EU-DORA**: Art. 6(1) — ICT risk management framework
- **EU-AI**: Art. 9(1) — Risk management system
- **Severity**: LOW
- **Statement**: API documentation shall clearly specify authentication requirements for each endpoint, including: supported auth methods, required headers, token format, and scope requirements.
- **Test**: Review API documentation for authentication details. Verify each endpoint's auth requirements are documented. Check for discrepancies between documented and actual auth behavior.

---

## GRAPHQL — GraphQL-Specific Controls

### GRAPHQL-001
- **Name**: Introspection Restriction
- **CIA**: C
- **OWASP-API**: API8:2023
- **NIST-800**: CM-7
- **ISO-27001**: A.12.1.4
- **CMMC**: CM.L2-3.4.6, CM.L2-3.4.7
- **DoD-SRG**: SRG-APP-000141, SRG-APP-000142
- **FedRAMP**: CM-7 (Low)
- **HIPAA**: §164.308(a)(8) — Evaluation
- **PCI-DSS**: Req 2.2.4 — Disable unnecessary services
- **SOC2**: CC6.8 — Prevent unauthorized software
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(e) — Configuration management
- **EU-AI**: Art. 15(3) — Robustness (minimization)
- **Severity**: MEDIUM
- **Statement**: GraphQL introspection shall be disabled in production environments. If introspection is required for development tools, it shall be restricted to authenticated administrators.
- **Test**: Send a GraphQL introspection query ({__schema{types{name}}}). Verify it is rejected or returns an error in production. Check if introspection is restricted by authentication.

### GRAPHQL-002
- **Name**: Query Depth & Cost Limiting
- **CIA**: A
- **OWASP-API**: API4:2023
- **NIST-800**: SC-5
- **ISO-27001**: A.12.1.3
- **CMMC**: SC.L2-3.13.1
- **DoD-SRG**: SRG-APP-000246
- **FedRAMP**: SC-5 (Low)
- **HIPAA**: §164.308(a)(7) — Contingency Plan
- **PCI-DSS**: Req 11.5 — Network intrusion detection
- **SOC2**: A1.2 — Environmental protections
- **SEC-FINRA**: FINRA Rule 4370 — Business Continuity
- **EU-DORA**: Art. 9(2) — Continuity and availability
- **EU-AI**: Art. 15(3) — Robustness (availability)
- **Severity**: HIGH
- **Statement**: GraphQL APIs shall enforce query depth limits (max 10 levels), query cost/complexity limits, and field count limits to prevent denial-of-service attacks.
- **Test**: Send deeply nested queries (15+ levels), queries with circular references, and queries requesting all fields on all types. Verify the server rejects overly complex queries.

### GRAPHQL-003
- **Name**: Batching Attack Prevention
- **CIA**: A, C
- **OWASP-API**: API4:2023
- **NIST-800**: SC-5
- **ISO-27001**: A.12.1.3
- **CMMC**: SC.L2-3.13.1
- **DoD-SRG**: SRG-APP-000246
- **FedRAMP**: SC-5 (Low)
- **HIPAA**: §164.308(a)(7) — Contingency Plan
- **PCI-DSS**: Req 11.5 — Network intrusion detection
- **SOC2**: A1.2 — Environmental protections
- **SEC-FINRA**: FINRA Rule 4370 — Business Continuity
- **EU-DORA**: Art. 9(2) — Continuity and availability
- **EU-AI**: Art. 15(3) — Robustness (availability)
- **Severity**: HIGH
- **Statement**: GraphQL APIs shall limit the number of queries per batch request and enforce rate limiting per query (not just per HTTP request) to prevent batching attacks.
- **Test**: Send a batch of 100+ queries in a single HTTP request (e.g., [{"query":"..."}, {"query":"..."}, ...]). Verify the server limits batch size or applies per-query rate limiting.

---

## WEBHOOK — Webhook Security

### WEBHOOK-001
- **Name**: Webhook Payload Signing
- **CIA**: I
- **NIST-800**: SI-7
- **ISO-27001**: A.14.2.5
- **CMMC**: SI.L2-3.14.4
- **DoD-SRG**: SRG-APP-000357
- **FedRAMP**: SI-7 (Moderate)
- **HIPAA**: §164.312(c)(1) — Integrity
- **PCI-DSS**: Req 11.5 — File integrity monitoring
- **SOC2**: CC7.1 — Vulnerability management
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(a) — ICT systems integrity
- **EU-AI**: Art. 15(3) — Robustness (integrity)
- **Severity**: HIGH
- **Statement**: Outbound webhook payloads shall be signed with HMAC (SHA-256+). Recipients shall be able to verify payload authenticity using a shared secret. The signature shall cover the entire payload body.
- **Test**: Register a webhook endpoint and inspect incoming payloads. Verify an HMAC signature header is present (e.g., X-Signature-256). Validate the signature against the payload using the shared secret.

### WEBHOOK-002
- **Name**: Webhook Retry & Timeout
- **CIA**: A
- **NIST-800**: SI-17
- **ISO-27001**: A.17.1.1
- **CMMC**: SI.L2-3.14.1
- **DoD-SRG**: SRG-APP-000516
- **FedRAMP**: SI-17 (Moderate)
- **HIPAA**: §164.312(c)(1) — Integrity
- **PCI-DSS**: Req 6.2.4 — Input validation
- **SOC2**: CC7.1 — Vulnerability management
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(a) — ICT systems integrity
- **EU-AI**: Art. 10(3) — Data governance (validation)
- **Severity**: LOW
- **Statement**: Webhook delivery shall implement retry logic with exponential backoff. Delivery timeouts shall be enforced (max 30 seconds). Failed webhooks shall be logged and made available for manual re-delivery.
- **Test**: Configure a webhook endpoint that returns 500 errors. Verify the API retries with exponential backoff. Check that delivery failures are logged and retrievable.
