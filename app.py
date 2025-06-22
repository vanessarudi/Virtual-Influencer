import os
import logging
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import content_generator

# Logging-Konfiguration
def setup_logging():
    """Richtet das Logging für die Anwendung ein."""
    # Stelle sicher, dass das logs-Verzeichnis existiert
    os.makedirs('logs', exist_ok=True)
    
    # Erstelle einheitlichen Formatter für alle Log-Einträge
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Haupt-Logdatei für allgemeine Anwendungsereignisse
    file_handler = logging.FileHandler('logs/app.log')
    file_handler.setFormatter(formatter)
    
    # API-spezifische Logdatei für detaillierte API-Logs
    api_file_handler = logging.FileHandler('logs/api.log')
    api_file_handler.setFormatter(formatter)
    
    # Console-Handler für Entwicklung und Debugging
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Haupt-Logger konfigurieren (für allgemeine Anwendungsereignisse)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # API-spezifische Logger konfigurieren (für OpenAI API-Aufrufe)
    api_logger = logging.getLogger('openai_api')
    api_logger.setLevel(logging.INFO)
    api_logger.addHandler(api_file_handler)
    
    # Routes-Logger konfigurieren (für API-Routen)
    routes_logger = logging.getLogger('api_routes')
    routes_logger.setLevel(logging.INFO)
    routes_logger.addHandler(api_file_handler)
    
    # Start-Nachrichten loggen für bessere Nachverfolgung
    logging.info("=== Porsche Social Content Generator gestartet ===")
    logging.info(f"Umgebung: {'development' if os.getenv('FLASK_ENV') == 'development' else 'production'}")
    logging.info(f"Debug-Modus: {'aktiviert' if os.getenv('FLASK_DEBUG') == '1' else 'deaktiviert'}")
    logging.info(f"OpenAI API Schlüssel: {'konfiguriert' if os.getenv('OPENAI_API_KEY') else 'FEHLT'}")

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()

# Richte das Logging-System ein
setup_logging()

# Erstelle Flask-Anwendung
app = Flask(__name__)

# Aktiviere CORS für Cross-Origin Requests (wichtig für API-Zugriffe)
CORS(app)


# Generiere einen zufälligen Secret Key für Session-Management
app.config['SECRET_KEY'] = os.urandom(24)

# Lade OpenAI API-Schlüssel aus Umgebungsvariablen
app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# Prüfe ob der API-Schlüssel konfiguriert ist
if not app.config['OPENAI_API_KEY']:
    logging.error("OPENAI_API_KEY nicht in .env-Datei gefunden oder leer!")
else:
    logging.info("OpenAI API-Schlüssel erfolgreich geladen")

# FLASK-ROUTEN (WEB-ENDPUNKTE)
# HAUPTSEITE

@app.route('/')
def index():
    """Hauptseite der Anwendung mit Landing Page und Generator."""
    logging.info("Hauptseite (/) mit Landing Page und Generator aufgerufen")
    return render_template('main_page.html')

# API-ENDPUNKTE
# API-VERBINDUNGSTEST
@app.route('/api/connection/test', methods=['GET'])
def test_connection():
    """API-Route zum Testen der OpenAI API-Verbindung."""
    try:
        logging.info("API-Verbindungstest gestartet (Meeting 1 Version)")
        
        # Rufe die Testfunktion aus content_generator auf
        result = content_generator.test_openai_connection()
        
        # Logge das Ergebnis
        if result["status"] == "success":
            logging.info(f"API-Verbindungstest erfolgreich: Antwortzeit: {result['response_time']}")
        else:
            logger.error(f"API-Verbindungstest fehlgeschlagen: {result['error']}")
        return jsonify(result)
    except Exception as e:
        logging.error(f"Fehler beim API-Verbindungstest: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__
        }), 500

# PERSONALISIERTE TEXTGENERIERUNG
@app.route('/api/generate/personalized', methods=['POST'])
def generate_personalized():
    """Generiert einen personalisierten Text basierend auf den angegebenen Parametern."""
    try:
        logging.info("Personalisierte Generierung gestartet")
        
        # Extrahiere JSON-Parameter aus dem HTTP-Request
        params = request.json
        if not params:
            return jsonify({
                "status": "error",
                "error": "Keine Parameter erhalten"
            }), 400
            
        # Validiere Pflichtfelder
        required_fields = ['topic', 'content_type', 'target_audience']
        for field in required_fields:
            if field not in params or not params[field]:
                return jsonify({
                    "status": "error",
                    "error": f"Feld '{field}' fehlt oder ist leer"
                }), 400
        
        # Rufe die Generierungsfunktion aus content_generator auf
        content = content_generator.generate_personalized_text(params)
        logging.info("Personalisierte Generierung erfolgreich.")
        
        # Gib den generierten Content zurück
        return jsonify({"status": "success", "content": content})
    except Exception as e:
        logging.error(f"Fehler bei der personalisierten Generierung: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "error": "Fehler bei der personalisierten Generierung",
            "details": str(e)
        }), 500

# FEHLERBEHANDLUNG
# 404 FEHLER (SEITE NICHT GEFUNDEN)
@app.errorhandler(404)
def page_not_found(e):
    """Fehlerseite 404."""
    logging.warning(f"404 Fehler: Pfad nicht gefunden")
    return render_template('404.html'), 404

# 500 FEHLER (SERVER-FEHLER)
@app.errorhandler(500)
def server_error(e):
    """Fehlerseite 500."""
    logging.error(f"500 Fehler: {str(e)}")
    return render_template('500.html'), 500

# SERVER-START
if __name__ == '__main__':
    logging.info("Server wird gestartet...")
    
    # Aktiviere automatisches Neuladen von Templates für Entwicklung
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
    # Starte den Flask-Server
    app.run(debug=True, host='0.0.0.0', port=8080)