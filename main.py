from board import GomokuBoard
from players.human import HumanPlayer
from players.minimax_ai import MinimaxAI
from players.alphabeta_ai import AlphaBetaAI
from utils.constants import HUMAN, AI


def select_ai(player_name):
    print(f"\nSelect AI type for {player_name}:")
    print("1. Minimax")
    print("2. Alpha-Beta")
    choice = input("Enter choice (1-2): ")
    depth = int(input("Enter depth limit (e.g., 2-3): "))
    return MinimaxAI(depth) if choice == "1" else AlphaBetaAI(depth)


def main():
    board_size = int(input("Enter board size (e.g., 5): "))

    print("\nSelect game mode:")
    print("1. Human vs AI")
    print("2. AI vs AI")
    mode = input("Enter choice (1-2): ")

    board = GomokuBoard(board_size)

    if mode == "1":
        human = HumanPlayer()
        ai = select_ai("Computer")
        players = {HUMAN: human, AI: ai}
    else:
        ai1 = select_ai("AI Player 1")
        ai2 = select_ai("AI Player 2")
        players = {HUMAN: ai1, AI: ai2}

    turn = HUMAN

    while not board.check_winner(HUMAN) and not board.check_winner(AI) and not board.is_full():
        board.display()
        current_player = players[turn]

        if isinstance(current_player, HumanPlayer):
            print("Your turn (X):")
            row, col = current_player.get_move(board)
            board.make_move(row, col, HUMAN)
        else:
            print(f"{'AI 1' if turn == HUMAN else 'AI 2'} is thinking...")
            move = current_player.get_move(board)
            if move:
                row, col = move
                board.make_move(row, col, turn)

        turn = AI if turn == HUMAN else HUMAN

    board.display()
    if board.check_winner(HUMAN):
        print("Human wins!" if mode == "1" else "AI 1 wins!")
    elif board.check_winner(AI):
        print("AI wins!" if mode == "1" else "AI 2 wins!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    main()