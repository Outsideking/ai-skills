# -*- coding: utf-8 -*-
"""
==================================================
🛠️ SKILL CREATOR — สร้างสกิลและอัปโหลดไป GitHub
เวอร์ชัน: 1.0.0
ใช้งาน: เขียนสกิล → บันทึก → อัปโหลด → ได้ลิงก์
==================================================
"""

import json
import base64
import datetime
from pathlib import Path
import urllib.request
import urllib.error
import ssl

# ปิด SSL สำหรับมือถือ
ssl._create_default_https_context = ssl._create_unverified_context

# ==================================================
# ⚙️ ตั้งค่า GitHub — แก้ตรงนี้
# ==================================================
GITHUB_TOKEN = "ใส่โทเค็น ghp_... ที่นี่"
GITHUB_USER = "seperneng-spec"
GITHUB_REPO = "ai-skills"  # แนะนำสร้างรีโปใหม่ชื่อนี้

# ==================================================
# 📝 สร้างไฟล์สกิล
# ==================================================
def create_skill_file(skill_id, name, description, code, author="Vider System"):
    """สร้างไฟล์สกิลในรูปแบบมาตรฐาน"""
    skill_data = {
        "skill_id": skill_id,
        "name": name,
        "description": description,
        "author": author,
        "version": "1.0.0",
        "created": datetime.datetime.now().isoformat(),
        "main": f"{skill_id}.py",
        "commands": extract_commands(code)
    }
    
    # บันทึกไฟล์ข้อมูลสกิล
    Path("skills").mkdir(exist_ok=True)
    json_path = Path(f"skills/{skill_id}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(skill_data, f, ensure_ascii=False, indent=2)
    
    # บันทึกไฟล์โค้ด
    py_path = Path(f"skills/{skill_id}.py")
    with open(py_path, 'w', encoding='utf-8') as f:
        f.write(code)
    
    print(f"✅ สร้างสกิล: {name}")
    print(f"   📄 {json_path}")
    print(f"   📄 {py_path}")
    return skill_data

def extract_commands(code):
    """แยกคำสั่งจากโค้ด"""
    commands = []
    for line in code.split('\n'):
        if line.strip().startswith('def '):
            cmd_name = line.split('def ')[1].split('(')[0].strip()
            commands.append(cmd_name)
    return commands

# ==================================================
# ☁️ อัปโหลดไป GitHub
# ==================================================
def upload_to_github(file_path, github_path, message="Add new skill"):
    """อัปโหลดไฟล์ขึ้นรีโป GitHub"""
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{github_path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "Skill-Creator"
    }
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    data = json.dumps({
        "message": message,
        "content": base64.b64encode(content.encode('utf-8')).decode(),
        "branch": "main"
    }).encode('utf-8')
    
    try:
        req = urllib.request.Request(url, data=data, headers=headers, method="PUT")
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read().decode())
            return result.get("content", {}).get("html_url", "success")
    except urllib.error.HTTPError as e:
        print(f"❌ อัปโหลดไม่ได้: {e.code}")
        print(e.read().decode())
        return None
    except Exception as e:
        print(f"❌ ผิดพลาด: {e}")
        return None

# ==================================================
# 🚀 เมนูหลัก
# ==================================================
def main():
    print("="*60)
    print("🛠️  SKILL CREATOR — สร้างสกิลและอัปโหลดไป GitHub")
    print("="*60)
    print()
    
    while True:
        print("📌 เมนู:")
        print("   1. สร้างสกิลใหม่")
        print("   2. อัปโหลดสกิลทั้งหมดไป GitHub")
        print("   3. ออก")
        choice = input("\nเลือก: ").strip()
        
        if choice == "1":
            print("\n📝 สร้างสกิลใหม่")
            skill_id = input("   รหัสสกิล (ภาษาอังกฤษ เช่น calculator): ").strip()
            name = input("   ชื่อสกิล: ").strip()
            desc = input("   คำอธิบายสั้นๆ: ").strip()
            print("   พิมพ์โค้ดสกิล (พิมพ์ --- เมื่อจบ):")
            code_lines = []
            while True:
                line = input("   │ ")
                if line.strip() == "---":
                    break
                code_lines.append(line)
            code = "\n".join(code_lines)
            
            skill_data = create_skill_file(skill_id, name, desc, code)
            print(f"\n✨ สกิล '{name}' สร้างสำเร็จ!")
        
        elif choice == "2":
            print("\n☁️  กำลังอัปโหลด...")
            skill_dir = Path("skills")
            if not skill_dir.exists():
                print("⚠️  ยังไม่มีสกิล ให้สร้างก่อนครับ")
                continue
            
            uploaded_links = []
            for f in skill_dir.iterdir():
                if f.is_file():
                    github_path = f.name
                    print(f"   กำลังอัปโหลด: {f.name}...")
                    url = upload_to_github(f, github_path, f"Update {f.name}")
                    if url:
                        raw_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/{github_path}"
                        uploaded_links.append((f.name, raw_url))
                        print(f"   ✅ สำเร็จ")
            
            print("\n" + "="*60)
            print("🎉 อัปโหลดเสร็จสิ้น!")
            print("📋 ลิงก์สำหรับนำไปใช้งาน:")
            for fname, link in uploaded_links:
                print(f"\n📄 {fname}:")
                print(f"   🔗 {link}")
            print("="*60)
        
        elif choice == "3":
            print("\n👑 ลาก่อนครับ")
            break
        
        print()

if __name__ == "__main__":
    main()

