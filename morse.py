import RPi.GPIO as GPIO
import time

# Definition der Morsezeichen (Buchstaben und Zahlen)
MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
    'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.',
    'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-',
    'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.',
}

# Definition der Pins des Raspberry Pi
GPIO.setmode(GPIO.BCM)
LED_PIN = 20
GPIO.setup(LED_PIN, GPIO.OUT)

# Funktion zum Senden eines Morsezeichens 
# (Es wird ein einzelnes Zeichen mit Pause dahinter gesendet bzw. Pause bei Leerzeichen)
def send_morse_character(character, dot_duration):
    if character == ' ':
        time.sleep(7 * dot_duration)  # Wortpause: 7 Einheiten (es wurde ein Leerzeichen übergeben)
    else:
        morse_code = MORSE_CODE.get(character.upper())
        if morse_code:
            for symbol in morse_code:
                if symbol == '.':
                    GPIO.output(LED_PIN, GPIO.HIGH)
                    time.sleep(dot_duration)
                elif symbol == '-':
                    GPIO.output(LED_PIN, GPIO.HIGH)
                    time.sleep(3 * dot_duration)
                GPIO.output(LED_PIN, GPIO.LOW)
                time.sleep(dot_duration)  # Pause zwischen Symbolen: 1 Einheit
            time.sleep(2 * dot_duration)  # Buchstabenpause: 3 Einheiten (2 + 1 aus vorheriger Zeile)

# Funktion zum Senden eines Texts in Morsezeichen
def send_morse_text(text, dot_duration, farnsworth_delay):
    for character in text:
        send_morse_character(character, dot_duration)
        # Zusätzliche Farnsworth Verzögerung nach dem Zeichenende (abhängig von Zeichen oder Leer)
        if character == ' ':
            time.sleep(2 * farnsworth_delay)  # Zusätzliche Pause von 2x Farnsworth Delay bei neuem Wort
        else:
            time.sleep(farnsworth_delay)  # Zusätzliche Pause von 1x Farnsworth-Verzögerung bei neuem Zeichen

# Funktion zum Berechnen der Farnsworth-Verzögerung basierend auf der Zeichengeschwindigkeit (WPM)
def calculate_farnsworth_delay(dot_duration, words_per_minute, farnsworth_speed):

    # Berechnung der zusätzlichen Zeit für Pausen, um eine effektive Farnswworth-Geschwindigkeit
    # zu erreichen (F *  t_dot). In einem Standardwort (PARIS) sind 6 Pausenblocks enthalten,
    # 4 Pausen zwischen Buchstaben und 2 Pausen (genau 7/3) zwischen Wörtern

    farnsworth_delay_factor = 50 * (words_per_minute / farnsworth_speed - 1)
    farnsworth_delay = farnsworth_delay_factor * dot_duration / 6

    return farnsworth_delay

# Main-Funktion, um den Text einzugeben und die Morsezeichen auszugeben
def main():
    try:
        text = input("Gib den Text ein, den du als Morsezeichen hören möchtest: ")
        words_per_minute = float(input("Gib die Zeichengeschwindigkeit in WPM (Worte pro Minute) ein: "))
        farnsworth_speed = float(input("Gib die Farnsworth-Geschwindigkeit in WPM ein: "))

        dot_duration = 1.2 / words_per_minute  # Dauer einer Punkt-Einheit in Sekunden
        farnsworth_delay = calculate_farnsworth_delay(dot_duration, words_per_minute, farnsworth_speed)

        # Ausgabe des Morsezeichen-Textes auf der Konsole
        print("Morsezeichen:", end=" ")
        for character in text:
            if character == ' ':
                print("/ ", end="")
            else:
                print(MORSE_CODE.get(character.upper()), end=" ")

        # Ausgabe der Morsezeichen als hörbare Töne
        send_morse_text(text, dot_duration, farnsworth_delay)

    except KeyboardInterrupt:
        pass

    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()

