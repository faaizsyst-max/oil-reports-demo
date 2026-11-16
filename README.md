# نظام تقارير الإنتاج اليومي للحقول النفطية — مشروع تدريبي

> ⚠️ **تنبيه:** هذا المشروع مخصص للتدريب فقط، ويحتوي على **ثغرات أمنية متعمّدة**.
> لا تشغّله على أي خادم، ولا تستخدم أي جزء منه في نظام حقيقي.
> كل البيانات والأسماء فيه وهمية.

## ما هذا المشروع؟

تطبيق ويب صغير مكتوب بلغة Python (إطار Flask) يحاكي نظاماً داخلياً تستخدمه جهة نفطية لعرض **تقارير الإنتاج اليومي** لكل حقل:
كمية النفط المنتجة بالبرميل، ونسبة الماء المصاحب، مع صفحة بحث، وتصدير التقارير، وتسجيل دخول للمستخدمين.

الهدف منه عرض إضافة **GitHub Security** داخل تطبيق **GitHub Copilot**:
اكتشاف الثغرات، وشرحها، واقتراح إصلاحها، مع بقاء قرار اعتماد التعديل بيد المبرمج.

## الثغرات الموجودة عمداً

| الملف | الثغرة | الخطورة المتوقعة |
|---|---|---|
| `src/api/reports.py` | حقن SQL (SQL Injection) في استعلام التقارير | حرجة / عالية |
| `src/api/export.py` | الوصول لملفات خارج المجلد (Path Traversal) | عالية |
| `src/api/search.py` | حقن شيفرة في الصفحة (Reflected XSS) | متوسطة / عالية |
| `web/views/search.js` | حقن شيفرة من جهة المتصفح (DOM XSS) | متوسطة / عالية |
| `src/auth/tokens.py` | تشفير كلمات المرور بخوارزمية MD5 الضعيفة | عالية |
| `src/api/errors.py` | عرض تفاصيل الأخطاء الداخلية للمستخدم | متوسطة |
| `src/app.py` | تشغيل وضع التصحيح (debug) | عالية |

> تصنيف الخطورة وأسماء التنبيهات الفعلية يحددها فحص CodeQL وقد تختلف قليلاً عن الجدول.

## تمرين المراجعة الأمنية المحلية (قبل Pull Request)

بعد فتح المشروع في تطبيق GitHub Copilot، أنشئ ملفاً جديداً باسم `src/api/admin.py` والصق فيه الكود التالي، ثم شغّل `/security-review`:

```python
from flask import Blueprint, request
from src.db import get_db

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/api/admin/delete")
def delete_report():
    report_id = request.args.get("id", "")
    db = get_db()
    db.execute("DELETE FROM reports WHERE id = " + report_id)
    db.commit()
    print("Deleted report", report_id, "by", request.args.get("password"))
    return "deleted"
```

هذا الكود فيه ثلاث مشاكل: حذف بدون تحقق من الصلاحية، وحقن SQL، وكتابة كلمة مرور في السجلات.

## التشغيل المحلي (اختياري)

```bash
pip install -r requirements.txt
python -m src.app
```

ثم افتح: http://127.0.0.1:5000
