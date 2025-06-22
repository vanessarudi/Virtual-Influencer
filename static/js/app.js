// Globale Variablen
let currentText = '';
let typingTimeout = null;

document.addEventListener('DOMContentLoaded', function() {
    // Event-Listener für API-Verbindungstest
    const connectionButton = document.getElementById('connection-test');
    if (connectionButton) {
        connectionButton.addEventListener('click', testApiConnection);
    }

    // Event-Listener zum Schließen der Statusanzeige
    const closeStatusButton = document.getElementById('close-status');
    if (closeStatusButton) {
        closeStatusButton.addEventListener('click', hideConnectionStatus);
    }
});

// Funktion zum Testen der API-Verbindung
async function testApiConnection() {
    const statusContainer = document.getElementById('connection-status');
    const statusIcon = document.getElementById('status-icon');
    const statusText = document.getElementById('status-text');
    const responseTime = document.getElementById('response-time');
    
    // Status-Container anzeigen
    statusContainer.style.display = 'block';
    
    // Status auf "Wird geprüft" setzen
    statusIcon.className = 'status-icon loading';
    statusText.innerText = 'Verbindung wird geprüft...';
    responseTime.innerText = '';
    
    const startTime = performance.now();
    
    try {
        const response = await fetch('/api/connection/test', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const endTime = performance.now();
        const responseTimeValue = Math.round(endTime - startTime);
        
        if (response.ok) {
            const data = await response.json();
            
            if (data.status === 'success') {
                statusIcon.className = 'status-icon success';
                statusText.innerText = 'API-Verbindung erfolgreich';
                responseTime.innerText = `Antwortzeit: ${responseTimeValue} ms`;
            } else {
                statusIcon.className = 'status-icon error';
                statusText.innerText = `Fehler: ${data.message || 'Unbekannter Fehler'}`;
                responseTime.innerText = `Antwortzeit: ${responseTimeValue} ms`;
            }
        } else {
            statusIcon.className = 'status-icon error';
            statusText.innerText = `HTTP-Fehler: ${response.status}`;
            responseTime.innerText = `Antwortzeit: ${responseTimeValue} ms`;
        }
    } catch (error) {
        statusIcon.className = 'status-icon error';
        statusText.innerText = `Netzwerkfehler: ${error.message}`;
        responseTime.innerText = '';
    }
    
    // Status nach 10 Sekunden automatisch ausblenden
    setTimeout(() => {
        hideConnectionStatus();
    }, 10000);
}

// Funktion zum Ausblenden der Statusanzeige
function hideConnectionStatus() {
    const statusContainer = document.getElementById('connection-status');
    statusContainer.style.display = 'none';
}

// ... existing code ... 