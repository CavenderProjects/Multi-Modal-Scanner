# Cross-System Vulnerability Controls Library

## Overview

This library defines **37 controls across 8 families** for evaluating vulnerabilities that emerge when two or more systems are connected. These controls are not testable against a single system in isolation — they specifically address attack chains, shared trust boundaries, and emergent risks that only exist because of the integration between systems.

**Assessment type**: Connected Systems Assessment (Workflow D)
**Input**: Two or more completed assessment reports (Website + API, API + API, Website + Skill, etc.)
**Focus**: Attack chain detection and CVSS/reachability re-scoring

## Framework References

Cross-system controls map to the same 12+ regulatory frameworks as the individual assessment controls. Framework mappings focus on controls related to interconnection security, supply chain risk, and system boundary protection.

---

## CHAIN — Attack Chain Analysis

### CHAIN-001
- **Name**: Authentication Token Relay
- **CIA**: C (Confidentiality)
- **Secondary**: I
- **NIST-800**: IA-4, IA-5, SC-23
- **ISO-27001**: A.9.4.2, A.14.1.3
- **CMMC**: IA.L2-3.5.1, IA.L2-3.5.2
- **DoD-SRG**: SRG-APP-000149, SRG-APP-000153
- **FedRAMP**: IA-4 (Moderate), IA-5 (Moderate)
- **HIPAA**: §164.312(d) — Person or Entity Authentication
- **PCI-DSS**: Req 8.3 — Secure authentication; Req 8.6 — Application/system account management
- **SOC2**: CC6.1 — Logical and physical access
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(c) — Strong authentication
- **EU-AI**: Art. 15(4) — Cybersecurity (authentication)
- **Severity**: CRITICAL
- **Statement**: Authentication tokens obtained or stolen from System A shall not grant unauthorized access to System B without independent validation.
- **Test**: Identify how System A authenticates users and what tokens/cookies it issues. Determine if System B accepts these tokens directly (shared JWT, shared session cookie, API key passed through). If a vulnerability in System A (XSS, session fixation, token leakage) would allow an attacker to obtain a token that System B also accepts, the control fails. Score: original severity of the token-stealing vulnerability PLUS the impact of the access it grants on System B.

### CHAIN-002
- **Name**: Privilege Escalation Across System Boundary
- **CIA**: C, I, A
- **NIST-800**: AC-6, AC-6(1), AC-6(5)
- **ISO-27001**: A.9.2.3, A.9.4.1
- **CMMC**: AC.L2-3.1.5, AC.L2-3.1.6
- **DoD-SRG**: SRG-APP-000062, SRG-APP-000063
- **FedRAMP**: AC-6 (Moderate)
- **HIPAA**: §164.312(a)(1) — Access Control
- **PCI-DSS**: Req 7.2.1 — Least privilege access
- **SOC2**: CC6.3 — Least privilege access
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(c) — Access control policies
- **EU-AI**: Art. 15(4) — Cybersecurity (access control)
- **Severity**: CRITICAL
- **Statement**: A user with limited privileges in System A shall not be able to leverage the connection between systems to obtain elevated privileges in System B.
- **Test**: Map the privilege model in each system. Identify cases where System A passes user context to System B (e.g., website sends user role in API request headers, API trusts frontend-supplied role claims). If a low-privilege user can manipulate the inter-system communication to gain higher privileges in System B, the control fails.

### CHAIN-003
- **Name**: Data Exfiltration via Cross-System Path
- **CIA**: C
- **NIST-800**: AC-4, SC-7
- **ISO-27001**: A.13.1.3, A.14.1.3
- **CMMC**: AC.L2-3.1.3; SC.L2-3.13.1
- **DoD-SRG**: SRG-APP-000038, SRG-APP-000039
- **FedRAMP**: AC-4 (Moderate), SC-7 (Moderate)
- **HIPAA**: §164.312(e)(1) — Transmission Security
- **PCI-DSS**: Req 1.3 — Network segmentation controls
- **SOC2**: CC6.6 — System boundary protection
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(b) — Network security management
- **EU-AI**: Art. 15(4) — Cybersecurity (data protection)
- **Severity**: HIGH
- **Statement**: Data accessible through System A shall not be exfiltrable through System B when neither system would allow exfiltration independently.
- **Test**: Identify data that System A can access but cannot expose externally (e.g., internal database records visible to authenticated API users but not downloadable). Determine if System B provides a path to extract that data (e.g., API excessive data exposure combined with website rendering that leaks API response content). If the combination creates an exfiltration path that neither system creates alone, the control fails.

### CHAIN-004
- **Name**: Injection Propagation Across Systems
- **CIA**: C, I
- **NIST-800**: SI-10, SI-3
- **ISO-27001**: A.12.2.1, A.14.2.5
- **CMMC**: SI.L2-3.14.2, SI.L2-3.14.6
- **DoD-SRG**: SRG-APP-000251, SRG-APP-000252
- **FedRAMP**: SI-10 (Moderate)
- **HIPAA**: §164.312(c)(1) — Integrity
- **PCI-DSS**: Req 6.2.4 — Input validation
- **SOC2**: CC7.1 — Vulnerability management
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(a) — ICT systems integrity
- **EU-AI**: Art. 10(3) — Data governance (validation)
- **Severity**: CRITICAL
- **Statement**: Injection payloads that are stored or reflected by System A shall not execute or cause harm when processed by System B.
- **Test**: Identify injection findings in either system (XSS, SQL injection, command injection, SSRF). Trace data flows between systems. If System A stores a payload (e.g., stored XSS in user profile) and System B retrieves and renders that data without its own sanitization (e.g., API returns unsanitized user profile data, website renders it), the control fails. This is a stored cross-system injection.

### CHAIN-005
- **Name**: SSRF to Internal API Exploitation
- **CIA**: C, I, A
- **NIST-800**: SI-10, SC-7
- **ISO-27001**: A.13.1.1, A.14.1.3
- **CMMC**: SI.L2-3.14.2; SC.L2-3.13.1
- **DoD-SRG**: SRG-APP-000251, SRG-APP-000383
- **FedRAMP**: SI-10 (Moderate), SC-7 (Moderate)
- **HIPAA**: §164.312(e)(1) — Transmission Security
- **PCI-DSS**: Req 6.2.4 — Input validation; Req 1.3 — Network segmentation
- **SOC2**: CC6.6 — System boundary protection; CC7.1 — Vulnerability management
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(a) — ICT systems integrity; Art. 9(4)(b) — Network security
- **EU-AI**: Art. 15(4) — Cybersecurity
- **Severity**: CRITICAL
- **Statement**: An SSRF vulnerability in System A shall not provide a path to exploit vulnerabilities in System B that are otherwise protected by network boundaries.
- **Test**: Identify any SSRF findings in either system. Determine if the SSRF can be used to reach the other system's internal endpoints (admin APIs, debug endpoints, health checks). If System B has findings rated INTERNAL reachability that become DIRECT through System A's SSRF, the control fails and the chain is critical.

---

## TRUST — Shared Trust Boundary Analysis

### TRUST-001
- **Name**: Shared Authentication Provider
- **CIA**: C, I
- **NIST-800**: IA-2, IA-8
- **ISO-27001**: A.9.2.1, A.9.4.2
- **CMMC**: IA.L2-3.5.1, IA.L2-3.5.3
- **DoD-SRG**: SRG-APP-000148, SRG-APP-000149
- **FedRAMP**: IA-2 (Moderate), IA-8 (Moderate)
- **HIPAA**: §164.312(d) — Person or Entity Authentication
- **PCI-DSS**: Req 8.3 — Secure authentication
- **SOC2**: CC6.1 — Logical and physical access
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(c) — Strong authentication
- **EU-AI**: Art. 15(4) — Cybersecurity (authentication)
- **Severity**: HIGH
- **Statement**: When multiple systems share an authentication provider (SSO, OAuth, shared identity store), a compromise of that provider shall not silently grant access to all connected systems.
- **Test**: Identify the authentication mechanism for each system. If they share a provider (same OAuth server, same LDAP, same JWT signing key), evaluate whether auth-related findings in either system (brute-force, MFA bypass, token weakness) affect the other system. If System A has no MFA and System B relies on the same auth provider, System B's effective MFA posture is also compromised.

### TRUST-002
- **Name**: Shared Data Store
- **CIA**: C, I
- **NIST-800**: AC-3, AC-6, SC-28
- **ISO-27001**: A.8.2.3, A.10.1.1
- **CMMC**: AC.L2-3.1.1; SC.L2-3.13.16
- **DoD-SRG**: SRG-APP-000033; SRG-APP-000231
- **FedRAMP**: AC-3 (Moderate), SC-28 (Moderate)
- **HIPAA**: §164.312(a)(1) — Access Control; §164.312(e)(2)(ii) — Encryption
- **PCI-DSS**: Req 3.5 — Protect stored account data; Req 7.2 — Restrict access
- **SOC2**: CC6.1 — Logical and physical access; CC6.7 — Encryption
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(d) — Data protection at rest
- **EU-AI**: Art. 15(4) — Cybersecurity (data protection)
- **Severity**: HIGH
- **Statement**: When systems share a database, cache, or file store, a SQL injection or data access vulnerability in one system shall not expose data that the other system intended to restrict.
- **Test**: Identify shared data stores. If System A has a SQL injection finding and both systems read from the same database, the SQL injection can access System B's restricted tables. Evaluate whether System B's access controls are enforced at the database level or only at the application level.

### TRUST-003
- **Name**: Shared Secrets and Credentials
- **CIA**: C, I
- **NIST-800**: IA-5, SC-12
- **ISO-27001**: A.10.1.2, A.9.2.4
- **CMMC**: IA.L2-3.5.10; SC.L2-3.13.10
- **DoD-SRG**: SRG-APP-000171; SRG-APP-000219
- **FedRAMP**: IA-5 (Moderate), SC-12 (Moderate)
- **HIPAA**: §164.312(d) — Authentication; §164.312(e)(2)(ii) — Encryption
- **PCI-DSS**: Req 8.3.2 — No shared credentials; Req 3.6 — Key management
- **SOC2**: CC6.1 — Logical and physical access
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(c) — Credential management; Art. 9(4)(d) — Cryptographic controls
- **EU-AI**: Art. 15(4) — Cybersecurity
- **Severity**: HIGH
- **Statement**: Systems shall not share API keys, database credentials, encryption keys, or signing secrets. Compromise of a shared secret in one system shall not grant access to the other.
- **Test**: Identify hardcoded secrets, API key exposure, or credential findings in either system. Determine if the exposed credential is also used by the other system. If System A exposes an API key in a client-side response and System B accepts that same key for privileged operations, the control fails.

### TRUST-004
- **Name**: Shared Network Boundary
- **CIA**: C, I, A
- **NIST-800**: SC-7, SC-7(5)
- **ISO-27001**: A.13.1.1, A.13.1.3
- **CMMC**: SC.L2-3.13.1, SC.L2-3.13.6
- **DoD-SRG**: SRG-APP-000383, SRG-APP-000385
- **FedRAMP**: SC-7 (Moderate)
- **HIPAA**: §164.312(e)(1) — Transmission Security
- **PCI-DSS**: Req 1.3 — Network segmentation
- **SOC2**: CC6.6 — System boundary protection
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(b) — Network security management
- **EU-AI**: Art. 15(4) — Cybersecurity
- **Severity**: MEDIUM
- **Statement**: Connected systems shall enforce network segmentation such that compromise of one system's network position does not provide unrestricted access to the other system's internal services.
- **Test**: Map the network topology between systems. Identify if they share a VPC, subnet, or network segment with no firewall rules between them. If System A has an SSRF or RCE finding and System B is reachable from System A's network without additional authentication, the network boundary control fails.

### TRUST-005
- **Name**: Shared Logging and Monitoring
- **CIA**: I, A
- **NIST-800**: AU-6, SI-4
- **ISO-27001**: A.12.4.1, A.16.1.2
- **CMMC**: AU.L2-3.3.5; SI.L2-3.14.6
- **DoD-SRG**: SRG-APP-000516
- **FedRAMP**: AU-6 (Moderate), SI-4 (Moderate)
- **HIPAA**: §164.312(b) — Audit Controls
- **PCI-DSS**: Req 10.6 — Review audit logs
- **SOC2**: CC7.2 — System monitoring; CC7.3 — Detection of anomalies
- **SEC-FINRA**: SEC Cyber Rule §229.106 — Incident Disclosure
- **EU-DORA**: Art. 10(1) — Detection of anomalous activities
- **EU-AI**: Art. 12(1) — Record-keeping
- **Severity**: MEDIUM
- **Statement**: Cross-system attack chains shall be detectable through correlated logging across connected systems.
- **Test**: Determine if each system's logging can be correlated (shared request IDs, trace headers, centralized log aggregation). If an attack chain spanning both systems would generate log entries in separate, uncorrelated stores with no shared identifier, the control fails — the chain would be invisible to monitoring.

---

## RESCORE — CVSS/Reachability Re-Scoring

### RESCORE-001
- **Name**: Reachability Promotion via Connected System
- **CIA**: —
- **NIST-800**: RA-3, RA-5
- **ISO-27001**: A.12.6.1
- **CMMC**: RA.L2-3.11.1, RA.L2-3.11.2
- **DoD-SRG**: SRG-APP-000141
- **FedRAMP**: RA-3 (Moderate), RA-5 (Moderate)
- **HIPAA**: §164.308(a)(1)(ii)(A) — Risk Analysis
- **PCI-DSS**: Req 6.3 — Vulnerability identification
- **SOC2**: CC3.2 — Risk assessment; CC7.1 — Vulnerability management
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 6(1) — ICT risk management framework
- **EU-AI**: Art. 9(1) — Risk management system
- **Severity**: —
- **Statement**: Findings rated INTERNAL or MULTI_STEP in isolation shall be re-evaluated for reachability when a connected system provides a shorter path.
- **Test**: For each INTERNAL or MULTI_STEP finding in System B, check whether any finding in System A provides a new attack path. If System A has an SSRF (DIRECT reachability) that can reach System B's internal admin endpoint (rated INTERNAL), the admin endpoint's effective reachability is promoted to ONE_HOP. Document the original and re-scored reachability with the chain justification.

### RESCORE-002
- **Name**: CVSS Score Elevation via Attack Chain
- **CIA**: —
- **NIST-800**: RA-3, RA-5
- **ISO-27001**: A.12.6.1
- **CMMC**: RA.L2-3.11.1, RA.L2-3.11.2
- **DoD-SRG**: SRG-APP-000141
- **FedRAMP**: RA-3 (Moderate), RA-5 (Moderate)
- **HIPAA**: §164.308(a)(1)(ii)(A) — Risk Analysis
- **PCI-DSS**: Req 6.3 — Vulnerability identification
- **SOC2**: CC3.2 — Risk assessment; CC7.1 — Vulnerability management
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 6(1) — ICT risk management framework
- **EU-AI**: Art. 9(1) — Risk management system
- **Severity**: —
- **Statement**: CVSS base scores shall be re-evaluated when a connected system changes the effective attack vector, complexity, or impact.
- **Test**: For each finding in an attack chain, recalculate the CVSS base score considering the connected system's contribution. Common re-scoring scenarios: (1) Attack Vector changes from Local to Network because the connected system provides remote access, (2) Attack Complexity decreases because the connected system provides an easier path, (3) Privileges Required changes from High to None because the connected system has an auth bypass. Document original and re-scored CVSS with justification.

### RESCORE-003
- **Name**: Impact Amplification via Shared Resources
- **CIA**: C, I, A
- **NIST-800**: RA-3, RA-5
- **ISO-27001**: A.12.6.1
- **CMMC**: RA.L2-3.11.1, RA.L2-3.11.2
- **DoD-SRG**: SRG-APP-000141
- **FedRAMP**: RA-3 (Moderate), RA-5 (Moderate)
- **HIPAA**: §164.308(a)(1)(ii)(A) — Risk Analysis
- **PCI-DSS**: Req 6.3 — Vulnerability identification
- **SOC2**: CC3.2 — Risk assessment
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 6(1) — ICT risk management framework
- **EU-AI**: Art. 9(1) — Risk management system
- **Severity**: —
- **Statement**: When systems share resources (databases, user stores, file systems), the impact of a finding in one system shall be re-evaluated to include the other system's data and users.
- **Test**: If System A has a SQL injection affecting a shared database, the CVSS impact metrics must reflect the total data at risk across BOTH systems, not just System A's data. A finding with C:L in System A may become C:H when System B's sensitive data in the same database is included. Document the impact expansion.

---

## DATAFLOW — Inter-System Data Flow Security

### DATAFLOW-001
- **Name**: API Response Data Leakage to Frontend
- **CIA**: C
- **NIST-800**: AC-4, SC-8
- **ISO-27001**: A.13.2.1, A.14.1.3
- **CMMC**: AC.L2-3.1.3; SC.L2-3.13.8
- **DoD-SRG**: SRG-APP-000038; SRG-APP-000219
- **FedRAMP**: AC-4 (Moderate), SC-8 (Moderate)
- **HIPAA**: §164.312(e)(1) — Transmission Security; §164.312(a)(1) — Access Control
- **PCI-DSS**: Req 3.4 — Render PAN unreadable; Req 6.2.4 — Input validation
- **SOC2**: CC6.1 — Logical access; CC6.7 — Encryption
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(d) — Data protection
- **EU-AI**: Art. 15(4) — Cybersecurity (data protection)
- **Severity**: HIGH
- **Statement**: Excessive data returned by the API shall not be exposed to end users through the website's rendering logic.
- **Test**: If the API has an "Excessive Data Exposure" (BOPLA-001) finding, check whether the website renders or stores the full API response, or filters it server-side before rendering. If the website's JavaScript makes API calls directly and receives fields that should be restricted (internal IDs, hashed passwords, admin flags), the control fails.

### DATAFLOW-002
- **Name**: User Input Sanitization at System Boundary
- **CIA**: C, I
- **NIST-800**: SI-10, SI-15
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
- **Statement**: Each system shall independently validate and sanitize all input received from the other system, regardless of whether the sending system performs its own validation.
- **Test**: Identify where System A sends user-controlled data to System B (form submissions relayed to API, API responses rendered in website). If System B trusts System A's validation and does not re-validate, a bypass of System A's input validation would directly expose System B to injection. The control fails if either system relies on the other for input sanitization.

### DATAFLOW-003
- **Name**: Error Information Propagation
- **CIA**: C
- **NIST-800**: SI-11
- **ISO-27001**: A.12.1.4
- **CMMC**: SI.L2-3.14.1
- **DoD-SRG**: SRG-APP-000266
- **FedRAMP**: SI-11 (Moderate)
- **HIPAA**: §164.312(a)(1) — Access Control
- **PCI-DSS**: Req 6.2.5 — Error handling
- **SOC2**: CC7.2 — System monitoring
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(a) — ICT systems integrity
- **EU-AI**: Art. 15(4) — Cybersecurity
- **Severity**: MEDIUM
- **Statement**: Detailed error messages from System B shall not be propagated through System A to external users.
- **Test**: If the API has detailed error messages (stack traces, database error codes, internal paths) and the website passes API error responses directly to the user interface, the API's information leakage finding is amplified. The website acts as a conduit for the API's internal details. Check if the website catches and sanitizes error responses before rendering.

### DATAFLOW-004
- **Name**: Rate Limiting at Integration Point
- **CIA**: A
- **NIST-800**: SC-5, SI-10
- **ISO-27001**: A.12.1.3, A.14.1.3
- **CMMC**: SC.L2-3.13.1; SI.L2-3.14.2
- **DoD-SRG**: SRG-APP-000246
- **FedRAMP**: SC-5 (Moderate)
- **HIPAA**: §164.312(a)(1) — Access Control
- **PCI-DSS**: Req 6.2.4 — Input validation
- **SOC2**: CC6.1 — Logical access; CC6.8 — System availability
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(b) — Network security
- **EU-AI**: Art. 15(4) — Cybersecurity
- **Severity**: MEDIUM
- **Statement**: Rate limiting shall be enforced at the boundary between connected systems to prevent one system from being used to amplify denial-of-service attacks against the other.
- **Test**: If the API has a rate limiting finding but the website makes server-side calls to the API using a service account (not end-user tokens), the website may bypass the API's per-user rate limits. A single attacker hitting the website could generate thousands of API calls under the service account, bypassing API rate limits.

---

## SESSION — Cross-System Session Management

### SESSION-001
- **Name**: Session Consistency Across Systems
- **CIA**: C, I
- **NIST-800**: SC-23, AC-12
- **ISO-27001**: A.9.4.2
- **CMMC**: SC.L2-3.13.9; AC.L2-3.1.11
- **DoD-SRG**: SRG-APP-000295, SRG-APP-000220
- **FedRAMP**: SC-23 (Moderate), AC-12 (Moderate)
- **HIPAA**: §164.312(d) — Authentication
- **PCI-DSS**: Req 8.2.8 — Session timeout
- **SOC2**: CC6.1 — Logical access
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(c) — Session management
- **EU-AI**: Art. 15(4) — Cybersecurity
- **Severity**: HIGH
- **Statement**: Session invalidation in one system (logout, timeout, revocation) shall propagate to all connected systems.
- **Test**: Log out of System A. Attempt to use the session to access System B. If the session remains valid in System B after being invalidated in System A, the control fails. This also applies to token revocation — if System A revokes a JWT but System B still accepts it (no token revocation check), the control fails.

### SESSION-002
- **Name**: Session Scope Isolation
- **CIA**: C, I
- **NIST-800**: AC-4, SC-23
- **ISO-27001**: A.9.4.1
- **CMMC**: AC.L2-3.1.3; SC.L2-3.13.9
- **DoD-SRG**: SRG-APP-000038; SRG-APP-000295
- **FedRAMP**: AC-4 (Moderate), SC-23 (Moderate)
- **HIPAA**: §164.312(a)(1) — Access Control
- **PCI-DSS**: Req 7.2 — Restrict access by need-to-know
- **SOC2**: CC6.1 — Logical access; CC6.3 — Least privilege
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(c) — Access control
- **EU-AI**: Art. 15(4) — Cybersecurity
- **Severity**: MEDIUM
- **Statement**: A session's scope in System A shall not automatically extend to System B beyond what is explicitly authorized.
- **Test**: Authenticate with limited scope in System A (e.g., read-only user). Determine what access the session grants in System B via the integration. If the session scope is broader in System B than intended (e.g., read-only website session grants write access to API), the control fails.

---

## CRYPTO — Cross-System Cryptographic Controls

### CRYPTO-001
- **Name**: TLS Termination at Integration Boundary
- **CIA**: C
- **NIST-800**: SC-8, SC-8(1)
- **ISO-27001**: A.10.1.1, A.14.1.3
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
- **Statement**: Communication between connected systems shall be encrypted in transit, even when both systems are in the same network.
- **Test**: If System A communicates with System B over HTTP (not HTTPS) on an internal network, a network-level compromise (ARP spoofing, compromised switch) would expose all inter-system traffic. This is especially critical if either system has a network-level vulnerability. Check that TLS is enforced on all inter-system communication channels.

### CRYPTO-002
- **Name**: Shared Signing Key Isolation
- **CIA**: C, I
- **NIST-800**: SC-12, SC-12(1)
- **ISO-27001**: A.10.1.2
- **CMMC**: SC.L2-3.13.10, SC.L2-3.13.11
- **DoD-SRG**: SRG-APP-000219
- **FedRAMP**: SC-12 (Moderate)
- **HIPAA**: §164.312(e)(2)(ii) — Encryption
- **PCI-DSS**: Req 3.6 — Key management; Req 3.7 — Key rotation
- **SOC2**: CC6.1 — Logical access; CC6.7 — Encryption
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(d) — Cryptographic controls
- **EU-AI**: Art. 15(4) — Cybersecurity
- **Severity**: HIGH
- **Statement**: JWT signing keys, HMAC secrets, and encryption keys shall not be shared between systems unless explicitly required and documented.
- **Test**: If both systems use JWTs and share the same signing key, a JWT forged or stolen from System A is valid in System B. If either system has a token-related finding (weak algorithm, key exposure), the impact extends to both systems. Each system should use its own signing key, or a centralized key management service with per-system key scoping.

---

## CONFIG — Cross-System Configuration

### CONFIG-001
- **Name**: CORS Reciprocal Policy
- **CIA**: C, I
- **NIST-800**: AC-4, SC-7
- **ISO-27001**: A.14.1.3
- **CMMC**: AC.L2-3.1.3; SC.L2-3.13.1
- **DoD-SRG**: SRG-APP-000038; SRG-APP-000383
- **FedRAMP**: AC-4 (Moderate), SC-7 (Moderate)
- **HIPAA**: §164.312(e)(1) — Transmission Security
- **PCI-DSS**: Req 6.2.4 — Input validation
- **SOC2**: CC6.6 — System boundary protection
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(b) — Network security
- **EU-AI**: Art. 15(4) — Cybersecurity
- **Severity**: MEDIUM
- **Statement**: CORS policies between connected systems shall be mutually restrictive and not weaken either system's same-origin protections.
- **Test**: If the API sets `Access-Control-Allow-Origin: *` and the website calls it from a browser, any website (including malicious ones) can make credentialed requests to the API. If the API has a CORS finding, evaluate whether the website's presence changes the exploitability (e.g., the website's domain is trusted by the API, but the website has an XSS — the XSS can now be used to make cross-origin API calls from a trusted origin).

### CONFIG-002
- **Name**: Deployment Environment Consistency
- **CIA**: C, I, A
- **NIST-800**: CM-2, CM-6
- **ISO-27001**: A.14.2.1, A.12.1.4
- **CMMC**: CM.L2-3.4.1, CM.L2-3.4.2
- **DoD-SRG**: SRG-APP-000380, SRG-APP-000381
- **FedRAMP**: CM-2 (Moderate), CM-6 (Moderate)
- **HIPAA**: §164.308(a)(8) — Evaluation
- **PCI-DSS**: Req 2.2 — System configuration standards
- **SOC2**: CC8.1 — Change management
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(e) — Change management
- **EU-AI**: Art. 9(9) — Risk management (change control)
- **Severity**: LOW
- **Statement**: Connected systems shall maintain consistent security configurations (TLS versions, cipher suites, security headers) to prevent the weaker system from downgrading the overall security posture.
- **Test**: Compare security configurations between systems. If System A enforces TLS 1.3 but System B accepts TLS 1.0, the inter-system communication may negotiate to the weaker protocol. If System A has strict security headers but System B does not, iframes or redirects between them may bypass System A's protections.

---

## INCIDENT — Cross-System Incident Response

### INCIDENT-001
- **Name**: Cross-System Audit Trail Correlation
- **CIA**: I
- **NIST-800**: AU-3, AU-12, SI-4
- **ISO-27001**: A.12.4.1, A.12.4.3
- **CMMC**: AU.L2-3.3.1, AU.L2-3.3.2
- **DoD-SRG**: SRG-APP-000095, SRG-APP-000096
- **FedRAMP**: AU-3 (Low), AU-12 (Low)
- **HIPAA**: §164.312(b) — Audit Controls
- **PCI-DSS**: Req 10.2 — Audit log events; Req 10.6 — Log review
- **SOC2**: CC7.2 — System monitoring; CC7.3 — Detection of anomalies
- **SEC-FINRA**: SEC Cyber Rule §229.106 — Incident Disclosure
- **EU-DORA**: Art. 10(1) — Detection of anomalous activities
- **EU-AI**: Art. 12(1) — Record-keeping (logging)
- **Severity**: MEDIUM
- **Statement**: Audit logs from connected systems shall support end-to-end request tracing through correlation identifiers.
- **Test**: If both systems have logging findings (insufficient detail, missing authentication events), evaluate whether the combined logging gaps would make a cross-system attack chain undetectable. If System A logs the incoming request but not the outgoing API call, and System B logs the API call but not the originating user, the chain is invisible. Check for shared request/trace IDs.

### INCIDENT-002
- **Name**: Cross-System Alerting Coverage
- **CIA**: A
- **NIST-800**: IR-4, IR-5, SI-4
- **ISO-27001**: A.16.1.2, A.16.1.4
- **CMMC**: IR.L2-3.6.1, IR.L2-3.6.2
- **DoD-SRG**: SRG-APP-000516
- **FedRAMP**: IR-4 (Moderate), IR-5 (Moderate)
- **HIPAA**: §164.308(a)(6) — Security Incident Procedures
- **PCI-DSS**: Req 10.7 — Timely detection; Req 12.10 — Incident response plan
- **SOC2**: CC7.3 — Detection and response; CC7.4 — Incident response
- **SEC-FINRA**: SEC Cyber Rule §229.106 — Incident Disclosure
- **EU-DORA**: Art. 10(1) — Detection; Art. 17(1) — ICT incident reporting
- **EU-AI**: Art. 62 — Reporting of serious incidents
- **Severity**: LOW
- **Statement**: Security alerting shall cover cross-system attack patterns, not just single-system anomalies.
- **Test**: Determine if alerting rules in either system can detect activity that spans both systems. For example, if an attacker uses a stolen API token from System A to access System B, does System B's alerting trigger? If each system's alerts are siloed and no cross-system correlation exists, the control fails.

---

## SUPPLY — Third-Party and Supply Chain

### SUPPLY-001
- **Name**: Third-Party API Trust Validation
- **CIA**: C, I
- **NIST-800**: SA-4, SA-9, SR-3
- **ISO-27001**: A.15.1.1, A.15.2.1
- **CMMC**: SA.L2-3.12.1; SR.L2-3.17.1
- **DoD-SRG**: SRG-APP-000516
- **FedRAMP**: SA-4 (Moderate), SA-9 (Moderate)
- **HIPAA**: §164.308(b)(1) — Business Associate Contracts
- **PCI-DSS**: Req 12.8 — Third-party service provider management
- **SOC2**: CC9.2 — Vendor and third-party risk management
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 28(1) — ICT third-party risk; Art. 30 — Key contractual provisions
- **EU-AI**: Art. 10(6) — Data governance (third-party data)
- **Severity**: MEDIUM
- **Statement**: When one of the connected systems consumes a third-party API, vulnerabilities in that third-party integration shall be evaluated for impact on all connected systems.
- **Test**: If System A integrates with a third-party API and has an "Unsafe API Consumption" finding, evaluate whether malicious data from the third-party could propagate through System A to System B. If the third-party sends data that System A stores without sanitization and System B reads, the attack chain extends from the third-party through both systems.

### SUPPLY-002
- **Name**: Shared Dependency Vulnerability Correlation
- **CIA**: C, I, A
- **NIST-800**: SI-2, RA-5
- **ISO-27001**: A.12.6.1
- **CMMC**: SI.L2-3.14.1; RA.L2-3.11.2
- **DoD-SRG**: SRG-APP-000456
- **FedRAMP**: SI-2 (Low), RA-5 (Moderate)
- **HIPAA**: §164.308(a)(5)(ii)(B) — Protection from Malicious Software
- **PCI-DSS**: Req 6.3.3 — Patch management
- **SOC2**: CC7.1 — Vulnerability management
- **SEC-FINRA**: Reg S-P §248.30(a) — Safeguards Rule
- **EU-DORA**: Art. 9(4)(e) — Patch management
- **EU-AI**: Art. 15(3) — Robustness (vulnerability management)
- **Severity**: HIGH
- **Statement**: When connected systems share dependencies (libraries, frameworks, runtime versions), a known vulnerability in that dependency shall be flagged as affecting all connected systems.
- **Test**: If both systems have "Known Vulnerability" or "Dependency Pinning" findings, check for overlap. If both use the same vulnerable version of a library (e.g., both use log4j 2.14), the impact is amplified — patching one system without the other leaves the connection vulnerable. Flag shared vulnerable dependencies as a single cross-system finding.

---

## Control Summary

| Family | Controls | Focus |
|--------|----------|-------|
| **CHAIN** | 5 | Attack chain detection across system boundaries |
| **TRUST** | 5 | Shared trust boundary analysis and weakest-link evaluation |
| **RESCORE** | 3 | CVSS and reachability re-scoring based on connected context |
| **DATAFLOW** | 4 | Inter-system data flow security and sanitization |
| **SESSION** | 2 | Cross-system session management and propagation |
| **CRYPTO** | 2 | Cryptographic controls at integration boundaries |
| **CONFIG** | 2 | Cross-system configuration consistency |
| **INCIDENT** | 2 | Cross-system logging, alerting, and incident response |
| **SUPPLY** | 2 | Third-party and supply chain risk across connected systems |
| **Total** | **27** | |
