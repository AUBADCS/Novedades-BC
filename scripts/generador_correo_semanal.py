"""
Generador de Correo Corporativo Semanal - AUBA Dynamics
Estructura oficial solicitada por Miquel:
1. Novedades encontradas (arriba)
2. Bugs corregidos e incidencias oficiales resueltas (en medio)
3. Enlaces a vídeos encontrados (abajo)
"""

import os
from datetime import datetime

def generar_html_correo(cambios, url_cuaderno="https://miquelangelribas.github.io/novedades-bc/"):
    fecha_str = datetime.now().strftime("%d/%m/%Y")
    novedades = cambios.get("new_features", [])
    bugs = cambios.get("new_bugs", [])
    videos = cambios.get("new_videos", [])
    
    hay_cambios = bool(novedades or bugs or videos)
    
    # 1. Bloque de Novedades (Arriba)
    if novedades:
        filas_novedades = ""
        for n in novedades:
            filas_novedades += f"""
            <tr style="border-bottom: 1px solid #e2e8f0;">
                <td style="padding: 12px 14px; font-size: 13px; color: #1e293b; font-weight: 600;">
                    <span style="display: inline-block; padding: 2px 8px; font-size: 11px; background: #eff6fc; color: #0f6cbd; border-radius: 4px; margin-right: 6px; border: 1px solid #bfdbfe;">
                        {n.get('version', 'BC')}
                    </span>
                    {n.get('title', '')}
                </td>
                <td style="padding: 12px 14px; font-size: 12px; color: #64748b; white-space: nowrap;">
                    {n.get('pillar', 'Aplicación')}
                </td>
                <td style="padding: 12px 14px; text-align: right; white-space: nowrap;">
                    <a href="{n.get('url', '#')}" target="_blank" style="display: inline-block; padding: 5px 10px; font-size: 11px; font-weight: 600; color: #0f6cbd; background: #eff6fc; border: 1px solid #bfdbfe; border-radius: 4px; text-decoration: none;">
                        Ver en Learn &rarr;
                    </a>
                </td>
            </tr>
            """
        bloque_novedades = f"""
        <div style="margin-bottom: 28px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
            <div style="background: #f8fafc; padding: 12px 18px; border-bottom: 1px solid #e2e8f0;">
                <h3 style="margin: 0; font-size: 15px; color: #0f172a; font-family: 'Segoe UI', Arial, sans-serif;">
                    📢 1. Nuevas Novedades Detectadas ({len(novedades)})
                </h3>
            </div>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                <thead>
                    <tr style="background: #f1f5f9; text-align: left; font-size: 11px; color: #475569; text-transform: uppercase; letter-spacing: 0.5px;">
                        <th style="padding: 8px 14px;">Novedad / Funcionalidad</th>
                        <th style="padding: 8px 14px;">Área / Pilar</th>
                        <th style="padding: 8px 14px; text-align: right;">Documentación</th>
                    </tr>
                </thead>
                <tbody>
                    {filas_novedades}
                </tbody>
            </table>
        </div>
        """
    else:
        bloque_novedades = """
        <div style="margin-bottom: 24px; padding: 14px 18px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; color: #64748b; font-size: 13px;">
            📢 <strong>1. Nuevas Novedades:</strong> No se han publicado nuevas funcionalidades en Microsoft Learn durante esta semana.
        </div>
        """

    # 2. Bloque de Bugs e Incidencias Resueltas (En medio)
    if bugs:
        filas_bugs = ""
        for b in bugs:
            filas_bugs += f"""
            <tr style="border-bottom: 1px solid #fecdd3;">
                <td style="padding: 10px 14px; font-size: 12px; font-weight: 700; color: #be123c; font-family: Consolas, monospace; white-space: nowrap;">
                    KB {b.get('kb', '')}
                </td>
                <td style="padding: 10px 14px; font-size: 13px; color: #334155;">
                    {b.get('problem', '')}
                </td>
                <td style="padding: 10px 14px; font-size: 12px; color: #64748b; white-space: nowrap;">
                    {b.get('module', 'General')}
                </td>
            </tr>
            """
        bloque_bugs = f"""
        <div style="margin-bottom: 28px; background: #ffffff; border: 1px solid #fecdd3; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 6px rgba(190,18,60,0.03);">
            <div style="background: #fff1f2; padding: 12px 18px; border-bottom: 1px solid #fecdd3;">
                <h3 style="margin: 0; font-size: 15px; color: #9f1239; font-family: 'Segoe UI', Arial, sans-serif;">
                    🛠️ 2. Incidencias Oficiales Resueltas por Microsoft - Bugs / Parches ({len(bugs)})
                </h3>
            </div>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                <thead>
                    <tr style="background: #fff5f5; text-align: left; font-size: 11px; color: #9f1239; text-transform: uppercase; letter-spacing: 0.5px;">
                        <th style="padding: 8px 14px;">Identificador</th>
                        <th style="padding: 8px 14px;">Problema / Error Corregido</th>
                        <th style="padding: 8px 14px;">Módulo</th>
                    </tr>
                </thead>
                <tbody>
                    {filas_bugs}
                </tbody>
            </table>
        </div>
        """
    else:
        bloque_bugs = """
        <div style="margin-bottom: 24px; padding: 14px 18px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; color: #64748b; font-size: 13px;">
            🛠️ <strong>2. Bugs e Incidencias Oficiales:</strong> Microsoft no ha emitido nuevos parches de Cumulative Updates esta semana.
        </div>
        """

    # 3. Bloque de Vídeos Encontrados (Abajo)
    if videos:
        filas_videos = ""
        for v in videos:
            filas_videos += f"""
            <tr style="border-bottom: 1px solid #e2e8f0;">
                <td style="padding: 12px 14px; font-size: 13px; color: #0f172a; font-weight: 600;">
                    <span style="display: inline-block; padding: 2px 8px; font-size: 11px; background: #fff1f2; color: #e11d48; border-radius: 4px; margin-right: 6px; border: 1px solid #fecdd3;">
                        {v.get('partner', 'YouTube')}
                    </span>
                    {v.get('title', '')}
                    <div style="font-size: 11px; color: #64748b; margin-top: 3px;">Asociado a: {v.get('feature_title', 'Novedad BC')}</div>
                </td>
                <td style="padding: 12px 14px; text-align: right; white-space: nowrap;">
                    <a href="{v.get('url', '#')}" target="_blank" style="display: inline-block; padding: 6px 12px; font-size: 12px; font-weight: 700; color: #ffffff; background: #e11d48; border-radius: 6px; text-decoration: none; box-shadow: 0 1px 3px rgba(225,29,72,0.2);">
                        ▶ Ver Vídeo &rarr;
                    </a>
                </td>
            </tr>
            """
        bloque_videos = f"""
        <div style="margin-bottom: 28px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
            <div style="background: #f8fafc; padding: 12px 18px; border-bottom: 1px solid #e2e8f0;">
                <h3 style="margin: 0; font-size: 15px; color: #0f172a; font-family: 'Segoe UI', Arial, sans-serif;">
                    🎥 3. Nuevos Vídeos y Recursos Multimedia Detectados ({len(videos)})
                </h3>
            </div>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                <tbody>
                    {filas_videos}
                </tbody>
            </table>
        </div>
        """
    else:
        bloque_videos = """
        <div style="margin-bottom: 24px; padding: 14px 18px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; color: #64748b; font-size: 13px;">
            🎥 <strong>3. Nuevos Vídeos:</strong> No se han detectado nuevas publicaciones en los canales homologados (Roberto Corella, Erik Hougaard, Triangle, etc.) esta semana.
        </div>
        """

    # Estado de resumen ejecutivo
    if hay_cambios:
        intro_resumen = f"""
        El escáner automático semanal de AUBA DCS ha detectado actualizaciones oficiales publicadas durante los últimos 7 días. El Cuaderno Técnico en HTML ha sido actualizado automáticamente.
        """
    else:
        intro_resumen = f"""
        El escáner automático semanal de AUBA DCS se ha completado con éxito. <strong>No se han detectado cambios esta semana</strong> en los Release Plans oficiales de Microsoft, ni parches nuevos de CUs, ni vídeos adicionales en los canales de referencia. Todo el sistema permanece 100% al día.
        """

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Informe Semanal de Novedades BC - AUBA Dynamics</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f4f6f9; font-family: 'Segoe UI', Arial, sans-serif; -webkit-font-smoothing: antialiased;">
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f4f6f9; padding: 24px 0;">
        <tr>
            <td align="center">
                <table border="0" cellpadding="0" cellspacing="0" width="680" style="background-color: #ffffff; border-radius: 14px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
                    
                    <!-- Cabecera Corporativa AUBA DCS -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #0f6cbd, #0b4a82); padding: 26px 32px; color: #ffffff;">
                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td>
                                        <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; color: #bfdbfe; margin-bottom: 4px;">
                                            AUBA DYNAMIC CONSULTING SOLUTIONS &bull; CONTROL DE VERSIONES
                                        </div>
                                        <h1 style="margin: 0; font-size: 20px; font-weight: 800; color: #ffffff; font-family: 'Segoe UI', sans-serif;">
                                            Informe Semanal de Novedades y Actualizaciones
                                        </h1>
                                        <div style="font-size: 13px; color: #e0f2fe; margin-top: 4px;">
                                            Microsoft Dynamics 365 Business Central &bull; Escaneo del {fecha_str}
                                        </div>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- Cuerpo Principal -->
                    <tr>
                        <td style="padding: 32px 32px 20px 32px; color: #334155;">
                            <p style="font-size: 14px; line-height: 1.6; margin-top: 0; margin-bottom: 24px; color: #475569;">
                                {intro_resumen}
                            </p>

                            <!-- SECCIÓN 1: NOVEDADES -->
                            {bloque_novedades}

                            <!-- SECCIÓN 2: BUGS CORREGIDOS -->
                            {bloque_bugs}

                            <!-- SECCIÓN 3: VÍDEOS ENCONTRADOS -->
                            {bloque_videos}

                            <!-- Botón de Acceso al Cuaderno Técnico -->
                            <div style="text-align: center; margin: 36px 0 20px 0;">
                                <a href="{url_cuaderno}" target="_blank" style="display: inline-block; padding: 13px 28px; font-size: 14px; font-weight: 700; color: #ffffff; background: #0f6cbd; border-radius: 8px; text-decoration: none; box-shadow: 0 3px 8px rgba(15,108,189,0.3);">
                                    Abrir Cuaderno Técnico de Versiones en Línea &rarr;
                                </a>
                            </div>
                        </td>
                    </tr>

                    <!-- Pie Corporativo -->
                    <tr>
                        <td style="background-color: #f8fafc; padding: 22px 32px; text-align: center; border-top: 1px solid #e2e8f0; color: #64748b; font-size: 12px; line-height: 1.5;">
                            <p style="margin: 0 0 4px 0; font-weight: 600; color: #334155;">
                                Auba Dynamic Consulting Solutions S.L. &bull; Partner Oficial Microsoft Dynamics 365
                            </p>
                            <p style="margin: 0; color: #94a3b8; font-size: 11px;">
                                Proceso automatizado semanal vía GitHub Actions. Datos 100% oficiales contrastados con Microsoft Learn.
                            </p>
                        </td>
                    </tr>

                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
    return html

if __name__ == "__main__":
    ejemplo_cambios = {
        "new_features": [
            {
                "version": "v29 Preview",
                "title": "Copilot Chat integrado en Business Central Web Client",
                "pillar": "IA y Copilot",
                "url": "https://learn.microsoft.com/es-es/dynamics365/release-plan/2026wave1/smb/dynamics365-business-central/copilot-chat"
            }
        ],
        "new_bugs": [
            {
                "kb": "5127206",
                "problem": "Error de redondeo de decimales en líneas de venta al aplicar retención de IRPF",
                "module": "Finanzas España"
            }
        ],
        "new_videos": [
            {
                "partner": "Roberto Corella",
                "title": "Novedades BC v29 - Primer vistazo a los agentes de IA",
                "feature_title": "Agentes autónomos de IA y Copilot",
                "url": "https://www.youtube.com/watch?v=ge9NJEuuxtA"
            }
        ]
    }
    
    html_output = generar_html_correo(ejemplo_cambios)
    with open("reporte_semanal_correo_preview.html", "w", encoding="utf-8") as f:
        f.write(html_output)
    print("Reporte de prueba generado en: reporte_semanal_correo_preview.html")
