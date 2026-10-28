#!/usr/bin/env python3
"""يتحقق من سلامة data/tools.json قبل البناء أو الالتزام."""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_docs import CATEGORIES, TYPES, load, validate  # noqa: E402


def main() -> int:
    doc = load()
    errors = validate(doc)
    if errors:
        print(f"✗ وُجدت {len(errors)} مشكلة:")
        for err in errors:
            print(" -", err)
        return 1

    tools = doc["tools"]
    counts = Counter(tool["category"] for tool in tools)
    types = Counter(tool["type"] for tool in tools)

    print(f"✓ {len(tools)} أداة صالحة في {len(counts)} تصنيفًا.")
    for slug, (title, _) in CATEGORIES.items():
        print(f"  - {title}: {counts.get(slug, 0)}")
    print("أنواع:", ", ".join(f"{k}={v}" for k, v in types.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
