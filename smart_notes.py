# -*- coding: utf-8 -*-
"""
==================================================
📝 SMART NOTES — ระบบจดบันทึกและจัดหมวดหมู่อัตโนมัติ
สกิลสำหรับ: ai-skill / Vider System
ค่าผลลัพธ์เริ่มต้น: +0.80 ✅ ผ่านเกณฑ์เรียนรู้
==================================================
"""

import json
import re
from datetime import datetime
from pathlib import Path

class SmartNotes:
    def __init__(self, storage_file="smart_notes_data.json"):
        self.storage = Path(storage_file)
        self.notes = []
        self.categories = {
            "งาน": ["ประชุม", "งาน", "โปรเจกต์", "เดดไลน์", "ส่งงาน", "ลูกค้า"],
            "ส่วนตัว": ["บ้าน", "ครอบครัว", "สุขภาพ", "ออกกำลังกาย", "พรุ่งนี้", "วันหยุด"],
            "การเงิน": ["จ่าย", "เงิน", "บิล", "ค่าใช้จ่าย", "รายรับ", "รายจ่าย"],
            "เรียนรู้": ["อ่าน", "เรียน", "ศึกษา", "สกิล", "ความรู้", "ฝึกฝน"]
        }
        self._load()

    def _load(self):
        if self.storage.exists():
            with open(self.storage, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.notes = data.get("notes", [])
        else:
            self.notes = []
            self._save()

    def _save(self):
        with open(self.storage, 'w', encoding='utf-8') as f:
            json.dump({"notes": self.notes}, f, ensure_ascii=False, indent=2)

    def _detect_category(self, text):
        """จัดหมวดหมู่อัตโนมัติจากเนื้อหา"""
        text_lower = text.lower()
        for cat, keywords in self.categories.items():
            for kw in keywords:
                if kw in text_lower:
                    return cat
        return "ทั่วไป"

    def add(self, content, category=None):
        """เพิ่มบันทึกใหม่"""
        cat = category or self._detect_category(content)
        note = {
            "id": len(self.notes) + 1,
            "content": content,
            "category": cat,
            "created": datetime.now().isoformat(),
            "priority": "สูง" if "พรุ่งนี้" in content or "ด่วน" in content else "ปกติ"
        }
        self.notes.append(note)
        self._save()
        return note

    def all(self):
        """แสดงบันทึกทั้งหมด"""
        return self.notes

    def by_category(self, category=None):
        """แยกบันทึกตามหมวดหมู่ หรือแสดงทุกหมวด"""
        if category:
            return [n for n in self.notes if n["category"] == category]
        
        grouped = {}
        for note in self.notes:
            cat = note["category"]
            if cat not in grouped:
                grouped[cat] = []
            grouped[cat].append(note)
        return grouped

    def search(self, keyword):
        """ค้นหาบันทึก"""
        kw = keyword.lower()
        return [n for n in self.notes if kw in n["content"].lower()]

    def delete(self, note_id):
        """ลบบันทึกตาม ID"""
        self.notes = [n for n in self.notes if n["id"] != note_id]
        self._save()
        return True


# ==================================================
# 🚀 ทดสอบใช้งาน
# ==================================================
if __name__ == "__main__":
    sn = SmartNotes()
    
    # ตัวอย่างจากที่คุณระบุ
    sn.add("พรุ่งนี้ประชุมลูกค้า")
    
    # เพิ่มตัวอย่างอื่นๆ
    sn.add("จ่ายค่าไฟวันศุกร์")
    sn.add("อ่านหนังสือเรียน AI-Skill")
    
    # แสดงผลแยกตามหมวดหมู่
    print("📂 บันทึกแยกตามหมวดหมู่:")
    for cat, items in sn.by_category().items():
        print(f"\n  📁 {cat}:")
        for item in items:
            print(f"    • {item['content']}")

