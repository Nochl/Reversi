
"""FIT1045 Algorithms and programming in Python, S1-2019 Assignment 1 - Reversi (Enoch Leow: 30600022) """

"""Part A -  New board, Print board, and Score Functions """


import copy


def new_board():                                                                                                        #defining new board as a list of lists with opening values
    board = [[0, 0, 0, 0, 0, 0, 0, 0],                                                                                  #0 - empty
             [0, 0, 0, 0, 0, 0, 0, 0],                                                                                  #1 - Player 1
             [0, 0, 0, 0, 0, 0, 0, 0],                                                                                  #2 - Player 2
             [0, 0, 0, 2, 1, 0, 0, 0],
             [0, 0, 0, 1, 2, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0]]
    return board


def print_board(board):                                                                                                 #print board function
    HLINE = '  +---+---+---+---+---+---+---+---+'
    for y in range(8):                                                                                                  #for each row
        print(HLINE)
        line = ""                                                                                                       #opening empty list for each row
        for x in range(8):                                                                                              #checks value of element and appends string accordingly
            line += "|"                                                                                                 #adds vertical line
            if board[y][x] == 1:
                line += " B "
            elif board[y][x] == 2:
                line += " W "
            elif board[y][x] == 0:
                line += "   "
        line += "|"
        print(y+1, line)                                                                                                #prints row references and the row itself
    print(HLINE)
    print('    a   b   c   d   e   f   g   h')                                                                          #prints column references


def score(board):                                                                                                       #score function
    white_count = 0                                                                                                     #setting initial variables
    black_count = 0
    for row in board:                                                                                                   #checks each element in board and counts number of pieces for each players
        for element in row:
            if element == 1:
                black_count += 1
            elif element == 2:
                white_count += 1
    return black_count, white_count                                                                                     #returns score in tuple in form (P1, P2)


"""Part B -  Enclosing, Valid moves and Next state Functions """


def enclosing(board, player, pos, direct):                                                                              #enclosing function checks if a move will enclose the opponents piece
    if player == 1:                                                                                                     #setting opposite opponent variables
        p_opposite = 2
    else:
        p_opposite = 1
    if board[pos[0]][pos[1]] != 0:                                                                                      #condition to check if position is already occupied
        return False
    if (pos[0]-direct[0]) < 0 or (pos[0]-direct[0]) > 7 or (pos[1]-direct[1]) < 0 or (pos[1]-direct[1]) > 7:            #checking if move in direction would be out of board
        return False
    if board[pos[0]-direct[0]][pos[1]-direct[1]] == p_opposite:                                                         #check if a move in direction will reach a opposite opponents piece
        pos_list = [pos[0], pos[1]]
        pos_list[0] -= direct[0]
        pos_list[1] -= direct[1]                                                                                        #moves the position in direction
        potato = pos_list[0] - direct[0]                                                                                #variable to test if next move will go out of rance
        tomato = pos_list[1] - direct[1]
        while board[pos_list[0]][pos_list[1]] == p_opposite and (0 <= potato <= 7) and (0 <= tomato <= 7):              #keeps moving in direction while in range of board
                pos_list[0] -= direct[0]
                pos_list[1] -= direct[1]
                potato = pos_list[0] - direct[0]
                tomato = pos_list[1] - direct[1]
        if board[pos_list[0]][pos_list[1]] == 0:
            return False
        elif board[pos_list[0]][pos_list[1]] == player:                                                                 #returns true if meets back with player (encloses the opposition)
            return True
    else:
        return False


def valid_moves(board, player):                                                                                         #valid moves function
    count = 0                                                                                                           #setting initial variables
    valid = []
    for row in range(len(board)):                                                                                       #iterates through each element in graph
        for ele in range(len(board[row])):
            for i in [(0, 0), (0, 1), (1, 0), (1, 1), (-1, 0), (-1, 1), (0, -1), (1, -1), (-1, -1)]:                    #checks if it encloses in any direction
                    if enclosing(board, player, (row, ele), i) is True:
                        if (row, ele) not in valid:
                            valid.append((row, ele))                                                                    #appends into valid list if its not already there
                            count += 1
    return valid                                                                                                        #returns list of players valid moves for a particular board


def next_state(board, player, pos):                                                                                     #next state function
    possible_moves = valid_moves(board, player)                                                                         #valid move variable
    if player == 1:
        p_opposite = 2
    else:
        p_opposite = 1
    if pos in possible_moves:
        next_board = copy.deepcopy(board)                                                                               #creates a complete (deep) copy of the current board
        next_board[pos[0]][pos[1]] = player                                                                             #places player piece on board if it is a valid move
        for i in [(0, 0), (0, 1), (1, 0), (1, 1), (-1, 0), (-1, 1), (0, -1), (1, -1), (-1, -1)]:
            pos_list = [pos[0], pos[1]]
            pos_list[0] -= i[0]
            pos_list[1] -= i[1]
            if (0 <= pos_list[0] <= 7) and (0 <= pos_list[1] <= 7):                                                     #check if position is within the board
                if board[pos_list[0]][pos_list[1]] == p_opposite:
                    potato = pos_list[0] - i[0]                                                                         #out of range checking variables
                    tomato = pos_list[1] - i[1]
                    while board[pos_list[0]][pos_list[1]] == p_opposite and (0 <= potato <= 7) and (0 <= tomato <= 7):  #moves position in direction until it reaches a blank / player piece
                        pos_list[0] -= i[0]
                        pos_list[1] -= i[1]
                        potato = pos_list[0] - i[0]
                        tomato = pos_list[1] - i[1]
                    if board[pos_list[0]][pos_list[1]] == player:                                                       #checks if non-opposition position is the player's piece
                        pos_list[0] += i[0]
                        pos_list[1] += i[1]
                        next_board[pos_list[0]][pos_list[1]] = player
                        pos_list[0] += i[0]
                        pos_list[1] += i[1]
                        while board[pos_list[0]][pos_list[1]] == p_opposite:                                            #reverses back whilst replacing the position with the players piece
                            next_board[pos_list[0]][pos_list[1]] = player
                            pos_list[0] += i[0]
                            pos_list[1] += i[1]
        return next_board                                                                                               #returns the new board
    else:
        return False


def position(string):                                                                                                   #position translation function
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h"]                                                                 #list of valid letter column names
    if string == "":                                                                                                    #checks if input is blank
        return
    if string[0] == "q":                                                                                                #bypasses if input is q
        return string
    if len(string) != 2:                                                                                                #ensures a 2 length inpuc
        return
    if string[0] not in alphabet:                                                                                       #checks if letter is valid
        return
    row = (int(string[1])-1)                                                                                            #takes board reference and turns it into a its proper index
    column = alphabet.index(string[0])                                                                                  #turns letter into its proper idndex
    output = (row, column)                                                                                              #returning format
    if (0 <= output[0] <= 7) and (0 <= output[1] <= 7):
       return output
    else:
        return


def run_two_players():                                                                                                  #two player function
    print("Welcome to Reversi: Player 1 => Black   Player 2 => White")
    quit = 0
    current_board = new_board()                                                                                         #sets initial board as new board
    print_board(current_board)                                                                                          #prints board
    p_count = 0
    print("Press enter to start the game")
    input()
    while (len(valid_moves(current_board, 1))+len(valid_moves(current_board, 2)) > 0) and quit == 0:                    #loops turns until neither player has any moves and quit variable not greater than 0
        p_count += 1                                                                                                    #player count to record whose turn it is
        if p_count%2 == 1:
            player = 1
        else:
            player = 2
        if len(valid_moves(current_board, player)) > 0:                                                                 #checks if the player has any moves
            valid = valid_moves(current_board, player)
            valid.append('q')
            move_to = position(input("Player "+str(player)+" move: "))                                                  #takes players move input and translates it to an index
            while move_to not in valid:                                                                                 #re-try input until a valid input is given
                print("Invalid move, please try again")
                move_to = position(input("Player "+str(player)+" move: "))
            if move_to == "q":                                                                                          #finishes game by initialising quit variable
                quit += 1
            elif move_to in valid:                                                                                      #if move is valid, the board = the next board state
                current_board = next_state(current_board, player, move_to)
                print_board(current_board)                                                                              #prints board
        else:
            print("no moves, next players turn")                                                                        #switches player if player has no valid moves
    print("==============Game Over==============")
    print("Score P1/P2 ==> "+str(score(current_board)))                                                                 #prints score
    if (score(current_board))[0] == (score(current_board))[1]:                                                          #prints winning player or draw
        print("Draw")
    elif (score(current_board))[0] > (score(current_board))[1]:
        print("Player 1 Wins!")
    elif (score(current_board))[0] < (score(current_board))[1]:
        print("Player 2 Wins!")


def run_single_player():                                                                                                #single player algorithm
    print("Welcome to Reversi: Player 1 => Black   Computer => White")
    quit = 0
    current_board = new_board()                                                                                         #sets initial board as new board
    print_board(current_board)                                                                                          #prints board
    p_count = 0
    print("Press enter to start the game")
    input()
    while (len(valid_moves(current_board, 1))+len(valid_moves(current_board, 2)) > 0) and quit == 0:                    #loops turns until neither player has any moves and quit variable not greater than 0
        p_count += 1                                                                                                    #player count to record whose turn it is
        if p_count%2 == 1:
            player = 1
        else:
            player = 2
            input("Press the Enter key to see computers move")
        if player == 1:                                                                                                 #if its player 1 (human) same code as above in 'run_two_players()'
            if len(valid_moves(current_board, player)) > 0:
                valid = valid_moves(current_board, player)
                valid.append('q')
                move_to = position(input("Player "+str(player)+" move: "))
                while move_to not in valid:
                    print("Invalid move, please try again")
                    move_to = position(input("Player "+str(player)+" move: "))
                if move_to == "q":
                    quit += 1
                elif move_to in valid:
                    current_board = next_state(current_board, player, move_to)
                    print_board(current_board)
            else:
                print("no moves, next players turn")
        else:
            if len(valid_moves(current_board, player)) > 0:                                                             #if its player 2 (bot)
                valid = valid_moves(current_board, player)                                                              #generates a list of valid moves as variable 'valid'
                highest_move = (valid[0], (score(next_state(current_board, player, valid[0])))[1])                      #sets initial highest move as valid[0]
                for i in valid:                                                                                         #iterates over all valid moves
                    this_score = score(next_state(current_board, player, i))                                            #generates score for the valid move
                    if this_score[1] > highest_move[1]:                                                                 #assigns i in valid has highest if its score is greater than previously assigned
                        highest_move = (i, (score(next_state(current_board, player, i)))[1])
                current_board = next_state(current_board, player, highest_move[0])                                      #generate the next board with using the position with the highest score value
                print_board(current_board)                                                                              #prints next board
            else:
                print("no moves, next players turn")                                                                    #switches player if player has no valid moves

    print("==============Game Over==============")
    print("Score P1/P2 ==> "+str(score(current_board)))                                                                 #prints score
    if (score(current_board))[0] == (score(current_board))[1]:                                                          #prints winning player or draw
        print("Draw")
    elif (score(current_board))[0] > (score(current_board))[1]:
        print("Player 1 Wins!")
    elif (score(current_board))[0] < (score(current_board))[1]:
        print("Computer Wins!")


def run_no_player():
    print("Welcome to Reversi: Computer 1 => Black   Computer 2 => White")                                              #just for fun Bot vs Bot function
    quit = 0
    current_board = new_board()
    print_board(current_board)
    p_count = 0
    print("Press enter to start the Bots game")
    input()
    while (len(valid_moves(current_board, 1))+len(valid_moves(current_board, 2)) > 0) and quit == 0:
        p_count += 1
        if p_count % 2 == 1:
            player = 1
        else:
            player = 2
        if len(valid_moves(current_board, player)) > 0:
            valid = valid_moves(current_board, player)
            score_place = 0
            if player == 2:
                score_place = 1
            highest_move = (valid[0], (score(next_state(current_board, player, valid[0])))[score_place])
            for i in valid:
                this_score = score(next_state(current_board, player, i))
                if this_score[score_place] > highest_move[1]:
                    highest_move = (i, (score(next_state(current_board, player, i)))[score_place])
            current_board = next_state(current_board, player, highest_move[0])
            print_board(current_board)
            print("Player "+str(player)+"'s Move")
            print(" ")
        else:
            print("no moves, next players turn")
    print("==============Game Over==============")
    print("Score P1/P2 ==> "+str(score(current_board)))
    if (score(current_board))[0] == (score(current_board))[1]:
        print("Draw")
    elif (score(current_board))[0] > (score(current_board))[1]:
        print("Player 1 Wins!")
    elif (score(current_board))[0] < (score(current_board))[1]:
        print("Player 2 Wins!")


def play(mode):                                                                                                         #just for fun, game mode selector function
    if mode == "1p":
        run_single_player()
    elif mode == "2p":
        run_two_players()
    elif mode == "bots":
        run_no_player()
    else:
        print("Not a valid game mode, please try again:")
        mode = input()
        play(mode)


mode = input("Play ==> 1p, 2p or bots: ")

play(mode)                                                                                                              #initialises game

