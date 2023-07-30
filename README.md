# Morse

Python Morse-Code Generator für den RaspberryPi.

Eingabe der Parameter am Prompt
* Wortgeschwindigkeit in WPM (Geschwindigkeit der eizelnen Zeichen)
* Fanrsworth Geschwindigkeit in WPM (Effektive Geschwindikgeit durch Verlängerung der Zwischenräume)
* Eingabe der zu generierenden Wörter.

Die Ausgabe erfolgt am Raspberry Py Zero am physischen Pin38 (GPIO 20). Bei Signal wird der Pin auf HIGH gesetzt. Zum Testen kann eine LED mit einem 120 Ohm Vorwiderstand gegen GND geschaltet werden (z.B. Pin 39). 

Vor der Ausführung muss die GPIO Bibliothek installiert werden:

	pip install RPi.GPIO

Initialer Code wurde über ChatGPT generiert.

(c) 2023 - Dipl.-Ing. Jens U. Moeller
