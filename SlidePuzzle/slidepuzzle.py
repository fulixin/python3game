import pygame, sys, random

from pygame.locals import *

# Create the constants(go ahead and experiment with different values)
BOARDWIDTH = 4  # 列模块个数
BOARDHEIGHT = 4  # 行模块个数
TILESIZE = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
BLANK = None

#                R    G    B
BLACK =         (0,   0,   0)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (0,   50,  255)
DARKTURQUOISE = (3,   54,  73)
GREEN =         (0,   204, 0)

BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH-(TILESIZE*BOARDWIDTH+(BOARDWIDTH-1)))/2)
YMARGIN = int((WINDOWHEIGHT-(TILESIZE*BOARDHEIGHT+(BOARDHEIGHT-1)))/2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


def main():
    # global定义全局变量
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT

    # 初始化pygame模块
    pygame.init()

    # 创建时钟对象（可以控制游戏循环频率）
    FPSCLOCK = pygame.time.Clock()
    # 创建游戏窗口大小
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    # 设置窗口标题
    pygame.display.set_caption('Slide Puzzle')
    # 设置窗口字体，得到字体对象
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    # 将选项按钮及其矩形存储在选项中。
    RESET_SURF, RESET_RECT = makeText(
        'Reset', TEXTCOLOR, TILECOLOR, WINDOWWIDTH-120, WINDOWHEIGHT-90)
    NEW_SURF, NEW_RECT = makeText(
        'New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH-120, WINDOWHEIGHT-60)
    SOLVE_SURF, SOLVE_RECT = makeText(
        'Solve', TEXTCOLOR, TILECOLOR, WINDOWWIDTH-120, WINDOWHEIGHT-30)

    mainBoard, solutionSeq = generateNewPuzzle(80)
    SOLVEDBOARD = getStartingBoard()
    allMoves = []

    while True:
        slideTo = None
        msg = 'Click tile or press arrow keys to slide.'
        if mainBoard == SOLVEDBOARD:
            msg = 'Solved!'

        drawBoard(mainBoard, msg)

        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(
                    mainBoard, event.pos[0], event.pos[1])

                if(spotx, spoty) == (None, None):
                    if RESET_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, allMoves)
                        allMoves = []
                    elif NEW_RECT.collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(80)
                        allMoves = []
                    elif SOLVE_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, solutionSeq+allMoves)
                        allMoves = []
                else:
                    blankx, blanky = getBlankPosition(mainBoard)
                    if spotx == blankx+1 and spoty == blanky:
                        slideTo = LEFT
                    elif spotx == blankx-1 and spoty == blanky:
                        slideTo = RIGHT
                    elif spotx == blankx and spoty == blanky+1:
                        slideTo = UP
                    elif spotx == blankx and spoty == blanky-1:
                        slideTo = DOWN

            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN

        if slideTo:
            slideAnimation(mainBoard, slideTo,
                           'Click tile or press arrow keys to slide.', 8)
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

# 获取开始模块
# 获取每个部位的长宽位置
def getStartingBoard():
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH*(BOARDHEIGHT-1)+BOARDWIDTH-1

    board[BOARDWIDTH-1][BOARDHEIGHT-1] = BLANK
    return board


def getBlankPosition(board):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK:
                return (x, y)


def makeMove(board, move):
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky +
                                             1] = board[blankx][blanky+1], board[blankx][blanky]
    if move == DOWN:
        board[blankx][blanky], board[blankx][blanky -
                                             1] = board[blankx][blanky-1], board[blankx][blanky]
    if move == LEFT:
        board[blankx][blanky], board[blankx +
                                     1][blanky] = board[blankx+1][blanky], board[blankx][blanky]
    if move == RIGHT:
        board[blankx][blanky], board[blankx -
                                     1][blanky] = board[blankx-1][blanky], board[blankx][blanky]


def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0])-1 or (move == DOWN and blanky != 0) or (move == LEFT and blankx != len(board)-1) or (move == RIGHT and blankx != 0))


def getRandomMove(board, lastMove=None):
    validMoves = [UP, DOWN, LEFT, RIGHT]

    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)
    return random.choice(validMoves)


def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN+(tileX*TILESIZE)+(tileX-1)
    top = YMARGIN+(tileY*TILESIZE)+(tileY-1)
    return (left, top)


def getSpotClicked(board, x, y):
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)


def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR,
                     (left+adjx, top+adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left+int(TILESIZE/2)+adjx, top+int(TILESIZE/2)+adjy
    DISPLAYSURF.blit(textSurf, textRect)

# 创建文本
# text文本内容
# color文字字体颜色
# bgcolor文字背景颜色
# top距顶部距离
# left距左侧距离
def makeText(text, color, bgcolor, top, left):
    # render在一个新的表面绘制文字
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    # 绘制矩形
    textRect = textSurf.get_rect()
    return (textSurf, textRect)

# 绘制页面
def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH*TILESIZE
    height = BOARDHEIGHT*TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR,
                     (left-5, top-5, width+11, height+11), 4)

    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)


def slideAnimation(board, direction, message, animationSpeed):
    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky+1
    elif direction == DOWN:
        movex = blankx
        movey = blanky-1
    elif direction == LEFT:
        movex = blankx+1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx-1
        movey = blanky

    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()

    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft,
                                         moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

# 创建新谜题
def generateNewPuzzle(numSlides):
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500)
    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'Generating new puzzle...',
                       animationSpeed=int(TILESIZE/3))
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)


def resetAnimation(board, allMoves):
    revAllMoves = allMoves[:]
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        slideAnimation(board, oppositeMove, '', animationSpeed=int(TILESIZE/2))
        makeMove(board, oppositeMove)

# 程序入口
if __name__ == "__main__":
    main()
