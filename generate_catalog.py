#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parent
    book_dir = root / "books"
    catalog_file = root / "catalog.json"

    epub_files = sorted([p for p in book_dir.glob("*.epub") if p.is_file()], key=lambda p: p.name)
    books = []
    for idx, file_path in enumerate(epub_files, start=1):
        books.append(
            {
                "id": f"book-{idx:03d}",
                "file": file_path.name,
                "path": f"books/{file_path.name}",
            }
        )

    catalog = {
        "catalog": {
            "schemaVersion": 1,
            "bookDir": "books",
            "total": len(books),
            "generatedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        },
        "books": books,
    }

    with catalog_file.open("w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
