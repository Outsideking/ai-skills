import json
from datetime import datetime

CATEGORIES = {
    "งาน": ["ประชุม", "งาน", "ส่ง", "deadline", "รายงาน", "ลูกค้า"],
    "การเงิน": ["จ่าย", "เงิน", "บิล", "ค่า", "ออม", "งบ"],
    "ไอเดีย": ["ไอเดีย", "อยากทำ", "ลองดู", "idea"],
    "ส่วนตัว": ["นัด", "ครอบครัว", "เพื่อน", "เที่ยว", "สุขภาพ"],
}


class SmartNotes:
    def __init__(self, categories=None):
        self.categories = categories or CATEGORIES
        self.notes = []

    def categorize(self, text):
        t = text.lower()
        scores = {c: sum(k in t for k in kws)
                  for c, kws in self.categories.items()}
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else "ทั่วไป"

    def add(self, text):
        note = {
            "text": text.strip(),
            "category": self.categorize(text),
            "time": datetime.now().isoformat(timespec="seconds"),
        }
        self.notes.append(note)
        return note

    def by_category(self):
        out = {}
        for n in self.notes:
            out.setdefault(n["category"], []).append(n["text"])
        return out

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.notes, f, ensure_ascii=False, indent=2)

    def load(self, path):
        try:
            with open(path, encoding="utf-8") as f:
                self.notes = json.load(f)
        except FileNotFoundError:
            self.notes = []
        return self
