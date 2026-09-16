# Cuaderno Técnico y Portal de Novedades - Microsoft Dynamics 365 Business Central
**AUBA Dynamic Consulting Solutions S.L.** &bull; *Partner Oficial Microsoft Dynamics 365*

Este repositorio centraliza el control de versiones, seguimiento de parches oficiales, biblioteca de recursos multimedia y publicaciones comerciales para clientes de **Microsoft Dynamics 365 Business Central**.

---

## 🌐 Acceso en Línea (GitHub Pages)
El Cuaderno Técnico interactivo está publicado y accesible en:
👉 **[https://aubadcs.github.io/Novedades-BC/](https://aubadcs.github.io/Novedades-BC/)**

---

## 📂 Estructura del Repositorio

```text
├── index.html                    # Cuaderno Técnico Multiversión (v27, v28, v29) - Portada GitHub Pages
├── icono_favicon.svg             # Icono oficial vectorizado de AUBA DCS (Favicon corporativo)
├── AubaDynamics_Logo_Principal.svg # Logotipo principal oficial de AUBA DCS
├── data/
│   └── novedades_bc.json         # Base de datos unificada de versiones, CUs, bugs y vídeos contrastados
├── scripts/
│   ├── scanner_novedades_bc.py   # Escáner semanal de Microsoft Learn, CUs y feeds de YouTube
│   ├── generador_correo_semanal.py # Generador de correo corporativo con estructura oficial
│   └── enviar_correo_semanal.py  # Despachador de correo por SMTP / GitHub Actions
├── .github/workflows/
│   └── scanner_semanal.yml       # Tarea automática programada semanalmente (Lunes 07:00 UTC)
└── Version Comercial/            # Portales y correos oficiales para clientes (Web de Auba)
    ├── v28/                      # Versión comercial enviada a clientes de la v28
    │   ├── index.html            # Publicado en https://aubadcs.com/NovedadesBC/V28/
    │   ├── correo.html
    │   ├── formacion.html
    │   └── assets (banners y logos)
    └── v29/                      # Reservado para la futura versión comercial v29
```

---

## ⚙️ Proceso de Escaneo Automático Semanal

1. **Rastreo Profundo de Microsoft**:
   - Inspección de los Release Plans oficiales en Microsoft Learn para v27, v28 y v29.
   - Detección de parches emitidos en Cumulative Updates (KBs oficiales resueltos).
2. **Rastreo Multimedia Homologado**:
   - Seguimiento de canales autorizados (Roberto Corella, Erik Hougaard, Saurav Dhyani, etc.).
   - Vinculación automática de vídeos técnicos a sus fichas correspondientes.
3. **Notificación por Correo**:
   - Envío semanal con el resumen clasificado:
     1. *Novedades oficiales detectadas*.
     2. *Bugs e incidencias resueltas por Microsoft*.
     3. *Vídeos y recursos multimedia publicados*.
   - Si no hay cambios, confirmación de estado al día.

---
© 2026 AUBA Dynamic Consulting Solutions S.L. Todos los derechos reservados.
