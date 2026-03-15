import sys

with open(r'c:\Users\destacio\.gemini\antigravity\scratch\siniestros_agent\cas_codes.py', 'r', encoding='utf-8') as f:
    cas_codes_content = f.read()

with open(r'c:\Users\destacio\.gemini\antigravity\scratch\siniestros_agent\new_codes_dict_v42.py', 'r', encoding='utf-8') as f:
    new_codes_content = f.read()

start_idx = cas_codes_content.find('CAS_CODES = {')
end_idx = cas_codes_content.find('}\n\n# ============================================================', start_idx) + 1

if start_idx != -1 and end_idx != -1:
    new_content = cas_codes_content[:start_idx] + new_codes_content.replace('ALL_CAS_CODES =', 'CAS_CODES =') + '\n\n# ============================================================\n' + cas_codes_content[end_idx:]
    with open(r'c:\Users\destacio\.gemini\antigravity\scratch\siniestros_agent\cas_codes.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('Successfully updated CAS_CODES in cas_codes.py')
else:
    print('Failed to find CAS_CODES boundaries in cas_codes.py')
