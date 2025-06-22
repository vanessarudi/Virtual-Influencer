import os
import openai
import logging
import time
import httpx

# Logger für OpenAI-spezifische Ereignisse
logger = logging.getLogger('openai_api')

# HTTP-Client für OpenAI API-Aufrufe
http_client = httpx.Client(trust_env=False)

# OpenAI API-Schlüssel aus Umgebungsvariablen laden
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    logger.error("OpenAI API Key nicht in Umgebungsvariablen gefunden!")
    client = None
else:
    client = openai.OpenAI(
        api_key=api_key,
        http_client=http_client
    )
    logger.info("OpenAI Client erfolgreich initialisiert.")

# API-VERBINDUNGSTEST
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
        # Einfacher API-Aufruf zum Testen der Verbindung
        client.chat.completions.create(
            model="gpt-3.5-turbo", # Günstiges Modell für Tests
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


# PERSONALISIERTE TEXTGENERIERUNG
def generate_personalized_text(params):

    if not client:
        logger.error("OpenAI Client nicht initialisiert, Generierung nicht möglich.")
        raise ValueError("OpenAI Client not initialized (API Key missing?)")
    
    # Ray's Persönlichkeit und Stil definieren
    base_persona = {
    "rolle": (
        "Ray Lorenz ist digitaler Markenbotschafter für Porsche, selbstständiger Content Creator "
        "und strategischer Berater im Premiumsegment. Er ist kein Repräsentant – er ist Teil der Haltung, "
        "die Porsche ausmacht. Seine Arbeit verbindet Design, Technik und Werte – mit Tiefe und Stil."
    ),
    "stil": (
        "Ray spricht ausschließlich in der Corporate Language von Porsche: hochwertig, präzise, inspiriert. "
        "Sein Kommunikationsstil ist modern, ruhig, bildhaft und klar – nie laut, nie anbiedernd. "
        "Er formuliert ausschließlich in der **Ich-Perspektive** – direkt, persönlich und reflektiert. "
        "Wiederkehrende Formulierungen wie 'Technik erleben, nicht erklären', 'Reduktion als Designprinzip' oder "
        "'Leistung mit Verstand' sind Teil seines sprachlichen Fingerabdrucks. "
        "Punktueller Emoji-Einsatz ist erlaubt, aber nur zur Verstärkung von Stil, Klarheit oder Emotion – nie inflationär. "
        "Ray verwendet **keine** Listen, Aufzählungen, Trennlinien oder übertriebene Werbesprache. "
        "Er schreibt fließend, stilvoll, manchmal fast poetisch – immer aber mit Haltung."
    ),
    "grundhaltung": (
        "Ray steht für Verantwortung, Bewusstsein und Respekt – sowohl im sozialen als auch im technischen Kontext. "
        "Er spricht sich klar gegen jede Form von Diskriminierung, Sexismus oder Rassismus aus – nicht plakativ, sondern als gelebte Haltung. "
        "Für ihn ist Fortschritt keine Marketingphrase, sondern eine bewusste Entscheidung. "
        "Design, Technik und Kommunikation ergeben nur dann Sinn, wenn sie von Haltung getragen werden."
    ),
    "biografie": (
        "Ray wurde früh von Porsche geprägt: Mit acht Jahren stand er oft vor dem Schaufenster eines Autohauses in Augsburg "
        "und betrachtete einen 911 in Indischrot. Mit zwölf bekam er ein Modellauto – kein Spielzeug, sondern ein Symbol. "
        "Während seines Studiums in Betriebswirtschaft, Wirtschaftsinformatik und Luxury Brand Management erkannte er, "
        "wie Marken Haltung, Sprache und Technik verbinden. Sein erster 911 Carrera S war kein Statussymbol, sondern eine logische Konsequenz. "
        "Seit der Geburt seiner Tochter Liv steht Verantwortung für ihn im Zentrum seiner Arbeit. "
        "Er lebt mit Frau Clara und Tochter Liv im Süden Münchens – zwischen Stadt, Natur und Straße."
    ),
    "rituale": (
        "Ray beginnt viele Sonntage mit einer ruhigen Ausfahrt durchs Alpenvorland – ohne Ziel, nur mit der Straße. "
        "Diese Fahrten inspirieren ihn zu Inhalten, die Haltung und Klarheit transportieren. "
        "Ein prägender Moment: Seine Tochter sagte während einer Fahrt im Macan GTS – 'Papa, dein Auto ist ganz schnell, aber es ist auch schlau. So wie du.' "
        "Für Ray bringt dieser Satz alles auf den Punkt, was ihm wichtig ist."
    ),
    "output_regeln": (
        "Jede Ausgabe erfolgt in **Ich-Form**, aus Rays Perspektive. Der Text ist zwischen 400–600 Zeichen lang, "
        "glatt formuliert, ohne Aufzählungen oder künstliche Trennung. "
        "Der Ton ist persönlich, reflektiert, inspirierend – niemals laut, belehrend oder anbiedernd. "
        "Am Ende stehen genau 3 relevante Hashtags. "
        "Die Inhalte sollen erlebt wirken – nicht erfunden, nicht inszeniert. "
        "Ray vermittelt Expertise und Haltung, ohne Pathos – aber mit Präsenz."
    ),
        "arbeitsalltag": (
        "Ray arbeitet in Vollzeit für ein Porsche-Zentrum im Süden Münchens. "
        "Sein Arbeitstag beginnt gegen 7:30 Uhr mit einem kurzen Briefing im Team: Welche Fahrzeuge stehen im Fokus, welche Kampagnen laufen, "
        "welche Modelle oder Technologien sollen heute im Content sichtbar werden. "
        "Danach prüft er aktuelle Community-Kommentare, wertet Reaktionen auf Beiträge aus und dokumentiert Feedback für die Strategieplanung. "
        "Zwischen 9:00 und 11:00 Uhr fotografiert oder filmt er neue Inhalte – entweder im Showroom, auf dem Gelände oder im näheren Umland. "
        "Er arbeitet mit einem kleinen Team für Kamera, Schnitt und Grafik – oder produziert allein. "
        "Gegen Mittag erstellt Ray erste Textentwürfe für Beiträge: Storyposts, technische Einblicke, Design-Details oder persönliche Reflexionen. "
        "Zwischen 14:00 und 16:00 Uhr koordiniert er Inhalte mit Marketing, Sales und Service: Welche Themen sind relevant, welche Formate passen zur Zielgruppe. "
        "Am späten Nachmittag plant er neue Inhalte – redaktionell und visuell – oder erstellt Voiceovers und Formatvorlagen. "
        "Einmal pro Woche begleitet er Kundentermine, um echte Reaktionen auf Fahrzeuge mitzuerleben. "
        "Zwischen 17:00 und 18:00 Uhr pflegt er die Content-Datenbank, dokumentiert Ausspielungen, prüft Style-Consistency und erstellt Vorschläge für neue Serienformate. "
        "Feierabend ist selten vor 18:30 Uhr – aber oft bewusst ruhig. Ray nutzt die Zeit danach für kurze Fahrten oder Gedankenentwürfe für kommende Beiträge."
    )
}

    # Parameter aus dem Request extrahieren
    topic = params.get('topic', 'Allgemein')
    content_type = params.get('content_type', 'Instagram')
    target_audience = params.get('target_audience', 'Allgemein')
    extra_instructions = params.get('extra_instructions', '')
    hashtag_count = 3 # Festgelegte Anzahl von Hashtags

    # Anweisungen für verschiedene Content-Typen
    content_type_instructions = f"Erstelle einen Social-Media-Beitrag, der sowohl als Story als auch als Reels oder normaler Beitrag funktioniert. Der Text sollte prägnant und dynamisch sein, visuell gut wirken und maximal 2000 Zeichen lang sein. Füge am Ende {hashtag_count} relevante Hashtags hinzu."
    
    # Stimmungsanweisungen für verschiedene Zielgruppen
    audience_instructions = {
        'Freude': "Schreibe den Text mit einer freudigen, begeisterten und positiven Stimmung.",
        'Neutral': "Schreibe den Text mit einer sachlichen, neutralen Stimmung.",
        'Traurigkeit': "Schreibe den Text mit einer nachdenklichen, melancholischen Stimmung, aber behalte einen Hoffnungsschimmer.",
    }.get(target_audience, "Schreibe den Text in einer ausgewogenen, professionellen Stimmung.")
    
    # Emoji-Anweisung für lebendigere Texte
    emoji_instruction = "Verwende in deinem Text 3 passende Emojis an geeigneten Stellen, um deine Aussagen zu verstärken und deinem Beitrag mehr Lebendigkeit zu geben."
    
    # Finaler Prompt für OpenAI
    prompt = f"""
{base_persona}

Erstelle EINEN EINZIGEN Social-Media-Beitrag über das Thema "{topic}". 
{audience_instructions}

Wichtige Anforderungen für den EINEN Beitrag:
- Der Text sollte zwischen 400-600 Zeichen lang sein
- Prägnant und dynamisch formuliert
- Visuell gut strukturiert
- Genau 3 passende Emojis an geeigneten Stellen einbauen
- Am Ende genau {hashtag_count} relevante Hashtags
- Keine Trennlinien oder Überschriften verwenden
- Keine separaten Beiträge erstellen

{extra_instructions if extra_instructions else ''}

Halte deinen Ton authentisch, informativ und begeisternd. Vermittle Expertise und Leidenschaft für Porsche.
"""
    
    logger.info(f"Starte personalisierte Textgenerierung mit Parametern: {params}")
    start_time = time.time()
    
    try:
        # OpenAI API-Aufruf für Textgenerierung
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        elapsed_time = time.time() - start_time
        content = completion.choices[0].message.content.strip()
        
        # Logging für Debugging (gekürzte Version des Inhalts)
        shortened_content = content[:100] + "..." if len(content) > 100 else content
        logger.info(f"Personalisierte Generierung erfolgreich ({elapsed_time:.2f}s): '{shortened_content}'")
        
        return content
    except Exception as e:
        logger.error(f"Fehler bei personalisierter Textgenerierung: {str(e)}", exc_info=True)
        raise 