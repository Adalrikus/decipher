from PyDictionary import PyDictionary

Dict = PyDictionary()

message = str(input("Enter a word: "))
message = message.upper()
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
for key in range(len(LETTERS)):
    translated = ''
    for symbol in message:
        if symbol in LETTERS:
            num = LETTERS.find(symbol)
            num = num - key
            if num < 0:
                num = num + len(LETTERS)
            translated = translated + LETTERS[num]
        else:
            translated = translated + symbol
    if bool(Dict.meaning(translated)):
        print("Key: " + str(key) + " Word: " + str(translated.lower()) + " Meaning: " + str(Dict.meaning(translated)))
        break
