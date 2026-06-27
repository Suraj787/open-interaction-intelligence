"""Interaction Specification Graph: load, validate, query.

Structured files (nodes + edges), no database. Queries surface real gaps such as
screens lacking error recovery or tasks lacking feedback.
"""
from __future__ import annotations
from . import data


def load():
    nodes = {d["id"]: d for _, d in data.load_kind("graph-nodes")}
    edges = [d for _, d in data.load_kind("graph-edges")]
    return nodes, edges


def validate() -> list[str]:
    nodes, edges = load()
    errs: list[str] = []
    for e in edges:
        if e["from"] not in nodes:
            errs.append(f"edge {e['from']}->{e['to']}: 'from' node missing")
        if e["to"] not in nodes:
            errs.append(f"edge {e['from']}->{e['to']}: 'to' node missing")
    return errs


def _nodes_of_type(nodes, t):
    return [n for n in nodes.values() if n["type"] == t]


def _has_edge(edges, frm=None, to=None, relation=None, to_type=None, nodes=None):
    for e in edges:
        if frm is not None and e["from"] != frm:
            continue
        if to is not None and e["to"] != to:
            continue
        if relation is not None and e["relation"] != relation:
            continue
        if to_type is not None and nodes is not None:
            tgt = nodes.get(e["to"])
            if not tgt or tgt["type"] != to_type:
                continue
        return True
    return False


QUERIES = {
    "screens-without-error-recovery":
        "Screens that have no linked error/permission-denied state",
    "tasks-without-feedback":
        "Tasks with no linked feedback pattern or success/error state",
    "components-violating-genome":
        "Components flagged conflicts-with a constraint",
    "effects-conflicting-reduced-motion":
        "Effects with a conflicts-with edge to a reduced-motion constraint",
    "workflows-without-offline":
        "Workflows with no linked offline state",
    "states-without-tests":
        "State nodes with no validated-by/evidenced-by test edge",
}


def query(name: str) -> list[str]:
    nodes, edges = load()
    findings: list[str] = []
    if name == "screens-without-error-recovery":
        for s in _nodes_of_type(nodes, "screen"):
            ok = False
            for e in edges:
                if e["from"] == s["id"] and e["relation"] == "has-state":
                    tgt = nodes.get(e["to"], {})
                    if "error" in tgt.get("id", "") or "error" in str(tgt.get("attributes", {})).lower() \
                       or "permission" in tgt.get("id", ""):
                        ok = True
            if not ok:
                findings.append(s["id"])
    elif name == "tasks-without-feedback":
        for t in _nodes_of_type(nodes, "task"):
            has_fb = any(e["from"] == t["id"] and e["relation"] in ("solves", "produces", "validated-by")
                         for e in edges)
            if not has_fb:
                findings.append(t["id"])
    elif name == "components-violating-genome":
        for e in edges:
            if e["relation"] == "conflicts-with":
                tgt = nodes.get(e["to"], {})
                frm = nodes.get(e["from"], {})
                if frm.get("type") == "component" and tgt.get("type") == "constraint":
                    findings.append(e["from"])
    elif name == "effects-conflicting-reduced-motion":
        for e in edges:
            if e["relation"] == "conflicts-with":
                frm = nodes.get(e["from"], {})
                tgt = nodes.get(e["to"], {})
                if frm.get("type") == "effect" and "reduced-motion" in tgt.get("id", ""):
                    findings.append(e["from"])
    elif name == "workflows-without-offline":
        for w in _nodes_of_type(nodes, "workflow"):
            has_offline = any(
                e["from"] == w["id"] and "offline" in nodes.get(e["to"], {}).get("id", "")
                for e in edges)
            if not has_offline:
                findings.append(w["id"])
    elif name == "states-without-tests":
        for s in _nodes_of_type(nodes, "state"):
            tested = any(e["from"] == s["id"] and e["relation"] in ("validated-by", "evidenced-by")
                         for e in edges)
            if not tested:
                findings.append(s["id"])
    else:
        raise KeyError(name)
    return findings
