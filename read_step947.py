import json

with open(r'C:\Users\Александр\.gemini\antigravity\brain\8dc77ab2-b9dd-4a62-9311-ed7a2c195cb3\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        data = json.loads(line)
        si = data.get('step_index')
        if si in [947, 948, 949, 950]:
            print(f'=== Step {si} ===')
            content = data.get('content', '')
            if content:
                print(content[:1500])
