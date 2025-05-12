import board
from utils.constants import HUMAN, AI, EMPTY, WIN_LENGTH
from board import GomokuBoard, is_win, is_full

def evaluate_line(line, player):
    score = 0
    opponent = HUMAN if player == AI else AI

    if line.count(player) == 5:
        score += 100000
    elif line.count(player) == 4 and line.count(EMPTY) == 1:
        score += 1000
    elif line.count(player) == 3 and line.count(EMPTY) == 2:
        score += 100
    elif line.count(player) == 2 and line.count(EMPTY) == 3:
        score += 10
    elif line.count(player) == 1 and line.count(EMPTY) == 4:
        score += 1

    # Penalty if opponent is about to win
    if line.count(opponent) == 4 and line.count(EMPTY) == 1:
        score -= 800

    return score

def evaluate_position(board, player):
    size = len(board)
    total_score = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for i in range(size):
        for j in range(size):
            for dx, dy in directions:
                line = []
                for k in range(WIN_LENGTH):
                    ni, nj = i + k * dx, j + k * dy
                    if 0 <= ni < size and 0 <= nj < size:
                        line.append(board[ni][nj])
                    else:
                        break
                if len(line) == WIN_LENGTH:
                    total_score += evaluate_line(line, player)

    return total_score

def utility(board_obj):
    if isinstance(board_obj, GomokuBoard):
        if is_win(board_obj, AI):  
            return 100000
        elif is_win(board_obj, HUMAN):
            return -100000 
        return evaluate_position(board_obj.board, AI) - evaluate_position(board_obj.board, HUMAN)


