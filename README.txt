WARNUNG: MainApp_halbautomatisch.py ist noch nicht fertig implementiert und sollte nur zu
Entwicklungszwecken und NUR mit angeschlossener Kamera gestartet werden, da ein Thread geöffnet wird, der ohne
angeschlossene Kamera nicht automatisch durch das Beenden des Programms geschlossen wird.

Die voll implementierte Variante ist MainApp.py.

Die in unserer Abschluss-Präsentation erwähnte dritte Variante MainApp_vollautomatisch.py ist nicht implementiert.
Allerdings sind Anfänge dieser Implementierung als einzelne Codeschnipsel bereits in manchen der Klassen enthalten und
können, sobald die nötige Hardware vorhanden ist benutzt werden.

Hier nochmal der gewünschte Ablauf:

1. alle 4 Sekunden macht eine der angeschlossenen Kameras eine Aufnahme des Bauscheins
2. aus dieser Aufnahme wird die Fahrzeugnummer ausgelesen
3. die ausgelesene Fahrzeugnummer wird mit der zuletzt ausgelesenen Fahrzeugnummer verglichen
4. sofern die Fahrzeugnummern nicht identisch sind -> mach über die angeschlossenen Kameras Aufnahmen der DMC-Codes
5. lies alle 4 Kennziffern aus und starte Abgleich automatisch

Um diese vollautomatisierte Lösung umzusetzen wird (sofern Hardware vorhanden) ein Arbeitsaufwand von ca 20-30 Stunden
geschätzt.