from board import GomokuBoard
from players.human import HumanPlayer
from players.minimax_ai import MinimaxAI
# from players.alphabeta_ai import AlphaBetaAI
from utils.constants import HUMAN, AI

def main():
    board_size = int(input("Enter board size (e.g., 5): "))
    depth_limit = int(input("Enter Minimax depth limit (e.g., 2 or 3): "))

    board = GomokuBoard(board_size)
    human = HumanPlayer()
    ai = MinimaxAI(depth_limit=depth_limit)

    turn = HUMAN 

    # Game loop
    while not board.check_winner(HUMAN) and not board.check_winner(AI) and not board.is_full():
        board.display()
        if turn == HUMAN:
            print("Your turn (X):")
            row, col = human.get_move(board)
            board.make_move(row, col, HUMAN)
            turn = AI
        else:
            print("AI is thinking (O)...")
            move = ai.get_move(board)
            if move:
                row, col = move
                board.make_move(row, col, AI)
                turn = HUMAN

    # Final board state
    board.display()

    # Game result
    if board.check_winner(HUMAN):
        print("You win!")
    elif board.check_winner(AI):
        print("AI wins!")
    else:
        print("It's a draw.")

if __name__ == "__main__":
    main()
