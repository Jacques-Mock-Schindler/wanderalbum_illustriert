# 📖 Wanderalbum – Dokumentation

Willkommen im Repository für das **Wanderalbum**. Dieses Projekt ist ein statischer Blog, der lokal mit **Quarto** generiert und via **Rclone** auf **Cloudflare R2** gehostet wird.

---

## ⚙️ Voraussetzungen & Setup

Damit du am Projekt arbeiten kannst, müssen folgende Tools installiert sein:

* **[Quarto](https://quarto.org/docs/get-started/)**: Zum Generieren der Webseite.
* **[Rclone](https://rclone.org/)**: Zum Hochladen der Dateien (muss im System-PATH sein).
* **Python**: Für die virtuelle Umgebung (`.venv`).

### Initiale Einrichtung

1.  **Repository klonen** & in das Verzeichnis wechseln.
2.  **Python Environment aktivieren**:
    ```powershell
    # Windows (PowerShell)
    .\.venv\Scripts\Activate.ps1
    ```
    *(Linux/Mac: `source .venv/bin/activate`)*
3.  **Rclone Konfiguration prüfen**:
    Stelle sicher, dass ein Remote namens `r2-bilder` konfiguriert ist.
    *(Details siehe Abschnitt [Troubleshooting](#-troubleshooting--setup-infos))*

---

## 📝 Täglicher Workflow

So bearbeitest du den Blog und testest Änderungen lokal.

### 1. Vorschau (Live-Server)
Startet einen lokalen Webserver. Änderungen werden beim Speichern automatisch neu geladen.

```bash
quarto preview