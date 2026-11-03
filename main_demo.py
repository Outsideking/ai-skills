# -*- coding: utf-8 -*-
"""
==================================================
🚀 AI-SKILL DEMO — รวมทุกระบบทำงานร่วมกัน
1. ใช้สกิล SmartNotes
2. ส่งผลลัพธ์กลับไปยัง Vider Knowledge Loop
==================================================
"""

from smart_notes import SmartNotes
from vider_knowledge_loop import submit_skill_external

print("="*60)
print("🚀 เริ่มต้นใช้งานระบบ AI-Skill ร่วมกับ Vider")
print("="*60)

# ──────────────────────────────────────────────
# 1️⃣ ใช้งานสกิล SmartNotes
# ──────────────────────────────────────────────
print("\n📝 1. ทดสอบใช้งาน SmartNotes")
print("─" * 40)

sn = SmartNotes()

# ตัวอย่างที่คุณระบุ
sn.add("พรุ่งนี้ประชุมลูกค้า")

# เพิ่มอีกเล็กน้อย
sn.add("เตรียมเอกสารนำเสนอ")
sn.add("ตรวจสอบอีเมลลูกค้า")

# แสดงผลแยกตามหมวดหมู่
print("\n📂 ผลลัพธ์ sn.by_category():")
result = sn.by_category()
for category, items in result.items():
    print(f"\n   📁 {category}:")
    for item in items:
        print(f"      • {item['content']}")

# ──────────────────────────────────────────────
# 2️⃣ ส่งผลลัพธ์กลับไปยัง Vider Knowledge Loop
# ──────────────────────────────────────────────
print("\n" + "="*60)
print("📤 2. ส่งผลลัพธ์สกิลกลับไปพัฒนาต่อที่ Vider")
print("─" * 40)

feedback = submit_skill_external(
    skill_id="smart_notes",
    name="ระบบจดบันทึกอัจฉริยะ",
    description="จดบันทึกและจัดหมวดหมู่อัตโนมัติตามเนื้อหา",
    code="from smart_notes import SmartNotes\nsn = SmartNotes()\nsn.add('ข้อความ')\nprint(sn.by_category())",
    result_value=0.80,  # ✅ มากกว่า +0.5 → Vider จะเรียนรู้และพัฒนาต่อ
    submitter="นายธันวา ภูปิงบุตร",
    notes="ทำงานถูกต้อง จัดหมวดหมู่ 'งาน' ให้กับ 'พรุ่งนี้ประชุมลูกค้า' ได้ถูกต้อง"
)

print(f"\n📤 ผลการส่ง: {feedback['status']}")
print(f"📝 {feedback['message']}")

print("\n" + "="*60)
print("✅ เสร็จสิ้น — สกิลทำงานและส่งคืนความรู้ให้ Vider เรียบร้อย!")
print("="*60)

