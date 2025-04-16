import random, pyperclip
from datetime import datetime
from tiles import Tile
from colors import Colors
from collections import Counter


class Pydle:
    colors = [
        Colors.BLACK,  # 0: Black
        Colors.YELLOW,  # 1: Yellow
        Colors.GREEN,  # 2: Green
    ]
    wordleFile = "data/wordles.txt"
    allowed_guesses = set(line.strip() for line in open("data/all_allowed_guesses.txt"))
    gameType = 0  # 0 is daily, 1 is random, -1 is easter egg/debug

    def __init__(self):
        self.currentWord = ""
        self.wordDict = dict()
        self.letters = {letter: Colors.END for letter in "qwertyuiopasdfghjklzxcvbnm"}
        self.endGame = False
        self.board = []

    def startGame(self):
        # set random seed
        if self.gameType == 0:
            print(f"Daily Pydle {(datetime.now() - datetime(2025, 4, 2)).days}")
            timeHash = datetime.now().strftime("%Y%m%d")
            random.seed(timeHash)
        else:
            print("Random Pydle")
            random.seed()

        with open(self.wordleFile) as file:
            wordIndex = random.randint(0, sum(1 for _ in open(self.wordleFile)))
            # pick word index
            i = 0
            for line in file:
                if i < wordIndex:
                    i += 1
                    continue
                if i == wordIndex:
                    word = line.strip()  # find word
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
                self.endGame = self.handleCommand(user_input[1:])
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

    def handleCommand(self, command):
        command = command.split(" ")
        match command[0]:
            case "help":
                print(
                    f"""/quit | close game\
                        \n/random | pick a random word for Wordle\
                        \n/daily | pick the daily word for Wordle"""
                )
            case "quit":
                return True
            case "random":
                if self.gameType != 1:
                    newPydle = Pydle(True)
                    newPydle.startGame()
                    return True
                else:
                    print("Already random wordle!")
            case "daily":
                if self.gameType != 0:
                    newPydle = Pydle(False)
                    newPydle.startGame()
                    return True
                else:
                    print("Already daily wordle!")
            case "philmode":
                self.currentWord = "burnt"
                # Literally Playable
                self.gameType = -1
            case "set":
                self.currentWord = command[1]
                self.gameType = -1
                print("set word to", self.currentWord)
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
            self.printBoard()
            print(
                f"You {"won" if recentWord == self.currentWord else "lost"}! The word was {self.currentWord}"
            )
            print(f"\nShare your results!\n{self.printShareable()}")
            response = input("Copy to Clipboard? [Y/N] ").lower()
            if "y" in response and not "n" in response:
                pyperclip.copy(f"```ansi\n{self.printShareable()}```")
                print("Copied!")
            return True
        return False

    def printBoard(self):
        for row in self.board:
            self.setRowColor(row)
            for tile in row:
                print(f"{tile.getColor()}[{tile.getLetter()}]{Colors.END}", end="")
            print("")
        if len(self.board) > 0 and self.board[-1] == self.currentWord:
            pass
        else:
            for _ in range(6 - len(self.board)):
                print(Colors.END, "[ ][ ][ ][ ][ ]", sep="")
        self.printKeyboard()

    def setRowColor(self, row):
        self.wordDict = {k: self.currentWord.count(k) for k in set(self.currentWord)}
        for index in range(5):
            tile = row[index]
            try:
                if self.currentWord.index(tile.getLetter(), index) == index:
                    self.wordDict[tile.getLetter()] -= 1
                    tile.setColor(Colors.GREEN)
            except ValueError as e:
                tile.setColor(Colors.BLACK)
        for index in range(5):
            tile = row[index]
            if (
                tile.getLetter() in self.currentWord
                and self.wordDict[tile.getLetter()] > 0
                and tile.getColor() != Colors.GREEN
            ):
                self.wordDict[tile.getLetter()] -= 1
                tile.setColor(Colors.YELLOW)

    def printShareable(self):
        wordList = self.board
        gameType = ["Daily", "Random", "Easter Egg'd"]
        fullPrint = f"{gameType[self.gameType]} Pydle{" " + str((datetime.now() - datetime(2025, 4, 2)).days) + " " if self.gameType==0 else " "}{len(self.board)}/6\n"
        colorToLetter = {Colors.GREEN: "+", Colors.YELLOW: "-", Colors.BLACK: "X"}
        for word in wordList:
            for letter in word:
                fullPrint += f"{letter.getColor()}[{colorToLetter[letter.getColor()]}]"
            fullPrint += f"{Colors.END}\n"
        return fullPrint

    def printKeyboard(self):
        for letter, color in self.letters.items():
            end_char = "\n " if letter in "plm" else " "
            print(
                f"{" " if letter in "z" else ""}{color}{letter.upper()}{Colors.END}",
                end=end_char,
            )


def main():
    pydle = Pydle()
    # start daily by default
    pydle.startGame()
    while True:
        response = input("Play again? [Y/N] ").lower()
        if "y" in response or "yes" in response:
            # continue playing (random)
            pydle = Pydle()
            pydle.gameType = 1  # replay sends them to random game instead of daily
            pydle.startGame()
            continue
        elif "n" in response or "no" in response:
            break
        else:
            print("Unknown input.")


main()
