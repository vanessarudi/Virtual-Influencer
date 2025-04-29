import os
import logging
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import content_generator

# Logging-Konfiguration
def setup_logging():
    """Richtet das Logging für die Anwendung ein."""
    # Stelle sicher, dass das logs-Verzeichnis existiert
    os.makedirs('logs', exist_ok=True)
    
    # Erstelle Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Haupt-Logdatei
    file_handler = logging.FileHandler('logs/app.log')
    file_handler.setFormatter(formatter)
    
    # API-Logdatei für detaillierte API-Logs
    api_file_handler = logging.FileHandler('logs/api.log')
    api_file_handler.setFormatter(formatter)
    
    # Console-Handler für Entwicklung
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Haupt-Logger konfigurieren
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # API-spezifische Logger konfigurieren
    api_logger = logging.getLogger('openai_api')
    api_logger.setLevel(logging.INFO)
    api_logger.addHandler(api_file_handler)
    
    routes_logger = logging.getLogger('api_routes')
    routes_logger.setLevel(logging.INFO)
    routes_logger.addHandler(api_file_handler)
    
    # Start-Nachricht loggen
    logging.info("=== Porsche Social Content Generator gestartet ===")
    logging.info(f"Umgebung: {'development' if os.getenv('FLASK_ENV') == 'development' else 'production'}")
    logging.info(f"Debug-Modus: {'aktiviert' if os.getenv('FLASK_DEBUG') == '1' else 'deaktiviert'}")
    logging.info(f"OpenAI API Schlüssel: {'konfiguriert' if os.getenv('OPENAI_API_KEY') else 'FEHLT'}")

# Umgebungsvariablen laden
load_dotenv()

# Logging einrichten
setup_logging()

app = Flask(__name__)
CORS(app)

# Konfiguration
app.config['SECRET_KEY'] = os.urandom(24)
app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# Prüfe API-Schlüssel
if not app.config['OPENAI_API_KEY']:
    logging.error("OPENAI_API_KEY nicht in .env-Datei gefunden oder leer!")
else:
    logging.info("OpenAI API-Schlüssel erfolgreich geladen")

# Füge die Routen direkt hier hinzu für Meeting
@app.route('/')
def index():
    """Hauptseite der Anwendung."""
    logging.info("Hauptseite (/) aufgerufen")
    return render_template('index.html')

@app.route('/api/connection/test', methods=['GET'])
def test_connection():
    """API-Route zum Testen der OpenAI API-Verbindung."""
    try:
        logging.info("API-Verbindungstest gestartet (Meeting 1 Version)")
        result = content_generator.test_openai_connection()
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

# Neue Route für einfache Beispielgenerierung
@app.route('/api/generate/example', methods=['GET'])
def generate_example():
    """Generiert einen einfachen Beispieltext mit OpenAI."""
    try:
        logging.info("Beispiel-Generierung gestartet")
        # Detaillierte Persona für Ray als festen Prompt
        fixed_prompt = """
Du bist Ray – ein virtueller männlicher Influencer mit einem klaren Fokus auf Luxus-Automotive, Performance und digitale Lifestyle-Themen.  
Ray verkörpert den Porsche-Spirit: stilvoll, ambitioniert, zukunftsorientiert. Seine Sprache ist selbstbewusst, inspirierend und leicht emotional – aber nie übertrieben oder floskelhaft.

Sprich nicht wie eine Werbung. Nutze klare und moderne Sprache. Kommuniziere wie ein authentischer Creator, nicht wie ein Marketingtext.
"""
        # Rufe die (vereinfachte) Generierungsfunktion auf
        content = content_generator.generate_simple_text(fixed_prompt)
        logging.info("Beispiel-Generierung erfolgreich.")
        return jsonify({"status": "success", "content": content})
    except Exception as e:
        logging.error(f"Fehler bei der Beispiel-Generierung: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "error": "Fehler bei der Beispiel-Generierung",
            "details": str(e)
        }), 500

@app.errorhandler(404)
def page_not_found(e):
    """Fehlerseite 404."""
    logging.warning(f"404 Fehler: Pfad nicht gefunden")
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Fehlerseite 500."""
    logging.error(f"500 Fehler: {str(e)}")
    return render_template('500.html'), 500

if __name__ == '__main__':
    logging.info("Server wird gestartet...")
    # Force template reloading
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    # Run on port 5001 to avoid conflicts
    app.run(debug=True, host='0.0.0.0', port=5001)