class Morse:

    # https://en.wikipedia.org/wiki/Morse_code

    def __init__(self):
        self.code = {'A': '.-',     'B': '-...',   'C': '-.-.',
                     'D': '-..',    'E': '.',      'F': '..-.',
                     'G': '--.',    'H': '....',   'I': '..',
                     'J': '.---',   'K': '-.-',    'L': '.-..',
                     'M': '--',     'N': '-.',     'O': '---',
                     'P': '.--.',   'Q': '--.-',   'R': '.-.',
                     'S': '...',    'T': '-',      'U': '..-',
                     'V': '...-',   'W': '.--',    'X': '-..-',
                     'Y': '-.--',   'Z': '--..',

                     '0': '-----',  '1': '.----',  '2': '..---',
                     '3': '...--',  '4': '....-',  '5': '.....',
                     '6': '-....',  '7': '--...',  '8': '---..',
                     '9': '----.',

                     ' ': '    '
                     }

        self.reverse_code = {value: key for key, value in self.code.items()}

    def _encode_char(self, c):
        try:
            return self.code[c]
        except KeyError:
            print('skipping ' + c)
            return ''

    def _decode_char(self, c):
        if c == '':
            return ''
        try:
            return self.reverse_code[c]
        except KeyError:
            print('skipping ' + c)
            return ''

    def _encode(self, plaintext):
        ciphertext = ''
        working = plaintext.upper()
        for c in working:
            ciphertext = ciphertext + self._encode_char(c) + ' '
        return ciphertext

    def _decode(self, ciphertext):
        print(ciphertext)
        plaintext = ''
        words = ciphertext.split('_')
        print(words)
        for word in words:
            print(word)
            for c in word.split(' '):
                plaintext = plaintext + self._decode_char(c)
            plaintext = plaintext + ' '
        return plaintext

    def encode(self, plaintext):
        return self._encode(plaintext)

    def decode(self, ciphertext):
        return self._decode(ciphertext)

    def cipher(self, c):
        return self._encode_char(c.upper())

    def plain(self, c):
        return self._decode_char(c.upper())


if __name__ == '__main__':
    m = Morse()
    print(m.encode('The quick brown fox jumped over the lazy dogs.'))
    print(m.decode('- .... . _ --.- ..- .. -.-. -.- _ -... .-. --- .-- -. _ ..-. --- -..- _ .--- ..- -- .--. . -.. _ --- ...- . .-. _ - .... . _ .-.. .- --.. -.-- _ -.. --- --. ...  '))
