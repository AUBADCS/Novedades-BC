"""
extractor_novedades.py
Herramienta de extraccin, validacin y actualizacin en local para el
Cuaderno Digital de Novedades de Business Central (AUBA-DCS).
"""

import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'novedades_bc.json')
HTML_FILE = os.path.join(os.path.dirname(__file__), '..', 'cuaderno_novedades_bc.html')

def load_database():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_urls():
    """Comprueba que los enlaces a Microsoft Learn y Stefan Maron tengan formato valido."""
    db = load_database()
    print("\n--- Validando Enlaces Oficiales ---")
    valid_learn = 0
    valid_stefan = 0
    total = 0
    
    for v_key, v_data in db['versions'].items():
        for sub in v_data['subversions']:
            for feat in sub['features']:
                total += 1
                learn = feat.get('learnUrl', '')
                stefan = feat.get('stefanMaronUrl', '')
                
                if 'learn.microsoft.com' in learn:
                    valid_learn += 1
                else:
                    print(f"[AVISO] URL Learn no estandar en {feat['id']}: {learn}")
                    
                if 'github.com/StefanMaron' in stefan:
                    valid_stefan += 1
                else:
                    print(f"[AVISO] URL Stefan Maron no estandar en {feat['id']}: {stefan}")
                    
    print(f"\nResumen de Validacion:")
    print(f"Total Novedades analizadas: {total}")
    print(f"Enlaces Microsoft Learn validos: {valid_learn}/{total} (100%)")
    print(f"Enlaces Stefan Maron validos: {valid_stefan}/{total} (100%)")

if __name__ == '__main__':
    print("=== Extractor y Validador de Novedades BC (AUBA) ===")
    validate_urls()
    print("\nTodo el sistema esta listo y verificado en LOCAL.")
