''' Run python3 project.py to start the game'''

import copy
import time
import random
def rolldice():
    return random.randint(1, 7) #the dice can goes up to 7 because you need a way to get from the lower left to the upper right corner
def probability(action): #dice value 1, can move 1 block/dice value 2, can move 1 or 2 block...
    #only used with king move
    if action[2] == True: #eat, move is the cost
        move = abs(action[1][0] - action[0][0]) + 1 #destination (action[1]) will be the position of the opponent, so it will jump over it (move + 1)
    else: 
        move = abs(action[1][0] - action[0][0])#cost of standard move
    if move > 7:
        return 0 #dice can not reach that number
    return 1 - (move-1)/7 #probability
    
def initial_state():
    start= [   ['x', '-', 'x', '-', 'x', '-', 'x', '-'],
               ['-', 'x', '-', 'x', '-', 'x', '-', 'x'],
               ['-', '-', '-', '-', '-', '-', '-', '-'],
               ['-', '-', '-', '-', '-', '-', '-', '-'],
               ['-', '-', '-', '-', '-', '-', '-', '-'],
               ['-', '-', '-', '-', '-', '-', '-', '-'],
               ['o', '-', 'o', '-', 'o', '-', 'o', '-'],
               ['-', 'o', '-', 'o', '-', 'o', '-', 'o']]
    return start
def convert_to_one(number): #this will be used to step over a piece just one block
    if number > 0:
        return 1
    elif number < 0:
        return -1
    else:
        return 0  # If the number is 0, it remains 0
def out_of_bound(pos):
    if pos[0] < 0 or pos[0] > 7 or pos[1] < 0 or pos[1]>7:
        #out of bound
        return True
    else:
        #Not out of bound
        return False
def available_moves(state,pos,k,turn):
    if turn == 'x' or turn == 'kx':
        if k == False: #Not King
            left = (pos[0]+1, pos[1]-1)
            right = (pos[0]+1,pos[1]+1)
            moves = [left,right]
            if  out_of_bound(left):
                moves.remove(left)
            elif state[left[0]][left[1]] == 'x' or state[left[0]][left[1]] == 'kx':#if the destination is stuck at X
                moves.remove(left) #you can have the move if the destination is O (to eat)
            if out_of_bound(right):
                moves.remove(right)
            elif state[right[0]][right[1]] == 'x' or state[right[0]][right[1]] == 'kx':
                moves.remove(right)
            return moves
        else:#king move
            i = 1
            moves = []
            while not out_of_bound((pos[0]+i,pos[1]-i)): #lower left
                if state[pos[0]+i][pos[1]-i] == 'x' or state[pos[0]+i][pos[1]-i] == 'kx': #if teammate piece, cannot move anymore
                    break
                if state[pos[0]+i][pos[1]-i] == 'o' or state[pos[0]+i][pos[1]-i] == 'ko': #if opponent piece, add the piece(eat) and stop
                    moves.append((pos[0]+i, pos[1]-i))
                    break
                moves.append((pos[0]+i,pos[1]-i))
                i += 1
            i = 1
            while not out_of_bound((pos[0]+i,pos[1]+i)): #lower right
                if state[pos[0]+i][pos[1]+i] == 'x' or state[pos[0]+i][pos[1]+i] == 'kx':
                    break
                if state[pos[0]+i][pos[1]+i] == 'o' or state[pos[0]+i][pos[1]+i] == 'ko':
                    moves.append((pos[0]+i,pos[1]+i))
                    break
                moves.append((pos[0]+i,pos[1]+i))
                i+=1
            i = 1
            while not out_of_bound((pos[0]-i,pos[1]-i)):#upper left
                if state[pos[0]-i][pos[1]-i] == 'x' or state[pos[0]-i][pos[1]-i] == 'kx':
                    break
                if state[pos[0]-i][pos[1]-i] == 'o' or state[pos[0]-i][pos[1]-i] == 'ko':
                    moves.append((pos[0]-i,pos[1]-i))
                    break
                moves.append((pos[0]-i,pos[1]-i))
                i+=1
            i = 1
            while not out_of_bound((pos[0]-i,pos[1]+i)):#upper right
                if state[pos[0]-i][pos[1]+i] == 'x' or state[pos[0]-i][pos[1]+i] == 'kx':
                    break
                if state[pos[0]-i][pos[1]+i] == 'o' or state[pos[0]-i][pos[1]+i] == 'ko':
                    moves.append((pos[0]-i,pos[1]+i))
                    break
                moves.append((pos[0]-i,pos[1]+i))
                i += 1
            return moves
    if turn == 'o' or turn == 'ko':
        if k == False:
            left = (pos[0]-1,pos[1]-1)
            right = (pos[0]-1,pos[1]+1)
            moves = [left,right]
            if out_of_bound(left):
                moves.remove(left)
            elif  state[left[0]][left[1]] == 'o' or state[left[0]][left[1]] == 'ko':#if the destination is stuck at O
                moves.remove(left) #you can have the move if the destination is X (to eat)

            if out_of_bound(right):
                moves.remove(right)
            elif state[right[0]][right[1]] == 'o' or state[right[0]][right[1]] == 'ko': 
                moves.remove(right)

            return moves
        else:
            i = 1
            moves = []
            while not out_of_bound((pos[0]+i,pos[1]-i)):#lower left
                if state[pos[0]+i][pos[1]-i] == 'o' or state[pos[0]+i][pos[1]-i] == 'ko':
                    break
                if state[pos[0]+i][pos[1]-i] == 'x' or state[pos[0]+i][pos[1]-i] == 'kx':
                    moves.append((pos[0]+i,pos[1]-i))
                    break
                moves.append((pos[0]+i,pos[1]-i))
                i += 1
            i = 1
            while not out_of_bound((pos[0]+i,pos[1]+i)):#lower right
                if state[pos[0]+i][pos[1]+i] == 'o' or state[pos[0]+i][pos[1]+i] == 'ko':
                    break
                if state[pos[0]+i][pos[1]+i] == 'x' or state[pos[0]+i][pos[1]+i] == 'kx':
                    moves.append((pos[0]+i,pos[1]+i))
                    break
                moves.append((pos[0]+i,pos[1]+i))
                i+=1
            i = 1
            while not out_of_bound((pos[0]-i,pos[1]-i)):#upper left
                if state[pos[0]-i][pos[1]-i] == 'o' or state[pos[0]-i][pos[1]-i] == 'ko': 
                    break 
                if state[pos[0]-i][pos[1]-i] == 'x' or state[pos[0]-i][pos[1]-i] == 'kx': 
                    moves.append((pos[0]-i,pos[1]-i))
                    break
                moves.append((pos[0]-i,pos[1]-i))
                i+=1
            i = 1
            while not out_of_bound((pos[0]-i,pos[1]+i)):#upper right
                if state[pos[0]-i][pos[1]+i] == 'o' or state[pos[0]-i][pos[1]+i] == 'ko':
                    break 
                if state[pos[0]-i][pos[1]+i] == 'x' or state[pos[0]-i][pos[1]+i] == 'kx':
                    moves.append((pos[0]-i,pos[1]+i))
                    break
                moves.append((pos[0]-i,pos[1]+i))
                i += 1
            return moves
def actionforone(state,pos,k,turn): #used with available_moves to obtain all the actions for one piece
    result = []
    start = pos
    moves = available_moves(state,pos,k,turn)
    eatable = False
    for move in moves:
        diff_row = convert_to_one(move[0]-start[0])
        diff_col = convert_to_one(move[1]-start[1])
        if state[move[0]][move[1]] in ['o','ko','x','kx']: #if the destination is at opponent piece (eat)
            if out_of_bound((move[0]+diff_row,move[1]+diff_col)):#if you jump over the opponent piece, and it is out of bound -> the move is unavailable
                continue
            elif state[move[0]+diff_row][move[1]+diff_col] != '-': #if you jump over the opponent piece, and the slot is not available                               
                continue
            else:
                result.append((start,move,True)) #cut out all possible errors, the move is valid and add that move
                eatable = True #tuple (start,end, eat)/ this means you can eat (eatable will be used later)
        else:
            result.append((start,move,False)) #no eat
    if eatable:
        temp = copy.deepcopy(result)
        for r in temp:
            if r[2] == False:
                result.remove(r) #If can eat u need to eat
    
    return (result,eatable) #result is the list of all available action for that piece, eatable state that this piece can eat
        

def actions(state,turn): #action for every piece on the board considering the turn
    #list of tuples (start,end,eat)
    result = []
    eatable = False
    if turn == 'x':
        for i in range(len(state)):#just calling actionforone for every piece
            for j in range(len(state[i])):
                if state[i][j] == 'x':
                    actions = actionforone(state,(i,j),False,'x') 
                    if actions[1] == True: #that particular piece can eat
                        eatable = True #there is an eat option
                    result = result + actions[0] #concatenate the available action for every piece
                elif state[i][j] == 'kx':
                    #king X
                    actions = actionforone(state,(i,j),True,'x') #actionforone for the king piece
                    if actions[1] == True:
                        eatable = True #there is an eat option
                    result = result + actions[0]
    else:
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 'o':
                    actions = actionforone(state,(i,j),False,'o')
                    if actions[1] == True:
                        eatable = True
                    result = result + actions[0]
                elif state[i][j] == 'ko':
                    #king X
                    actions = actionforone(state,(i,j),True,'o')
                    if actions[1] == True:
                        eatable = True
                    result = result + actions[0]
    temp = copy.deepcopy(result)

    if eatable: #if any piece can eat the only action you can do is eat
        for r in temp:
            if r[2] == False:
                result.remove(r)
    return result

def result(state, action, results = None): #obtain the list of result boards for the action
    if results is None:
        results = []
    resultstate = copy.deepcopy(state)
    start = resultstate[action[0][0]][action[0][1]]
    resultstate[action[0][0]][action[0][1]] = '-' 
    
    if action[2] == False: #dont eat
        resultstate[action[1][0]][action[1][1]] = start
        if start == 'x' and action[1][0] == 7: #goes into king slot as a normal piece
            resultstate[action[1][0]][action[1][1]] = 'kx'
        elif start == 'o' and action[1][0] == 0:
            resultstate[action[1][0]][action[1][1]] = 'ko'
        results.append(resultstate) #if you don't eat then there will be only one result
        return results 
    else: #eat
        resultstate[action[1][0]][action[1][1]] = '-' #eat that piece
        diff_row= convert_to_one(action[1][0]-action[0][0])
        diff_col= convert_to_one(action[1][1]-action[0][1])
        resultstate[action[1][0]+diff_row][action[1][1]+diff_col] = start #move to the block after
        if start == 'x' and action[1][0]+diff_row == 7: #if you go into king slots as a normal piece after eating, you cannot eat anymore in a row
            resultstate[action[1][0]+diff_row][action[1][1]+diff_col] = 'kx'
            results.append(resultstate)
            return results
        elif start == 'o' and action[1][0]+diff_row == 0:
            resultstate[action[1][0]+diff_row][action[1][1]+diff_col] = 'ko'
            results.append(resultstate)
            return results
        #as a normal piece, eat and does not go in to king slot/ as a king piece, eat in any slots
        results.append(resultstate) #append the move, you can then check for eat 2 in a row
        #-------------------------------------eat more than one in a row---------------------------------------------
        if start == 'kx' or start == 'ko':
            king = True
        else:
            king = False
        if start == 'kx' or start == 'x':
            turn = 'x'
        if start == 'ko' or start == 'o':
            turn = 'o'
        actions = actionforone(resultstate,(action[1][0]+diff_row,action[1][1]+diff_col),king,turn)[0] #get the actions of that piece after eating
        #print(actions)
        for action in actions: #there will be choices when eating like upper left, upper right so we need to loop all those action
            if action[2] == True: #you can choose to eat 1-2-3-4-... in a row, NO NORMAL MOVE 
                 results = result(resultstate,action,results) #run recursively to see all the possible cases of eats in a row
        
        return results #results is all the possible resultstate of eats in a row
                
def terminal(state,turn):
    count_x = 0
    count_o = 0
    if turn == 'x' or turn == 'kx':
        if not actions(state,'x'): #cannot move anymore
            return True
    if turn == 'o' or turn == 'ko':
        if not actions(state,'o'):
            return True 
    for r in state:
        for c in r:
            if c == 'x' or c == 'kx':
                count_x += 1
            elif c == 'o' or c =='ko':
                count_o += 1
            if count_x != 0 and count_o != 0:
                return False
    return True #either no X piece on the board or no O piece on the board
def utility2(state): #win or lose
    count_x = 0
    count_o = 0
    for r in state:
        for c in r:
            if c == 'x' or c == 'kx':
                count_x += 1
            if c == 'o' or c == 'ko':
                count_o += 1
    if count_x > 0 and count_o == 0: #X wins 
        return 500
    elif count_x == 0 and count_o > 0:#O wins
        return -500
    else:
        if not actions(state,'o'): #O has no more actions , X wins
            return 500
        elif not actions(state, 'x'): #X has no more actions, O wins
            return -500
def countking(state,turn):
    count_kx = 0
    count_ko = 0
    for r in state:
        for c in r:
            if c == 'kx':
                count_kx += 1
            elif c =='ko':
                count_ko += 1
    if turn == 'x' or turn == 'kx':
        return count_kx
    else:
        return count_ko
        
def utility(state,turn): #calculate win chance mid game (I have turn parameter because I also have another heuristic)
    #MAX is 'x'
    #MAX is 'x'
    result = 0
    actions_o = actions(state,'o') #Because I cant go to the state to see which side wins, I need a good heuristic
    actions_x = actions(state,'x') #I have tried many including checking only numbers of pieces and kings
    if not actions_o:              #This one seems to be the best heuristic
        result += 0 #this will be handled in the ultility2
    else:
        if actions_o[0][2] == True: #can eat
            vuln_x = len(actions_o) #how many actions of O can eat X 
            result = result + (-3)*vuln_x #vulnerable piece X (rough approximation because len(actions_o) can have two pieces of O that can eat a single piece of X)
    if not actions_x:
        result += 0
    else:
        if actions_x[0][2] == True: #can eat
            vuln_o = len(actions_x) #how many actions of X can eat O
            result += 3*vuln_o #vulnerable piece O (rough approximation because len(actions_x) can have two pieces of X that can eat a single piece of O)
    for i in range(8):
        for j in range(8):
            if state[i][j] == 'x':
                result += 5 #number of regular
                if i == 0:
                    result += 4 #regular in the back
            if state[i][j] == 'o':
                result -= 5 #number of regular
                if i == 7:
                    result -= 4 #regular in the back
            if state[i][j] == 'kx':
                result += 7.75 #number of king
            if state[i][j] == 'ko':
                result -= 7.75 #number of king
            if i == 3 or i == 4:# in the middle row
                if j>=2 and j<=5:#in the middle column
                    if state[i][j] == 'x' or state[i][j] == 'kx':
                        result += 2.5
                    if state[i][j] == 'o' or state[i][j] == 'ko':
                        result -= 2.5
                else: #in the side column
                    if state[i][j] == 'x' or state[i][j] == 'kx':
                        result += 0.5
                    if state[i][j] == 'o' or state[i][j] == 'ko':
                        result -= 0.5
#-------------------------------------------------Another Heuristic-----------------------------------
            # if state[i][j] == 'x':
            #     result += 500
            # if state[i][j] == 'kx':
            #     result += 1000
            # if state[i][j] == 'o':
            #     result -= 500
            # if state[i][j] == 'ko':
            #     result -= 1000
            # if turn == 'x' or turn == 'kx':
            #     if state[i][j] == 'x' or state[i][j] == 'kx':

            #         #EAT
            #         if can_eat(state,(i,j),turn) == True:
            #             result += 8
            
            #     elif state[i][j] == 'o' or state[i][j] == 'ko':
            #         if can_eat(state,(i,j),'o') == True:
            #             result -= 4
            #         if state[i][j] == 'o':
            #             if not actionforone(state,(i,j),False,'o'):
            #                 result += 3
            #         if state[i][j] == 'ko':
            #             if not actionforone(state,(i,j),True,'o'):
            #                 result += 6
            # else:
            #     if state[i][j] == 'o' or state[i][j] == 'ko':
            #         if state[i][j] == 'o':
            #             result -= 5
            #         if state[i][j] == 'ko':
            #             result -= 10
            #         #EAT
            #         if can_eat(state,(i,j),turn) == True:
            #             result -= 8
            #     elif state[i][j] == 'x' or state[i][j] == 'kx':
            #         if can_eat(state,(i,j),'x') == True:
            #             result += 4
            #         if state[i][j] == 'x':
            #             if not actionforone(state,(i,j),False,'x'):
            #                 result -= 3
            #         if state[i][j] == 'kx':
            #             if not actionforone(state,(i,j),True,'x'):
            #                 result -= 6
    return result
#maxvalue and minvalue runs recursively against each other combining into a depth first search
def maxvalue(state,depth,max_depth,alpha,beta,turn,prob = 1): #maxvalue return max of all minvalue of the children 
    # print("max = "+ str(depth))
    if terminal(state, 'x'):
        # print_board(state)
        # print("max utility = "+ str(utility2(state)))  
        return prob*(utility(state,turn)+utility2(state)) #prob which multiply repeatedly for every move to reach this state will be passed down
        #at the end, eventhough it is a lost, we want to try to lose while trying our best/ and if we win, we would aim on flawless win
        #If we use only utility2 and the bots see all possible path as lost, It cannot decide which path to go
    if depth >= max_depth:
        # print_board(state)
        # print("max utility = "+ str(utility(state,turn)))
        return prob*(utility(state,turn)) #prob which multiply repeatedly for every move to reach this state will be passed down
    v = -999999999
    for action in actions(state,'x'):
        results = result(state,action)
        if state[action[0][0]][action[0][1]] == 'kx': #you need to toss a dice to see how many blocks king can go (only apply to kings)
            probb = probability(action)
            if probb == 0: #cost of this action > 7
                continue
        if state[action[0][0]][action[0][1]] == 'x': #regular piece can always move
            probb = 1
        for r in results: #this is all the possible children
            v = max(v,minvalue(r,depth+1,max_depth,alpha,beta,turn,prob*probb)) #pass the probb down, repeatedly multiplying
            alpha = max(alpha,v) 
            if alpha >= beta:
                return v #prune
    return v
def minvalue(state,depth,max_depth,alpha,beta,turn,prob = 1): #minvalue return min of all maxvalue of the children
    # print("min = " + str(depth))
    if terminal(state,'o'):
        # print_board(state)
        # print("max utility = "+ utility2(state))
        return prob*(utility2(state)+utility(state,turn))
    if depth >= max_depth:
        # print_board(state)
        # print("min utility = "+str(utility(state,turn)))
        return prob*(utility(state,turn))
    v = 9999999999
    for action in actions(state,'o'):
        if state[action[0][0]][action[0][1]] == 'ko':
            probb = probability(action)
            if probb == 0:
                continue
        if state[action[0][0]][action[0][1]] == 'o':
            probb = 1
        results = result(state,action)
        for r in results:
            v = min(v,maxvalue(r,depth+1,max_depth,alpha,beta,turn,prob*probb)) #pass the probb down, repeatedly multiplying
            beta = min(beta,v) #BETAAA
            if alpha >= beta:
                return v
    return v
def minimax(state,turn,max_depth,dice):
    """
    Returns the optimal action for the current player on the state.
    """
    if terminal(state,turn):
        return None
    else:
        if turn == 'x':
            moves = []
            alpha = -9999999
            beta = 99999999
            
            for action in actions(state,'x'):
                results = result(state,action)
                if state[action[0][0]][action[0][1]] == 'kx':
                    if action[2] == False:
                        cost = abs(action[1][0] - action[0][0])
                    else:
                        cost = abs(action[1][0] - action[0][0]) + 1
                    if cost > dice: #extend the first depth with all the possible moves considering the dice value
                        continue
                for r in results: #X prioritize MAX so we will run minvalue of all the children
                    #print_board(r)
                    new_v = minvalue(r,1,max_depth,alpha,beta,'x') 
                    moves.append((r,new_v)) #keep that resultstate and its v value
                    alpha = max(alpha,new_v)
                    
                    # if alpha >= beta:
                    #     return getbestmoves(moves,'x')
            
            if not moves: #the game does not end but there is no available move because of dice
                return state 
            return getbestmoves(moves,'x') #keep every move and its v, randomize the best one
        if turn == 'o':
            moves = []
            alpha = -99999999
            beta = 99999999

            for action in actions(state,'o'):
                if state[action[0][0]][action[0][1]] == 'ko':
                    if action[2] == False:
                        cost = abs(action[1][0] - action[0][0])
                    else:
                        cost = abs(action[1][0] - action[0][0]) + 1
                    if cost > dice:#extend the first depth with all the possible moves considering the dice value
                        continue
                results = result(state,action)
                for r in results: #O prioritize MIN so we will run maxvalue of all the children
                    #print_board(r)
                    new_v = maxvalue(r,1,max_depth,alpha,beta,'o')
                    moves.append((r,new_v)) #keep that resultstate and its v
                    beta = min(beta,new_v)
                    # if alpha >= beta:
                    #     return getbestmoves(moves,'o')
            if not moves: #the game does not end but there is no available move because of dice
                return state
            return getbestmoves(moves,'o')#keep every move and its v, randomize the best one
def print_board(state):
    """
    Prints the board with row and column indices.
    """
    print("   0  1  2  3  4  5  6  7")
    for i, row in enumerate(state):
        print(i, end="  ")
        for cell in row:
            print(cell, end="  ")
        print()
def is_valid_move(state, selected_row, selected_col, dest_row, dest_col, turn, dice, eat): #used with player mode
    available_a = []
    cost = abs(dest_row - selected_row)
    king = False
    if state[selected_row][selected_col] == 'ko' or state[selected_row][selected_col] == 'kx':
        king = True
    if king == True and cost > dice and eat == False:
        return False
    acts = actions(state,turn)
    for action in acts:
        if action[2] == True: #eat
            diff_row= convert_to_one(action[1][0]-action[0][0])
            diff_col= convert_to_one(action[1][1]-action[0][1])
            nrow = action[1][0] + diff_row
            ncol = action[1][1] + diff_col
            available_a.append(((action[0][0],action[0][1]),(nrow,ncol)))
        else:
            available_a.append((action[0],action[1]))
    if ((selected_row,selected_col),(dest_row,dest_col)) in available_a and out_of_bound((dest_row,dest_col)) == False:
        return True # Valid
    else:
        return False #Not Valid
def can_eat(state,pos,turn): #used in player mode
    king = False
    if state[pos[0]][pos[1]] == 'ko' or state[pos[0]][pos[1]] == 'kx':
        king = True
    actions = actionforone(state,pos,king,turn)[0]
    for action in actions:
        if action[2] == True:
            return True
    return False
def getbestmoves(moves,turn):
    if turn == 'x':

        max_value = max(moves, key=lambda x: x[1])[1]
        result = []
        for move in moves:
            if move[1] == max_value:
                result.append(move[0])
        return random.choice(result) #randomized the best move
    elif turn == 'o':
        min_value = min(moves, key=lambda x: x[1])[1]
        result = []
        for move in moves:
            if move[1] == min_value:
                result.append(move[0]) #randomized the best move

        return random.choice(result)

#-----------------------------------------DEBUGGING ZONE -----------------------------------------------------------------
# dice = 1
# print(dice)
# state = [['-', '-', '-', '-', '-', '-', '-', '-'],
#         ['-', '-', '-', 'kx', '-', '-', '-', '-'],
#         ['-', '-', '-', '-', '-', '-', '-', '-'],
#         ['-', '-', '-', '-', '-', '-', '-', '-'],
#         ['-', '-', '-', '-', '-', '-', '-', '-'],
#         ['-', '-', '-', '-', '-', '-', '-', 'o'],
#         ['o', '-', '-', '-', '-', '-', 'o', '-'],
#         ['-', '-', '-', '-', '-', 'o', '-', 'o']]
# state = minimax(state,'x',6,dice)
# print_board(state)
# for action in actions(state,'x'):
#     for r in result(state,action):
#         print_board(r)
# state = minimax(state,'x',6)
# print('-----------------------------------------------------------------------')
# print("current")
# print_board(state)

#state = minimax(state,'o',3)

# print(terminal(state,'x'))
# turn = 'o'
# turn = 'o'
# state = initial_state()
# print(actions(state,turn))


# action = ((5,1),(6,2), True)
# results = result(initial_state,action)
# for r in results:
#     print_board(r)


# print_board(initial_state)
# action = ((6,2),(7,1),False)
# results = result(initial_state,action)
# for r in results:
#     print_board(r)
#---------------------------------------------Bots vs Bots--------------------------------------------
# initial = [['-', '-', '-', '-', '-', '-', '-', '-'],
#                ['-', '-', '-', '-', '-', '-', '-', '-'],
#                ['-', '-', '-', '-', '-', '-', '-', '-'],
#                ['-', '-', '-', 'x', '-', '-', '-', '-'],
#                ['-', '-', '-', '-', '-', '-', '-', '-'],
#                ['-', 'o', '-', 'o', '-', 'o', '-', 'o'],
#                ['o', '-', 'o', '-', 'o', '-', 'o', '-'],
#                ['-', 'o', '-', 'o', '-', 'o', '-', 'o']]
# turn = 'o'
# while terminal(state,turn) == False:
#     if turn == 'x':
#         print('---------------------------'+ 'turn x' + '-------------------------------')
#         res = minimax(state,'x',9)
#         state = res
#         print_board(state)
#         turn = 'o'
#         time.sleep(1)
#     else:
#         print('---------------------------'+ 'turn o' + '-------------------------------')
#         res = minimax(state,'o',9)
#         state = res
#         print_board(state)
#         turn = 'x'
#         time.sleep(1)
# if turn == 'o':
#     print("X wins")
# if turn == 'x':
#     print('O wins')
        # start_x = int(input("Pick one (X-Axis) : "))
        # start_y = int(input("Pick one (Y-Axis) : "))
        # move_to_x = int(input("Move to (X): "))
        # move_to_y = int(input("Move to (Y): "))
        # eat = int(input("Eat or not: "))
        # if eat == 1:
        #     eat = True
        # else:
        #     eat = False
        # action = ((start_x,start_y),(move_to_x,move_to_y), eat)
        # initial_state=result(initial_state,action)
        # print_board(initial_state)
        # turn = 'x'
        # action = minimax(initial_state,'o',5)
        # initial_state = result(initial_state,action)
        # print_board(initial_state)
        # turn = 'x'

# action = (actions(initial_state,'x'))
# print("initial")
# print_board(initial_state)
# print("----------------------------------------------------------------")
# for act in action:
#     print(act)
#     print_board(result(initial_state,act))
#     print("---------------------------------------------------------------------------")
            
            
            #HEURISTIC
            # if state[i][j] == 'x':
            #     result += 500
            # if state[i][j] == 'kx':
            #     result += 1000
            # if state[i][j] == 'o':
            #     result -= 500
            # if state[i][j] == 'ko':
            #     result -= 1000
            # if turn == 'x' or turn == 'kx':
            #     if state[i][j] == 'x' or state[i][j] == 'kx':

            #         #EAT
            #         if can_eat(state,(i,j),turn) == True:
            #             result += 8
            
            #     elif state[i][j] == 'o' or state[i][j] == 'ko':
            #         if can_eat(state,(i,j),'o') == True:
            #             result -= 4
            #         if state[i][j] == 'o':
            #             if not actionforone(state,(i,j),False,'o'):
            #                 result += 3
            #         if state[i][j] == 'ko':
            #             if not actionforone(state,(i,j),True,'o'):
            #                 result += 6
            # else:
            #     if state[i][j] == 'o' or state[i][j] == 'ko':
            #         if state[i][j] == 'o':
            #             result -= 5
            #         if state[i][j] == 'ko':
            #             result -= 10
            #         #EAT
            #         if can_eat(state,(i,j),turn) == True:
            #             result -= 8
            #     elif state[i][j] == 'x' or state[i][j] == 'kx':
            #         if can_eat(state,(i,j),'x') == True:
            #             result += 4
            #         if state[i][j] == 'x':
            #             if not actionforone(state,(i,j),False,'x'):
            #                 result -= 3
            #         if state[i][j] == 'kx':
            #             if not actionforone(state,(i,j),True,'x'):
            #                 result -= 6