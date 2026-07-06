
def decryptFromMorse(text):
    morse_code_dict = {
        '.-': 'A', '-...': 'B', '-.-.': 'C',
        '-..': 'D', '.': 'E', '..-.': 'F',
        '--.': 'G', '....': 'H', '..': 'I',
        '.---': 'J', '-.-': 'K', '.-..': 'L',
        '--': 'M', '-.': 'N', '---': 'O',
        '.--.': 'P', '--.-': 'Q', '.-.': 'R',
        '...': 'S', '-': 'T', '..-': 'U',
        '...-': 'V', '.--': 'W', '-..-': 'X',
        '-.--': 'Y', '--..': 'Z', '-----': '0',
        '.----': '1', '..---': '2', '...--': '3',
        '....-': '4', '.....': '5', '-....': '6',
        '--...': '7', '---..': '8', '----.': '9',
        '/': ' '
    }

    # Validate input
    valid_chars = set(".-/ ")

    if not all(char in valid_chars for char in text):
        return "Please enter valid Morse Code"

    def morse_to_text(morse_code):
        words = morse_code.split(' / ')
        text = ''

        for word in words:
            chars = word.split()

            for char in chars:
                if char in morse_code_dict:
                    text += morse_code_dict[char]
                else:
                    return "Invalid Morse Code"

            text += ' '

        return text.strip()

    output = morse_to_text(text)

    return output
