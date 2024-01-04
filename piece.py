class ChessPiece:
    def __init__(self, colour, name):
        self.colour = colour  # white = 1, black = -1
        self.name = name
        self.row = None
        self.col = None
        self.value = None
        self.heatmap = None
        self.alive = 1  # 1 if alive, -1 if dead
        self.history = [[(self.row, self.col), False]]  # [[(row, column), special],]

    def starting_pos(self, board):
        """
        Method which returns starting position for a piece
        :param board: board of interest
        :return: starting position [row, column]
        """
        row_idx = 0 if self.colour == 1 else 7
        starting = None
        if self.name == "P":
            self.value = 1
            self.heatmap = [[0, 0, 0, 0, 0, 0, 0, 0],
                            [2, 2, 2, 2, 2, 2, 2, 2],
                            [1, 2, 2, 2, 2, 2, 2, 1],
                            [1, 1, 2, 2, 2, 2, 1, 1],
                            [0, 1, 1, 2, 2, 1, 1, 0],
                            [0, 0, 0, 1, 1, 0, 0, 0],
                            [0, 0, 0, -1, -1, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]]

            if self.colour == 1:
                self.heatmap = list(reversed(self.heatmap))

            self.heatmap = [[0.25 * c for c in r] for r in self.heatmap]

            for c in range(8):
                if not board[(row_idx + self.colour, c)]:
                    starting = [row_idx + self.colour, c]
                    break
        elif self.name == "R":
            self.value = 5
            self.heatmap = [[1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 2, 2, 2, 1, 1]]

            if self.colour == 1:
                self.heatmap = list(reversed(self.heatmap))

            self.heatmap = [[0.25 * c for c in r] for r in self.heatmap]

            if not board[(row_idx, 0)]:
                starting = [row_idx, 0]
            else:
                starting = [row_idx, 7]
        elif self.name == "N":
            self.value = 3
            self.heatmap = [[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 1, 1, 1, 1, 1, 0],
                            [0, 1, 1, 1, 1, 1, 1, 0],
                            [0, 1, 1, 2, 2, 1, 1, 0],
                            [0, 1, 1, 2, 2, 1, 1, 0],
                            [0, 1, 2, 1, 1, 2, 1, 0],
                            [0, 1, 1, 1, 1, 1, 1, 0],
                            [0, -1, 0, 0, 0, 0, -1, 0]]

            if self.colour == 1:
                self.heatmap = list(reversed(self.heatmap))

            self.heatmap = [[0.25 * c for c in r] for r in self.heatmap]

            if not board[(row_idx, 1)]:
                starting = [row_idx, 1]
            else:
                starting = [row_idx, 6]
        elif self.name == "B":
            self.value = 3
            self.heatmap = [[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 1, 1, 1, 1, 1, 0],
                            [0, 1, 1, 1, 1, 1, 1, 0],
                            [0, 1, 1, 2, 2, 1, 1, 0],
                            [0, 1, 1, 2, 2, 1, 1, 0],
                            [0, 1, 2, 2, 2, 2, 1, 0],
                            [0, 2, 0, 0, 0, 0, 2, 0],
                            [0, 0, -1, 0, 0, -1, 0, 0]]

            if self.colour == 1:
                self.heatmap = list(reversed(self.heatmap))

            self.heatmap = [[0.25 * c for c in r] for r in self.heatmap]

            if not board[(row_idx, 2)]:
                starting = [row_idx, 2]
            else:
                starting = [row_idx, 5]
        elif self.name == "Q":
            self.value = 9
            self.heatmap = [[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 1, 1, 1, 1, 1, 0],
                            [0, 1, 1, 1, 1, 1, 1, 0],
                            [0, 1, 1, 2, 2, 1, 1, 0],
                            [0, 1, 1, 2, 2, 1, 1, 0],
                            [0, 1, 1, 1, 1, 1, 1, 0],
                            [0, 1, 1, 1, 1, 1, 1, 0],
                            [0, 1, 1, 2, 1, 1, 1, 0]]

            if self.colour == 1:
                self.heatmap = list(reversed(self.heatmap))

            self.heatmap = [[0.25 * c for c in r] for r in self.heatmap]

            starting = [row_idx, 3]
        else:  # "K"
            self.value = 999  # priceless
            self.heatmap = [[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [3, 3, 3, 0, 0, 0, 3, 3]]

            if self.colour == 1:
                self.heatmap = list(reversed(self.heatmap))

            self.heatmap = [[0.25 * c for c in r] for r in self.heatmap]

            starting = [row_idx, 4]

        return starting

    def possible_moves(self):
        """
        Method which returns the mobility of a piece
        :return: directions, distance
        """
        directions = []
        distance = []
        if self.name == "P":
            directions = [(self.colour, 0), (self.colour, -1), (self.colour, 1)]
            distance = [1] * 3
        elif self.name == "N":
            directions = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
            distance = [1] * 8
        elif self.name == "K":
            directions = ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, -1), (-1, 1))
            distance = [1] * 8
        elif self.name in "RQ":
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            distance = [7 - self.row, 7 - self.col, self.row, self.col]

        if self.name in "BQ":
            directions += [(1, 1), (-1, 1), (-1, -1), (1, -1)]
            distance += [min([7 - self.row, 7 - self.col]), min([self.row, 7 - self.col]), min(self.row, self.col), min([7 - self.row, self.col])]

        return directions, distance

 