from flask import jsonify, render_template
from app import app
import content_generator
import logging

# Logging-Konfiguration für API-Routen
logger = logging.getLogger('api_routes')

# Route für die Hauptseite
@app.route('/')
def index():
    """Hauptseite der Anwendung."""
    logger.info("Hauptseite (/) aufgerufen")
    return render_template('index.html')

# Route zum Testen der OpenAI API-Verbindung (vereinfacht für Meeting)
@app.route('/api/connection/test', methods=['GET'])
def test_connection():
    """API-Route zum Testen der OpenAI API-Verbindung."""
    try:
        logger.info("API-Verbindungstest gestartet")
        result = content_generator.test_openai_connection()
        if result["status"] == "success":
            logger.info(f"API-Verbindungstest erfolgreich: Antwortzeit: {result['response_time']}")
        else:
            logger.error(f"API-Verbindungstest fehlgeschlagen: {result['error']}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Fehler beim API-Verbindungstest: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__
        }), 500
