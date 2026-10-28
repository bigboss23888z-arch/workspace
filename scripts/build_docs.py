#!/usr/bin/env python3
"""يبني ملفات التوثيق من data/tools.json ويحدّث جدول الإحصاءات في README."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "tools.json"
DOCS = ROOT / "docs"
README = ROOT / "README.md"

CATEGORIES = {
    "models": ("نماذج اللغة والاستدلال", "🔤"),
    "coding": ("البرمجة والوكلاء البرمجيون", "⌨️"),
    "agents": ("أطر الوكلاء والأتمتة", "🤖"),
    "rag": ("RAG وقواعد البيانات المتجهية", "🔎"),
    "image": ("توليد الصور ومعالجتها", "🎨"),
    "video": ("الفيديو والرسوم المتحركة", "🎬"),
    "audio": ("الصوت والكلام والموسيقى", "🎧"),
    "mlops": ("MLOps والتشغيل والمراقبة", "⚙️"),
    "data": ("البيانات والوسم والجودة", "🗂️"),
    "productivity": ("الإنتاجية والمعرفة", "🧠"),
    "safety": ("الأمان والحماية", "🛡️"),
    "learning": ("التعلّم والمراجع", "📚"),
}

TYPES = {
    "open": "مفتوح المصدر",
    "open-core": "مفتوح جزئيًا",
    "commercial": "تجاري",
    "freemium": "مجاني محدود",
}

RUNS = {
    "local": "محلي",
    "cloud": "سحابي",
    "hybrid": "محلي/سحابي",
}

REQUIRED = ("name", "url", "category", "type", "run", "desc")


def load() -> dict:
    with DATA.open(encoding="utf-8") as fh:
        return json.load(fh)


def validate(doc: dict) -> list[str]:
    errors: list[str] = []
    tools = doc.get("tools", [])
    if not tools:
        errors.append("لا توجد أدوات في data/tools.json")
    seen: set[str] = set()
    for i, tool in enumerate(tools):
        label = tool.get("name") or f"#{i}"
        for key in REQUIRED:
            if not str(tool.get(key, "")).strip():
                errors.append(f"{label}: الحقل {key} مفقود")
        if tool.get("category") not in CATEGORIES:
            errors.append(f"{label}: تصنيف غير معروف {tool.get('category')!r}")
        if tool.get("type") not in TYPES:
            errors.append(f"{label}: نوع غير معروف {tool.get('type')!r}")
        if tool.get("run") not in RUNS:
            errors.append(f"{label}: بيئة تشغيل غير معروفة {tool.get('run')!r}")
        url = tool.get("url", "")
        if url and not re.match(r"^https?://\S+$", url):
            errors.append(f"{label}: رابط غير صالح {url!r}")
        key = tool.get("name", "").strip().lower()
        if key in seen:
            errors.append(f"{label}: اسم مكرر")
        seen.add(key)
    return errors


def slug(name: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return value or "tool"


def render_category(slug_name: str, tools: list[dict]) -> str:
    title, icon = CATEGORIES[slug_name]
    lines = [
        f"# {icon} {title}",
        "",
        f"عدد الأدوات: **{len(tools)}** — عودة إلى [الفهرس](../README.md)",
        "",
        "| الأداة | النوع | التشغيل | الوصف |",
        "| --- | --- | --- | --- |",
    ]
    for tool in tools:
        lines.append(
            "| [{name}]({url}) | {type} | {run} | {desc} |".format(
                name=tool["name"],
                url=tool["url"],
                type=TYPES[tool["type"]],
                run=RUNS[tool["run"]],
                desc=tool["desc"],
            )
        )
    lines.append("")
    return "\n".join(lines)


def update_readme(counts: dict[str, int], total: int, updated: str) -> None:
    table = [
        "| التصنيف | العدد | الملف |",
        "| --- | --- | --- |",
    ]
    for slug_name, (title, icon) in CATEGORIES.items():
        table.append(
            f"| {icon} {title} | {counts.get(slug_name, 0)} | [docs/{slug_name}.md](docs/{slug_name}.md) |"
        )
    table.append(f"| **الإجمالي** | **{total}** | — |")
    block = "\n".join(table)

    text = README.read_text(encoding="utf-8")
    text = re.sub(
        r"(<!-- STATS:START -->)(.*?)(<!-- STATS:END -->)",
        lambda m: f"{m.group(1)}\n{block}\n\n_آخر تحديث: {updated}_\n{m.group(3)}",
        text,
        flags=re.S,
    )
    README.write_text(text, encoding="utf-8")


def main() -> int:
    doc = load()
    errors = validate(doc)
    if errors:
        print("فشل التحقق:")
        for err in errors:
            print(" -", err)
        return 1

    tools = doc["tools"]
    DOCS.mkdir(exist_ok=True)
    counts: dict[str, int] = {}

    for slug_name in CATEGORIES:
        subset = sorted(
            (t for t in tools if t["category"] == slug_name),
            key=lambda t: t["name"].lower(),
        )
        counts[slug_name] = len(subset)
        (DOCS / f"{slug_name}.md").write_text(
            render_category(slug_name, subset), encoding="utf-8"
        )

    meta = doc.get("meta", {})
    update_readme(counts, len(tools), meta.get("updated", ""))
    print(f"تم بناء {len(CATEGORIES)} ملفات توثيق لـ {len(tools)} أداة.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
