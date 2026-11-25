from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path

WORD_PATTERN = re.compile(r"[а-яёa-z]+", re.IGNORECASE)
STOP_WORDS = {
    "и", "в", "на", "с", "не", "что", "это", "как", "по", "из", "у", "к", "за", "для",
    "а", "но", "или", "то", "все", "уже", "же", "бы", "мы", "вы", "он", "она", "они",
    "the", "and", "for", "with", "that", "this", "you", "are",
}


def count_lines(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip())


def top_words(text: str, limit: int = 10) -> list[tuple[str, int]]:
    words = [word.lower() for word in WORD_PATTERN.findall(text)]
    meaningful = [word for word in words if len(word) > 2 and word not in STOP_WORDS]
    return Counter(meaningful).most_common(limit)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python main.py <file.txt>")
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}")
        return 1

    text = path.read_text(encoding="utf-8")
    words = WORD_PATTERN.findall(text)

    print(f"File: {path.name}")
    print(f"{'lines':>13}: {count_lines(text)}")
    print(f"{'words':>13}: {len(words)}")
    print(f"{'unique':>13}: {len({word.lower() for word in words})}")
    print(f"{'characters':>13}: {len(text)}")

    tops = top_words(text)
    print("\nTop words:")
    for index, (word, count) in enumerate(tops, start=1):
        print(f"{index:>2}. {word:<16} {count}")

    report = path.with_suffix(".csv")
    with report.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle, delimiter=";")
        writer.writerow(["word", "count"])
        writer.writerows(tops)

    print(f"\nReport: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
