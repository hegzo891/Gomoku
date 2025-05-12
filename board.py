from utils.constants import EMPTY, HUMAN, AI, WIN_LENGTH

class GomokuBoard:
    def __init__(self, size):
        self.size = size
        self.board = [['.' for _ in range(size)] for _ in range(size)]

    def make_move(self, row, col, player):
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            return True
        return False

    def is_valid_move(self, row, col):
        return (
            0 <= row < self.size and
            0 <= col < self.size and
            self.board[row][col] == EMPTY
        )

    def get_available_moves(self):
        return [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i][j] == EMPTY]

    def is_full(self):
        return all(cell != EMPTY for row in self.board for cell in row)

    def check_winner(self, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == player:
                    for dx, dy in directions:
                        count = 1
                        x, y = i + dx, j + dy
                        while (
                            0 <= x < self.size and
                            0 <= y < self.size and
                            self.board[x][y] == player
                        ):
                            count += 1
                            x += dx
                            y += dy
                            if count >= WIN_LENGTH:
                                return True
        return False

    def display(self):
        print("  " + " ".join(f"{i:2}" for i in range(self.size)))
        for idx, row in enumerate(self.board):
            print(f"{idx:2} " + " ".join(row))


def is_win(board, player):
    return board.check_winner(player)

def is_full(board):
    return board.is_full()
