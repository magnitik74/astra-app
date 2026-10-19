import zipfile
import json
import io
import os

xapk = r"C:\Users\Александр\Downloads\Moonly_+Moon+Phases+&+Calendar_1.0.326_APKPure.xapk"
out_dir = r"D:\projects\monly\АСТРА_АССЕТЫ"
os.makedirs(out_dir, exist_ok=True)

with zipfile.ZipFile(xapk) as xz:
    data = xz.read('com.moonly.android.apk')
    with zipfile.ZipFile(io.BytesIO(data)) as apk:
        tarot_content = json.loads(apk.read('assets/content/tarot/content.json').decode('utf-8'))
        tarot_texts = json.loads(apk.read('assets/content/tarot/texts/ru.json').decode('utf-8'))
        runes_texts = json.loads(apk.read('assets/content/runes/ru.json').decode('utf-8'))

taros = tarot_content.get('taros', {}).get('items', [])
compiled_tarot = []

for c in taros:
    cid = c.get('id')
    name_key = c.get('name')
    name_ru = tarot_texts.get(name_key, name_key)
    brief_key = c.get('brief')
    brief_ru = tarot_texts.get(brief_key, "")
    
    # Description default (upright)
    def_desc = c.get('description', {}).get('position_default', {})
    d1 = def_desc.get('first_description', {})
    d1_text = tarot_texts.get(d1.get('text', ''), '')
    d1_rec_title = tarot_texts.get(d1.get('rec_title', ''), 'Рекомендации')
    d1_rec_text = tarot_texts.get(d1.get('rec_text', ''), '')
    
    d2 = def_desc.get('second_description', {})
    d2_text = tarot_texts.get(d2.get('text', ''), '')
    
    d3 = def_desc.get('third_description', {})
    d3_text = tarot_texts.get(d3.get('text', ''), '')

    # Description alternative (reversed)
    alt_desc = c.get('description', {}).get('position_alternative', {})
    alt_d1 = alt_desc.get('first_description', {})
    alt_text = tarot_texts.get(alt_d1.get('text', ''), '')
    alt_rec_text = tarot_texts.get(alt_d1.get('rec_text', ''), '')

    compiled_tarot.append({
        'id': cid,
        'name': name_ru,
        'image': c.get('image'),
        'num_arab': c.get('num_arab'),
        'num_roman': c.get('num_roman'),
        'arcana': c.get('arcana'),
        'suit': c.get('suit'),
        'rank': c.get('rank'),
        'free': c.get('free', True),
        'brief': brief_ru,
        'upright': {
            'text': d1_text,
            'rec_title': d1_rec_title,
            'rec_text': d1_rec_text,
            'meaning_2': d2_text,
            'meaning_3': d3_text
        },
        'reversed': {
            'text': alt_text or d1_text,
            'rec_title': 'Рекомендации',
            'rec_text': alt_rec_text or d1_rec_text
        }
    })

print(f"Compiled {len(compiled_tarot)} tarot cards.")

# Export to JS
js_content = f"// ASTRA TAROT & RUNES DATABASE (CLEAN-ROOM COMPILATION)\n"
js_content += f"const ASTRA_TAROT_DATABASE = {json.dumps(compiled_tarot, ensure_ascii=False, indent=2)};\n\n"
js_content += f"const ASTRA_RUNES_DATABASE = {json.dumps(runes_texts, ensure_ascii=False, indent=2)};\n"

out_file = os.path.join(out_dir, "astra_tarot_runes_data.js")
with open(out_file, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"Saved to {out_file}")
