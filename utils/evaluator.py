from utils.constants import AI, HUMAN, EMPTY, WIN_LENGTH
from board import is_win

def utility(board):
  
    if is_win(board, AI):
        return 100000
    elif is_win(board, HUMAN):
        return -100000

    score = 0
    size = len(board.board)
    b = board.board

    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    
    for x in range(size):
        for y in range(size):
            for dx, dy in directions:
                line = []
                for i in range(WIN_LENGTH):
                    nx = x + i * dx
                    ny = y + i * dy
                    if 0 <= nx < size and 0 <= ny < size:
                        line.append(b[nx][ny])
                    else:
                        break
                if len(line) == WIN_LENGTH:
                    score += evaluate_line(line, AI, HUMAN, EMPTY)

    # Center bias
    center = size // 2
    for i in range(size):
        for j in range(size):
            if b[i][j] == AI:
                score += max(0, 5 - (abs(i - center) + abs(j - center)))
            elif b[i][j] == HUMAN:
                score -= max(0, 5 - (abs(i - center) + abs(j - center)))

    return score

def evaluate_line(line, ai, human, empty):

    score = 0
    ai_count = line.count(ai)
    human_count = line.count(human)
    empty_count = line.count(empty)

    if ai_count > 0 and human_count == 0:
        # AI only
        if ai_count == 4 and empty_count == 1:
            score += 1000
        elif ai_count == 3 and empty_count == 2:
            score += 100
        elif ai_count == 2 and empty_count == 3:
            score += 10
        else:
            score += ai_count
    elif human_count > 0 and ai_count == 0:
        # HUMAN only
        if human_count == 4 and empty_count == 1:
            score -= 5000
        elif human_count == 3 and empty_count == 2:
            score -= 2000
        elif human_count == 2 and empty_count == 3:
            score -= 10
        else:
            score -= human_count

    return score
