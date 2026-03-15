import re
import json

with open(r'c:\Users\destacio\.gemini\antigravity\scratch\siniestros_agent\normas_v42.txt', 'r', encoding='utf-8') as f:
    text = f.read()

lines = [l.strip() for l in text.split('\n') if l.strip()]

codes = {}
for line in lines:
    m = re.match(r'^(\d{3})\s+([A-Za-z].*)', line)
    if m:
        code = m.group(1)
        desc = m.group(2).strip()
        
        # some lines have continuation or garbage, let's clean
        desc = desc.split(' | ')[0] # if there's table pipe, stop there
        if len(desc) > 150:
            desc = desc[:147] + '...'
            
        if code not in codes or len(desc) > len(codes.get(code, '')):
            codes[code] = desc

print(f'Unique 3-digit codes found: {len(codes)}')

if '300' in codes:
    print('Code 300 found: ' + codes['300'])
else:
    print('Code 300 NOT found.')

with open(r'c:\Users\destacio\.gemini\antigravity\scratch\siniestros_agent\codes_v42_unique.json', 'w', encoding='utf-8') as f:
    json.dump(codes, f, ensure_ascii=False, indent=2)

print('Sample of keys:')
print(sorted(list(codes.keys()))[:20])
