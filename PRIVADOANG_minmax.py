# Andrea Nicole G. Privado
# X-1L
# Min-Max Algorithm

#!/usr/bin/env python
import os
# Set window position in screen
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (533,200) # (c) https://www.pygame.org/wiki/SettingWindowPosition

import pygame

pygame.init()
# Initialize windows size and background
window_surface = pygame.display.set_mode((300, 100))
pygame.display.set_caption('Tic-Tac-Toe')

background = pygame.Surface((300, 100))
background.fill(pygame.Color('#cfd8dc'))

clock = pygame.time.Clock()

# Fonts used
text_font = pygame.font.SysFont('montserrat',53)            # For tile markers
text_font_gameover = pygame.font.SysFont('montserrat',25)   # Winner and Draw prompt
text_font_small = pygame.font.SysFont('montserrat',12)      # Buttons and texts

# Text
text_start = text_font_small.render('What do you want to play?',True, '#0c0c0c')    # Starting window

# Buttons
# Starting window
buttonX_rect = pygame.Rect(83,55, 40, 25) 
buttonO_rect = pygame.Rect(128,55, 40, 25)   
buttonExit_rect = pygame.Rect(173,55, 40, 25) 
text_buttonX= text_font_small.render('X',True, '#0c0c0c')
text_buttonO = text_font_small.render('O',True, '#0c0c0c')
text_buttonExit = text_font_small.render('Exit',True, '#0c0c0c')
# Game Over window
buttonOk_rect = pygame.Rect(130,250, 40, 25) 
text_buttonOk= text_font_small.render('Ok',True, '#0c0c0c')

#Button Background Colors
btnX_color = '#fcfdff'
btnO_color = '#fcfdff'
btnExit_color = '#fcfdff'
btnOk_color = '#fcfdff'

# Initialize Variables (Flags)
isGameStart = False         
isGameOver = False
isLastMove = False
isTurnX = True          
isAfterGame = True

# Main game board elements
image = pygame.image.load('title.jpg')
image = pygame.transform.smoothscale(image, (300, 100))
game_rects = []
# x and y positions of the rectables and markers
rect_xy_values = []
marker_xy_values = []
for i in range(3):
    rect_xy_values.append([(i * 100),(i * 100)+100])

for x in range(3):
    temp1 = []
    temp2 = []
    for y in range(3):
        temp1.append([pygame.Rect((x * 100),(y * 100)+100, 100, 100),""])
        temp2.append([(x * 100)+31,(y * 100)+119])
    game_rects.append(temp1)
    marker_xy_values.append(temp2)

###### MINMAX ALGORITHM ######

# Getting the 2d Array of values from the rects
def getS(game_rects):
    value_table = []
    for i in range(3):
        temp = []
        for j in range(3):
            temp.append(game_rects[i][j][1])
        value_table.append(temp)

    return value_table

# Count the occurences of X in the state
def countX(s):
    count = 0
    for r in s:
        for c in r:
            if c == 'X':
                count += 1
            
    return count

# Count the occurences of O in the state
def countO(s):
    count = 0
    for r in s:
        for c in r:
            if c == 'O':
                count += 1
            
    return count

# Check if state is terminal
def isTerminal(s):
    res = checkBoard(s)
    if res == 0:
        return False
    return True

# Check if the state is a max node
def isMaxNode(s):
    if countX(s) == countO(s):
        return True
    return False

# Check if the state is a min node
def isMinNode(s):
    if countX(s) > countO(s):
        return True
    return False

# Get list of indices of vacant rectangles
def getActions(s):
    a = []      # List of tuples (row-col index)
    for x in range(3):
        for y in range(3):
            if s[x][y] == "":   # If vacant
                a.append((x,y))
    return a

# Getting the action indices and it's corresponding resulting states
# Returns a dictionary
def getSuccessors(s,p):
    a = getActions(s)
    children = {}           # Key = (x,y), value = resulting state
    for index in a:
        state = []          # Copying the s to state
        for i in range(3):
            temp = []
            for j in range(3):
                temp.append(s[i][j])
            state.append(temp)
       
        state[index[0]][index[1]] = p   # Changing the copied s
        children[index] = state
    return children

# Returns 0 is the state results to draw
# Returns 1 if player X won
# Return -1 if player O won
def utility(s):
    res = checkBoard(s)
    if res == 'X':
        return 1
    elif res == -1:
        return 0
    return -1

# Getting state value using maximizaer with alpha-beta pruning
def max_value(s,alpha,beta):
    m = float('-inf')   #https://www.geeksforgeeks.org/python-infinity
    successors = getSuccessors(s,'X')
    for child in successors:
        v = value(successors[child],alpha,beta)
        m = max(m,v)
        if v >= beta:
            return m
        alpha = max(alpha,m)
    return m

# Getting state value using minimizer with alpha-beta pruning
def min_value(s,alpha,beta):
    m = float('inf')
    successors = getSuccessors(s,'O')
    for child in successors:
        v = value(successors[child],alpha,beta)
        m = min(m,v)
        if v <= alpha:
            return m
        beta = min(beta,m)
    return m

# Getting state value with alpha-beta pruning
def value(s,alpha,beta):
    if isTerminal(s):
        return utility(s)
    if isMaxNode(s):
        return max_value(s,alpha,beta)
    if isMinNode(s):
        return min_value(s,alpha,beta) 

# Checks if the board has winning pattern or if already full
# Returns the winning marker/player
# Returns -1 if draw
# Returns 0 is not yet completed/no winner yet
def checkBoard(s):
    # Check rows (3)
    for r in s:
        basis = r[0]
        if basis != "" and r[1] == basis and r[2] == basis:
            return basis
    # Check columns (3)
    for c in range(3):
        basis = s[0][c]
        if basis != "" and s[1][c] == basis and s[2][c] == basis:
            return basis
    # Check diagonals (2)
    basis = s[1][1]
    if(basis != "" and s[0][0] == basis and s[2][2] == basis):
        return basis
    if(basis != "" and s[0][2] == basis and s[2][0] == basis):
        return basis

    # Check if draw
    isDraw = True
    for r in s:
        for c in r:
            if c == '':
                isDraw = False
                break
    
    if isDraw :
        return -1       # draw
    return 0            # no winner yet

# AI Smart move for the game
# Returns an (x,y) index for the 2d Array of rects
# Index returned will be the chosen position of the AI agent
def getSmartMove():     
    global game_rects
    s = getS(game_rects)
    # Check if the AI is player X
    if isMaxNode(s):
        p = 'X'
    else: p = 'O'
    # Get immediate successors
    children = getSuccessors(s,p)
    values = {}         # Key = index -> (x,y), Value = value of state from the value()
    for index in children:
        values[index] = value(children[index],float('-inf'),float('inf'))
    
    # After computing for the values of the successors, check if state is min or max
    if isMaxNode(s):
        n = max(values, key=values.get)     # Returns the key of the max value in the dict: https://stackoverflow.com/a/280156
        return n
    else:
        n = min(values, key=values.get)     # Returns the key of the min value in the dict
        return n

player_marker = ''  # Will hold preferred marker of player
while 1: 
    time_delta = clock.tick(60) / 1000.0

    # Stores the (x,y) mouse position coordinates to variable(tuple)
    mouse = pygame.mouse.get_pos()

    # For every event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       # Clicked exit button
            quit()

        # Button Click events (Start window)
        if event.type == pygame.MOUSEBUTTONDOWN and not isGameStart and pygame.mouse.get_pressed()[0]:
            if buttonX_rect.collidepoint(mouse):
                isGameStart = True
                player_marker = 'X'
            if buttonO_rect.collidepoint(mouse):
                isGameStart = True 
                player_marker = 'O'
            if buttonExit_rect.collidepoint(mouse):
                quit()   
            print("Player marker:",player_marker)

        # Hover events (Start Window)
        if event.type == pygame.MOUSEMOTION and not isGameStart :
            # X button hover
            if buttonX_rect.collidepoint(mouse):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                btnX_color = "#e8f0ff"
            # O button hover
            elif buttonO_rect.collidepoint(mouse):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                btnO_color = "#e8f0ff"
            # Exit button hover
            elif buttonExit_rect.collidepoint(mouse):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
                btnExit_color = "#e8f0ff"
            else:  #Default
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                btnX_color = "#fcfdff"
                btnO_color = "#fcfdff"
                btnExit_color = "#fcfdff"

        # Default
        if event.type == pygame.MOUSEMOTION and isGameStart:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Hover event (Game over window)
        if event.type == pygame.MOUSEMOTION and isGameOver:
            # Ok button hover
            if buttonOk_rect.collidepoint(mouse):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                btnOk_color = "#e8f0ff"
            else:  #Default
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                btnOk_color = "#fcfdff"

        # Game Over window click events
        if event.type == pygame.MOUSEBUTTONDOWN and isGameOver and pygame.mouse.get_pressed()[0]:
            if buttonOk_rect.collidepoint(mouse):
                # Resetting flags and game rects if Ok button is clicked
                isGameStart = False
                isTurnX = True
                isGameOver = False
                isAfterGame = True
                isLastMove = False
                for r in game_rects:
                    for c in r:
                        c[1] = ""
                pygame.time.delay(300)
            
        # Tile clicked / AI move
        if event.type == pygame.MOUSEBUTTONDOWN and isGameStart and pygame.mouse.get_pressed()[0]:
            for i in range(3):
                for j in range(3):
                    # AI is Player O
                    if(player_marker == 'X'):
                        if game_rects[i][j][0].collidepoint(mouse) and game_rects[i][j][1] == "" and isTurnX:
                            game_rects[i][j][1] = 'X'
                            isTurnX = False
                        # AI Smart move
                        if not isTurnX and not isLastMove:
                            index = getSmartMove()      
                            game_rects[index[0]][index[1]][1]  = 'O'
                            isTurnX = True
                    # AI is Player X
                    else:
                        if game_rects[i][j][0].collidepoint(mouse) and game_rects[i][j][1] == "" and not isTurnX:
                            game_rects[i][j][1] = 'O'
                            isTurnX = True
                        # AI Smart move
                        if isTurnX:
                            index = getSmartMove()
                            game_rects[index[0]][index[1]][1] = 'X'
                            isTurnX = False
            
## GUI Elements
    window_surface.blit(background, (0, 0))
    
    #  Window if game is over
    if isGameOver:
        if isAfterGame:         # Making sure the delay will just happen once
            pygame.time.delay(500)  
            isAfterGame = False
        # Reset window background
        window_surface.blit(background, (0, 0))
        window_surface.blit(image, (0, 0))
        # Winner or Draw prompt
        if winner == -1:
            text_draw= text_font_gameover.render("Draw!",True, 'white')
            window_surface.blit(text_draw,(111,190))
        else:
            text_win= text_font_gameover.render("Player "+str(winner)+" won!",True, 'white')
            window_surface.blit(text_win,(60,190))
        # Ok button
        pygame.draw.rect(window_surface, btnOk_color, buttonOk_rect, 0)
        pygame.draw.rect(window_surface, 'gray', buttonOk_rect, 1)
        window_surface.blit(text_buttonOk,(140,255))
    
    #  Starting window
    elif not isGameStart:
        # Display Start Window
        window_surface = pygame.display.set_mode((300, 100))
        background = pygame.Surface((300, 100))
        background.fill(pygame.Color('#cfd8dc'))
        window_surface.blit(background, (0, 0))
        window_surface.blit(text_start,(67,25))
        # Buttons
        pygame.draw.rect(window_surface, btnX_color, buttonX_rect, 0)
        pygame.draw.rect(window_surface, 'gray', buttonX_rect, 1)
        window_surface.blit(text_buttonX,(99,60))
        pygame.draw.rect(window_surface, btnO_color, buttonO_rect, 0)
        pygame.draw.rect(window_surface, 'gray', buttonO_rect, 1)
        window_surface.blit(text_buttonO,(144,60))
        pygame.draw.rect(window_surface, btnExit_color, buttonExit_rect, 0)
        pygame.draw.rect(window_surface, 'gray', buttonExit_rect, 1)
        window_surface.blit(text_buttonExit,(182,60))
    # Game window (tiled)
    else:
        window_surface = pygame.display.set_mode((300, 400))
        background = pygame.Surface((300, 400))
        background.fill(pygame.Color('#3a638a'))
        window_surface.blit(background, (0, 0))
        window_surface.blit(image, (0, 0))
        # Tic-Tac-Toe Tiles
        for i in range(3):
            for j in range(3):
                pygame.draw.rect(window_surface, 'white', game_rects[i][j][0], 1)
                text_tile = text_font.render(game_rects[i][j][1],True, 'white')
                window_surface.blit(text_tile,(marker_xy_values[i][j][0],marker_xy_values[i][j][1]))
        s = getS(game_rects)
        # Check if current move is last move
        if countX(s) >= 4:
            isLastMove = True
        # Check the board for winners/draw
        winner = checkBoard(s)
        if winner != 0 :
            isGameOver = True

# Display update
    pygame.display.update()