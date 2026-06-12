# OS & Software Vulnerability Controls Library

**Assessment type**: OS & Software Security Assessment
**Scope**: Local machine OS patch level, installed software CVE exposure, running services, and endpoint hardening
**Control count**: 12 controls across 5 families

---

## PATCH — Operating System & Software Patching

### PATCH-001
- **Name**: OS security updates current
- **Family**: PATCH
- **CIA**: C, I, A
- **NIST-800**: SI-2, SI-2(2)
- **ISO-27001**: A.12.6.1
- **CMMC**: SI.L2-3.14.4
- **CIS**: CIS Control 7.3 — Automated Operating System Patch Management
- **SOC2**: CC7.1 — Vulnerability management
- **Severity**: CRITICAL
- **Statement**: The operating system shall have all available security patches applied. No critical or high-severity OS security updates shall remain uninstalled.
- **Test**: Query the system's update mechanism for pending security updates. On Windows, check Windows Update for uninstalled critical and important updates. On Linux, check the package manager for available security-classified updates. If any security-classified updates are pending installation, the control fails.
- **Fix**: Apply all pending security updates immediately. Enable automatic security update installation where policy permits. Document any updates deferred with business justification and a remediation deadline no longer than 30 days.

### PATCH-002
- **Name**: Vulnerability patch SLA compliance
- **Family**: PATCH
- **CIA**: C, I, A
- **NIST-800**: SI-2(3), RA-3
- **ISO-27001**: A.12.6.1, A.16.1.3
- **CMMC**: SI.L2-3.14.4; RA.L2-3.11.3
- **CIS**: CIS Control 7.1 — Establish and Maintain a Vulnerability Management Process
- **SOC2**: CC7.1 — Vulnerability management
- **Severity**: HIGH
- **Statement**: A documented patch SLA shall define maximum remediation timelines by severity: critical vulnerabilities within 24–72 hours, high within 7 days, medium within 30 days, low within 90 days.
- **Test**: Request the organization's vulnerability management or patch management policy. Verify that severity-based patching timelines are defined in writing. Review the last 90 days of patch history and confirm critical and high CVEs were remediated within the stated SLA. Identify any CVEs that exceeded the SLA and determine whether exceptions were formally approved. Verify that the policy assigns ownership for tracking patch compliance.
- **Fix**: Define and publish a patch SLA policy covering all severity levels. Implement automated tracking to flag SLA breaches. Assign an owner for each unpatched CVE. Conduct monthly reviews of patch compliance metrics.

### PATCH-003
- **Name**: Installed software CVE exposure
- **Family**: PATCH
- **CIA**: C, I, A
- **NIST-800**: SI-2, RA-5
- **ISO-27001**: A.12.6.1
- **CMMC**: SI.L2-3.14.1; RA.L2-3.11.2
- **CIS**: CIS Control 7.4 — Manage Operating System Vulnerabilities
- **SOC2**: CC7.1 — Vulnerability management
- **Severity**: HIGH
- **Statement**: Installed software shall not contain known CVEs with a CVSS v3 score of 7.0 or higher. Any such CVE shall be tracked and remediated within the severity-appropriate patch SLA.
- **Test**: Enumerate all installed software packages with version numbers. For each package, query the NVD (nvd.nist.gov) or OSV (osv.dev) for known CVEs affecting that specific version. Flag any package with a critical (CVSS ≥9.0) or high (CVSS 7.0–8.9) severity CVE. Verify whether updated versions exist that resolve the CVE. Prioritize findings by CVSS score and exploit availability.
- **Fix**: Update or replace all software with critical or high CVEs to a patched version. Where no patch exists, apply vendor-recommended mitigations or remove the software if not business-critical. Subscribe to vendor security advisories for installed software.

---

## EOL — End-of-Life Detection

### EOL-001
- **Name**: Operating system end-of-life status
- **Family**: EOL
- **CIA**: C, I, A
- **NIST-800**: SA-22, SI-2
- **ISO-27001**: A.14.2.3
- **CMMC**: SI.L2-3.14.4; SA.L2-3.12.4
- **CIS**: CIS Control 2.3 — Address Unauthorized Software
- **SOC2**: CC6.8 — Malware protection
- **Severity**: CRITICAL
- **Statement**: The operating system shall be a vendor-supported version. End-of-life operating systems that no longer receive security updates shall not be in production use.
- **Test**: Identify the exact OS version and build number. Cross-reference the version against the vendor's official end-of-life date schedule (Microsoft Lifecycle Policy, Ubuntu LTS release schedule, Red Hat product lifecycle, etc.). If the current date is past the vendor-published end-of-support date, the control fails. Note whether Extended Security Updates (ESU) or paid extended support is in place as a mitigating control.
- **Fix**: Upgrade to a supported OS version. Plan migrations at least 12 months before EOL dates. If immediate upgrade is not possible, obtain paid extended security updates from the vendor and document the migration plan with a committed date.

### EOL-002
- **Name**: Installed software end-of-life status
- **Family**: EOL
- **CIA**: C, I
- **NIST-800**: SA-22
- **ISO-27001**: A.14.2.3, A.12.6.1
- **CMMC**: SA.L2-3.12.4
- **CIS**: CIS Control 2.7 — Use Only Supported Operating Systems and Applications
- **SOC2**: CC6.8 — Malware protection
- **Severity**: HIGH
- **Statement**: Installed software shall be supported by its vendor with active security updates. Software that has reached end-of-life and no longer receives security patches shall not be installed on production systems.
- **Test**: For each installed software package, check the vendor's support lifecycle page or the endoflife.date project (endoflife.date) for the specific version in use. Flag any software version that is past its security support end date and is not receiving vendor-provided security patches. Pay particular attention to runtimes (Java, Python, Node.js), web servers (Apache, IIS, Nginx), database engines, and browsers.
- **Fix**: Upgrade end-of-life software to a currently supported version. Where upgrade is not immediately possible, evaluate whether the software can be isolated, access-restricted, or removed. Document all EOL software with migration plans and target dates.

---

## SOFTINV — Software Inventory

### SOFTINV-001
- **Name**: Software inventory documented and current
- **Family**: SOFTINV
- **CIA**: C, I, A
- **NIST-800**: CM-8, CM-8(1)
- **ISO-27001**: A.8.1.1, A.8.1.2
- **CMMC**: CM.L2-3.4.1
- **CIS**: CIS Control 2.1 — Establish and Maintain a Software Inventory
- **SOC2**: CC6.1 — Logical access; CC7.1 — Vulnerability management
- **Severity**: MEDIUM
- **Statement**: A complete and current inventory of all authorized software installed on the system shall be maintained and reviewed at least quarterly.
- **Test**: Request the software inventory document or CMDB record for this system. Verify the inventory includes software name, version, vendor, license status, and installation date for all installed software. Compare the documented inventory against the actual installed software list to identify undocumented items. Confirm the inventory was reviewed or updated within the last 90 days. Verify that an approval process exists for adding new software to the authorized list.
- **Fix**: Create a software inventory using an automated discovery tool (e.g., SCCM, Ansible, osquery). Establish a quarterly review process. Define an approved software list and a process for authorizing new software. Integrate inventory management with the vulnerability management process.

### SOFTINV-002
- **Name**: Unauthorized software absent
- **Family**: SOFTINV
- **CIA**: C, I, A
- **NIST-800**: CM-7(5), CM-10
- **ISO-27001**: A.12.5.1
- **CMMC**: CM.L2-3.4.7
- **CIS**: CIS Control 2.5 — Allowlist Authorized Software
- **SOC2**: CC6.8 — Malware protection
- **Severity**: HIGH
- **Statement**: Only authorized software shall be installed on production systems. Software not approved through the change management process shall not be present.
- **Test**: Compare the list of installed software against the approved software inventory or baseline. Flag any installed software that does not appear in the authorized list. Pay particular attention to: remote access tools (TeamViewer, AnyDesk, ngrok), hacking tools or security research software installed on production systems, personal software (gaming, media, personal productivity), software installed by user accounts without administrative approval, and dual-use utilities (packet sniffers, port scanners) not required for the system's function.
- **Fix**: Remove all unauthorized software. Review and update the approved software list. Implement application allowlisting or AppLocker policies to prevent unauthorized software installation. Require administrator approval and change control documentation for all software additions.

---

## SVCCONFIG — Service Configuration & Hardening

### SVCCONFIG-001
- **Name**: Services run as least-privilege accounts
- **Family**: SVCCONFIG
- **CIA**: C, I, A
- **NIST-800**: AC-6, AC-6(1)
- **ISO-27001**: A.9.2.3, A.9.4.4
- **CMMC**: AC.L2-3.1.5; AC.L2-3.1.6
- **CIS**: CIS Control 5.4 — Restrict Administrator Privileges to Dedicated Administrator Accounts
- **SOC2**: CC6.3 — Least privilege
- **Severity**: HIGH
- **Statement**: Services and daemons shall run under dedicated least-privilege service accounts, not under SYSTEM, root, Administrator, or other highly privileged accounts unless technically required and documented.
- **Test**: Enumerate all running services and their associated user accounts. On Windows, check Service Control Manager for services running as SYSTEM, LocalSystem, or Administrator accounts. On Linux, check /etc/passwd and running process ownership for services running as root. Flag any service that runs as a highly privileged account where a less-privileged dedicated service account could be used. Document and justify any that must run with elevated privileges.
- **Fix**: Create dedicated service accounts for each service with only the minimum required permissions. On Windows, use Group Managed Service Accounts (gMSA) or virtual service accounts where possible. On Linux, create dedicated user accounts with no interactive login shell. Configure services to use these least-privilege accounts.

### SVCCONFIG-002
- **Name**: Unnecessary and insecure services disabled
- **Family**: SVCCONFIG
- **CIA**: C, I, A
- **NIST-800**: CM-7, CM-7(1)
- **ISO-27001**: A.12.5.1, A.13.1.1
- **CMMC**: CM.L2-3.4.6; CM.L2-3.4.7
- **CIS**: CIS Control 4.8 — Uninstall or Disable Unnecessary Services on Enterprise Assets
- **SOC2**: CC6.6 — System boundary protection
- **Severity**: HIGH
- **Statement**: Legacy, unnecessary, or inherently insecure network services shall be disabled or removed. Services that transmit data in cleartext (Telnet, FTP, rsh, rexec) shall not be running.
- **Test**: Enumerate all running services on the system. Check specifically for the following services that are enabled by default on some systems but are insecure or unnecessary: Telnet (TlntSvr on Windows, telnetd on Linux), FTP (FTPSVC / vsftpd / proftpd) if not required, TFTP server, RSH or rexec (remote shell without encryption), SNMP v1/v2 (cleartext community strings), SMBv1 (Windows), NFS with no_root_squash on Linux, and print spooler on non-print servers. Flag any of these services as running.
- **Fix**: Stop and disable all identified unnecessary services. On Windows, use sc config [service] start=disabled. On Linux, use systemctl disable [service] and systemctl stop [service]. Remove the service packages if the service is not needed. For required services using insecure protocols, replace with secure alternatives (SFTP instead of FTP, SSH instead of Telnet).

---

## SVCEXPOSE — Network Service Exposure

### SVCEXPOSE-001
- **Name**: Listening network services minimized
- **Family**: SVCEXPOSE
- **CIA**: C, I, A
- **NIST-800**: CM-7, SC-7
- **ISO-27001**: A.13.1.1, A.13.1.3
- **CMMC**: CM.L2-3.4.6; SC.L2-3.13.1
- **CIS**: CIS Control 4.4 — Implement and Manage a Firewall on Servers
- **SOC2**: CC6.6 — System boundary protection
- **Severity**: MEDIUM
- **Statement**: The system shall expose the minimum necessary network services. All listening ports shall correspond to an authorized, documented service.
- **Test**: Run netstat -ano (Windows) or ss -tlnp (Linux) to enumerate all listening TCP and UDP ports. For each listening port, identify the associated process and service. Cross-reference listening ports against the authorized service list. Flag any port that is not associated with a documented business requirement. Pay particular attention to: ports in the range 1024–65535 bound on 0.0.0.0 (all interfaces), database ports (1433, 3306, 5432, 27017) accessible beyond localhost, management interfaces (WMI, WinRM port 5985/5986, SNMP 161) exposed on network-accessible interfaces.
- **Fix**: Disable or stop services bound to unauthorized ports. Configure services to bind to 127.0.0.1 only where external access is not required. Implement host-based firewall rules to block unauthorized inbound connections. Document all authorized listening ports in the system's network baseline.

### SVCEXPOSE-002
- **Name**: Remote management services secured
- **Family**: SVCEXPOSE
- **CIA**: C, I, A
- **NIST-800**: AC-17, SC-8
- **ISO-27001**: A.6.2.2, A.9.4.2, A.13.1.1
- **CMMC**: AC.L2-3.1.12; SC.L2-3.13.8
- **CIS**: CIS Control 12.3 — Securely Manage Network Infrastructure
- **SOC2**: CC6.6 — System boundary protection; CC6.1 — Logical access
- **Severity**: HIGH
- **Statement**: Remote management services (RDP, SSH, WinRM, VNC) shall be configured securely: exposed only to authorized source addresses, using strong authentication, with logging enabled, and accessible only through approved pathways such as a VPN or bastion host.
- **Test**: Identify all remote management services running (RDP on port 3389, SSH on port 22, WinRM on 5985/5986, VNC on 5900). For each service, determine whether it is accessible from the internet or only from internal/VPN networks. Check RDP for Network Level Authentication (NLA) enforcement. Check SSH for password authentication disabled (keys only). Check whether account lockout is configured for authentication failures on these services. Verify that connection logging is enabled. Check whether access is restricted by source IP or only reachable through a VPN or jump server.
- **Fix**: Restrict remote management service access to specific source IP ranges or require VPN connectivity before access is possible. Enable NLA on RDP. Disable SSH password authentication and require key-based authentication. Enable account lockout after 5 failed attempts. Enable and retain logs for all remote management sessions. Consider placing all remote management services behind a bastion host or PAM solution.

---

## OSAUDIT — OS Audit Logging

### OSAUDIT-001
- **Name**: OS audit logging enabled and retained
- **Family**: OSAUDIT
- **CIA**: I
- **NIST-800**: AU-2, AU-3, AU-12
- **ISO-27001**: A.12.4.1, A.12.4.3
- **CMMC**: AU.L2-3.3.1; AU.L2-3.3.2
- **CIS**: CIS Control 8.2 — Collect Audit Logs
- **SOC2**: CC7.2 — System monitoring; CC7.3 — Detection
- **Severity**: MEDIUM
- **Statement**: OS-level audit logging shall be enabled and configured to record security-relevant events: logon and logoff, privilege escalation, account management changes, process creation, and object access. Logs shall be retained for a minimum of 90 days.
- **Test**: On Windows, open Event Viewer and verify Security log is enabled. Check the audit policy via auditpol /get /category:* and confirm at minimum these categories are auditing success and failure: Logon/Logoff, Account Management, Privilege Use, Process Tracking. Check log retention settings and confirm Security log maximum size and retention policy. On Linux, verify auditd is running via systemctl status auditd and check /etc/audit/audit.rules for rules covering authentication events (execve, open, chmod, chown). Verify log centralization to a SIEM or log collector.
- **Fix**: Enable OS auditing for all required categories. On Windows, use Group Policy or auditpol to configure the audit policy. On Linux, install and configure auditd with a ruleset aligned to CIS or DISA STIG recommendations. Configure log forwarding to a centralized SIEM. Set retention to a minimum of 90 days locally and 12 months in the SIEM.

---

## Control Summary

| Family | Controls | Focus |
|--------|----------|-------|
| **PATCH** | 3 | OS and software patching, CVE remediation |
| **EOL** | 2 | End-of-life OS and software detection |
| **SOFTINV** | 2 | Software inventory and unauthorized software |
| **SVCCONFIG** | 2 | Service hardening and least privilege |
| **SVCEXPOSE** | 2 | Network service exposure and remote access |
| **OSAUDIT** | 1 | OS-level audit logging and retention |
| **Total** | **12** | |
