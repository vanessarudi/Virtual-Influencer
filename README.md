# Porsche Virtual Influencer Ray

Ein Prototyp für einen digitalen Influencer namens Ray, der personalisierte Inhalte für Porsche Cardealershipper mithilfe von OpenAI generiert.

## 📋 Übersicht
Dieser Prototyp demonstriert die Fähigkeiten eines virtuellen Influencers, der automatisch personalisierte Social Media Inhalte für Porsche-Händler erstellt. Die Anwendung nutzt OpenAI's GPT-Modelle, um authentische und zielgruppenspezifische Inhalte zu generieren.

## 📂 Git-Repository
Der Prototyp ist auf GitHub verfügbar und kann von dort geklont werden:
- **Repository-URL**: https://github.com/vanessarudi/Virtual-Influencer
- **Zugriff**: Öffentliches Repository

## ✨ Funktionen
- **API-Verbindungstest**: Überprüfung der OpenAI API-Konnektivität
- **Personalisierte Textgenerierung** mit verschiedenen Parametern:
  - **Themen**: Fahrerlebnis, Nachhaltigkeit, Design, Technologie, Lifestyle, Rennsport
  - **Instagram-Formate**: Feed-Beitrag, Story, Reels
  - **Zielgruppen**: Porsche Enthusiasten, Technik-Interessierte, Umweltbewusste, Design-Liebhaber, Junge Zielgruppe
  - **Zusätzliche Anweisungen**: Für individuellere und spezifischere Inhalte
- **Web-basierte Benutzeroberfläche**: Einfache Bedienung über Browser
- **Detailliertes Logging**: Vollständige Protokollierung aller Aktivitäten

## 🛠️ Voraussetzungen
Bevor Sie beginnen, stellen Sie sicher, dass folgende Software installiert ist:
- **Python 3.8 oder höher** ([Download hier](https://www.python.org/downloads/))
- **Git** ([Download hier](https://git-scm.com/downloads))
- **Ein OpenAI API-Konto** ([Registrierung hier](https://platform.openai.com/signup))

## 🔑 OpenAI API-Schlüssel erhalten
1. **Anmelden**: Melden Sie sich bei [https://platform.openai.com](https://platform.openai.com) an

2. **API-Schlüssel erstellen**:
   - Gehen Sie auf [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys) 
   - Klicken Sie auf **"Create new secret key"** oder **"Neuen geheimen Schlüssel erstellen"**

3. **Schlüssel konfigurieren**:
   - Geben Sie einen **Namen** für Ihren Schlüssel ein (z.B. "Porsche Prototyp")
   - Wählen Sie die **Berechtigungen** aus (für diesen Prototyp reichen Standard-Berechtigungen)
   - Klicken Sie auf **"Create secret key"**

4. **Schlüssel kopieren**:
   - **WICHTIG**: Kopieren Sie den API-Schlüssel sofort! Er beginnt mit `sk-`
   - Der Schlüssel wird nur einmal angezeigt und kann später nicht mehr eingesehen werden
   - Format: `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Schritt 3: Ggf. Guthaben hinzufügen
1. **Billing-Sektion**: Gehen Sie zu **"Billing"** oder **"Abrechnung"** im Menü

2. **Payment Method**: Fügen Sie eine **Zahlungsmethode** hinzu (Kreditkarte oder PayPal)

3. **Guthaben**: 
   - OpenAI bietet oft **kostenloses Startguthaben** (z.B. $5)
   - Für Tests reicht das kostenlose Guthaben normalerweise aus
   - Sie können zusätzliches Guthaben hinzufügen

**Beispiel für die `.env` Datei**:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

## 📦 Installation
### Schritt 1: Repository klonen

```bash
# Klonen Sie das Repository
git clone https://github.com/vanessarudi/Virtual-Influencer.git
cd Virtual-Influencer
```

**Hinweis**: Ersetzen Sie `[Repository-URL]` mit der tatsächlichen URL Ihres Git-Repositories.

### Schritt 2: Virtuelle Umgebung erstellen
```bash
# Virtuelle Umgebung erstellen
python -m venv venv

# Virtuelle Umgebung aktivieren
# Für Windows:
venv\Scripts\activate

# Für macOS/Linux:
source venv/bin/activate
```

**Wichtiger Hinweis**: Nach der Aktivierung sollte `(venv)` am Anfang Ihrer Kommandozeile erscheinen.

### Schritt 3: Abhängigkeiten installieren

```bash
# Alle erforderlichen Pakete installieren
pip install -r requirements.txt
```

### Schritt 4: OpenAI API-Schlüssel konfigurieren
1. **Erstellen Sie eine `.env` Datei** im Hauptverzeichnis des Projekts:

```bash
# Für Windows (PowerShell):
New-Item -Path ".env" -ItemType File

# Für macOS/Linux:
touch .env
```

2. **Fügen Sie Ihren API-Schlüssel hinzu**:

Öffnen Sie die `.env` Datei in einem Texteditor und fügen Sie folgende Zeile hinzu:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Wichtige Hinweise**:
- Ersetzen Sie `sk-your-actual-api-key-here` mit Ihrem tatsächlichen OpenAI API-Schlüssel
- Die `.env` Datei wird automatisch von `.gitignore` ausgeschlossen und nicht ins Repository hochgeladen
- Bewahren Sie Ihren API-Schlüssel sicher auf und teilen Sie ihn nicht mit anderen

## 🚀 Verwendung
### Anwendung starten

1. **Stellen Sie sicher, dass die virtuelle Umgebung aktiviert ist**:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Starten Sie den Flask-Server**:
   ```bash
   python app.py
   ```

3. **Öffnen Sie einen Webbrowser** und navigieren Sie zu:
   ```
   http://localhost:8080
   ```

### Benutzeroberfläche verwenden
1. **API-Verbindung testen**: Klicken Sie auf "API-Verbindung testen" um sicherzustellen, dass Ihre OpenAI API korrekt konfiguriert ist

2. **Inhalte generieren**:
   - Wählen Sie ein **Thema** aus (z.B. Fahrerlebnis, Nachhaltigkeit)
   - Wählen Sie ein **Instagram-Format** (Feed-Beitrag, Story, Reels)
   - Wählen Sie eine **Zielgruppe**
   - Fügen Sie **zusätzliche Anweisungen** hinzu (optional)
   - Klicken Sie auf "Inhalt generieren"

3. **Ergebnisse**: Der generierte Text wird angezeigt und kann kopiert werden

## 📁 Projektstruktur

```
Prototyp/
├── app.py                 # Hauptanwendungsdatei mit Flask-App und Routen
├── content_generator.py   # Module zur Generierung von Inhalten mit OpenAI
├── requirements.txt       # Python-Abhängigkeiten (vereinfacht)
├── .env                  # API-Schlüssel (nicht im Repository)
├── README.md             # Diese Datei
├── .gitignore            # Git-Ignore-Datei
├── templates/            # HTML-Templates für die Benutzeroberfläche
│   ├── base.html         # Basis-Template mit Header und Navigation
│   ├── main_page.html    # Hauptseite (Landing Page + Generator kombiniert)
│   ├── 404.html          # Fehlerseite - Seite nicht gefunden
│   └── 500.html          # Fehlerseite - Serverfehler
├── static/               # Statische Dateien
│   ├── css/
│   │   └── style.css     # Hauptstylesheet
│   ├── js/
│   │   └── app.js        # JavaScript-Funktionen
│   └── public/           # Bilder und Schriftarten
│       ├── Antonio-Regular.ttf
│       ├── Antonio-SemiBold.ttf
│       ├── hintergrundbild.png
│       ├── porsche logo.png
│       └── Ray.png
├── logs/                 # Log-Dateien
│   ├── app.log           # Allgemeine Anwendungslogs
│   └── api.log           # API-spezifische Logs
└── venv/                 # Virtuelle Umgebung (wird bei Installation erstellt)
```

## 📊 Logging
Die Anwendung verwendet ein detailliertes Logging-System für Debugging und Monitoring:

- **Allgemeine Logs**: `logs/app.log` - Enthält allgemeine Anwendungsereignisse
- **API-spezifische Logs**: `logs/api.log` - Enthält detaillierte API-Aufrufe und Antworten

## ⚠️ Wichtige Hinweise
### Kosten und API-Nutzung
- **OpenAI berechnet Kosten pro Token**: Achten Sie auf Ihre API-Nutzung
- **Verwendetes Modell**: `gpt-3.5-turbo` (kostengünstiger als GPT-4)
- **Empfohlene Vorgehensweise**: Testen Sie zunächst mit wenigen Anfragen

### Technische Hinweise
- **Emoticons**: Generierte Texte können Emoticons enthalten, die in manchen Konsolen zu Anzeigefehlern führen können
- **Browser-Kompatibilität**: Die Anwendung funktioniert am besten mit modernen Browsern (Chrome, Firefox, Safari, Edge)
- **Port 8080**: Falls der Port bereits belegt ist, können Sie ihn in `app.py` ändern

### Sicherheit
- **API-Schlüssel**: Teilen Sie Ihren OpenAI API-Schlüssel niemals mit anderen
- **Umgebungsvariablen**: Die `.env` Datei wird automatisch von Git ignoriert
- **Lokale Ausführung**: Die Anwendung läuft nur lokal auf Ihrem Computer

