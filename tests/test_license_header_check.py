from pathlib import Path

from license_header_check import has_header, scan, main


def test_has_header_true(tmp_path: Path) -> None:
    path = tmp_path / "example.py"
    path.write_text("# SPDX-License-Identifier: MIT\nprint('hello')\n", encoding="utf-8")
    assert has_header(path, ["SPDX-License-Identifier"], 5) is True


def test_has_header_false(tmp_path: Path) -> None:
    path = tmp_path / "example.py"
    path.write_text("print('hello')\n", encoding="utf-8")
    assert has_header(path, ["SPDX-License-Identifier", "Copyright"], 5) is False


def test_scan_reports_missing(tmp_path: Path) -> None:
    (tmp_path / "missing.py").write_text("print('hello')\n", encoding="utf-8")
    (tmp_path / "licensed.py").write_text(
        "# Copyright 2026 Example\nprint('hello')\n", encoding="utf-8"
    )
    missing = scan(tmp_path, {".py"}, ["Copyright"], set(), 5)
    assert [path.name for path in missing] == ["missing.py"]


def test_main_json_output(tmp_path: Path, capsys) -> None:
    (tmp_path / "missing.py").write_text("print('hello')\n", encoding="utf-8")
    status = main([str(tmp_path), "--format", "json"])
    captured = capsys.readouterr()
    assert status == 1
    assert '"missing"' in captured.out
    assert "missing.py" in captured.out
