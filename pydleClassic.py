from datetime import datetime
import random

global currentWord
global wordIndex
global checkedLetters


global filename
filename = "pydle/data/wordListClassic.txt"

global color
color = {
    "END": "\033[0m",
    "YELLOW": "\033[1;33m",
    "GREEN": "\033[0;32m",
    "BLACK": "\033[0;30m",
}

global letters
letters = {
    "a": color["END"],
    "b": color["END"],
    "c": color["END"],
    "d": color["END"],
    "e": color["END"],
    "f": color["END"],
    "g": color["END"],
    "h": color["END"],
    "i": color["END"],
    "j": color["END"],
    "k": color["END"],
    "l": color["END"],
    "m": color["END"],
    "n": color["END"],
    "o": color["END"],
    "p": color["END"],
    "q": color["END"],
    "r": color["END"],
    "s": color["END"],
    "t": color["END"],
    "u": color["END"],
    "v": color["END"],
    "w": color["END"],
    "x": color["END"],
    "y": color["END"],
    "z": color["END"],
}


def startGame(isRandom=False):
    # filename = "pydle/data/wordList.txt"
    # setWordIndex
    if not isRandom:
        print("Daily Wordle")
        now = datetime.now()
        timeHash = f"{now.strftime("%Y")}{now.strftime("%m")}{now.strftime("%d")}"
        random.seed(timeHash)
    else:
        print("Random Wordle")
    # debugHash = "19700101"
    # random.seed(debugHash)

    global wordIndex
    wordIndex = random.randint(0, 500)

    with open(filename) as file:
        i = 0
        for line in file:
            if i < wordIndex:
                i += 1
                continue
            if i == wordIndex:
                word = line.strip()
                break
    global currentWord
    currentWord = "hello"
    wordleCLI(currentWord, isRandom)


def getFilename():
    global filename
    return filename


def validateWord(word, filename):
    with open(filename) as file:
        for line in file:
            if word == line.strip():
                return True
    return False


def wordleCLI(word, isRandom):
    global currentWord
    endGame = False
    guessCount = 0
    guessList = []
    while not endGame:
        printBoard(guessList)
        inpt = input(": ")
        if inpt.startswith("/"):
            inpt = inpt[1:]
            match inpt.lower():
                case "help":
                    print(
                        f"""/quit | close game\
                            \n/letters | view all letters and what color you've achieved on them\
                            \n/random | pick a random word for Wordle\
                            \n/daily | pick the daily word for Wordle"""
                    )
                case "quit":
                    break
                case "letters":
                    printLetters()
                case "random":
                    if not isRandom:
                        endGame = True
                        startGame(True)
                    else:
                        print("Already random wordle!")
                case "daily":
                    if isRandom:
                        endGame = True
                        startGame(False)
                    else:
                        print("Already daily wordle!")
            continue
        if len(inpt) == 5 and validateWord(inpt, filename):
            guessList.append(inpt)
            guessCount += 1
        elif len(inpt) != 5:
            print("incorrect word length")
        else:
            print("word not on list\n\n")
        if guessCount == 6 or len(guessList) > 0 and guessList[-1] == currentWord:
            print(guessList)
            printBoard(guessList)
            endGame = True
            print(
                f"You {"won" if guessList[-1] == currentWord else "lost"}! The word was {currentWord}"
            )
            break


def printBoard(wordsGuessed):
    for word in wordsGuessed:
        global checkedLetters
        checkedLetters = set()
        i = 0
        for letter in word:
            print(checkColor(letter, i), end="")
            i += 1
        print("")
    for word in range(0, 6 - len(wordsGuessed)):
        print("[ ][ ][ ][ ][ ]")


def checkColor(letter, index):
    global checkedLetters
    selectColor = color["END"]
    if letter in currentWord and letter not in checkedLetters:
        # print("yellow/green letter")
        selectColor = color["YELLOW"]
        letters[letter] = color["YELLOW"]
        # print(f"{letter}, {currentWord[index]}, {index}")
        if currentWord[index] == letter:
            selectColor = color["GREEN"]
            letters[letter] = color["GREEN"]
    else:
        selectColor = color["BLACK"]
        if letter not in checkedLetters:
            letters[letter] = color["BLACK"]
    checkedLetters.add(letter)
    return selectColor + "[" + letter + "]" + color["END"]


def printLetters():
    i = 0
    for item in letters:
        if item.lower() in ["e", "j", "o", "t", "z"]:
            print(f"{letters[item]}{item.upper()}{color["END"]}", sep="")
        else:
            print(f"{letters[item]}{item.upper()}{color["END"]} ", end="")


def main():
    startGame(False)


if __name__ == "__main__":
    main()
