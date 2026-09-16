"""
Envío del Informe Corporativo Semanal - AUBA Dynamics
Conecta con servidor SMTP (si está configurado en GitHub Secrets o local)
o guarda el reporte en local para revisión.
"""

import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from generador_correo_semanal import generar_html_correo

def enviar_reporte():
    cambios_file = os.path.join("data", "ultimos_cambios_semanales.json")
    if os.path.exists(cambios_file):
        with open(cambios_file, "r", encoding="utf-8") as f:
            cambios = json.load(f)
    else:
        cambios = {"new_features": [], "new_bugs": [], "new_videos": []}

    html_content = generar_html_correo(cambios)

    # Guardar copia local del correo
    with open("reporte_semanal_correo.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Reporte de correo guardado localmente en: reporte_semanal_correo.html")

    smtp_server = os.environ.get("SMTP_SERVER")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    email_to = os.environ.get("EMAIL_TO")

    if not (smtp_server and smtp_user and smtp_password and email_to):
        print("Aviso: Credenciales SMTP no configuradas. El correo se ha generado en local con exito.")
        return

    try:
        msg = MIMEMultipart("alternative")
        fecha_str = datetime.now().strftime("%d/%m/%Y")
        
        hay_novedades = bool(cambios.get("new_features") or cambios.get("new_bugs") or cambios.get("new_videos"))
        if hay_novedades:
            asunto = f"[AUBA DCS] Actualizaciones de Business Central detectadas ({fecha_str})"
        else:
            asunto = f"[AUBA DCS] Resumen Semanal Business Central - Sin novedades ({fecha_str})"

        msg["Subject"] = asunto
        msg["From"] = smtp_user
        msg["To"] = email_to

        part = MIMEText(html_content, "html", "utf-8")
        msg.attach(part)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, [e.strip() for e in email_to.split(",")], msg.as_string())
        
        print(f"Correo enviado exitosamente a: {email_to}")
    except Exception as e:
        print(f"Error al enviar correo por SMTP: {e}")

if __name__ == "__main__":
    enviar_reporte()
