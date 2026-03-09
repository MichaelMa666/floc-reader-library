#!/usr/bin/env python3
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parent
    book_dir = root / "books"
    catalog_file = root / "catalog.json"

    epub_files = sorted(
        [p for p in book_dir.rglob("*.epub") if p.is_file()],
        key=lambda p: str(p.relative_to(book_dir)),
    )
    grouped_books = defaultdict(list)
    book_count = 0
    for idx, file_path in enumerate(epub_files, start=1):
        relative_to_books = file_path.relative_to(book_dir)
        parts = relative_to_books.parts
        category = parts[0] if len(parts) > 1 else "未分类"
        relative_path = file_path.relative_to(root).as_posix()
        grouped_books[category].append(
            {
                "id": f"book-{idx:03d}",
                "file": file_path.name,
                "path": relative_path,
            }
        )
        book_count += 1

    books = []
    for group_idx, category in enumerate(sorted(grouped_books.keys()), start=1):
        books.append(
            {
                "id": f"group-{group_idx:03d}",
                "name": category,
                "books": grouped_books[category],
            }
        )

    catalog = {
        "catalog": {
            "schemaVersion": 1,
            "bookDir": "books",
            "total": book_count,
            "groupTotal": len(books),
            "generatedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        },
        "books": books,
    }

    with catalog_file.open("w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
