import json
import sys

with open(r'c:\Users\destacio\.gemini\antigravity\scratch\siniestros_agent\cas_codes_parsed.json', 'r', encoding='utf-8') as f:
    codes = json.load(f)

# Group them and generate the python dictionary format
out = []
out.append('ALL_CAS_CODES = {')
for code in sorted(codes.keys()):
    info = codes[code]
    desc = info['desc'].replace('\"', '\\\"')
    emisor = info['emisor'].strip()
    
    # Try to determine 'tipo' based on first digit or keyword
    tipo = 'DESCONOCIDO'
    if code.startswith('1'): tipo = 'INICIO'
    elif code.startswith('2') or code.startswith('300'): tipo = 'RESPUESTA'
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
    out.append(f'        "nombre": "{desc[:50]}..." if len("{desc}") > 50 else "{desc}",')
    out.append(f'        "descripcion": "{desc}",')
    if emisor and emisor != 'Desconocido':
        if 'CH' in emisor and 'EA' in emisor: emisor_enum = 'AMBOS'
        elif 'CH' in emisor: emisor_enum = 'HOSPITAL'
        elif 'EA' in emisor: emisor_enum = 'ASEGURADORA'
        else: emisor_enum = 'DESCONOCIDO'
        out.append(f'        "emisor": "{emisor_enum}",')
    out.append(f'        "tipo": "{tipo}",')
    out.append(f'    }},')
out.append('}')

with open(r'c:\Users\destacio\.gemini\antigravity\scratch\siniestros_agent\new_codes_dict.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

print(f'Done generating dictionary for {len(codes)} codes.')
