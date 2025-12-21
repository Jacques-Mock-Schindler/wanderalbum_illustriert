# 📖 Wanderalbum – Projektdokumentation

Dies ist das Repository für das **Wanderalbum**. Es handelt sich um einen statischen Blog, der lokal mit **Quarto** generiert und via **Rclone** auf **Cloudflare R2** gehostet wird.


## 🛠️ Voraussetzungen

Folgende Software muss auf deinem Rechner installiert sein:

1.  **[Quarto](https://quarto.org/docs/get-started/)**: Die Engine zum Rendern der Webseite.
2.  **[Rclone](https://rclone.org/)**: Zum Synchronisieren mit der Cloud (muss im System-PATH verfügbar sein).
3.  **Python**: Für die virtuelle Umgebung (wird für Skripte oder Erweiterungen benötigt).



## 🚀 Setup & Installation

### 1. Repository klonen
```bash
git clone <DEIN-REPO-URL>
cd wanderalbum

```

### 2. Python Environment aktivieren

Damit alle Abhängigkeiten korrekt geladen werden:

* **Linux / macOS:**
```bash
source .venv/bin/activate

```


* **Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1

```



### 3. Rclone Konfiguration prüfen

Stelle sicher, dass der Remote `r2-bilder` korrekt eingerichtet ist:

```bash
rclone listremotes
# Sollte "r2-bilder:" ausgeben

```


## 🔄 Multi-Machine Workflow (WICHTIG)

Wenn du an verschiedenen Rechnern arbeitest (z.B. Desktop & Laptop), ist die **Reihenfolge** entscheidend, um Datenverlust zu vermeiden.

### ⬇️ Schritt 1: Arbeitsbeginn (Download)

Bevor du schreibst, hole dir den aktuellen Stand aus der Cloud. Wir nutzen hier `copy`, damit lokal **nichts gelöscht** wird, falls Ordner fehlen.

```bash
# Lädt fehlende Dateien aus der Cloud in deinen lokalen Ordner
rclone copy r2-bilder:wanderalbum-web docs --progress

```

### 📝 Schritt 2: Bearbeiten & Vorschau

Starte den lokalen Server, um deine Änderungen live zu sehen:

```bash
quarto preview

```

*(Die Vorschau aktualisiert sich automatisch beim Speichern von Dateien.)*

### 🔨 Schritt 3: Finales Bauen (Build)

Wenn du fertig bist, generiere die statischen HTML-Dateien:

```bash
quarto render

```

### ⬆️ Schritt 4: Veröffentlichen (Upload)

Lade die neue Version hoch. Hier nutzen wir `sync`, um die Cloud auf den exakten Stand deines Rechners zu bringen (löscht alte Dateien in der Cloud, die du lokal entfernt hast).

```bash
rclone sync docs r2-bilder:wanderalbum-web --progress

```


## ⚠️ Rclone: Sync vs. Copy

Verstehe den Unterschied, um versehentliches Löschen zu vermeiden:

| Befehl | Verhalten | Wann nutzen? |
| --- | --- | --- |
| **`rclone sync`** | **Spiegeln.** Macht das Ziel exakt gleich wie die Quelle. <br>

<br>❗ **Löscht** Dateien am Ziel, wenn sie an der Quelle fehlen. | Nur beim **Upload** (Deployment), um aufzuräumen. |
| **`rclone copy`** | **Kopieren.** Kopiert nur neue/geänderte Dateien. <br>

<br>✅ **Löscht nichts** am Ziel. Bestehende Dateien bleiben erhalten. | Beim **Download** oder Backup. |


## 🧹 Git Branch-Management

Wir halten das Repository sauber, indem wir Branches löschen, sobald ein Feature gemerged ist.

| Ziel | Befehl |
| --- | --- |
| **Lokal löschen (Sicher)** | `git branch -d feature/name` |
| **Lokal löschen (Force)** | `git branch -D feature/name` |
| **Auf GitHub löschen** | `git push origin --delete feature/name` |
| **Aufräumen (Prune)** | `git fetch --prune` |


## 🔧 Troubleshooting & R2 Konfiguration

Falls du Rclone neu einrichten musst (`rclone config`), beachte die Besonderheiten von Cloudflare R2.

**Muster für `~/.config/rclone/rclone.conf`:**

```ini
[r2-bilder]
type = s3
provider = Cloudflare
access_key_id = <DEINE_ACCESS_KEY_ID>
secret_access_key = <DEIN_SECRET_ACCESS_KEY>
region = auto
endpoint = https://<ACCOUNT_ID>.r2.cloudflarestorage.com
acl = private

```

### Häufige Fehlerquellen:

1. **Fehler `SignatureDoesNotMatch`:**
* Prüfe, ob `region = auto` gesetzt ist.
* Stelle sicher, dass Access Key und Secret Key **unterschiedlich** sind (nicht zweimal denselben kopieren!).


2. **Fehler `NoCredentialProviders`:**
* Die Config-Datei ist fehlerhaft oder Keys fehlen. Bearbeite die Datei direkt.


3. **Falscher Endpoint:**
* Der Endpoint darf **keinen** Bucket-Namen enthalten (z.B. `/wanderalbum-web` am Ende ist falsch).



