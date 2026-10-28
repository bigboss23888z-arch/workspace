#!/usr/bin/env python3
"""بحث وتصفية في دليل أدوات الذكاء الاصطناعي.

أمثلة:
  python3 scripts/search.py --query whisper
  python3 scripts/search.py --category coding --type open
  python3 scripts/search.py --tag rag --run local --limit 5
  python3 scripts/search.py --query "صوت" --json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_docs import DATA, RUNS, TYPES, load  # noqa: E402


def matches(tool: dict, args: argparse.Namespace) -> bool:
    if args.category and tool["category"] != args.category:
        return False
    if args.type and tool["type"] != args.type:
        return False
    if args.run and tool["run"] != args.run:
        return False
    if args.tag:
        tags = [t.lower() for t in tool.get("tags", [])]
        if args.tag.lower() not in tags:
            return False
    if args.query:
        needle = args.query.lower()
        haystack = " ".join(
            [
                tool["name"],
                tool["desc"],
                tool["url"],
                " ".join(tool.get("tags", [])),
                tool["category"],
            ]
        ).lower()
        if needle not in haystack:
            return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="بحث في دليل أدوات الذكاء الاصطناعي")
    parser.add_argument("-q", "--query", help="كلمة للبحث في الاسم والوصف والوسوم")
    parser.add_argument("-c", "--category", help="تصنيف محدد")
    parser.add_argument("-t", "--tag", help="وسم محدد")
    parser.add_argument("--type", choices=sorted(TYPES), help="نوع الترخيص/النموذج")
    parser.add_argument("--run", choices=sorted(RUNS), help="بيئة التشغيل")
    parser.add_argument("-l", "--limit", type=int, default=40, help="أقصى عدد نتائج")
    parser.add_argument("--json", action="store_true", help="إخراج JSON")
    parser.add_argument("--stats", action="store_true", help="إحصاءات سريعة")
    args = parser.parse_args()

    doc = load()
    tools = doc["tools"]

    if args.stats:
        counts: dict[str, int] = {}
        for tool in tools:
            counts[tool["category"]] = counts.get(tool["category"], 0) + 1
        for name, count in sorted(counts.items(), key=lambda kv: -kv[1]):
            print(f"{name:14} {count}")
        print(f"{'TOTAL':14} {len(tools)}")
        return 0

    results = [t for t in tools if matches(t, args)]
    results.sort(key=lambda t: (t["category"], t["name"].lower()))
    results = results[: args.limit]

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0

    if not results:
        print("لا نتائج مطابقة.")
        return 1

    for tool in results:
        print(f"{tool['name']}  [{tool['category']}]")
        print(f"  {tool['desc']}")
        print(
            f"  {tool['url']}  |  {TYPES[tool['type']]}  |  {RUNS[tool['run']]}"
        )
    print(f"\n{len(results)} نتيجة.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
