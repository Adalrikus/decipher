import string
import collections
from tkinter import *
from tkinter import messagebox
from math import log
from tabulate import tabulate


ENGLISH_FREQS = {'a':0.08167, 'b':0.01492, 'c':0.02782, 'd':0.04253, 'e':0.12702, 'f':0.02228, 'g':0.02015, 'h':0.06094, 'i':0.06966, 'j':0.00153, 'k':0.00772, 'l':0.04025, 'm':0.02406, 'n':0.06749, 'o':0.07507, 'p':0.01929, 'q':0.00095, 'r':0.05987, 's':0.06327, 't':0.09056, 'u':0.02758, 'v':0.00978, 'w':0.02360, 'x':0.00150, 'y':0.01974, 'z':0.00074}
GERMAN_FREQS = {'a':0.0651, 'b':0.0189, 'c':0.0306, 'd':0.0508, 'e':0.174, 'f':0.0166, 'g':0.0301, 'h':0.0476, 'i':0.0755, 'j':0.0027, 'k':0.0121, 'l':0.0344, 'm':0.0253, 'n':0.0978, 'o':0.0251, 'p':0.0079, 'q':0.0002, 'r':0.07, 's':0.0727, 't':0.0615, 'u':0.0435, 'v':0.0067, 'w':0.0189, 'x':0.0003, 'y':0.0004, 'z':0.0113}
LITHUANIAN_FREQS = {'a':0.1148, 'b':0.0156, 'c':0.0066, 'd':0.0165, 'e':0.0771, 'f':0.0005, 'g':0.0234, 'i':1614, 'y':0.0155, 'j':0.0178, 'k':0.0441, 'l':0.027, 'm':0.0404, 'n':0.047, 'o':0.0512, 'p':0.0205, 'r':0.0529, 's':0.1025, 't':0.0675, 'u':0.0586, 'v':0.0284, 'z':0.0109}


def caesar(rotate_string, number_to_rotate_by, lang):

    string_up = string.ascii_uppercase
    string_lw = string.ascii_lowercase

    if lang is 'English':
        string_up = string.ascii_uppercase
        string_lw = string.ascii_lowercase
    elif lang is 'German':
        string_lw = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        string_up = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    elif lang is 'Lithuanian':
        string_lw = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'i', 'y', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'z']
        string_up = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'I', 'Y', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'Z']

    upper = collections.deque(string_up)
    lower = collections.deque(string_lw)

    upper.rotate(number_to_rotate_by)
    lower.rotate(number_to_rotate_by)

    upper = ''.join(list(upper))
    lower = ''.join(list(lower))

    return rotate_string.translate(str.maketrans(''.join(string_up), upper)).translate(str.maketrans(''.join(string_lw), lower))


def getEntropy(string, lang):

    sum_en, sum_de, sum_lt = 0, 0, 0
    ignored = 0

    for char in string.lower():
        code = ord(char)
        if 97 <= code <= 122:
            if lang is 'English':
                sum_en += log(ENGLISH_FREQS[char])
            elif lang is 'German':
                sum_de += log(GERMAN_FREQS[char])
            elif lang is 'Lithuanian':
                if char is not 'h' and char is not 'w' and char is not 'x' and char is not 'q':
                    sum_lt += log(LITHUANIAN_FREQS[char])
                else:
                    ignored += 1
        else:
            ignored += 1

    if lang is 'English':
        return (-(sum_en)/log(2))/(len(string)-ignored)
    elif lang is 'German':
        return (-(sum_de)/log(2))/(len(string)-ignored)
    elif lang is 'Lithuanian':
        return (-(sum_lt)/log(2))/(len(string)-ignored)


def getAllEntropies(string):

    result_en = {}
    result_de = {}
    result_lt = {}

    for i in range(26):
        result_en[i], result_de[i], result_lt[i] = getEntropy(caesar(string, i, 'English'), 'English'), getEntropy(caesar(string, i, 'German'), 'German'), getEntropy(caesar(string, i, 'Lithuanian'), 'Lithuanian')

    return result_en, result_de, result_lt


def minVal(entropies):

    minimum = entropies[0]
    for i in range(len(entropies)):
        if minimum > entropies[i]:
            minimum = entropies[i]

    return minimum


def minValLoc(entropies):

    location = 0
    minimum = entropies[0]
    for i in range(len(entropies)):
        if minimum > entropies[i]:
            minimum = entropies[i]
            location = i

    return location


def dict2list(d, lang):

    l = []
    for i in range(26):
        l.append([d[i], lang])

    return l


def search(obj, d):

    i = 0
    while obj is not d[i]:
        i += 1

    return i


def print_ent(string, l, d, window):

    tabulated = []

    for i, lang in l:
        if lang is 'English':
            shift = search(i, d[0])
        elif lang is 'German':
            shift = search(i, d[1])
        else:
            shift = search(i, d[2])
        tabulated.append([shift, i, caesar(string, shift, lang), lang])

    tabulated = tabulate(tabulated, headers = ['Shift', 'Entropy', 'Shifted string', 'Language'])
    resultMsg = messagebox.showinfo("Result", tabulated)
    print(tabulated)


def doBreak(string, window):

    entropies_en, entropies_de, entropies_lt = getAllEntropies(string)
    lang = ''

    minimum_en = minVal(entropies_en)
    minimum_de = minVal(entropies_de)
    minimum_lt = minVal(entropies_lt)

    if minimum_en < minimum_de and minimum_en < minimum_lt:
        lang = 'English'
        minimum = minimum_en
        index = minValLoc(entropies_en)
    elif minimum_de < minimum_en and minimum_de < minimum_lt:
        lang = 'German'
        minimum = minimum_de
        index = minValLoc(entropies_de)
    else:
        lang = 'Lithuanian'
        minimum = minimum_lt
        index = minValLoc(entropies_lt)

    list_entr_en = dict2list(entropies_en, 'English')
    list_entr_de = dict2list(entropies_de, 'German')
    list_entr_lt = dict2list(entropies_lt, 'Lithuanian')
    list_entr = list_entr_en + list_entr_de + list_entr_lt
    list_entr.sort()

    checkVars(string, lang, index, window, 3, 1)
    print_ent(string, list_entr, [entropies_en, entropies_de, entropies_lt], window)


def checkVars(plainText, lang, shift, window, row, columnspan):
    resLab = Label(window, text = "Result")
    resLab.grid(row = row, columnspan = columnspan)

    resVar = "Shift: " + str(shift) + " Shifted string: " + caesar(plainText, shift, lang) + " Language: " + lang
    resultLab = Label(window, text = resVar)
    resultLab.grid(row = row+1, columnspan = columnspan)


def checkChoice(varChoice, window):

    if varChoice is 1:
        for widget in window.winfo_children():
            widget.destroy()

        plainEntry = Entry(window)
        plainEntry.grid(row = 1, column = 1)

        labShift = Label(window, text = "Shift")
        labShift.grid(row = 1, column = 2)

        SHIFT_OPTIONS = [i for i in range(26)]

        shift = IntVar(window)
        shift.set(SHIFT_OPTIONS[0])
        shiftOptionMenu = OptionMenu(*(window, shift) + tuple(SHIFT_OPTIONS))
        shiftOptionMenu.grid(row = 2, column = 2)

        labLang = Label(window, text = "Language")
        labLang.grid(row = 1, column = 3)

        LANG_OPTIONS = [
                'English',
                'German',
                'Lithuanian'
                ]

        langOption = StringVar(window)
        langOption.set(LANG_OPTIONS[0])
        langOptionMenu = OptionMenu(*(window, langOption) + tuple(LANG_OPTIONS))
        langOptionMenu.grid(row = 2, column = 3)

        butCipher = Button(window, text = "Cipher",
                command = lambda: checkVars(plainEntry.get(), langOption.get(), shift.get(), window, 4, 3))
        butCipher.grid(row = 3, columnspan = 3)

    elif varChoice is 2:
        for widget in window.winfo_children():
            widget.destroy()

        cipheredEntry = Entry(window)
        cipheredEntry.grid(row = 1, column = 1)

        butDecipher = Button(window, text = "Decipher",
                command = lambda: doBreak(cipheredEntry.get(), window))
        butDecipher.grid(row = 2, column = 1)

    else:
        msg = messagebox.showerror("ERROR", "CHOOSE PROPERLY")


def gui():

    window = Tk()

    labChoice = Label(window, text = 'Caesar Cipher\nChoose')
    labChoice.grid(row = 1, column = 1)

    cipChoice = Button(window, text = "Cipher",
            command = lambda: checkChoice(1, window))
    cipChoice.grid(row = 2, column = 1)

    decChoice = Button(window, text = "Decipher",
            command = lambda: checkChoice(2, window))
    decChoice.grid(row = 3, column = 1)

    window.mainloop()


gui()
