from colors import Colors


class Tile:
    __slots__ = ("letter", "col", "index", "color")

    def __init__(self, letter, col, index, color="\033[0;30m"):
        self.letter = letter
        self.col = col
        self.index = index
        self.color = Colors.CYAN

    def getLetter(self):
        return self.letter

    def getCol(self):
        return self.col

    def getIndex(self):
        return self.index

    def getColor(self):
        return self.color

    def setColor(self, color):
        self.color = str(color)

    def __str__(self):
        return f"{self.color}[{self.letter}]{Colors.END}"

    def __repr__(self):
        return f"{self.color}[{self.letter}]{Colors.END}"
