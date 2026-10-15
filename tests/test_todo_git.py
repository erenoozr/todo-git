import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import todo_git


def test_scans_and_skips(tmp_path):
    (tmp_path / "a.py").write_text("x = 1  # TODO: fix later\n# shortcut: single file\n", encoding="utf-8")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "b.js").write_text("// FIXME: must not appear\n", encoding="utf-8")
    (tmp_path / "binary.bin").write_bytes(b"\x00TODO: binary\n")
    items = todo_git.scan(tmp_path)
    assert items == [("TODO", "a.py", 1, "fix later"), ("SHORTCUT", "a.py", 2, "single file")]
    assert "fix later" in todo_git.render(items)


def test_no_false_positives(tmp_path):
    (tmp_path / "a.py").write_text("todos = []\nsize = 'XXXL'\nadd keyboard shortcut\nTODOS\n", encoding="utf-8")
    assert todo_git.scan(tmp_path) == []


def test_non_utf8_file(tmp_path):
    (tmp_path / "legacy.txt").write_bytes("# FIXME: café\n".encode("cp1252"))
    assert [t for t, *_ in todo_git.scan(tmp_path)] == ["FIXME"]


def test_report_does_not_count_itself(tmp_path):
    (tmp_path / "a.py").write_text("# HACK: temporary\n", encoding="utf-8")
    out = tmp_path / "todo-report.html"
    for _ in range(2):
        todo_git.main([str(tmp_path), "-o", str(out)])
    assert out.read_text(encoding="utf-8").count("<tr>") == 1


def test_html_escaping(tmp_path):
    (tmp_path / "a.py").write_text("# TODO: <script>\n", encoding="utf-8")
    assert "&lt;script&gt;" in todo_git.render(todo_git.scan(tmp_path))
