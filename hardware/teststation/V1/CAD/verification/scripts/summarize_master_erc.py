#!/usr/bin/env python3
"""Create a deterministic, non-prescriptive summary of a KiCad ERC report."""
from __future__ import annotations
import re, sys
from collections import Counter, defaultdict
from pathlib import Path
RULE = re.compile(r'^\\[([a-z0-9_]+)\\]:\\s*(.+)$')
SYMBOL = re.compile(r'Symbol\\s+([A-Za-z0-9_]+)\\s+Pin\\s+([0-9]+)\\s+\\[([^\\]]+)\\]')
LABEL = re.compile(r"Label\\s+'([^']+)'")
WIRE = re.compile(r'(Horizontal|Vertical) Wire, length ([0-9.]+) mm')
def summarize(report: str) -> str:
    counts = Counter()
    affected = defaultdict(set)
    current = None
    severity = 'unknown'
    for line in report.splitlines():
        match = RULE.match(line.strip())
        if match:
            current = (match.group(1), match.group(2))
            continue
        stripped = line.strip()
        if stripped == '; error':
            severity = 'error'; continue
        if stripped == '; warning':
            severity = 'warning'; continue
        if current is None or not stripped.startswith('@'):
            continue
        counts[(severity, current[0])] += 1
        symbol, label, wire = SYMBOL.search(stripped), LABEL.search(stripped), WIRE.search(stripped)
        if symbol:
            affected[(severity, current[0])].add(f'{symbol.group(1)} pin {symbol.group(2)} [{symbol.group(3)}]')
        elif label:
            affected[(severity, current[0])].add(f'label {label.group(1)}')
        elif wire:
            affected[(severity, current[0])].add(f'{wire.group(1).lower()} wire endpoint ({wire.group(2)} mm)')
        else:
            affected[(severity, current[0])].add(stripped)
    match = re.search(r'\\*\\*\\s*ERC messages:\\s*(\\d+)\\s+Errors\\s+(\\d+)\\s+Warnings\\s+(\\d+)', report)
    if not match:
        raise ValueError('KiCad ERC total summary not found')
    total, errors, warnings = map(int, match.groups())
    if sum(counts.values()) != total:
        raise ValueError(f'parsed {sum(counts.values())} issue locations but ERC summary reports {total}')
    out = ['# M2.9-K master schematic ERC triage', '', f'- Total ERC messages: **{total}** ({errors} errors, {warnings} warnings)', '- Classification of KiCad report only; not a circuit repair or approval.', '- Multiple ERC messages may describe the same underlying open net; do not count each as an independent root cause.', '', '## Counts by rule', '', '| Severity | Rule | Count |', '|---|---|---:|']
    for (level, rule), count in sorted(counts.items()):
        out.append(f'| {level} | {rule} | {count} |')
    out += ['', '## Affected references and labels', '']
    for (level, rule), items in sorted(affected.items()):
        out.append(f'### {level}: {rule}')
        out.extend(f'- {item}' for item in sorted(items))
        out.append('')
    out += ['## Review boundary', '', 'This report does not infer intended wiring, assign missing nets, suppress ERC checks, or approve footprints. Resolve root causes against the approved interface register and manufacturer pin tables, then regenerate netlist and ERC.', '']
    return '\\n'.join(out)
def main() -> int:
    if len(sys.argv) != 3:
        print('usage: summarize_master_erc.py INPUT.rpt OUTPUT.md', file=sys.stderr); return 2
    source, target = map(Path, sys.argv[1:])
    try:
        target.write_text(summarize(source.read_text(encoding='utf-8', errors='replace')), encoding='utf-8')
    except (OSError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr); return 1
    print(f'PASS ERC triage summary: {target}'); return 0
if __name__ == '__main__':
    raise SystemExit(main())
