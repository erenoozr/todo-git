"""todo-git: koddaki TODO/FIXME/HACK/XXX/shortcut: notlarını tarar, tek sayfalık HTML rapor üretir."""
import argparse
import html
import os
import re
import sys
from collections import Counter
from pathlib import Path

# büyük harfli etiketler tam kelime olmalı (todos, XXXL eşleşmesin); shortcut yalnızca "shortcut:" biçiminde
PATTERN = re.compile(r"\b(TODO|FIXME|HACK|XXX)\b:?\s*(.*)|\b(shortcut):\s*(.*)")
SKIP_DIRS = {".git", ".hg", ".svn", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".pytest_cache"}
MAX_BYTES = 1_000_000  # büyük dosyaları atla


def scan(root, skip_files=()):
    """[(etiket, dosya, satır_no, metin), ...] döndürür."""
    root = Path(root).resolve()
    skip = {Path(f).resolve() for f in skip_files}
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(n for n in dirnames if n not in SKIP_DIRS)  # içine hiç girme
        for name in sorted(filenames):
            p = Path(dirpath) / name
            if p in skip:
                continue
            try:
                if p.stat().st_size > MAX_BYTES:
                    continue
                data = p.read_bytes()
            except OSError:
                continue
            if b"\0" in data[:8192]:
                continue  # ikili dosya
            rel = p.relative_to(root).as_posix()
            for n, line in enumerate(data.decode("utf-8", errors="replace").splitlines(), 1):
                if m := PATTERN.search(line):
                    tag, msg = (m.group(1), m.group(2)) if m.group(1) else ("SHORTCUT", m.group(4))
                    out.append((tag, rel, n, msg.strip()))
    return out


def render(items, title="todo-git"):
    counts = Counter(t for t, *_ in items)
    summary = " · ".join(f"{t}: {c}" for t, c in counts.most_common())
    rows = "".join(
        f"<tr><td class='t {tag.lower()}'>{tag}</td><td class='f'>{html.escape(f)}:{n}</td><td>{html.escape(msg)}</td></tr>"
        for tag, f, n, msg in items
    )
    return (
        "<!doctype html><html lang=tr><meta charset=utf-8>"
        "<meta name=viewport content='width=device-width,initial-scale=1'>"
        f"<title>{html.escape(title)}</title>"
        "<style>:root{color-scheme:light dark}body{font:14px system-ui;margin:2rem;max-width:1100px}"
        "table{border-collapse:collapse;width:100%}td{padding:.4rem .6rem;border-bottom:1px solid #8884;vertical-align:top}"
        ".f{font-family:ui-monospace,monospace;white-space:nowrap}.t{font-weight:700}"
        ".fixme,.hack{color:#d9534f}.todo{color:#d4a017}.xxx,.shortcut{color:#a569bd}</style>"
        f"<h1>{html.escape(title)}: {len(items)} not</h1><p>{summary or 'Not bulunamadı.'}</p><table>{rows}</table></html>"
    )


def main(argv=None):
    sys.stdout.reconfigure(errors="replace")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("klasor")
    ap.add_argument("-o", "--cikti", default="todo-rapor.html")
    a = ap.parse_args(argv)
    root = Path(a.klasor)
    if not root.is_dir():
        sys.exit(f"Klasör yok: {root}")
    items = scan(root, skip_files=[a.cikti])  # rapor klasörün içindeyse kendini saymasın
    Path(a.cikti).write_text(render(items, f"todo-git · {root.resolve().name}"), encoding="utf-8")
    print(f"{len(items)} not bulundu -> {a.cikti}")


if __name__ == "__main__":
    main()
