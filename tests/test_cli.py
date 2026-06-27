"""CLI smoke tests, exit codes + key behaviours."""
from motif import cli


def test_validate_ok(capsys):
    assert cli.main(["validate"]) == 0


def test_doctor_runs(capsys):
    # doctor may warn on missing optional tools but should return cleanly here
    rc = cli.main(["doctor"])
    assert rc in (0, 1)


def test_search(capsys):
    assert cli.main(["search", "save"]) == 0
    out = capsys.readouterr().out
    assert "result" in out


def test_rank_pattern(capsys):
    assert cli.main(["rank", "skeleton-loading", "--profile", "enterprise-strict"]) == 0
    out = capsys.readouterr().out
    assert "Selected:" in out


def test_rank_sources(capsys):
    assert cli.main(["rank-sources"]) == 0


def test_source_completeness(capsys):
    assert cli.main(["source", "completeness"]) == 0


def test_source_scan_eval_button(capsys):
    rc = cli.main(["source", "scan", "evals/fixtures/eval-button"])
    assert rc == 3  # reject verdict
    assert "REJECT" in capsys.readouterr().out


def test_retrieve_refused_offline(capsys):
    assert cli.main(["source", "retrieve"]) == 3


def test_generate_index(capsys):
    assert cli.main(["generate-index"]) == 0
