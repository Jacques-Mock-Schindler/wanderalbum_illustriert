# 📖 Wanderalbum – Dokumentation

Willkommen im Repository für das **Wanderalbum**. Dieses Projekt ist ein statischer Blog, der lokal mit **Quarto** generiert und via **Rclone** auf **Cloudflare R2** gehostet wird.

---

## ⚙️ Voraussetzungen & Setup

Damit du am Projekt arbeiten kannst, müssen folgende Tools installiert sein:

*   **[Quarto](https://quarto.org/docs/get-started/)**: Zum Generieren der Webseite.
*   **[Rclone](https://rclone.org/)**: Zum Hochladen der Dateien (muss im System-PATH sein).
*   **Python**: Für die virtuelle Umgebung (`.venv`).

### Initiale Einrichtung

1.  **Repository klonen** & in das Verzeichnis wechseln.
2.  **Python Environment aktivieren**:
    ```powershell
    # Windows (PowerShell)
    .\.venv\Scripts\Activate.ps1
    ```
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
```

### 2. Generieren (Build)
Erstellt die finalen statischen HTML-Dateien und Bilder im Output-Ordner (in der Regel `docs/` oder `_site/`).

```bash
quarto render
```

---

## 🚀 Veröffentlichen (Deployment)

Sobald der Build (`quarto render`) erfolgreich war, wird die Seite synchronisiert.

**Achtung:** Der `sync`-Befehl macht den Ziel-Bucket zu einem exakten Spiegelbild des lokalen Ordners. Dateien, die lokal nicht mehr existieren, werden auch auf dem Server gelöscht.

```powershell
rclone sync docs r2-bilder:wanderalbum-web --progress
```
*(Hinweis: Falls dein Output-Ordner `_site` heißt, ersetze `docs` im Befehl oben durch `_site`)*

> **Die Seite ist danach erreichbar unter:**
> `https://[DEINE-R2-SUBDOMAIN].r2.dev/index.html`

---

## 🗑️ Git Branch-Management

Wir halten das Repository sauber, indem wir Branches löschen, sobald ein Feature gemerged oder ein Experiment beendet ist.

### Cheatsheet (Schnellübersicht)

| Ziel | Befehl |
| :--- | :--- |
| **Lokal löschen (Sicher)** | `git branch -d feature/name` |
| **Lokal löschen (Force)** | `git branch -D feature/name` |
| **Auf GitHub löschen** | `git push origin --delete feature/name` |
| **Branch-Liste aufräumen** | `git fetch --prune` |

### Detail-Anleitung

<details>
<summary>Klicken für Details zum Löschen von Branches</summary>

#### 1. Lokalen Branch löschen
Wechsle zuerst auf den Main-Branch: `git checkout main`

*   **Sicher (Standard):** `git branch -d <branch-name>`
    *(Warnt dich, falls Änderungen noch nicht gemerged sind.)*
*   **Erzwungen:** `git branch -D <branch-name>`
    *(Löscht ohne Rücksicht auf Verluste.)*

#### 2. Remote Branch löschen (Server)
Entfernt den Branch für alle Teammitglieder auf GitHub/GitLab:
`git push origin --delete <branch-name>`

#### 3. Lokale Referenzen aufräumen
Entfernt "Geister-Branches" (origin/...), die auf dem Server schon gelöscht wurden:
`git fetch --prune`

</details>

---

## 🔧 Troubleshooting & Setup-Infos

### Rclone Setup (Cloudflare R2)
Falls du Rclone neu einrichten musst (`rclone config`), nutze folgende Einstellungen:
*   **Remote Name:** `r2-bilder`
*   **Storage Type:** S3 Compatible
*   **Provider:** Cloudflare
*   **Access Key / Secret Key:** (Aus dem Cloudflare Dashboard)
*   **Endpoint:** `https://<ACCOUNT_ID>.r2.cloudflarestorage.com`

### Probleme mit PowerShell?
Falls Skripte (wie `.venv` Aktivierung) geblockt werden, muss die Execution Policy angepasst werden:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```
```