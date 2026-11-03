# -*- coding: utf-8 -*-
"""
==================================================
🧠 AI-SKILL LEARNER — ระบบเรียนรู้และสร้างสกิลอัจฉริยะ
เวอร์ชัน: 2.0.0
ทำงาน: วิเคราะห์โค้ด/โปรแกรม → แยกเป็นเครื่องมือ → สร้างสกิลใหม่ได้
==================================================
"""

import json
import re
import ast
import datetime
from pathlib import Path
from collections import defaultdict

# ==================================================
# 🧠 ฐานข้อมูลความรู้เกี่ยวกับโปรแกรมและรูปแบบโค้ด
# ==================================================
PROGRAM_PATTERNS = {
    "API_Request": {
        "keywords": ["requests", "urllib", "http", "api", "get(", "post("],
        "category": "network",
        "template": """# สกิล: เชื่อมต่อ API ภายนอก
import requests

def fetch_data(url, timeout=10):
    \"\"\"ดึงข้อมูลจาก API/เว็บไซต์\"\"\"
    try:
        r = requests.get(url, timeout=timeout)
        return {"success": True, "data": r.json() if r.headers.get('content-type', '').startswith('application/json') else r.text, "status": r.status_code}
    except Exception as e:
        return {"success": False, "error": str(e)}
"""
    },
    "File_Manager": {
        "keywords": ["open(", "Path", "os.", "json.load", "json.dump", "read", "write"],
        "category": "file",
        "template": """# สกิล: จัดการไฟล์และข้อมูล
import json
from pathlib import Path

def save_json(data, filepath):
    \"\"\"บันทึกข้อมูลเป็นไฟล์ JSON\"\"\"
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True

def load_json(filepath):
    \"\"\"อ่านข้อมูลจากไฟล์ JSON\"\"\"
    if not Path(filepath).exists():
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
"""
    },
    "Text_Processor": {
        "keywords": ["split", "replace", "strip", "re.", "match", "search", "sub"],
        "category": "text",
        "template": """# สกิล: ประมวลผลข้อความ
import re

def extract_between(text, start, end):
    \"\"\"แยกข้อความระหว่างข้อความสองส่วน\"\"\"
    try:
        pattern = re.escape(start) + r'(.*?)' + re.escape(end)
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else None
    except:
        return None

def clean_text(text):
    \"\"\"ลบช่องว่างและอักขระพิเศษซ้ำซ้อน\"\"\"
    return ' '.join(text.split())
"""
    },
    "GitHub_Uploader": {
        "keywords": ["github", "api.github.com", "token", "base64", "content"],
        "category": "github",
        "template": """# สกิล: อัปโหลดไฟล์ไป GitHub
import json
import base64
import urllib.request

def upload_to_github(token, user, repo, filepath, content, message="Update file", branch="main"):
    \"\"\"เขียนไฟล์ขึ้นรีโป GitHub\"\"\"
    import urllib.error
    url = f"https://api.github.com/repos/{user}/{repo}/contents/{filepath}"
    headers = {"Authorization": f"token {token}", "Content-Type": "application/json"}
    data = json.dumps({
        "message": message,
        "content": base64.b64encode(content.encode('utf-8')).decode(),
        "branch": branch
    }).encode('utf-8')
    try:
        req = urllib.request.Request(url, data=data, headers=headers, method="PUT")
        with urllib.request.urlopen(req, timeout=30) as r:
            return {"success": True, "result": json.loads(r.read().decode())}
    except Exception as e:
        return {"success": False, "error": str(e)}
"""
    },
    "Data_Analyzer": {
        "keywords": ["sum(", "len(", "max(", "min(", "sorted", "filter", "map", "statistics"],
        "category": "data",
        "template": """# สกิล: วิเคราะห์ข้อมูลเบื้องต้น
def analyze_list(data_list):
    \"\"\"คำนวณค่าสถิติพื้นฐานจากรายการข้อมูล\"\"\"
    if not data_list:
        return {"count": 0, "message": "ไม่มีข้อมูล"}
    numbers = [x for x in data_list if isinstance(x, (int, float))]
    return {
        "count": len(data_list),
        "numeric_count": len(numbers),
        "sum": sum(numbers) if numbers else None,
        "max": max(numbers) if numbers else None,
        "min": min(numbers) if numbers else None,
        "average": sum(numbers)/len(numbers) if numbers else None
    }
"""
    }
}

# ==================================================
# 🔬 ตัววิเคราะห์โค้ด — แยกส่วนประกอบและฟังก์ชัน
# ==================================================
class CodeAnalyzer:
    def __init__(self):
        self.functions = []
        self.imports = []
        self.variables = []
        self.detected_patterns = []
    
    def analyze(self, code_text):
        """วิเคราะห์โค้ดและแยกส่วนประกอบสำคัญ"""
        self.functions = []
        self.imports = []
        self.detected_patterns = []
        
        try:
            tree = ast.parse(code_text)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    args = [a.arg for a in node.args.args]
                    self.functions.append({
                        "name": node.name,
                        "args": args,
                        "docstring": ast.get_docstring(node) or ""
                    })
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        self.imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    self.imports.append(node.module or "")
        except SyntaxError:
            # ถ้า parse ไม่ได้ ใช้ regex แทน
            self.functions = re.findall(r'def\s+(\w+)\s*\(([^)]*)\)', code_text)
            self.functions = [{"name": f[0], "args": [a.strip() for a in f[1].split(',') if a.strip()]} for f in self.functions]
            self.imports = re.findall(r'^import\s+(\w+)', code_text, re.MULTILINE)
            self.imports += re.findall(r'^from\s+(\w+)\s+import', code_text, re.MULTILINE)
        
        # ตรวจจับรูปแบบโปรแกรม
        for pattern_name, pattern_info in PROGRAM_PATTERNS.items():
            score = sum(1 for kw in pattern_info["keywords"] if kw in code_text)
            if score >= 2:
                self.detected_patterns.append({
                    "name": pattern_name,
                    "category": pattern_info["category"],
                    "match_score": score
                })
        
        return {
            "functions": self.functions,
            "imports": self.imports,
            "patterns": self.detected_patterns
        }

# ==================================================
# 🧠 ตัวเรียนรู้ — สร้างสกิลใหม่จากสิ่งที่พบ
# ==================================================
class SkillLearner:
    def __init__(self, knowledge_base="skill_knowledge.json"):
        self.kb_path = Path(knowledge_base)
        self.learned_skills = {}
        self.analyzer = CodeAnalyzer()
        self._load_knowledge()
    
    def _load_knowledge(self):
        if self.kb_path.exists():
            with open(self.kb_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.learned_skills = data.get("skills", {})
        else:
            self.learned_skills = {}
            self._save_knowledge()
    
    def _save_knowledge(self):
        data = {
            "skills": self.learned_skills,
            "updated": datetime.datetime.now().isoformat(),
            "total_learned": len(self.learned_skills)
        }
        with open(self.kb_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # ──────────────────────────────────────────────
    # 📚 เรียนรู้จากโค้ด/โปรแกรม
    # ──────────────────────────────────────────────
    def learn_from_code(self, code_text, source_name="unknown_program"):
        """วิเคราะห์โค้ด → แยกเครื่องมือ → บันทึกเป็นความรู้"""
        print(f"\n🧠 กำลังเรียนรู้จาก: {source_name}")
        
        analysis = self.analyzer.analyze(code_text)
        
        print(f"   📦 พบโมดูลที่ใช้: {', '.join(analysis['imports']) or '-'}")
        print(f"   🔧 พบฟังก์ชัน: {len(analysis['functions'])} รายการ")
        
        skills_created = []
        
        # สร้างสกิลจากรูปแบบที่ตรวจพบ
        for pattern in analysis["patterns"]:
            pid = pattern["name"]
            if pid in PROGRAM_PATTERNS:
                skill_id = f"auto_{pid.lower()}"
                skill_name = pid.replace("_", " ")
                skill_code = PROGRAM_PATTERNS[pid]["template"]
                
                self.learned_skills[skill_id] = {
                    "name": skill_name,
                    "category": pattern["category"],
                    "source": source_name,
                    "created": datetime.datetime.now().isoformat(),
                    "code": skill_code,
                    "functions": [f["name"] for f in analysis["functions"] if hasattr(f, '__getitem__')] or [],
                    "pattern_match": pattern["match_score"]
                }
                skills_created.append(skill_id)
                print(f"   ✅ สร้างสกิลอัตโนมัติ: {skill_name}")
        
        # สร้างสกิลจากฟังก์ชันที่พบ
        for func in analysis["functions"]:
            if isinstance(func, dict):
                func_name = func["name"]
                skill_id = f"func_{func_name.lower()}"
                if skill_id not in self.learned_skills:
                    self.learned_skills[skill_id] = {
                        "name": f"ฟังก์ชัน: {func_name}",
                        "category": "extracted",
                        "source": source_name,
                        "created": datetime.datetime.now().isoformat(),
                        "functions": [func_name],
                        "args": func.get("args", []),
                        "docstring": func.get("docstring", "")
                    }
                    skills_created.append(skill_id)
        
        self._save_knowledge()
        return {"learned": len(skills_created), "skills": skills_created}
    
    # ──────────────────────────────────────────────
    # 🧪 ประยุกต์ใช้ความรู้ → สร้างสกิลใหม่
    # ──────────────────────────────────────────────
    def generate_skill(self, purpose, skill_id=None):
        """ใช้ความรู้ที่มีสร้างสกิลใหม่ตามวัตถุประสงค์"""
        if not skill_id:
            skill_id = f"gen_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # ค้นหาสกิลที่เกี่ยวข้อง
        related = []
        purpose_lower = purpose.lower()
        for sid, skill in self.learned_skills.items():
            score = sum(1 for w in purpose_lower.split() if w in skill.get("name", "").lower() or w in skill.get("category", ""))
            if score > 0:
                related.append((sid, skill, score))
        
        related.sort(key=lambda x: x[2], reverse=True)
        
        print(f"\n🧪 กำลังสร้างสกิลสำหรับ: {purpose}")
        if related:
            print(f"   📖 ใช้ความรู้จาก: {', '.join([s[1]['name'] for s in related[:3]])}")
        else:
            print("   ⚠️  ไม่พบความรู้ที่เกี่ยวข้องโดยตรง ใช้แม่แบบพื้นฐาน")
        
        # ประกอบร่างสกิลใหม่
        imports_needed = set()
        functions_combined = []
        
        for sid, skill, _ in related[:2]:
            if "code" in skill:
                for imp in re.findall(r'^import\s+(\w+)', skill["code"], re.MULTILINE):
                    imports_needed.add(imp)
                for func_match in re.findall(r'(def\s+\w+\s*\([^)]*\):.*?(?=\ndef|\Z))', skill["code"], re.DOTALL):
                    functions_combined.append(func_match)
        
        # เขียนโค้ดสกิลใหม่
        code_lines = []
        code_lines.append("# -*- coding: utf-8 -*-")
        code_lines.append(f'"""')
        code_lines.append(f"# สกิลที่สร้างโดย AI-Skill Learner")
        code_lines.append(f"# วัตถุประสงค์: {purpose}")
        code_lines.append(f'# สร้างเมื่อ: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        code_lines.append(f'"""')
        code_lines.append("")
        
        if imports_needed:
            for imp in imports_needed:
                code_lines.append(f"import {imp}")
            code_lines.append("")
        
        if functions_combined:
            code_lines.extend(functions_combined[:3])  # จำกัดไม่ให้ยาวเกินไป
        else:
            code_lines.append("def main():")
            code_lines.append(f'    """ฟังก์ชันหลักสำหรับ: {purpose}"""')
            code_lines.append("    print(f'✅ กำลังทำงาน: {purpose}')")
            code_lines.append("    return {'status': 'ready', 'purpose': purpose}")
        
        code_lines.append("")
        code_lines.append("if __name__ == '__main__':")
        code_lines.append("    main()")
        
        final_code = "\n".join(code_lines)
        
        # บันทึกสกิลใหม่
        self.learned_skills[skill_id] = {
            "name": purpose,
            "category": "generated",
            "purpose": purpose,
            "created": datetime.datetime.now().isoformat(),
            "code": final_code,
            "based_on": [s[0] for s in related[:3]]
        }
        self._save_knowledge()
        
        # บันทึกไฟล์
        Path("generated_skills").mkdir(exist_ok=True)
        out_path = Path(f"generated_skills/{skill_id}.py")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(final_code)
        
        print(f"   ✅ สร้างสกิลสำเร็จ: {out_path}")
        return final_code
    
    # ──────────────────────────────────────────────
    # 📋 ดูรายการความรู้
    # ──────────────────────────────────────────────
    def list_skills(self, category=None):
        print("\n📚 คลังความรู้สกิลทั้งหมด:")
        count = 0
        for sid, skill in self.learned_skills.items():
            if category and skill.get("category") != category:
                continue
            count += 1
            print(f"   {count}. [{skill.get('category', '—')}] {skill.get('name', sid)}")
            print(f"      ID: {sid} | แหล่ง: {skill.get('source', 'สร้างเอง')}")
        if count == 0:
            print("   (ยังไม่มีความรู้)")
        print(f"\n   📊 รวมทั้งหมด: {len(self.learned_skills)} สกิล")
        return count


# ==================================================
# 🚀 เมนูหลัก
# ==================================================
def main():
    learner = SkillLearner()
    print("╔" + "═"*60 + "╗")
    print("║  🧠 AI-SKILL LEARNER — เรียนรู้ สร้าง ประยุกต์ใช้                    ║")
    print("╠" + "═"*60 + "╣")
    print(f"║  คลังความรู้: {len(learner.learned_skills)} สกิล ที่พร้อมใช้งาน{' '*30}║")
    print("╚" + "═"*60 + "╝")
    
    while True:
        print("\n📌 เมนูหลัก:")
        print("   1. 📖 เรียนรู้จากโค้ด/โปรแกรม (วางโค้ด)")
        print("   2. 📂 เรียนรู้จากไฟล์.py ในเครื่อง")
        print("   3. 🧪 สร้างสกิลใหม่ตามวัตถุประสงค์")
        print("   4. 📋 ดูคลังความรู้ทั้งหมด")
        print("   5. 📤 ส่งออกสกิลไปใช้งาน")
        print("   6. ❌ ออก")
        
        choice = input("\nเลือก: ").strip()
        
        if

