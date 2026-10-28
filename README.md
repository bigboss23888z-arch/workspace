# 🤖 دليل أدوات الذكاء الاصطناعي

دليل عربي منظّم لأهم أدوات الذكاء الاصطناعي: نماذج، وكلاء برمجة، أطر عمل، RAG، صور، فيديو، صوت، MLOps، بيانات، أمان، ومصادر تعلّم — مع روابط رسمية ونوع الترخيص وبيئة التشغيل.

كل البيانات في ملف واحد [`data/tools.json`](data/tools.json)، والتوثيق مُولَّد منه آليًا، لذا لا يتعارض المحتوى مع نفسه.

<!-- STATS:START -->
| التصنيف | العدد | الملف |
| --- | --- | --- |
| 🔤 نماذج اللغة والاستدلال | 28 | [docs/models.md](docs/models.md) |
| ⌨️ البرمجة والوكلاء البرمجيون | 22 | [docs/coding.md](docs/coding.md) |
| 🧬 استنساخ المواقع والتطبيقات | 22 | [docs/cloning.md](docs/cloning.md) |
| 🤖 أطر الوكلاء والأتمتة | 22 | [docs/agents.md](docs/agents.md) |
| 🔎 RAG وقواعد البيانات المتجهية | 17 | [docs/rag.md](docs/rag.md) |
| 🎨 توليد الصور ومعالجتها | 18 | [docs/image.md](docs/image.md) |
| 🎬 الفيديو والرسوم المتحركة | 14 | [docs/video.md](docs/video.md) |
| 🎧 الصوت والكلام والموسيقى | 18 | [docs/audio.md](docs/audio.md) |
| ⚙️ MLOps والتشغيل والمراقبة | 20 | [docs/mlops.md](docs/mlops.md) |
| 🗂️ البيانات والوسم والجودة | 15 | [docs/data.md](docs/data.md) |
| 🧠 الإنتاجية والمعرفة | 15 | [docs/productivity.md](docs/productivity.md) |
| 🛡️ الأمان والحماية | 10 | [docs/safety.md](docs/safety.md) |
| 📚 التعلّم والمراجع | 13 | [docs/learning.md](docs/learning.md) |
| **الإجمالي** | **234** | — |

_آخر تحديث: 2026-10-28_
<!-- STATS:END -->

## كيف تستخدم الدليل

- تصفّح التصنيف الذي يهمك من الجدول أعلاه.
- للبحث السريع من الطرفية:

```bash
python3 scripts/search.py --query whisper
python3 scripts/search.py --category coding --type open
python3 scripts/search.py --tag rag --run local
python3 scripts/search.py --stats
```

- لتصدير نتائج كـ JSON:

```bash
python3 scripts/search.py --category agents --json
```

## بنية المستودع

```
.
├── README.md            # هذا الملف (الفهرس)
├── data/tools.json      # المصدر الوحيد للبيانات
├── docs/                # صفحات مولّدة لكل تصنيف
├── scripts/
│   ├── build_docs.py    # يبني docs/ ويحدّث جدول الإحصاءات
│   ├── search.py        # بحث وتصفية
│   └── validate.py      # فحص سلامة البيانات
└── CONTRIBUTING.md      # طريقة الإضافة
```

## إضافة أداة

1. أضف عنصرًا إلى `data/tools.json`:

```json
{
  "name": "اسم الأداة",
  "url": "https://example.com",
  "category": "coding",
  "type": "open",
  "run": "local",
  "desc": "وصف عربي قصير في سطر واحد",
  "tags": ["cli", "agent"]
}
```

2. تحقّق ثم أعد البناء:

```bash
python3 scripts/validate.py
python3 scripts/build_docs.py
git add -A && git commit -m "إضافة أداة" && git push
```

## قيم الحقول

| الحقل | القيم المسموحة |
| --- | --- |
| `category` | `models`, `coding`, `cloning`, `agents`, `rag`, `image`, `video`, `audio`, `mlops`, `data`, `productivity`, `safety`, `learning` |
| `type` | `open` (مفتوح المصدر), `open-core` (مفتوح جزئيًا), `commercial` (تجاري), `freemium` (مجاني محدود) |
| `run` | `local` (محلي), `cloud` (سحابي), `hybrid` (كلاهما) |

## ملاحظات

- الروابط تشير إلى المواقع الرسمية فقط، والوصف يعكس الاستخدام الأساسي للأداة.
- الترتيب داخل كل صفحة أبجدي، وليس تقييمًا للأفضلية.
- الأسعار والخطط تتغير باستمرار؛ راجع الموقع الرسمي قبل الاعتماد على أي خطة.

## الترخيص

الكود في `scripts/` متاح بموجب MIT، والمحتوى (البيانات والتوثيق) متاح لإعادة الاستخدام مع الإشارة إلى هذا المستودع.
