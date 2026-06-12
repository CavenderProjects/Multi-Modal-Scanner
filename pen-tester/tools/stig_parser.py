#!/usr/bin/env python3
"""
DISA STIG XCCDF Parser — Converts STIG XML files into pen-tester controls library format.

Accepts DISA STIG XCCDF 1.1 XML files (the standard format from https://cyber.mil/stigs/)
and produces a Markdown controls library compatible with the pen-tester skill's assessment workflows.

Usage:
    python stig_parser.py <stig_xccdf.xml> [--output <output.md>] [--profile <profile_id>] [--format md|json]

The parser extracts:
    - Benchmark metadata (title, version, release date, description)
    - All Rule/Group entries with: Vuln ID, Rule ID, version, severity, title,
      VulnDiscussion, SRG references, CCI identifiers, fix text, check content
    - MAC/Confidentiality profiles and their rule selections
    - Maps STIG severities (CAT I/II/III) to CRITICAL/HIGH/MEDIUM/LOW
"""

import xml.etree.ElementTree as ET
import argparse
import json
import re
import sys
import os
from datetime import datetime


# XCCDF 1.1 namespace
NS = {
    'x': 'http://checklists.nist.gov/xccdf/1.1',
    'dc': 'http://purl.org/dc/elements/1.1/',
}

# Severity mapping: STIG severity → pen-tester severity
SEVERITY_MAP = {
    'high': 'CRITICAL',
    'medium': 'HIGH',
    'low': 'MEDIUM',
}

# Reverse for display
CAT_MAP = {
    'high': 'CAT I',
    'medium': 'CAT II',
    'low': 'CAT III',
}


def parse_stig(xml_path, profile_id=None):
    """Parse a DISA STIG XCCDF XML file and return structured data."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Benchmark metadata
    benchmark = {
        'id': root.get('id', ''),
        'title': _text(root, 'x:title'),
        'description': _text(root, 'x:description'),
        'version': _text(root, 'x:version'),
        'release_info': '',
        'date': '',
        'publisher': '',
        'source': '',
    }

    # Release info
    for pt in root.findall('x:plain-text', NS):
        if pt.get('id') == 'release-info':
            benchmark['release_info'] = pt.text or ''
            # Extract date from "Release: 1 Benchmark Date: 27 May 2025"
            date_match = re.search(r'Benchmark Date:\s*(.+)', pt.text or '')
            if date_match:
                benchmark['date'] = date_match.group(1).strip()

    # Reference
    ref = root.find('x:reference', NS)
    if ref is not None:
        benchmark['publisher'] = _text(ref, 'dc:publisher')
        benchmark['source'] = _text(ref, 'dc:source')

    # Profiles
    profiles = []
    for p in root.findall('x:Profile', NS):
        pid = p.get('id', '')
        ptitle = _text(p, 'x:title')
        selected = [s.get('idref') for s in p.findall('x:select', NS) if s.get('selected') == 'true']
        profiles.append({'id': pid, 'title': ptitle, 'selected_rules': selected})

    # Determine which rules are in scope (if profile specified)
    in_scope = None
    if profile_id:
        for p in profiles:
            if p['id'] == profile_id:
                in_scope = set(p['selected_rules'])
                break
        if in_scope is None:
            print(f"Warning: Profile '{profile_id}' not found. Using all rules.", file=sys.stderr)

    # Parse rules
    rules = []
    for group in root.findall('.//x:Group', NS):
        gid = group.get('id', '')  # Vuln ID (V-XXXXXX)

        # Profile filtering
        if in_scope is not None and gid not in in_scope:
            continue

        gtitle = _text(group, 'x:title')  # SRG reference

        rule_el = group.find('x:Rule', NS)
        if rule_el is None:
            continue

        rule = _parse_rule(rule_el, gid, gtitle)
        rules.append(rule)

    return {
        'benchmark': benchmark,
        'profiles': profiles,
        'rules': rules,
        'stats': {
            'total_rules': len(rules),
            'cat_i': sum(1 for r in rules if r['stig_severity'] == 'high'),
            'cat_ii': sum(1 for r in rules if r['stig_severity'] == 'medium'),
            'cat_iii': sum(1 for r in rules if r['stig_severity'] == 'low'),
        }
    }


def _parse_rule(rule_el, vuln_id, srg_title):
    """Parse a single XCCDF Rule element."""
    severity = rule_el.get('severity', 'medium')
    rule_id = rule_el.get('id', '')

    # Description contains VulnDiscussion and other structured XML-like content
    desc_raw = _text(rule_el, 'x:description')

    # Extract VulnDiscussion
    vuln_disc = ''
    vd_match = re.search(r'<VulnDiscussion>(.*?)</VulnDiscussion>', desc_raw, re.DOTALL)
    if vd_match:
        vuln_disc = vd_match.group(1).strip()

    # Extract SRG references from VulnDiscussion
    srg_refs = re.findall(r'SRG-APP-\d+', desc_raw)

    # Extract Satisfies line (additional SRGs)
    satisfies = []
    sat_match = re.search(r'Satisfies:\s*(.*?)(?:<|$)', vuln_disc, re.DOTALL)
    if sat_match:
        satisfies = re.findall(r'SRG-APP-\d+', sat_match.group(1))

    # CCI identifiers
    ccis = []
    for ident in rule_el.findall('x:ident', NS):
        system = ident.get('system', '')
        if 'cci' in system.lower():
            ccis.append(ident.text)

    # Fix text
    fixtext_el = rule_el.find('x:fixtext', NS)
    fixtext = fixtext_el.text.strip() if fixtext_el is not None and fixtext_el.text else ''

    # Check content
    check_content = ''
    check_el = rule_el.find('.//x:check-content', NS)
    if check_el is not None and check_el.text:
        check_content = check_el.text.strip()

    # Reference/DPMS Target
    dpms_target = ''
    dpms_id = ''
    ref_el = rule_el.find('x:reference', NS)
    if ref_el is not None:
        dpms_target = _text(ref_el, 'dc:subject')
        dpms_id = _text(ref_el, 'dc:identifier')

    # Clean VulnDiscussion — remove the Satisfies line for the statement
    statement = vuln_disc
    if sat_match:
        statement = vuln_disc[:sat_match.start()].strip()

    # Map severity
    mapped_severity = SEVERITY_MAP.get(severity, 'MEDIUM')
    cat = CAT_MAP.get(severity, 'CAT II')

    # Determine CIA impact from description keywords
    cia = _infer_cia(statement, _text(rule_el, 'x:title'))

    return {
        'vuln_id': vuln_id,
        'rule_id': rule_id,
        'version': _text(rule_el, 'x:version'),
        'srg_title': srg_title,
        'title': _text(rule_el, 'x:title'),
        'statement': statement,
        'stig_severity': severity,
        'mapped_severity': mapped_severity,
        'cat': cat,
        'cia': cia,
        'srg_refs': list(set(srg_refs)),
        'satisfies': satisfies,
        'ccis': ccis,
        'fixtext': fixtext,
        'check_content': check_content,
        'dpms_target': dpms_target,
        'dpms_id': dpms_id,
    }


def _infer_cia(statement, title):
    """Infer CIA classification from rule description keywords."""
    text = (statement + ' ' + title).lower()
    cia = []

    # Confidentiality indicators
    if any(w in text for w in ['encrypt', 'tls', 'ssl', 'certificate', 'credential',
                                'password', 'authentication', 'confidential', 'pii',
                                'sensitive data', 'disclosure', 'privacy', 'banner',
                                'identity provider', 'siem', 'audit', 'log']):
        cia.append('C')

    # Integrity indicators
    if any(w in text for w in ['integrity', 'tamper', 'modify', 'certificate', 'tls',
                                'digital signature', 'hash', 'checksum', 'update',
                                'patch', 'version', 'configuration']):
        cia.append('I')

    # Availability indicators
    if any(w in text for w in ['availability', 'timeout', 'session', 'denial',
                                'database', 'port', 'protocol', 'service',
                                'disable', 'function']):
        cia.append('A')

    return ', '.join(cia) if cia else 'C, I'  # Default to C, I if can't determine


def _text(parent, tag):
    """Get text of a child element, or empty string."""
    el = parent.find(tag, NS)
    return (el.text or '').strip() if el is not None else ''


def to_markdown(parsed, include_profiles=False):
    """Convert parsed STIG data to Markdown controls library format."""
    b = parsed['benchmark']
    rules = parsed['rules']
    stats = parsed['stats']

    lines = []
    lines.append(f'# STIG Controls Library: {b["title"]}')
    lines.append('')
    lines.append('## Overview')
    lines.append('')
    lines.append(f'This library was auto-generated from a DISA STIG XCCDF file.')
    lines.append(f'It contains **{stats["total_rules"]} security controls** derived from the STIG.')
    lines.append('')
    lines.append('| Field | Value |')
    lines.append('|---|---|')
    lines.append(f'| **STIG Title** | {b["title"]} |')
    lines.append(f'| **STIG ID** | {b["id"]} |')
    lines.append(f'| **Version** | {b["version"]} |')
    lines.append(f'| **Release** | {b["release_info"]} |')
    lines.append(f'| **Publisher** | {b["publisher"]} |')
    lines.append(f'| **Source** | {b["source"]} |')
    lines.append(f'| **Import Date** | {datetime.now().strftime("%Y-%m-%d %H:%M")} |')
    lines.append('')
    lines.append('### Severity Distribution')
    lines.append('')
    lines.append(f'| Category | Count | Mapped Severity |')
    lines.append(f'|---|---|---|')
    lines.append(f'| **CAT I** (High) | {stats["cat_i"]} | CRITICAL |')
    lines.append(f'| **CAT II** (Medium) | {stats["cat_ii"]} | HIGH |')
    lines.append(f'| **CAT III** (Low) | {stats["cat_iii"]} | MEDIUM |')
    lines.append(f'| **Total** | {stats["total_rules"]} | — |')
    lines.append('')

    if include_profiles and parsed['profiles']:
        lines.append('### Available Profiles')
        lines.append('')
        lines.append('| Profile ID | Title | Rules |')
        lines.append('|---|---|---|')
        for p in parsed['profiles']:
            lines.append(f'| {p["id"]} | {p["title"]} | {len(p["selected_rules"])} |')
        lines.append('')

    lines.append('### Framework References')
    lines.append('')
    lines.append('Each control maps to:')
    lines.append('- **SRG**: Security Requirements Guide application controls (SRG-APP-XXXXXX)')
    lines.append('- **CCI**: Control Correlation Identifier (CCI-XXXXXX) — maps to NIST SP 800-53')
    lines.append('- **STIG**: Product-specific rule version (e.g., CYLN-OP-000010)')
    lines.append('')
    lines.append('---')
    lines.append('')

    # Rules
    lines.append('## Controls')
    lines.append('')

    for i, rule in enumerate(rules, 1):
        lines.append(f'### {rule["vuln_id"]}')
        lines.append(f'- **Control ID**: {rule["version"]}')
        lines.append(f'- **Name**: {rule["title"]}')
        lines.append(f'- **Vuln ID**: {rule["vuln_id"]}')
        lines.append(f'- **Rule ID**: {rule["rule_id"]}')
        lines.append(f'- **SRG**: {rule["srg_title"]}')
        lines.append(f'- **STIG Severity**: {rule["cat"]} ({rule["stig_severity"].upper()})')
        lines.append(f'- **Mapped Severity**: {rule["mapped_severity"]}')
        lines.append(f'- **CIA**: {rule["cia"]}')

        if rule['ccis']:
            cci_str = ', '.join(rule['ccis'][:5])
            if len(rule['ccis']) > 5:
                cci_str += f' (+{len(rule["ccis"]) - 5} more)'
            lines.append(f'- **CCIs**: {cci_str}')

        if rule['satisfies']:
            lines.append(f'- **Also Satisfies**: {", ".join(rule["satisfies"])}')

        lines.append(f'- **Statement**: {rule["statement"]}')
        lines.append(f'- **Check**: {rule["check_content"]}')
        lines.append(f'- **Fix**: {rule["fixtext"]}')
        lines.append('')

    # Footer
    lines.append('---')
    lines.append('')
    lines.append(f'*Total Controls: {stats["total_rules"]}*')
    lines.append(f'*CAT I: {stats["cat_i"]}, CAT II: {stats["cat_ii"]}, CAT III: {stats["cat_iii"]}*')
    lines.append(f'*Generated from: {b["title"]} v{b["version"]}*')

    return '\n'.join(lines)


def to_json(parsed):
    """Convert parsed STIG data to JSON format."""
    return json.dumps(parsed, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description='Parse DISA STIG XCCDF XML into pen-tester controls format')
    parser.add_argument('xml_file', help='Path to STIG XCCDF XML file')
    parser.add_argument('--output', '-o', help='Output file path (default: stdout)')
    parser.add_argument('--profile', '-p', help='Profile ID to filter rules (default: all rules)')
    parser.add_argument('--format', '-f', choices=['md', 'json'], default='md',
                        help='Output format: md (Markdown) or json (default: md)')
    parser.add_argument('--profiles', action='store_true',
                        help='Include profile listing in output')

    args = parser.parse_args()

    if not os.path.exists(args.xml_file):
        print(f"Error: File not found: {args.xml_file}", file=sys.stderr)
        sys.exit(1)

    parsed = parse_stig(args.xml_file, profile_id=args.profile)

    if args.format == 'json':
        output = to_json(parsed)
    else:
        output = to_markdown(parsed, include_profiles=args.profiles)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Written to {args.output} ({parsed['stats']['total_rules']} rules)", file=sys.stderr)
    else:
        print(output)


if __name__ == '__main__':
    main()
