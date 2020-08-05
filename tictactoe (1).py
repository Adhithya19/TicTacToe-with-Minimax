import random
import pygame

pygame.init()

# pygame globals

WIDTH = 270
VHEIGHT = 270
HEIGHT = 300
DIMENSIONS = (WIDTH, HEIGHT)
WHITE = (255, 255, 255)
GREY = (25, 25, 25)
LGREY = (51, 51, 51)
BLACK = (0, 0, 0)


# tictactoe globals

board = [['','',''],
         ['','',''],
         ['','','']]
ai = 'X'
human = 'O'
scores = {'X':10, 'O':-10, 'tie':0}
infinity = float('inf')


playerFont = pygame.font.Font('freesansbold.ttf', 32)
winFont = pygame.font.Font('freesansbold.ttf', 36)
retFont = pygame.font.Font('freesansbold.ttf', 32)

text = winFont.render('', True, WHITE, GREY)

X = playerFont.render('X', True, WHITE, GREY)
O = playerFont.render('O', True, WHITE, GREY)

draw = winFont.render('Tie!', True, WHITE, GREY)
xWins = winFont.render('HA, LOSER!', True, WHITE, GREY)
oWins = winFont.render('O wins!', True, WHITE, GREY)

retryFont = retFont.render('Retry', True, BLACK, LGREY)
retRect = text.get_rect()
retRect.center = (WIDTH // 2 - 40, HEIGHT // 2 + 50)

winRect = text.get_rect()
winRect.center = (WIDTH // 2 - 120, HEIGHT // 2)
tieRect = text.get_rect()
tieRect.center = (WIDTH // 2 - 30, HEIGHT // 2)

textRect = [['','',''],['','',''],['','','']]
for i in range(3):
    for j in range(3):
        textRect[i][j] = text.get_rect()
        textRect[i][j].center = (((j+1)*WIDTH//3)-WIDTH//6) - 10, (((i+1)*VHEIGHT//3)-VHEIGHT//6)


window = pygame.display.set_mode(DIMENSIONS)
window.fill(GREY)
pygame.display.set_caption("Tic Tac Toe")


def main():
    global board
    compMove()
    if retry():
        board = [['','',''], ['','',''], ['','','']]
        textRect = [['','',''], ['','',''], ['','','']]
        main()

def retry():
    global board
    global textRect
    result = isFinished(board)
    run = True
    window.fill(GREY)
    if result == 'X':
        window.blit(xWins, winRect)
    elif result == 'O':
        window.blit(oWins, winRect)
    elif result == 'tie':
        window.blit(draw, tieRect)
    window.blit(retryFont, retRect)
    pygame.display.update()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                x, y = mouse[0], mouse[1]
                if x >= (WIDTH // 3) and x <= ((2 * WIDTH) // 3) and y >= (HEIGHT // 2 + 30) and y <= (HEIGHT // 2 + 60):
                    return True
            elif event.type == pygame.QUIT:
                return False
            
def compMove():
    result = isFinished(board)
    if result != False:
        return 0
    move = bestMove()
    board[move[0]][move[1]] = ai
    showBoard()
    pygame.time.delay(500)
    playerMove()

def playerMove():
    result = isFinished(board)
    if result != False:
        return 0
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            # pygame events
            if event.type == pygame.QUIT:
                return 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                current = pygame.mouse.get_pos()
                # mouse clicks
                x, y = current[0], current[1]
                if x >= 0 and x <= WIDTH/3 and y >= 0 and y <= VHEIGHT/3:
                    i, j = 0, 0
                elif x >= WIDTH/3 and x <= (2*WIDTH)/3 and y >= 0 and y <= VHEIGHT/3:
                    i, j = 0, 1
                elif x >= (2*WIDTH)/3 and x <= WIDTH and y >= 0 and y <= VHEIGHT/3:
                    i, j = 0, 2
                elif x >= 0 and x <= WIDTH/3 and y >= 0 and y <= (2*VHEIGHT)/3:
                    i, j = 1, 0
                elif x >= WIDTH/3 and x <= (2*WIDTH)/3 and y >= 0 and y <= (2*VHEIGHT)/3:
                    i, j = 1, 1
                elif x >= (2*WIDTH)/3 and x <= WIDTH and y >= 0 and y <= (2*VHEIGHT)/3:
                    i, j = 1, 2
                elif x >= 0 and x <= WIDTH/3 and y >= 0 and y <= VHEIGHT:
                    i, j = 2, 0
                elif x >= WIDTH/3 and x <= (2*WIDTH)/3 and y >= 0 and y <= VHEIGHT:
                    i, j = 2, 1
                elif x >= (2*WIDTH)/3 and x <= WIDTH and y >= 0 and y <= VHEIGHT:
                    i, j = 2, 2
                if y < VHEIGHT:
                    if board[i][j] == '':
                        board[i][j] = human
                        run = False
                    
    showBoard()
    pygame.time.delay(500)
    compMove()

def showBoard():
    result = isFinished(board)
    window.fill(GREY)
    pygame.draw.line(window, WHITE, (int(WIDTH/3), 0), (int(WIDTH/3), VHEIGHT))
    pygame.draw.line(window, WHITE, (int((2*WIDTH)/3), 0), (int((2*WIDTH)/3), VHEIGHT))
    pygame.draw.line(window, WHITE, (0, int(VHEIGHT/3)), (WIDTH, int(VHEIGHT/3)))
    pygame.draw.line(window, WHITE, (0, int((2*VHEIGHT)/3)), (WIDTH, int((2*VHEIGHT)/3)))

    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                window.blit(X, textRect[i][j])
            elif board[i][j] == 'O':
                window.blit(O, textRect[i][j])
            elif board[i][j] == '':
                window.blit(text, textRect[i][j])
    pygame.display.update()

# DO NOT TOUCH THESE FUNCTIONS (CORE GAME MECHANICS)

def isFinished(b):
    for i in range(3):
        if equalsThree(b[i][0], b[i][1], b[i][2]):
            return b[i][1]
        if equalsThree(b[0][i], b[1][i], b[2][i]):
            return b[1][i]
        if equalsThree(board[0][0], board[1][1], board[2][2]) or equalsThree(board[2][0], board[1][1], board[0][2]):
            return board[1][1]
    for i in b:
        for j in i:
            if j == '':
                return False
    return 'tie'

def equalsThree(a, b, c):
    return a == b and b == c and a != ''

def bestMove():
    bestScore = -infinity
    move = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = ai
                score = minimax(board, 8, -infinity, infinity, False)
                board[i][j] = ''
                if score > bestScore:
                    bestScore = score
                    move = [[i, j]]
                elif score == bestScore:
                    move.append([i, j])
    return random.choice(move)

def minimax(board, depth, alpha, beta, isMaximizing):
    result = isFinished(board)
    if result != False:
        return scores[result]
    if isMaximizing:
        bestScore = -infinity
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    score = minimax(board, depth - 1, alpha, beta, False) + depth
                    board[i][j] = ''
                    bestScore = max(score, bestScore)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        return bestScore
    else:
        bestScore = infinity
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    score = minimax(board, depth - 1, alpha, beta, True) - depth
                    board[i][j] = ''
                    bestScore = min(score, bestScore)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return bestScore

main()
pygame.quit()

