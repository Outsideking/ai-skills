# -*- coding: utf-8 -*-
"""
==================================================
🔁 VIDER KNOWLEDGE FEEDBACK LOOP — ระบบป้อนกลับความรู้
เวอร์ชัน: 1.0.0
กฎ: ผลลัพธ์ +0.5 ขึ้นไป → ✅ เรียนรู้ & พัฒนาต่อ
    ผลลัพธ์ -0.5 ขึ้นไป → ❌ ข้าม ไม่เรียนรู้
==================================================
"""

import json
import datetime
from pathlib import Path
from typing import Dict, List, Optional

# ==================================================
# ⚙️ กฎระบบ — ตั้งค่าตรงนี้
# ==================================================
class Config:
    THRESHOLD_LEARN = 0.5      # ✅ ค่าผลลัพธ์ต่ำสุดที่จะเรียนรู้
    THRESHOLD_SKIP = -0.5      # ❌ ค่าผลลัพธ์เริ่มต้นที่จะข้าม
    KNOWLEDGE_FILE = "vider_knowledge_base.json"
    SUBMISSION_LOG = "skill_submissions.json"

# ==================================================
# 📦 โครงสร้างฐานความรู้
# ==================================================
class KnowledgeBase:
    def __init__(self):
        self.kb_path = Path(Config.KNOWLEDGE_FILE)
        self.log_path = Path(Config.SUBMISSION_LOG)
        self.skills = {}          # สกิลที่ผ่านเกณฑ์และเรียนรู้แล้ว
        self.submissions = []     # บันทึกทุกสกิลที่ส่งเข้ามา
        self._load()

    def _load(self):
        # โหลดฐานความรู้
        if self.kb_path.exists():
            with open(self.kb_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.skills = data.get("learned_skills", {})
        else:
            self.skills = {}
            self._save_kb()
        
        # โหลดประวัติการส่ง
        if self.log_path.exists():
            with open(self.log_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.submissions = data.get("submissions", [])
        else:
            self.submissions = []
            self._save_log()

    def _save_kb(self):
        data = {
            "version": "1.0.0",
            "updated": datetime.datetime.now().isoformat(),
            "total_skills": len(self.skills),
            "learned_skills": self.skills
        }
        with open(self.kb_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _save_log(self):
        data = {
            "total_submissions": len(self.submissions),
            "submissions": self.submissions[-100:]  # เก็บล่าสุด 100 รายการ
        }
        with open(self.log_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ==================================================
    # 📥 รับสกิลที่ส่งเข้ามาจากผู้ใช้/ระบบภายนอก
    # ==================================================
    def submit_skill(self, skill_id: str, name: str, description: str, 
                     code: str, result_value: float, submitter: str = "anonymous",
                     notes: str = "") -> Dict:
        """
        รับสกิลที่ส่งเข้ามา ประเมิน และตัดสินใจเรียนรู้หรือข้าม
        
        Args:
            skill_id: รหัสสกิล
            name: ชื่อสกิล
            description: คำอธิบาย
            code: โค้ดสกิล
            result_value: ค่าผลลัพธ์ (-1.0 ถึง +1.0)
            submitter: ผู้ส่ง
            notes: หมายเหตุ
        
        Returns:
            Dict: ผลการประเมิน
        """
        timestamp = datetime.datetime.now().isoformat()
        
        # บันทึกประวัติการส่งทุกกรณี
        submission = {
            "skill_id": skill_id,
            "name": name,
            "result_value": result_value,
            "submitter": submitter,
            "timestamp": timestamp,
            "notes": notes
        }
        self.submissions.append(submission)
        self._save_log()

        # ประเมินตามกฎ
        if result_value >= Config.THRESHOLD_LEARN:
            # ✅ ผ่านเกณฑ์ — เรียนรู้และเก็บเข้าฐานความรู้
            return self._accept_and_learn(skill_id, name, description, code, 
                                          result_value, submitter, timestamp)
        
        elif result_value <= Config.THRESHOLD_SKIP:
            # ❌ ไม่ผ่านเกณฑ์ — ข้าม ไม่เรียนรู้
            return self._skip_skill(skill_id, result_value)
        
        else:
            # ⚠️ อยู่ระหว่างรอประเมิน — เก็บไว้แต่ยังไม่เรียนรู้
            return {
                "status": "pending",
                "skill_id": skill_id,
                "result_value": result_value,
                "message": f"⏳ ค่าผลลัพธ์ {result_value:.2f} อยู่ระหว่างเกณฑ์ — รอการประเมินเพิ่มเติม",
                "action": "stored_only"
            }

    # ==================================================
    # ✅ เรียนรู้ — ผลลัพธ์ +0.5 ขึ้นไป
    # ==================================================
    def _accept_and_learn(self, skill_id: str, name: str, description: str,
                          code: str, value: float, submitter: str, ts: str) -> Dict:
        
        self.skills[skill_id] = {
            "name": name,
            "description": description,
            "code": code,
            "result_value": value,
            "submitted_by": submitter,
            "learned_at": ts,
            "status": "active",
            "version": "1.0"
        }
        self._save_kb()
        
        print(f"\n✅ 🧠 VIDER เรียนรู้สกิลใหม่!")
        print(f"   📦 สกิล: {name} ({skill_id})")
        print(f"   ⭐ ค่าผลลัพธ์: +{value:.2f} ✅ ผ่านเกณฑ์ +0.5")
        print(f"   💾 เก็บเข้าฐานความรู้เรียบร้อย")
        print(f"   🚀 พร้อมพัฒนาต่อยอดในระบบ Vider")
        
        return {
            "status": "LEARNED",
            "skill_id": skill_id,
            "result_value": value,
            "message": "✅ สกิลมีค่า — เรียนรู้และพัฒนาต่อโดย Vider",
            "action": "added_to_knowledge_base"
        }

    # ==================================================
    # ❌ ข้าม — ผลลัพธ์ -0.5 ขึ้นไป
    # ==================================================
    def _skip_skill(self, skill_id: str, value: float) -> Dict:
        print(f"\n❌ ข้ามสกิล: {skill_id}")
        print(f"   ⚠️  ค่าผลลัพธ์: {value:.2f} ❌ ต่ำกว่าเกณฑ์ -0.5")
        print(f"   🚫 ไม่บันทึก ไม่เรียนรู้")
        
        return {
            "status": "SKIPPED",
            "skill_id": skill_id,
            "result_value": value,
            "message": "❌ ผลลัพธ์ไม่เป็นไปตามเกณฑ์ — ข้าม ไม่เรียนรู้",
            "action": "not_stored"
        }

    # ==================================================
    # 📋 ดูสถิติและรายงาน
    # ==================================================
    def get_stats(self) -> Dict:
        total = len(self.submissions)
        learned = len(self.skills)
        skipped = sum(1 for s in self.submissions if s.get("result_value", 0) <= Config.THRESHOLD_SKIP)
        pending = total - learned - skipped
        return {
            "total_submissions": total,
            "learned_skills": learned,
            "skipped_skills": skipped,
            "pending_review": pending
        }

    def list_learned(self):
        print("\n" + "="*60)
        print("🧠 ฐานความรู้ของ Vider — สกิลที่เรียนรู้และพัฒนาต่อ")
        print("="*60)
        if not self.skills:
            print("   (ยังไม่มีสกิลที่เรียนรู้)")
            return
        for idx, (sid, skill) in enumerate(self.skills.items(), 1):
            print(f"\n   {idx}. 📦 {skill['name']}")
            print(f"      ID: {sid}")
            print(f"      ⭐ ค่าผลลัพธ์: +{skill['result_value']:.2f}")
            print(f"      👤 ส่งโดย: {skill.get('submitted_by', 'ไม่ระบุ')}")
            print(f"      📅 เรียนรู้: {skill['learned_at'][:19]}")
            print(f"      📝 {skill.get('description', '')}")
        print("\n" + "="*60)
        print(f"   📊 รวมทั้งหมด: {len(self.skills)} สกิลที่พร้อมพัฒนาต่อ")
        print("="*60)


# ==================================================
# 🚀 เมนูหลัก — ระบบรับสกิลและป้อนกลับ
# ==================================================
def main():
    kb = KnowledgeBase()
    
    print("╔" + "═"*60 + "╗")
    print("║  🔁 VIDER KNOWLEDGE FEEDBACK LOOP — ป้อนกลับความรู้                ║")
    print("╠" + "═"*60 + "╣")
    print(f"║  ✅ เรียนรู้: ผลลัพธ์ ≥ +0.5  |  ❌ ข้าม: ผลลัพธ์ ≤ -0.5{' '*18}║")
    stats = kb.get_stats()
    print(f"║  📊 รับทั้งหมด: {stats['total_submissions']}  |  เรียนรู้แล้ว: {stats['learned_skills']}{' '*24}║")
    print("╚" + "═"*60 + "╝")

    while True:
        print("\n📌 เมนู:")
        print("   1. 📥 ส่งสกิลเข้าประเมิน")
        print("   2. 🧠 ดูสกิลที่ Vider เรียนรู้แล้ว")
        print("   3. 📊 สรุปสถิติทั้งหมด")
        print("   4. ❌ ออก")
        
        choice = input("\nเลือก: ").strip()
        
        if choice == "1":
            print("\n📥 ส่งสกิลเพื่อให้ Vider ประเมินและเรียนรู้")
            print("─" * 50)
            skill_id = input("   รหัสสกิล (ภาษาอังกฤษ): ").strip()
            name = input("   ชื่อสกิล: ").strip()
            desc = input("   คำอธิบายสั้นๆ: ").strip()
            print("   โค้ดสกิล (พิมพ์ --- เมื่อจบ):")
            code_lines = []
            while True:
                line = input("   │ ")
                if line.strip() == "---":
                    break
                code_lines.append(line)
            code = "\n".join(code_lines)
            value_str = input("   ⭐ ค่าผลลัพธ์จากการใช้งาน (-1.0 ถึง +1.0): ").strip()
            try:
                result_value = float(value_str)
            except ValueError:
                print("❌ ค่าผลลัพธ์ต้องเป็นตัวเลข!")
                continue
            submitter = input("   👤 ผู้ส่ง (เว้นว่างได้): ").strip() or "anonymous"
            notes = input("   📝 หมายเหตุเพิ่มเติม: ").strip()
            
            result = kb.submit_skill(skill_id, name, desc, code, result_value, submitter, notes)
            print(f"\n📤 ผลการประเมิน: {result['status']}")
            print(f"   📝 {result['message']}")
        
        elif choice == "2":
            kb.list_learned()
        
        elif choice == "3":
            stats = kb.get_stats()
            print("\n📊 สรุปสถิติระบบป้อนกลับความรู้")
            print("─" * 40)
            print(f"   📥 รับสกิลทั้งหมด: {stats['total_submissions']} รายการ")
            print(f"   ✅ เรียนรู้ & พัฒนาต่อ: {stats['learned_skills']} รายการ")
            print(f"   ❌ ข้าม ไม่เรียนรู้: {stats['skipped_skills']} รายการ")
            print(f"   ⏳ รอประเมิน: {stats['pending_review']} รายการ")
            print("─" * 40)
        
        elif choice == "4":
            print("\n👑 ปิดระบบป้อนกลับความรู้ — ขอบคุณที่ร่วมพัฒนา Vider")
            break
        
        print()


# ==================================================
# 🔧 ฟังก์ชันสำหรับเรียกใช้จากระบบอื่น
# ==================================================
def submit_skill_external(skill_id, name, description, code, result_value, 
                          submitter="external", notes=""):
    """
    ฟังก์ชันสำหรับเรียกจากระบบภายนอก / AI-Skill Installer
    
    ตัวอย่าง:
        result = submit_skill_external(
            skill_id="new_calculator",
            name="เครื่องคิดเลขอัจฉริยะ",
            description="คำนวณและวิเคราะห์ผลลัพธ์",
            code="def add(a,b): return a+b",
            result_value=0.85,
            submitter="user_001"
        )
    """
    kb = KnowledgeBase()
    return kb.submit_skill(skill_id, name, description, code, 
                           result_value, submitter, notes)


# ==================================================
# 🏃 เริ่มทำงาน
# ==================================================
if __name__ == "__main__":
    main()

