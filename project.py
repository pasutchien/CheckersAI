''' Run python3 project.py to start the game'''

import pygame
import time
import probcheckers as checkers
import copy
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers Game")
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
user = None
running = True

BOARD_SIZE = min(WIDTH, HEIGHT)
SQUARE_SIZE = BOARD_SIZE // 8
PIECE_RADIUS = SQUARE_SIZE // 2 - 10

turn = 'x'
board_state = [   ['x', '-', 'x', '-', 'x', '-', 'x', '-'],
               ['-', 'x', '-', 'x', '-', 'x', '-', 'x'],
               ['-', '-', '-', '-', '-', '-', '-', '-'],
               ['-', '-', '-', '-', '-', '-', '-', '-'],
               ['-', '-', '-', '-', '-', '-', '-', '-'],
               ['-', '-', '-', '-', '-', '-', '-', '-'],
               ['o', '-', 'o', '-', 'o', '-', 'o', '-'],
               ['-', 'o', '-', 'o', '-', 'o', '-', 'o']]
max_level = 5
selected_piece = None
moved = False
eat = False
have_rolled = False
dice_value = 0

red_king_image = pygame.image.load('redking.png')
blue_king_image = pygame.image.load('blueking.png')
def draw_board():
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                pygame.draw.rect(screen, GRAY, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            else:
                pygame.draw.rect(screen, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            piece = board_state[row][col]
            if piece != '-':
                # Draw kings
                if piece == 'kx':  # Red king
                    king_image = red_king_image
                elif piece == 'ko':  # Blue king
                    king_image = blue_king_image
                else:
                    # Draw regular pieces
                    if piece == 'x':
                        color = RED
                    else:
                        color = BLUE
                    pygame.draw.circle(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), PIECE_RADIUS)
                if piece in ['kx', 'ko']:  # If it's a king
                    # Resize the image to fit the square size
                    king_image = pygame.transform.scale(king_image, (SQUARE_SIZE, SQUARE_SIZE))
                    # Get the rect of the king image and center it in the square
                    king_rect = king_image.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
                    screen.blit(king_image, king_rect)
select = True
dest_row= None
dest_col = None
count = 0
redwin = 0 
bluewin = 0
def hasking(state, turn):
    if turn == 'x' or turn == 'kx':
        king = 'kx'
    if turn == 'o' or turn == 'ko':
        king = 'ko'
    for r in state:
        for c in r:
            if c == king:
                return True
    return False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Clear the screen
    screen.fill(BLACK)
    if user == None:
        title = largeFont.render("Play Checkers", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((WIDTH / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons
        playXButton = pygame.Rect((WIDTH / 8), (HEIGHT / 2), WIDTH / 4, 50)
        playX = mediumFont.render("Play With Bots", True, BLACK)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, WHITE, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (WIDTH / 8), (HEIGHT / 2), WIDTH / 4, 50)
        playO = mediumFont.render("Bots Duel", True, BLACK)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, WHITE, playOButton)
        screen.blit(playO, playORect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = "X"
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = "Bots"
        
    elif user == "Bots":
        draw_board()
        if checkers.terminal(board_state,turn) == True:
            if turn == 'o':
                winner = 'RED'
                redwin +=1
            elif turn == 'x':
                winner = 'BLUE'
                bluewin +=1
            title = f"Game Over: {winner} wins."
        elif turn  == 'x':
            title = "RED thinking..."
        else:
            title = "BLUE thinking..."
        title = largeFont.render(title, True, BLACK)
        titleRect = title.get_rect()
        titleRect.center = ((WIDTH / 2), 30)
        screen.blit(title, titleRect)

        # Roll the dice and display the value
        
        dice_value = checkers.rolldice()
        if not hasking(board_state,'x') and not hasking(board_state,'o'):
            dice_value = 0
        dice_text = mediumFont.render(f"DICE: {dice_value}", True, BLACK)
        dice_rect = dice_text.get_rect(midtop=(WIDTH / 2, 60))
        screen.blit(dice_text, dice_rect)
        if turn == 'x' and checkers.terminal(board_state,turn)== False: 
            #checkers.print_board(board_state)
            kx_count= checkers.countking(board_state,'x')
            res = checkers.minimax(board_state,'x',max_level,dice_value)
            board_state = res
            turn = 'o'
            time.sleep(1)
        elif turn == 'o' and checkers.terminal(board_state,turn)== False:
            #checkers.print_board(board_state)
            ko_count = checkers.countking(board_state,'o')
            res = checkers.minimax(board_state,'o',max_level,dice_value)
            board_state = res
            turn = 'x'
            time.sleep(1) 
        # if checkers.terminal(board_state,turn) == True:
        #     againButton = pygame.Rect(WIDTH / 3, HEIGHT - 65, WIDTH / 3, 50)
        #     again = mediumFont.render("Play Again", True, BLACK)
        #     againRect = again.get_rect()
        #     againRect.center = againButton.center
        #     pygame.draw.rect(screen, WHITE, againButton)
        #     screen.blit(again, againRect)
        #     click, _, _ = pygame.mouse.get_pressed()
        #     if click == 1:
        #         mouse = pygame.mouse.get_pos()
        #         if againButton.collidepoint(mouse):
        #             time.sleep(0.2)
        #             user = None
        #             board_state = checkers.initial_state()
        #             turn = 'x'
        if checkers.terminal(board_state,turn) == True:
            if turn == 'o':
                winner = 'RED'
                redwin +=1
            elif turn == 'x':
                winner = 'BLUE'
                bluewin +=1
            time.sleep(0.2)
            user = "Bots"
            board_state = checkers.initial_state()
            turn = 'x'
            count += 1
            print("redwin" + str(redwin))
            print("bluewin" + str(bluewin))
        if count % 10 == 0 and count != 0:
            print("redwin" + str(redwin))
            print("bluewin" + str(bluewin))
            break
        

    elif user == "X":
        draw_board()
        if hasking(board_state,'x') == True and have_rolled == False and turn == 'x':
            rollButton = pygame.Rect(WIDTH / 3, HEIGHT - 120, WIDTH / 3, 50)
            rollText = mediumFont.render("Roll Dice", True, BLACK)
            rollRect = rollText.get_rect()
            rollRect.center = rollButton.center
            pygame.draw.rect(screen, WHITE, rollButton)
            screen.blit(rollText, rollRect)

            # Check for mouse click on the roll dice button
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if rollButton.collidepoint(mouse):
                    # Trigger roll dice action here
                    dice_value = checkers.rolldice()
                    draw_board()
                    time.sleep(1)  # Adjust delay as needed
                    have_rolled = True
        elif turn == 'x' and checkers.terminal(board_state,turn)== False and (have_rolled == True or hasking(board_state,'x') == False):
            available = checkers.actions(board_state,'x')
            temp = copy.deepcopy(available)
            for a in temp:
                if board_state[a[0][0]][a[0][1]] == 'kx':
                    if a[2] == True:
                        cost = abs(a[1][0] - a[0][0]) + 1
                    else:
                        cost = abs(a[1][0]-a[0][0])
                    if cost > dice_value:
                        available.remove(a)
            if (not available) and eat == False: #skip round if no move available because of dice
                turn = 'o'
                selected_piece = None
                eat = False
                select = True
                have_rolled = False
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                selected_col = mouse[0] // SQUARE_SIZE
                selected_row = mouse[1] // SQUARE_SIZE
                if (board_state[selected_row][selected_col] == 'x' or board_state[selected_row][selected_col] == 'kx') and eat == False:
                    selected_piece = (selected_row, selected_col)
                    dest_click = 0
                    time.sleep(0.2)
            if selected_piece:
                selected_row, selected_col = selected_piece
                pygame.draw.circle(screen, (0,255,0), (selected_col * SQUARE_SIZE + SQUARE_SIZE // 2, selected_row * SQUARE_SIZE + SQUARE_SIZE // 2), PIECE_RADIUS)           
                dest_click, _, _ = pygame.mouse.get_pressed()
                if dest_click == 1:

                    dest_mouse = pygame.mouse.get_pos()
                    dest_col = dest_mouse[0] // SQUARE_SIZE
                    dest_row = dest_mouse[1] // SQUARE_SIZE

                    time.sleep(0.2)
                    
                    if eat == True and (dest_row == selected_row and dest_col == selected_col):
                        turn = 'o'
                        selected_piece = None
                        eat = False
                        select = True
                        have_rolled = False
                        draw_board()
                    if checkers.is_valid_move(board_state, selected_row, selected_col, dest_row, dest_col, turn, dice_value, eat):
                        diff_row= checkers.convert_to_one(dest_row - selected_row)
                        diff_col= checkers.convert_to_one(dest_col - selected_col)
                        if board_state[dest_row-diff_row][dest_col-diff_col] == 'o' or board_state[dest_row-diff_row][dest_col-diff_col] == 'ko': #eat
                            board_state[dest_row-diff_row][dest_col-diff_col] = '-'
                            board_state[dest_row][dest_col] = board_state[selected_row][selected_col]
                            board_state[selected_row][selected_col] = '-'
                            selected_row = dest_row
                            selected_col = dest_col
                            selected_piece = (selected_row,selected_col)
                            eat = True
                            dest_row = -99
                            dest_col = -99

                            if selected_row == 7 and board_state[selected_row][selected_col] == 'x':
                                board_state[selected_row][selected_col] = 'kx'
                                turn = 'o'
                                eat = False
                                selected_piece = None
                                select = True
                                have_rolled = False
                            #king กิน 2 ต่อไม่เจอ
                            
                            elif (not checkers.can_eat(board_state,selected_piece,'x')) or (dest_row == selected_row and dest_col == selected_col):
                                turn = 'o'
                                selected_piece = None
                                eat = False
                                select = True
                                have_rolled = False
                            draw_board()
                            time.sleep(1)
                        elif board_state[dest_row][dest_col] == '-' and eat == False:
                            select = True
                            board_state[dest_row][dest_col] = board_state[selected_row][selected_col]
                            board_state[selected_row][selected_col] = '-'
                            selected_piece = None
                            turn = 'o'
                            have_rolled = False
                            if dest_row == 7:
                                board_state[dest_row][dest_col] = 'kx'
                            draw_board()
                            time.sleep(1)
        
        elif turn == 'o' and checkers.terminal(board_state,turn) == False:
            dice_value = checkers.rolldice()
            count_o = checkers.countking(board_state,'o')
            res = checkers.minimax(board_state,'o',max_level,dice_value)
            board_state = res
            turn = 'x'
            draw_board()
            time.sleep(1)        
        
        if checkers.terminal(board_state,turn) == True:
            if turn == 'o':
                winner = 'RED'
            elif turn == 'x':
                winner = 'BLUE'
            title = f"Game Over: {winner} wins."
        elif turn  == 'x':
            title = "Play as RED"
        else:
            title = "BLUE thinking..."
        title = largeFont.render(title, True, BLACK)
        titleRect = title.get_rect()
        titleRect.center = ((WIDTH / 2), 30)
        screen.blit(title, titleRect)  
        
        #roll dice
        if not hasking(board_state,'x') and not hasking(board_state,'o'):
            dice_value = 0
        dice_text = mediumFont.render(f"DICE: {dice_value}", True, BLACK)
        dice_rect = dice_text.get_rect(midtop=(WIDTH / 2, 60))
        screen.blit(dice_text, dice_rect)
        
        if checkers.terminal(board_state,turn) == True:
            againButton = pygame.Rect(WIDTH / 3, HEIGHT - 65, WIDTH / 3, 50)
            again = mediumFont.render("Play Again", True, BLACK)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, WHITE, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board_state = checkers.initial_state()
                    turn = 'x'        


    pygame.display.flip()

pygame.quit()

