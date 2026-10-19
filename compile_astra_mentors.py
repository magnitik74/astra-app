import json
import os

with open(r"D:\projects\monly\АСТРА_АССЕТЫ\astra_ru_data\astra_mentors_system.json", "r", encoding="utf-8") as f:
    mentors_data = json.load(f)

personas = mentors_data.get("personas", [])

js_content = """// ASTRA 5 AI MENTORS & CONTEXTUAL INSIGHTS ENGINE
const ASTRA_MENTORS = """ + json.dumps(personas, ensure_ascii=False, indent=2) + """;

let currentMentorIndex = 0; // Default: Алтея (Luna Altea)

function getActiveMentor() {
  return ASTRA_MENTORS[currentMentorIndex] || ASTRA_MENTORS[0];
}

function setMentor(index) {
  if (index >= 0 && index < ASTRA_MENTORS.length) {
    currentMentorIndex = index;
    updateMentorUI();
  }
}
""";

out_file = r"D:\projects\monly\АСТРА_АССЕТЫ\astra_mentors_engine.js"
with open(out_file, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"Saved {out_file}")
