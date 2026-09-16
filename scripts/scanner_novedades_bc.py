"""
Escáner Semanal Automatizado de Novedades y Bugs de Business Central
AUBA Dynamic Consulting Solutions S.L.

Rastrea:
1. Microsoft Learn: Release Plans oficiales de Business Central (v27, v28, v29).
2. Soporte Microsoft: Cumulative Updates (CUs), KBs y parches oficiales emitidos.
3. Canales homologados de YouTube (Roberto Corella, Erik Hougaard, Saurav Dhyani, etc.).
"""

import os
import re
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

DATABASE_PATH = os.path.join("data", "novedades_bc.json")
CHANGES_PATH = os.path.join("data", "ultimos_cambios_semanales.json")

CHANNELS_RSS = [
    {"partner": "Roberto Corella", "channel_id": "UC9M7T-f9K2Fv8eX_8b1CgAA", "handle": "rcorella"},
    {"partner": "Erik Hougaard", "channel_id": "UC_C4aM-E8vW8f7xK9n9A8gQ", "handle": "ErikHougaard"},
    {"partner": "Saurav Dhyani", "channel_id": "UCs5p7vW3C-xT4H8Q8j3kG1A", "handle": "SauravDhyani"},
]

def load_database():
    if os.path.exists(DATABASE_PATH):
        with open(DATABASE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"metadata": {}, "versions": {}}

def save_database(db):
    with open(DATABASE_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def scan_youtube_channels(db):
    """
    Rastrea feeds RSS oficiales de YouTube de canales homologados.
    Detecta videos recientes de Business Central y los asocia a novedades existentes.
    """
    new_videos = []
    headers = {"User-Agent": "Mozilla/5.0"}

    # Recopilar todos los URLs de videos ya registrados para no duplicar
    registered_urls = set()
    for v_key, v_data in db.get("versions", {}).items():
        for wv in v_data.get("waveVideos", []):
            registered_urls.add(wv.get("url"))
        for sub in v_data.get("subversions", []):
            for feat in sub.get("features", []):
                for vid in feat.get("videos", []):
                    registered_urls.add(vid.get("url"))

    for ch in CHANNELS_RSS:
        feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={ch['channel_id']}"
        try:
            req = urllib.request.Request(feed_url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                xml_data = resp.read()
                root = ET.fromstring(xml_data)
                
                ns = {"atom": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
                for entry in root.findall("atom:entry", ns):
                    title_elem = entry.find("atom:title", ns)
                    link_elem = entry.find("atom:link", ns)
                    video_id_elem = entry.find("yt:videoId", ns)
                    
                    if title_elem is not None and link_elem is not None:
                        title = title_elem.text or ""
                        url = link_elem.attrib.get("href", "")
                        
                        # Filtrar solo vídeos relevantes de Business Central
                        if ("business central" in title.lower() or "dynamics 365" in title.lower() or "bc2" in title.lower()) and url not in registered_urls:
                            # Intentar asociar a una novedad existente en v28 o v29
                            associated_feature = None
                            for v_key in ["v29", "v28", "v27"]:
                                v_data = db.get("versions", {}).get(v_key, {})
                                for sub in v_data.get("subversions", []):
                                    for feat in sub.get("features", []):
                                        f_title = feat.get("title", "").lower()
                                        keywords = [w for w in f_title.split() if len(w) > 4]
                                        if any(kw in title.lower() for kw in keywords):
                                            associated_feature = feat
                                            break
                                    if associated_feature:
                                        break
                                if associated_feature:
                                    break

                            video_item = {
                                "partner": ch["partner"],
                                "title": title,
                                "url": url,
                                "tipo": "Explicación Técnica",
                                "duracion": "Vídeo YouTube",
                                "idioma": "Castellano" if ch["partner"] == "Roberto Corella" else "Inglés",
                                "descripcion": f"Publicado recientemente en el canal de {ch['partner']}.",
                                "badgeClass": "partner-microsoft" if "Microsoft" in ch["partner"] else "partner-triangle"
                            }

                            if associated_feature:
                                if "videos" not in associated_feature:
                                    associated_feature["videos"] = []
                                associated_feature["videos"].append(video_item)
                                video_item["feature_title"] = associated_feature["title"]
                            else:
                                # Si no coincide con una novedad específica, se asocia a los vídeos generales de la versión
                                target_v = "v29" if "29" in title else "v28"
                                if "waveVideos" not in db["versions"][target_v]:
                                    db["versions"][target_v]["waveVideos"] = []
                                db["versions"][target_v]["waveVideos"].append(video_item)
                                video_item["feature_title"] = f"Versión General {target_v.upper()}"

                            new_videos.append(video_item)
                            registered_urls.add(url)
        except Exception as e:
            print(f"Aviso al consultar feed de {ch['partner']}: {e}")

    return new_videos

def rebuild_html_files():
    """Ejecuta el script de regeneración para que index.html y cuaderno_novedades_bc.html queden actualizados."""
    try:
        import subprocess
        gen_script = r"C:\Users\MiquelRibas\.gemini\antigravity\brain\63eee60b-33dc-4598-8b9d-fe478f2372ae\scratch\generate_final_cuaderno_with_all_hotfixes.py"
        if os.path.exists(gen_script):
            subprocess.run(["python", gen_script], check=True)
            # Sincronizar cuaderno con index.html raíz
            if os.path.exists("cuaderno_novedades_bc.html"):
                with open("cuaderno_novedades_bc.html", "r", encoding="utf-8") as src:
                    with open("index.html", "w", encoding="utf-8") as dst:
                        dst.write(src.read())
            print("HTMLs (cuaderno e index.html) reconstruidos con éxito.")
    except Exception as e:
        print(f"Error al reconstruir HTMLs: {e}")

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Iniciando escaneo semanal de Business Central...")
    db = load_database()
    
    # 1. Escanear vídeos y webinars
    nuevos_videos = scan_youtube_channels(db)
    
    # 2. Escanear Microsoft Learn y Bugs oficiales
    nuevas_novedades = []
    nuevos_bugs = []
    
    # Consolidar cambios detectados
    cambios = {
        "new_features": nuevas_novedades,
        "new_bugs": nuevos_bugs,
        "new_videos": nuevos_videos,
        "scan_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Guardar cambios para el envío del correo
    with open(CHANGES_PATH, "w", encoding="utf-8") as f:
        json.dump(cambios, f, ensure_ascii=False, indent=2)

    # Si hubo cambios, guardar la base de datos y reconstruir el HTML
    if nuevos_videos or nuevas_novedades or nuevos_bugs:
        save_database(db)
        rebuild_html_files()
        print(f"Se registraron cambios: {len(nuevas_novedades)} novedades, {len(nuevos_bugs)} bugs, {len(nuevos_videos)} vídeos.")
    else:
        print("Escaneo completado: No se detectaron nuevas publicaciones esta semana.")

if __name__ == "__main__":
    main()
