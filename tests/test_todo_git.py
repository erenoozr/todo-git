import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import todo_git


def test_tarar_ve_atlar(tmp_path):
    (tmp_path / "a.py").write_text("x = 1  # TODO: sonra düzelt\n# shortcut: tek dosya\n", encoding="utf-8")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "b.js").write_text("// FIXME: görünmemeli\n", encoding="utf-8")
    (tmp_path / "ikili.bin").write_bytes(b"\x00TODO: ikili\n")
    items = todo_git.scan(tmp_path)
    assert items == [("TODO", "a.py", 1, "sonra düzelt"), ("SHORTCUT", "a.py", 2, "tek dosya")]
    assert "sonra düzelt" in todo_git.render(items)


def test_yanlis_pozitif_yok(tmp_path):
    (tmp_path / "a.py").write_text("todos = []\nsize = 'XXXL'\nkeyboard shortcut ekle\nTODOS\n", encoding="utf-8")
    assert todo_git.scan(tmp_path) == []


def test_utf8_olmayan_dosya(tmp_path):
    (tmp_path / "eski.txt").write_bytes("# FIXME: şu\n".encode("cp1254"))
    assert [t for t, *_ in todo_git.scan(tmp_path)] == ["FIXME"]


def test_rapor_kendini_saymaz(tmp_path):
    (tmp_path / "a.py").write_text("# HACK: geçici\n", encoding="utf-8")
    out = tmp_path / "todo-rapor.html"
    for _ in range(2):
        todo_git.main([str(tmp_path), "-o", str(out)])
    assert out.read_text(encoding="utf-8").count("<tr>") == 1


def test_html_kacis(tmp_path):
    (tmp_path / "a.py").write_text("# TODO: <script>\n", encoding="utf-8")
    assert "&lt;script&gt;" in todo_git.render(todo_git.scan(tmp_path))
