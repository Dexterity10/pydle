import random, pyperclip
from datetime import datetime
from tiles import Tile
from colors import Colors


class Pydle:
    colors = [
        Colors.BLACK,  # 0: Black
        Colors.YELLOW,  # 1: Yellow
        Colors.GREEN,  # 2: Green
    ]
    wordleFile = "data/wordles.txt"
    allowed_guesses = set(line.strip() for line in open("data/all_allowed_guesses.txt"))

    def __init__(self, isRandom=False):
        self.isRandom = isRandom
        self.currentWord = ""
        self.wordIndex = 0
        self.checkedLetters = set()
        self.letters = {letter: Colors.END for letter in "qwertyuiopasdfghjklzxcvbnm"}
        self.endGame = False
        self.board = []

    def startGame(self):
        # setWordIndex
        if not self.isRandom:
            print(f"Daily Pydle {(datetime.now() - datetime(2025, 4, 2)).days}")
            timeHash = datetime.now().strftime("%Y%m%d")
            random.seed(timeHash)
        else:
            print("Random Pydle")
            random.seed()
        # debug values; returns inbox
        # debugHash = "19700101"
        # random.seed(debugHash)

        self.wordIndex = random.randint(0, sum(1 for _ in open(self.wordleFile)))
        with open(self.wordleFile) as file:
            i = 0
            for line in file:
                if i < self.wordIndex:
                    i += 1
                    continue
                if i == self.wordIndex:
                    word = line.strip()
                    break
            self.currentWord = word

            self.wordleCLI()

    def wordleCLI(self):
        self.endGame = False
        while not self.endGame:
            self.printBoard()
            user_input = input(": ").strip().lower()

            # commands
            if user_input.startswith("/"):
                self.endGame = self.handleCommand(user_input[1:], self.isRandom)
                continue
            else:
                # guess
                if user_input in self.allowed_guesses:
                    # items_list = [Item(i, name) for i, name in zip(range(num_items), names_list)]
                    length = len(self.board)
                    row = [
                        Tile(char, length, i)
                        for i, char in zip(range(len(user_input)), user_input)
                    ]
                    self.board.append(row)
                elif len(user_input) != 5:
                    print("incorrect word length")
                else:
                    print("word not on list\n\n")
            if not self.endGame:
                self.endGame = self.checkEndGame()

    def handleCommand(self, command, isRandom):
        match command:
            case "help":
                print(
                    f"""/quit | close game\
                                        \n/letters | view all letters and what color you've achieved on them\
                                        \n/random | pick a random word for Wordle\
                                        \n/daily | pick the daily word for Wordle"""
                )
            case "quit":
                return True
            case "letters":
                self.printKeyboard()
            case "random":
                if not isRandom:
                    newPydle = Pydle(True)
                    newPydle.startGame()
                    return True
                else:
                    print("Already random wordle!")
            case "daily":
                if isRandom:
                    newPydle = Pydle(False)
                    newPydle.startGame()
                    return True
                else:
                    print("Already daily wordle!")
            case _:
                print("Unknown command!")

    def checkEndGame(self):
        recentWord = len(self.board) > 0 and "".join(
            [tile.getLetter() for tile in self.board[-1]]
        )
        if (
            len(self.board) == 6
            or len(self.board) > 0
            and recentWord == self.currentWord
        ):
            global didDaily
            if not didDaily and not self.isRandom:
                didDaily = True
            self.printBoard()
            print(
                f"You {"won" if recentWord == self.currentWord else "lost"}! The word was {self.currentWord}"
            )
            print(f"\nShare your results!\n{self.printShareable(self.board)}")
            response = input("Copy to Clipboard? [Y/N] ").lower()
            if "y" in response and not "n" in response:
                pyperclip.copy(f"```ansi\n{self.printShareable(self.board)}```")
                print("Copied!")
            return True
        return False

    def printBoard(self):
        for row in self.board:
            self.checkedLetters = set()
            for tile in row:
                self.setTileColor(tile)
                print(f"{tile.getColor()}[{tile.getLetter()}]{Colors.END}", end="")
            print("")
        if len(self.board) > 0 and self.board[-1] == self.currentWord:
            pass
        else:
            for _ in range(6 - len(self.board)):
                print(Colors.END, "[ ][ ][ ][ ][ ]", sep="")
        self.printKeyboard()

    def setTileColor(self, tile):
        colorEnum = Colors.BLACK
        self.letters[tile.getLetter()] = Colors.BLACK

        letter = tile.getLetter()
        letterCount = self.currentWord.count(letter)
        guessLetterCount = sum(
            1 for t in self.board[tile.getRow()] if t.getLetter() == letter
        )

        if letter in self.currentWord:
            colorEnum = Colors.YELLOW
            self.letters[tile.getLetter()] = Colors.YELLOW
            if self.currentWord[tile.getIndex()] == letter:
                colorEnum = Colors.GREEN
                self.letters[tile.getLetter()] = Colors.GREEN
            elif guessLetterCount > letterCount:
                colorEnum = Colors.YELLOW
                self.letters[tile.getLetter()] = Colors.YELLOW
        tile.setColor(colorEnum)

    def printShareable(self, wordList, isAscii=True):
        fullPrint = f"Daily Pydle {(datetime.now() - datetime(2025, 4, 2)).days} {len(self.board)}/6\n"
        colorToLetter = {Colors.GREEN: "+", Colors.YELLOW: "-", Colors.BLACK: "X"}
        for word in wordList:
            for letter in word:
                fullPrint += f"{letter.getColor()}[{colorToLetter[letter.getColor()]}]"
            fullPrint += f"{Colors.END}\n"
        return fullPrint

    def printKeyboard(self):
        for letter, color in self.letters.items():
            end_char = "\n" if letter in "plm" else " "
            print(
                f"{color}{letter.upper()}{Colors.END}",
                end=end_char,
            )


global didDaily
didDaily = False


def main():
    pydle = Pydle(False)
    pydle.startGame()
    while True:
        response = input("Play again? [Y/N] ").lower()
        if "y" in response or "yes" in response:
            # continue playing (random)
            pydle = Pydle(didDaily)
            pydle.startGame()
            continue
        elif "n" in response or "no" in response:
            break
        else:
            print("Unknown input.")


main()
