from utils.constants import EMPTY

class HumanPlayer:
    def get_move(self, board_obj):
        size = board_obj.size
        while True:
            try:
                row = int(input("Enter row: "))
                col = int(input("Enter col: "))

                if board_obj.is_valid_move(row, col):
                    return row, col
                else:
                    print("Invalid move. Cell is already occupied or out of bounds.")
            except ValueError:
                print("Invalid input. Please enter integer values.")
