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
LED_PIN = 18
GPIO.setup(LED_PIN, GPIO.OUT)

# Funktion zum Senden eines Morsezeichens
def send_morse_character(character, dot_duration):
    if character == ' ':
        time.sleep(7 * dot_duration)  # Wortpause: 7 Einheiten
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
                time.sleep(dot_duration)
            time.sleep(2 * dot_duration)  # Buchstabenpause: 3 Einheiten

# Funktion zum Senden eines Texts in Morsezeichen
def send_morse_text(text, dot_duration, farnsworth_delay):
    for character in text:
        if character == ' ':
            time.sleep(3 * dot_duration)  # Wortpause: 3 Einheiten
        else:
            send_morse_character(character, dot_duration)
        time.sleep(farnsworth_delay)  # Farnsworth-Verzögerung

# Funktion zum Berechnen der Farnsworth-Verzögerung basierend auf der Zeichengeschwindigkeit (WPM)
def calculate_farnsworth_delay(dot_duration, words_per_minute):
    # Einheitliche Morsezeichen-Geschwindigkeit in Sekunden pro Zeichen
    character_duration = dot_duration * 3

    # Farnsworth-Verzögerung berechnen basierend auf der gewünschten WPM-Geschwindigkeit
    farnsworth_delay = (60.0 / words_per_minute - character_duration) / 2
    return farnsworth_delay

# Main-Funktion, um den Text einzugeben und die Morsezeichen auszugeben
def main():
    try:
        text = input("Gib den Text ein, den du als Morsezeichen hören möchtest: ")
        words_per_minute = float(input("Gib die Zeichengeschwindigkeit in WPM (Worte pro Minute) ein: "))

        dot_duration = 1.2 / words_per_minute  # Dauer einer Punkt-Einheit in Sekunden
        farnsworth_delay = calculate_farnsworth_delay(dot_duration, words_per_minute)

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

