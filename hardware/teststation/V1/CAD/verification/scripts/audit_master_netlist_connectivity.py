#!/usr/bin/env python3
"""Triage the current KiCad XML netlist without treating it as approved wiring.

The known U19/U2 nets are intentionally reported as BLOCKED. This script does
not modify the schematic and never turns suspicious connectivity into approval.
"""
from __future__ import annotations

import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

EXPECTED_COMPONENTS = 24
EXPECTED_NETS = 165
CRITICAL_NETS = {
    "Net-(U19-GND)": {("U19", "3"), ("U2", "17")},
    "Net-(U19-IN-)": {("U19", "2"), ("U2", "20")},
    "Net-(U19-VS)": {("U19", "8"), ("U2", "19")},
}


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: audit_master_netlist_connectivity.py NETLIST.xml REPORT.md", file=sys.stderr)
        return 2

    netlist_path = Path(sys.argv[1])
    report_path = Path(sys.argv[2])
    if not netlist_path.is_file():
        print(f"ERROR: netlist not found: {netlist_path}", file=sys.stderr)
        return 2

    try:
        root = ET.parse(netlist_path).getroot()
    except (ET.ParseError, OSError) as exc:
        print(f"ERROR: cannot parse KiCad XML netlist: {exc}", file=sys.stderr)
        return 2

    components = root.findall(".//components/comp")
    nets = root.findall(".//nets/net")
    observed = {}
    multi = []
    for net in nets:
        name = net.get("name", "")
        nodes = net.findall("node")
        node_set = {(node.get("ref", ""), node.get("pin", "")) for node in nodes}
        observed[name] = node_set
        if len(nodes) > 1:
            multi.append((name, nodes))

    critical_found = [name for name, expected in CRITICAL_NETS.items() if observed.get(name) == expected]
    if len(critical_found) == len(CRITICAL_NETS):
        status = "BLOCKED_KNOWN_SUSPICIOUS_CONNECTIONS"
    else:
        status = "REVIEW_REQUIRED_NETLIST_CHANGED"

    lines = [
        "# Master schematic netlist connectivity triage",
        "",
        f"- Components: {len(components)} (baseline expectation: {EXPECTED_COMPONENTS})",
        f"- Nets: {len(nets)} (baseline expectation: {EXPECTED_NETS})",
        f"- Multi-node nets: {len(multi)}",
        f"- Known suspicious U19/U2 connections detected: {len(critical_found)}/{len(CRITICAL_NETS)}",
        f"- Connectivity status: **{status}**",
        "",
        "This is automated triage, not circuit approval. A changed netlist requires manual review; this checker never infers intended wiring.",
        "",
        "## Multi-node nets",
        "",
        "| Net | Nodes |",
        "|---|---|",
    ]
    for name, nodes in multi:
        node_text = "; ".join(
            f"{node.get('ref')} pin {node.get('pin')} ({node.get('pinfunction', '?')}; {node.get('pintype', '?')})"
            for node in nodes
        )
        lines.append(f"| {name} | {node_text} |")

    lines += [
        "",
        "## Known high-priority unresolved connections",
        "",
        "| Net | Expected observed nodes | Triage |",
        "|---|---|---|",
    ]
    for name, expected in CRITICAL_NETS.items():
        actual = sorted(observed.get(name, set()))
        expected_text = ", ".join(f"{ref}.{pin}" for ref, pin in sorted(expected))
        actual_text = ", ".join(f"{ref}.{pin}" for ref, pin in actual) or "(net absent)"
        finding = "PRESENT — do not suppress or accept without reviewed intent" if name in critical_found else "NOT MATCHED — review netlist change"
        lines.append(f"| {name} | expected {expected_text}; actual {actual_text} | {finding} |")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
            output.write(f"connectivity_status={status}\n")
            output.write(f"netlist_components={len(components)}\n")
            output.write(f"netlist_nets={len(nets)}\n")
            output.write(f"netlist_multi_node={len(multi)}\n")
            output.write(f"critical_connections={len(critical_found)}\n")

    print(f"NETLIST_COMPONENTS={len(components)}")
    print(f"NETLIST_NETS={len(nets)}")
    print(f"NETLIST_MULTI_NODE={len(multi)}")
    print(f"CRITICAL_CONNECTIONS={len(critical_found)}/{len(CRITICAL_NETS)}")
    print(f"CONNECTIVITY_STATUS={status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
