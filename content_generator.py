import os
import openai
import logging
import time
import httpx

# Die Logging-Konfiguration wird jetzt bereits in app.py durchgeführt
# Hier nur noch den Logger holen
logger = logging.getLogger('openai_api')

# OpenAI-Konfiguration
# Explicitly create an httpx client that doesn't trust environment proxies
http_client = httpx.Client(trust_env=False)

# Stelle sicher, dass der API-Schlüssel geladen wird
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    logger.error("OpenAI API Key nicht in Umgebungsvariablen gefunden!")
    # Du könntest hier einen Fehler auslösen oder mit einem Dummy-Client fortfahren
    client = None # Oder eine Dummy-Implementierung
else:
    client = openai.OpenAI(
        api_key=api_key,
        http_client=http_client
    )
    logger.info("OpenAI Client erfolgreich initialisiert.")

# Behalte die Testfunktion
def test_openai_connection():
    """
    Testet die Verbindung zur OpenAI API mit einem einfachen API-Aufruf.
        
    Returns:
        dict: Ein Dictionary mit dem Status der Verbindung und der Antwortzeit.
    """
    if not client:
        logger.error("OpenAI Client nicht initialisiert, Test übersprungen.")
        return {"status": "error", "error": "OpenAI Client not initialized (API Key missing?)"}
        
    logger.info("Starte OpenAI API Verbindungstest...")
    start_time = time.time()
    
    try:
        # Einfacher API-Aufruf zum Testen, z.B. Auflisten der Modelle
        # client.models.list() 
        # Oder ein sehr günstiger Completion-Aufruf:
        client.chat.completions.create(
            model="gpt-3.5-turbo", # Ein günstigeres Modell für den Test
            messages=[{"role": "user", "content": "Test"}],
            max_tokens=1
        )
        
        end_time = time.time()
        response_time = f"{(end_time - start_time) * 1000:.0f} ms"
        logger.info(f"OpenAI API Verbindungstest erfolgreich. Antwortzeit: {response_time}")
        return {"status": "success", "response_time": response_time}
    except openai.AuthenticationError as e:
        logger.error(f"OpenAI API Authentifizierungsfehler: {str(e)}")
        return {"status": "error", "error": "Authentication Error (Invalid API Key?)", "details": str(e)}
    except openai.APIConnectionError as e:
        logger.error(f"OpenAI API Verbindungsfehler: {str(e)}")
        return {"status": "error", "error": "Connection Error", "details": str(e)}
    except openai.RateLimitError as e:
        logger.error(f"OpenAI API Rate Limit erreicht: {str(e)}")
        return {"status": "error", "error": "Rate Limit Exceeded", "details": str(e)}
    except openai.APIError as e:
        logger.error(f"Allgemeiner OpenAI API Fehler: {str(e)}")
        return {"status": "error", "error": "API Error", "details": str(e)}
    except Exception as e:
        logger.error(f"Unerwarteter Fehler beim OpenAI API Test: {str(e)}", exc_info=True)
        return {"status": "error", "error": "Unexpected Error", "details": str(e)}

# Neue, vereinfachte Generierungsfunktion für Meeting 1
def generate_simple_text(prompt):
    """
    Generiert einen kurzen Text mit OpenAI basierend auf einem einfachen Prompt.
    Verwendet ein günstigeres Modell und minimale Parameter.
    """
    if not client:
        logger.error("OpenAI Client nicht initialisiert, Generierung nicht möglich.")
        raise ValueError("OpenAI Client not initialized (API Key missing?)")
        
    logger.info(f"Starte einfache Textgenerierung mit Prompt: '{prompt}'")
    start_time = time.time()
    
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo", # Günstigeres Modell
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150 # Erhöht, um längere Antworten zu ermöglichen
        )
        elapsed_time = time.time() - start_time
        content = completion.choices[0].message.content.strip()
        logger.info(f"Einfache Generierung erfolgreich ({elapsed_time:.2f}s): '{content}'")
        return content
    except Exception as e:
        logger.error(f"Fehler bei einfacher Textgenerierung: {str(e)}", exc_info=True)
        # Werfe den Fehler weiter, damit die API-Route ihn fangen kann
        raise 