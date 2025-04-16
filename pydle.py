import random, pyperclip
from datetime import datetime
from tiles import Tile
from colors import Colors
from collections import Counter

WORDLE_FILE = "data/wordles.txt"
ALLOWED_GUESSES = set(line.strip() for line in open("data/all_allowed_guesses.txt"))
START_DATE = datetime(2025, 4, 2)


class Pydle:
    colors = [
        Colors.BLACK,  # 0: Black
        Colors.YELLOW,  # 1: Yellow
        Colors.GREEN,  # 2: Green
    ]

    def __init__(self, is_random: bool = False):
        # 0 is daily, 1 is random, -1 is easter egg/debug
        self.game_type = 1 if is_random else 0
        self.current_word = ""
        self.letters = {letter: Colors.END for letter in "qwertyuiopasdfghjklzxcvbnm"}
        self.board = []
        self.end_game = False

    def startGame(self):
        # set random seed
        self.set_random_seed()
        self.current_word = self.choose_word()

        if self.game_type == 0:
            print(f"Daily Pydle {(datetime.now() - datetime(2025, 4, 2)).days}")
            time_hash = datetime.now().strftime("%Y%m%d")
            random.seed(time_hash)
        else:
            print("Random Pydle")
            random.seed()
        self.wordle_cli()

    def set_random_seed(self):
        if self.game_type == 0:
            seed = datetime.now().strftime("%Y%m%d")
            random.seed(seed)
        else:
            random.seed()

    def choose_word(self):
        with open(WORDLE_FILE) as file:
            words = file.read().splitlines()
        return random.choice(words)

    def get_game_header(self):
        if self.game_type == 0:
            # daily
            day_num = (datetime.now() - START_DATE).days
            return f"Daily Pydle {day_num}"
        return "Random Pydle"

    def wordle_cli(self):
        # print("before while loop")
        while not self.end_game:
            # print("into while loop")
            self.print_board()
            user_input = input(": ").strip().lower()

            # commands
            if user_input.startswith("/"):
                self.end_game = self.handleCommand(user_input[1:])
                continue

            # guess
            if len(user_input) != 5:
                print("incorrect word length")
            elif user_input not in ALLOWED_GUESSES:
                print("word not on list\n\n")
            else:
                self.add_guess(user_input)
                self.end_game = self.check_end_game()

    def add_guess(self, guess: str):
        row = [Tile(char, len(self.board), i) for i, char in enumerate(guess)]
        self.board.append(row)

    def handleCommand(self, command):
        parts = command.split(" ")
        command = parts[0]
        match command:
            case "help":
                print(
                    f"/quit | close game\n/random | pick a random word for Wordle\n/daily | pick the daily word for Wordle"
                )
            case "quit":
                return True
            case "random":
                if self.game_type != 1:
                    Pydle(True).startGame()
                    return True
                else:
                    print("Already random wordle!")
            case "daily":
                if self.game_type != 0:
                    Pydle(False).startGame()
                    return True
                else:
                    print("Already daily wordle!")
            # sv_cheats 1
            case "philmode":
                self.current_word = "burnt"
                # Literally Playable
                self.game_type = -1
            case "set":
                if len(parts) > 1:
                    if len(parts[1]) == 5:
                        self.current_word = parts[1]
                        self.game_type = -1
                        print(f"Set word to {self.current_word}")
                    else:
                        print("word must be 5 letters long")
                else:
                    print("Usage: /set <word>")

            case _:
                print("Unknown command!")

    def check_end_game(self):
        if not self.board:
            return False
        guess = "".join(tile.getLetter() for tile in self.board[-1])
        is_correct = guess == self.current_word

        if len(self.board) == 6 or is_correct:
            self.print_board()
            print(
                f"You {"won" if is_correct else "lost"}! The word was {self.current_word}."
            )
            print(f"\nShare your results!\n{self.printShareable()}")
            if input("Copy to Clipboard? [Y/N] ").lower().startswith("y"):
                pyperclip.copy(f"```ansi\n{self.printShareable()}```")
                print("Copied!")
            return True
        return False

    def print_board(self):
        for row in self.board:
            self.set_row_color(row)
            print(
                "".join(
                    f"{tile.getColor()}[{tile.getLetter()}]{Colors.END}" for tile in row
                )
            )
        for _ in range(6 - len(self.board)):
            print(f"{Colors.END}[ ][ ][ ][ ][ ]")
        self.print_keyboard()

    def set_row_color(self, row):
        word_dict = Counter(self.current_word)

        # check green
        for i, tile in enumerate(row):
            if tile.getLetter() == self.current_word[i]:
                word_dict[tile.getLetter()] -= 1
                tile.setColor(Colors.GREEN)
                self.letters[tile.getLetter()] = Colors.GREEN
        # check yellow; else black
        for i, tile in enumerate(row):
            if tile.getColor() == Colors.GREEN:
                continue  # skip letters that have already been assigned green
            letter = tile.getLetter()
            if letter in self.current_word and word_dict[letter] > 0:
                word_dict[letter] -= 1
                tile.setColor(Colors.YELLOW)
                self.letters[letter] = Colors.YELLOW

    def print_keyboard(self):
        for letter, color in self.letters.items():
            end_char = "\n " if letter in "plm" else " "
            print(
                f"{" " if letter in "z" else ""}{color}{letter.upper()}{Colors.END}",
                end=end_char,
            )

    def printShareable(self):
        type_list = ["Daily", "Random", "Easter Egg'd"]
        day_str = (
            f" {((datetime.now()-START_DATE).days)}" if self.game_type == 0 else ""
        )
        full_print = f"{type_list[self.game_type]} Pydle{day_str} {len(self.board)}/6\n"
        color_map = {Colors.GREEN: "+", Colors.YELLOW: "-", Colors.BLACK: "X"}
        for row in self.board:
            full_print += "".join(
                f"{t.getColor()}[{color_map[t.getColor()]}]" for t in row
            )
            full_print += Colors.END + "\n"
        return full_print


def main():
    game = Pydle()
    # start daily by default
    game.startGame()
    while True:
        response = input("Play again? [Y/N] ").lower()
        if response.startswith("y"):
            # continue playing (random)
            game = Pydle(True)
            game.game_type = 1  # replay sends them to random game instead of daily
            game.startGame()
        elif response.startswith("n"):
            break
        else:
            print("Unknown input.")


main()
