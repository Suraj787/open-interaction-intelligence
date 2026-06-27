"""Interface Intelligence OS layer tests (pytest mirror of tools/ii_selfcheck.py)."""
import tempfile
import pathlib
from ii import cli, data, graph, originality, states, debt, genome


def test_ii_validate_ok():
    assert cli.main(["validate"]) == 0


def test_engine_data_no_errors():
    _counts, errs = data.validate_all_data()
    assert not errs, errs[:5]


def test_engine_data_present():
    counts, _ = data.validate_all_data()
    assert counts.get("styles", 0) >= 10
    assert counts.get("layouts", 0) >= 10
    assert counts.get("industry-packs", 0) >= 10
    assert counts.get("state-requirements", 0) >= 10


def test_graph_valid_and_queries():
    assert not graph.validate()
    assert len(graph.query("screens-without-error-recovery")) >= 1
    for q in graph.QUERIES:
        assert isinstance(graph.query(q), list)


def test_states_completeness():
    m = dict(states.matrix())
    assert len(m) >= 10
    r = states.validate_states("data-fetch-region", ["loading", "success"])
    assert not r["ok"] and "error" in r["missing"]


def test_originality_detector(tmp_path):
    g = tmp_path / "hero.html"
    g.write_text('<div class="bg-gradient-to-r from-purple-500 backdrop-blur rounded-3xl">Supercharge your workflow</div>')
    _f, score, _b = originality.audit_path(g)
    assert score > 0
    c = tmp_path / "plain.html"
    c.write_text("<table><tr><td>Invoice</td></tr></table>")
    _f2, clean, _b2 = originality.audit_path(c)
    assert clean == 0


def test_interface_debt(tmp_path):
    f = tmp_path / "c.css"
    f.write_text(".x{color:#ff0033 !important}")
    d = debt.calculate(tmp_path)
    assert d.score > 0
    assert "hex-colour-inline" in d.by_category


def test_genome_ops():
    assert not [e for e in genome.validate("enterprise-pm-genome") if "no genome" not in e]
    assert len(genome.explain("enterprise-pm-genome")) > 1


def test_cli_smoke():
    assert cli.main(["motion", "validate"]) == 0
    assert cli.main(["density", "validate"]) == 0
    assert cli.main(["context", "validate"]) == 0
    assert cli.main(["states", "matrix"]) == 0
    assert cli.main(["search", "save"]) == 0  # delegation to motif
