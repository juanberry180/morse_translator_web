import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Morse_code#Decoding_software"

class MorseCode:
    """With this Class we crate the morse code dictionary from Wikipedia Page using Beautiful Soup"""

    def __init__(self):
        self.response = requests.get(f"{URL}")
        self.soup = BeautifulSoup(self.response.text, "html.parser")
        self.list_latin_sign = []
        self.list_morse_sign = []
        self.dict_morse = {}
        self.translated_text = ''
        self.dataIn()
        self.dataOut()
        self.morsDictCreation()
        self.adding_signs()


    def dataIn(self):
        for piece in self.soup.select("table tbody tr td b a"):
            self.list_latin_sign.append(piece.text)

    def dataOut(self):
        for piece in self.soup.select("table tbody tr td span span span a span span"):
            self.list_morse_sign .append(piece.text.replace("\xa0", " "))

    def morsDictCreation(self):
        for index in range(len(self.list_latin_sign[:36])):
            self.dict_morse[self.list_latin_sign[index].split(', ')[0].lower()] = self.list_morse_sign[index]

    def adding_signs(self):
        self.dict_morse['.'] = '  ▄ ▄▄▄ ▄ ▄▄▄ ▄ ▄▄▄'
        self.dict_morse[','] = '  ▄▄▄ ▄▄▄ ▄ ▄ ▄▄▄ ▄▄▄'
        self.dict_morse['?'] = '  ▄ ▄ ▄▄▄ ▄▄▄ ▄ ▄'
        self.dict_morse['!'] = '  ▄▄▄ ▄ ▄▄▄ ▄ ▄▄▄ ▄▄▄'





