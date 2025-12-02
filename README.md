# Wanderalbum

Hier ist eine auf dein Projekt zugeschnittene Zusammenfassung für dein README. Du kannst den folgenden Block direkt kopieren und in deine `README.md` einfügen.

-----


## 🗑️ Branch-Management & Aufräumen

Diese Anleitung beschreibt, wie wir Branches in diesem Projekt sauber löschen, wenn ein Feature abgeschlossen oder ein Experiment beendet ist.

### 1. Lokalen Branch löschen
*Entfernt den Branch nur auf deinem eigenen Rechner.*

Zuerst musst du sicherstellen, dass du dich **nicht** in dem Branch befindest, den du löschen möchtest:
```bash
git checkout main
````

**Option A: Das sichere Löschen (Standard)**
Verwende dies, wenn der Branch bereits gemerged wurde. Git warnt dich, falls Daten verloren gehen könnten.

```bash
git branch -d <branch-name>
```

**Option B: Das erzwungene Löschen**
Verwende dies nur, wenn du den Branch (und alle ungespeicherten Änderungen darin) wirklich verwerfen willst.

```bash
git branch -D <branch-name>
```

-----

### 2\. Remote Branch löschen (GitHub/Server)

*Entfernt den Branch für alle Teammitglieder auf dem Server.*

Wenn der Branch auf GitHub nicht mehr benötigt wird (z. B. nach einem Merge):

```bash
git push origin --delete <branch-name>
```

-----

### 3\. Git aufräumen (Synchronisation)

*Entfernt veraltete Referenzen in deinem lokalen Git.*

Wenn ein Kollege einen Branch auf dem Server gelöscht hat, wird er dir lokal oft noch als `origin/<branch-name>` angezeigt. Um deine Branch-Liste mit dem Server zu synchronisieren und diese "Geister-Branches" zu entfernen:

```bash
git fetch --prune
```

*(Alternativ funktioniert auch das manuelle Löschen der Referenz: `git branch -d -r origin/<branch-name>`)*

-----

### ⚡ Schnelle Übersicht (Cheatsheet)

| Ziel | Befehl |
| :--- | :--- |
| **Lokal löschen (Sicher)** | `git branch -d feature/xyz` |
| **Lokal löschen (Force)** | `git branch -D feature/xyz` |
| **Auf GitHub löschen** | `git push origin --delete feature/xyz` |
| **Branch-Liste aufräumen** | `git fetch --prune` |

```

***

### Ein paar Tipps zum Einfügen:

* **Platzhalter:** Ich habe `<branch-name>` als Platzhalter verwendet. Das ist Standard in Dokumentationen.
* **Stil:** Die Emojis (🗑️, ⚡) helfen, den Abschnitt im README optisch schnell zu finden, können aber weggelassen werden, wenn ihr einen sehr strikten Stil habt.

**Möchtest du noch einen Abschnitt hinzufügen, wie man Branches korrekt benennt (Naming Conventions, z.B. `feature/`, `bugfix/`)?**
```

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
rclone sync docs r2-bilder:wanderalbum-web --progress
```

> **Hinweis:** Falls `rclone` nicht im PATH ist, nutze `.\rclone.exe` statt `rclone`.

### 4\. Webseite aufrufen

Die Seite ist unter der R2 Public URL erreichbar (ggf. `/index.html` anhängen):

  * `https://[DEINE-R2-SUBDOMAIN].r2.dev/index.html`


Quarto Blog Deployment Guide (Cloudflare Pages & R2)Diese Anleitung beschreibt die Schritte, um das lokale Quarto-Projekt auf Cloudflare zu veröffentlichen. Das Setup nutzt Cloudflare Pages für die statische Webseite (HTML, CSS, JS) und Cloudflare R2 als Speicher für größere Assets (den files/ Ordner), um das Git-Repository schlank zu halten und Bandbreite effizient zu nutzen.1. Problembehebung: wrangler InstallationDie Fehlermeldung The term 'wrangler' is not recognized bedeutet, dass Windows den Befehl nicht findet. Dies liegt meist daran, dass Node.js nicht installiert ist oder der npm-Pfad nicht in den Umgebungsvariablen steht.Schritt 1.1: Node.js & NPM prüfenWrangler ist ein Node.js-Tool.Öffne die Eingabeaufforderung (PowerShell oder CMD).Tippe: node -v.Falls Fehler: Installiere Node.js (LTS Version).Falls Version angezeigt wird: Fahre fort.Schritt 1.2: Wrangler global installierenAuch wenn du es installiert hast, muss es global verfügbar sein. Führe in der PowerShell (als Administrator) folgenden Befehl aus:npm install -g wrangler
Schritt 1.3: Pfad aktualisieren & Execution PolicyNach der Installation:Wichtig: Schließe das PowerShell-Fenster und öffne ein neues.Teste erneut: wrangler --version.Falls es immer noch fehlschlägt, ist die PowerShell-Ausführungsrichtlinie evtl. zu strikt. Erlaube Skripte:Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
2. Cloudflare R2 Setup (Für den files Ordner)Wir lagern den Ordner files/ (Bilder, PDFs, Daten) in einen R2 Bucket aus.Schritt 2.1: LoginMelde dich über die CLI bei Cloudflare an (Browser-Fenster öffnet sich):wrangler login
Schritt 2.2: Bucket erstellenErstelle einen Bucket (z.B. mit dem Namen mein-quarto-assets):wrangler r2 bucket create mein-quarto-assets
Schritt 2.3: Dateien hochladenLade den Inhalt deines lokalen files/ Ordners in den R2 Bucket hoch.Hinweis: Dies kopiert den lokalen Ordner files in den R2 Bucket.# Syntax: wrangler r2 object put <bucket-name>/<datei-pfad> --file <lokale-datei>
# Für ganze Ordner ist rclone oft besser, aber für den Anfang manuell oder via Script:
Empfehlung (einfacher Weg):Nutze das Cloudflare Dashboard im Browser, gehe zu R2 > mein-quarto-assets und lade die Ordnerstruktur dort per Drag & Drop hoch, oder nutze ein Tool wie rclone.Schritt 2.4: Öffentlichen Zugriff aktivierenDamit dein Blog die Bilder anzeigen kann:Gehe im Cloudflare Dashboard zu deinem R2 Bucket.Klicke auf Settings > Public Access.Aktiviere R2.dev subdomain (oder verbinde eine eigene Domain).Kopiere die URL (z.B. https://pub-12345.r2.dev).Schritt 2.5: Quarto anpassenIn deinen .qmd Dateien, verlinke Bilder nun nicht mehr lokal (/files/bild.jpg), sondern über die R2-URL, oder konfiguriere eine base-url wenn du technisch versiert bist.Alternativ: Wenn du R2 nur als Backup nutzt und files trotzdem deployen willst, überspringe Schritt 2.5.3. Projekt Rendering (Lokal)Bevor wir die Seite hochladen, muss Quarto sie rendern. Da du eine .venv (Python Virtual Environment) hast, stelle sicher, dass sie aktiv ist.# 1. Venv aktivieren
.\.venv\Scripts\Activate.ps1

# 2. Projekt rendern (Output landet standardmäßig in 'docs/' oder '_site')
quarto render
Prüfe in deiner _quarto.yml, wohin der Output geht. Standard ist oft _site. Wenn du output-dir: docs gesetzt hast, ist es docs.4. Deployment auf Cloudflare PagesWir laden nun den gerenderten HTML-Ordner (docs oder _site) hoch.Schritt 4.1: Projekt erstellen & HochladenFühre diesen Befehl im Hauptverzeichnis deines Projekts aus (ersetze docs durch deinen Output-Ordnernamen):wrangler pages deploy docs --project-name mein-quarto-blog
Wrangler fragt beim ersten Mal: "No project with this name found. Create it?". Antworte mit Y.Wähle als Branch main (oder drücke Enter).Wrangler lädt die Dateien hoch und gibt dir eine URL (z.B. https://mein-quarto-blog.pages.dev).5. Workflow für UpdatesWenn du einen neuen Blogpost schreibst:Inhalt ändern: Schreibe deinen Text, speichere Bilder in files/ (und lade sie ggf. zu R2 hoch, falls du das strikt trennst).Rendern:quarto render
Deployen:wrangler pages deploy docs
Zusammenfassung der Befehle# Einmaliges Setup
npm install -g wrangler
wrangler login

# Regelmäßiger Workflow
.\.venv\Scripts\Activate.ps1
quarto render
wrangler pages deploy docs
