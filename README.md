# Wanderalbum

Hier ist eine auf dein Projekt zugeschnittene Zusammenfassung für dein README. Du kannst den folgenden Block direkt kopieren und in deine `README.md` einfügen.

-----

## 🚀 Publikations-Workflow

Dieser Blog wird lokal mit **Quarto** generiert und als statische Seite via **Rclone** auf **Cloudflare R2** gehostet.

### Voraussetzungen

  * **Quarto** muss installiert sein.
  * **Rclone** muss installiert und konfiguriert sein (Remote Name: `r2-bilder`).
  * Python Environment (`.venv`) sollte aktiviert sein, falls neue Notebooks ausgeführt werden müssen.

### 1\. Vorschau (Lokal testen)

Startet einen lokalen Webserver, um Änderungen live zu sehen.

```bash
quarto preview
```

### 2\. Generieren (Build)

Erstellt die statischen HTML-Dateien inklusive aller Bilder im Ordner `_site`.

```bash
quarto render
```

### 3\. Veröffentlichen (Deploy)

Synchronisiert den lokalen `_site` Ordner mit dem Cloudflare R2 Bucket.

  * **Achtung:** `sync` löscht Dateien im Bucket, die lokal nicht mehr existieren (exaktes Spiegelbild).

<!-- end list -->

```powershell
rclone sync _site r2-bilder:wanderalbum-web --progress
```

> **Hinweis:** Falls `rclone` nicht im PATH ist, nutze `.\rclone.exe` statt `rclone`.

### 4\. Webseite aufrufen

Die Seite ist unter der R2 Public URL erreichbar (ggf. `/index.html` anhängen):

  * `https://[DEINE-R2-SUBDOMAIN].r2.dev/index.html`
