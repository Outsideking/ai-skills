# -*- coding: utf-8 -*-
"""
==================================================
🔌 SKILL INSTALLER — ติดตั้งสกิลจาก GitHub ลิงก์
เวอร์ชัน: 1.0.0
ใช้งาน: วางลิงก์ raw.githubusercontent.com → ติดตั้ง → เรียกใช้
==================================================
"""

import json
import urllib.request
import urllib.error
import importlib.util
import sys
from pathlib import Path
import ssl

# ปิด SSL สำหรับมือถือ
ssl._create_default_https_context = ssl._create_unverified_context

# ==================================================
# 📦 จัดการคลังสกิลที่ติดตั้งแล้ว
# ==================================================
class SkillManager:
    def __init__(self, storage_file="installed_skills.json"):
        self.storage_file = storage_file
        self.skills_dir = Path("installed_skills")
        self.skills_dir.mkdir(exist_ok=True)
        self.installed = {}
        self._load_registry()
    
    def _load_registry(self):
        path = Path(self.storage_file)
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                self.installed = json.load(f)
        else:
            self.installed = {}
            self._save_registry()
    
    def _save_registry(self):
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(self.installed, f, ensure_ascii=False, indent=2)
    
    # ==================================================
    # ⬇️ ดาวน์โหลดและติดตั้งสกิลจากลิงก์
    # ==================================================
    def install(self, raw_url, skill_id=None):
        """
        ติดตั้งสกิลจากลิงก์ GitHub raw
        ตัวอย่างลิงก์: https://raw.githubusercontent.com/seperneng-spec/ai-skills/main/calculator.py
        """
        print(f"📥 กำลังติดตั้งจาก:\n   {raw_url}")
        
        # ดาวน์โหลดไฟล์
        try:
            req = urllib.request.Request(raw_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                code = r.read().decode('utf-8')
        except Exception as e:
            print(f"❌ ดาวน์โหลดไม่ได้: {e}")
            return False
        
        # กำหนดชื่อไฟล์
        if not skill_id:
            skill_id = raw_url.split('/')[-1].replace('.py', '')
        
        file_path = self.skills_dir / f"{skill_id}.py"
        
        # บันทึกไฟล์
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        # บันทึกลงทะเบียน
        self.installed[skill_id] = {
            "url": raw_url,
            "path": str(file_path),
            "installed_at": __import__('datetime').datetime.now().isoformat()
        }
        self._save_registry()
        
        print(f"✅ ติดตั้งสกิล '{skill_id}' สำเร็จ!")
        return True
    
    # ==================================================
    # ▶️ เรียกใช้สกิล
    # ==================================================
    def run(self, skill_id, *args, **kwargs):
        """เรียกใช้สกิลที่ติดตั้งแล้ว"""
        if skill_id not in self.installed:
            print(f"❌ ไม่พบสกิล '{skill_id}' ให้ติดตั้งก่อนครับ")
            return None
        
        skill_info = self.installed[skill_id]
        module_path = skill_info["path"]
        
        # โหลดโมดูลแบบไดนามิก
        try:
            spec = importlib.util.spec_from_file_location(skill_id, module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[skill_id] = module
            spec.loader.exec_module(module)
            
            print(f"▶️  กำลังทำงาน: {skill_id}")
            return module
        except Exception as e:
            print(f"❌ เรียกใช้ไม่ได้: {e}")
            return None
    
    # ==================================================
    # 📋 ดูรายการสกิล
    # ==================================================
    def list_skills(self):
        print("\n📋 สกิลที่ติดตั้งแล้ว:")
        if not self.installed:
            print("   (ยังไม่มีสกิลติดตั้ง)")
            return
        
        for idx, (sid, info) in enumerate(self.installed.items(), 1):
            print(f"   {idx}. {sid}")
            print(f"      🔗 {info['url']}")
            print(f"      📅 ติดตั้ง: {info['installed_at'][:19]}")
        print()
    
    # ==================================================
    # 🗑️ ลบสกิล
    # ==================================================
    def uninstall(self, skill_id):
        if skill_id not in self.installed:
            print(f"❌ ไม่พบสกิล '{skill_id}'")
            return False
        
        info = self.installed[skill_id]
        Path(info["path"]).unlink(missing_ok=True)
        del self.installed[skill_id]
        self._save_registry()
        print(f"🗑️  ถอนการติดตั้ง '{skill_id}' แล้ว")
        return True


# ==================================================
# 🚀 เมนูหลัก
# ==================================================
def main():
    manager = SkillManager()
    print("="*60)
    print("🔌 SKILL INSTALLER — ติดตั้งสกิลจาก GitHub")
    print("="*60)
    print()
    
    while True:
        print("📌 เมนู:")
        print("   1. ติดตั้งสกิลจากลิงก์ GitHub")
        print("   2. ดูรายการสกิลที่ติดตั้ง")
        print("   3. เรียกใช้สกิล")
        print("   4. ลบสกิล")
        print("   5. ออก")
        choice = input("\nเลือก: ").strip()
        
        if choice == "1":
            print("\n📥 วางลิงก์ raw.githubusercontent.com ของสกิล")
            print("   (ตัวอย่าง: https://raw.githubusercontent.com/seperneng-spec/ai-skills/main/calculator.py)")
            url = input("   ลิงก์: ").strip()
            sid = input("   ชื่อสั้นๆ (เว้นว่างใช้ชื่อจากไฟล์): ").strip() or None
            manager.install(url, sid)
        
        elif choice == "2":
            manager.list_skills()
        
        elif choice == "3":
            if not manager.installed:
                print("⚠️  ยังไม่มีสกิล ติดตั้งก่อนนะครับ")
                continue
            manager.list_skills()
            sid = input("   เรียกใช้สกิลชื่อ: ").strip()
            manager.run(sid)
        
        elif choice == "4":
            manager.list_skills()
            sid = input("   ลบสกิลชื่อ: ").strip()
            manager.uninstall(sid)
        
        elif choice == "5":
            print("\n👑 ลาก่อนครับ")
            break
        
        print()

if __name__ == "__main__":
    main()

