import json

with open(r'c:\Users\destacio\.gemini\antigravity\scratch\siniestros_agent\codes_v42_unique.json', 'r', encoding='utf-8') as f:
    codes = json.load(f)

out = []
out.append('ALL_CAS_CODES = {')
for code in sorted(codes.keys()):
    desc = codes[code].replace('"', '\\"').replace('\n', ' ')
    
    tipo = 'DESCONOCIDO'
    if code.startswith('1'): tipo = 'INICIO'
    elif code.startswith('2'): tipo = 'RESPUESTA'
    elif code.startswith('3'): tipo = 'DOCUMENTACION'
    elif code.startswith('4'): tipo = 'CONFIRMACION'
    elif code.startswith('5'): tipo = 'FACTURACION'
    elif code.startswith('6'): tipo = 'PAGO'
    elif code.startswith('7'): tipo = 'PAGO'
    elif code.startswith('8'): tipo = 'RECLAMACION'
    elif code.startswith('9'): 
        if code == '999': tipo = 'CIERRE'
        else: tipo = 'REHUSE'
        
    out.append(f'    "{code}": {{')
    out.append(f'        "nombre": "{desc[:60]}..." if len("{desc}") > 60 else "{desc}",')
    out.append(f'        "descripcion": "{desc}",')
    out.append(f'        "emisor": "DESCONOCIDO",') 
    out.append(f'        "tipo": "{tipo}",')
    out.append(f'    }},')
out.append('}')

with open(r'c:\Users\destacio\.gemini\antigravity\scratch\siniestros_agent\new_codes_dict_v42.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
    
print(f'Wrote dictionary for {len(codes)} codes.')
