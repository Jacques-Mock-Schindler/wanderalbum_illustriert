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
rclone sync _site r2-bilder:wanderalbum-web --progress
```

> **Hinweis:** Falls `rclone` nicht im PATH ist, nutze `.\rclone.exe` statt `rclone`.

### 4\. Webseite aufrufen

Die Seite ist unter der R2 Public URL erreichbar (ggf. `/index.html` anhängen):

  * `https://[DEINE-R2-SUBDOMAIN].r2.dev/index.html`
