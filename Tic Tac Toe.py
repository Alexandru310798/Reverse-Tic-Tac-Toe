import math
import datetime
from itertools import permutations
from tkinter import *
from tkinter.messagebox import showinfo

available_positions = [11, 12, 13, 21, 22, 23, 31, 32, 33]  # the positions of the table

root = Tk()  # root of the GUI
button_1_1 = Button(root, width=20, height=10, command=lambda: define_sign(11))  # buttons for the GUI
button_1_2 = Button(root, width=20, height=10, command=lambda: define_sign(12))
button_3_3 = Button(root, width=20, height=10, command=lambda: define_sign(33))
button_3_2 = Button(root, width=20, height=10, command=lambda: define_sign(32))
button_2_3 = Button(root, width=20, height=10, command=lambda: define_sign(23))
button_2_2 = Button(root, width=20, height=10, command=lambda: define_sign(22))
button_3_1 = Button(root, width=20, height=10, command=lambda: define_sign(31))
button_2_1 = Button(root, width=20, height=10, command=lambda: define_sign(21))
button_1_3 = Button(root, width=20, height=10, command=lambda: define_sign(13))

# default values
AI_wins = 0
player_wins = 0
player = []  # player moves
AI = []  # AI moves
AI_turn = False
AI_sign = 'O'
player_sign = 'X'
alphabeta_choice = 0


def lost(list_of_positions=[]):  # This is the function to verify if someone lose( win in the regular Tic Tac Toe)
    if list_of_positions.count(11) > 0 and list_of_positions.count(12) > 0 and list_of_positions.count(13) > 0:
        return True
    if list_of_positions.count(21) > 0 and list_of_positions.count(22) > 0 and list_of_positions.count(23) > 0:
        return True
    if list_of_positions.count(31) > 0 and list_of_positions.count(32) > 0 and list_of_positions.count(33) > 0:
        return True
    if list_of_positions.count(11) > 0 and list_of_positions.count(21) > 0 and list_of_positions.count(31) > 0:
        return True
    if list_of_positions.count(12) > 0 and list_of_positions.count(22) > 0 and list_of_positions.count(32) > 0:
        return True
    if list_of_positions.count(13) > 0 and list_of_positions.count(23) > 0 and list_of_positions.count(33) > 0:
        return True
    if list_of_positions.count(11) > 0 and list_of_positions.count(22) > 0 and list_of_positions.count(33) > 0:
        return True
    if list_of_positions.count(13) > 0 and list_of_positions.count(22) > 0 and list_of_positions.count(31) > 0:
        return True
    return False


def winner(
        list_of_positions=[]):  # being a Reverse Tic Tac Toe, the winning rule, is the opposite of the regular Tic Tac Toe
    valid = 0
    if not available_positions:
        valid += 1
    if not (list_of_positions.count(11) > 0 and list_of_positions.count(12) > 0 and list_of_positions.count(13) > 0):
        valid += 1
    if not (list_of_positions.count(21) > 0 and list_of_positions.count(22) > 0 and list_of_positions.count(23) > 0):
        valid += 1
    if not (list_of_positions.count(31) > 0 and list_of_positions.count(32) > 0 and list_of_positions.count(33) > 0):
        valid += 1
    if not (list_of_positions.count(11) > 0 and list_of_positions.count(21) > 0 and list_of_positions.count(31) > 0):
        valid += 1
    if not (list_of_positions.count(12) > 0 and list_of_positions.count(22) > 0 and list_of_positions.count(32) > 0):
        valid += 1
    if not (list_of_positions.count(13) > 0 and list_of_positions.count(23) > 0 and list_of_positions.count(33) > 0):
        valid += 1
    if not (list_of_positions.count(11) > 0 and list_of_positions.count(22) > 0 and list_of_positions.count(33) > 0):
        valid += 1
    if not (list_of_positions.count(13) > 0 and list_of_positions.count(22) > 0 and list_of_positions.count(31) > 0):
        valid += 1

    if valid == 9:  # If all "losing" rules are false, the function will return True
        return True
    return False


def minimax(positions, depth, artificial_intelligence, a_i_positions=[], player_positions=[]):
    if not positions:
        if winner(a_i_positions):  # if the AI can win in this state, it'll receive 10 pts - depth
            return dict(position=None, score=10 - depth)
        elif winner(player_positions):  # if the AI lose in this state, it'll receive - 10 pts - depth
            return dict(position=None, score=-10 - depth)
        else:
            return dict(position=None,
                        score=0 - depth)  # if none of them win in this state, the AI will receive 0 pts - depth

    if artificial_intelligence:  # this search is for the AI, so search for the max value
        best = {'position': None, 'score': (-1) * math.inf}
        for possible_move in positions:
            positions.remove(possible_move)
            a_i_positions.append(possible_move)
            value = minimax(positions, depth + 1, False, a_i_positions, player_positions)
            value['position'] = possible_move
            if best['score'] < value['score']:
                best = value
            a_i_positions.remove(possible_move)
            positions.append(possible_move)

    else:  # this search is for the player, so the AI will try to find the min value
        best = {'position': None, 'score': math.inf}
        for possible_move in positions:
            player.append(possible_move)
            positions.remove(possible_move)
            value = minimax(positions, depth + 1, True, a_i_positions, player_positions)
            value['position'] = possible_move
            if best['score'] > value['score']:
                best = value
            positions.append(possible_move)
            player.remove(possible_move)
    return best  # the best returned will be :{'position': x, 'score': maximum available}, so we will use that position


def alphabeta(positions, depth, artificial_intelligence, a_i_positions=[], player_positions=[], alpha=(-1) * math.inf,
              beta=math.inf):  # the alpha beta prunning is same as minimax, except that here will take care of 2 new variables
    if not positions:
        if winner(a_i_positions):
            return dict(position=None, score=10 - depth)
        elif winner(player_positions):
            return dict(position=None, score=-10 - depth)
        else:
            return dict(position=None, score=0 - depth)

    if artificial_intelligence:
        best = {'position': None, 'score': (-1) * math.inf}
        for possible_move in positions:
            positions.remove(possible_move)
            a_i_positions.append(possible_move)
            value = alphabeta(positions, depth + 1, False, a_i_positions, player_positions, alpha, beta)
            value['position'] = possible_move
            if best['score'] < value['score']:
                best = value
            a_i_positions.remove(possible_move)
            positions.append(possible_move)
            alpha = max(alpha,
                        value['score'])  # if the alpha conditions will be true, will stop searching for useless values
            if alpha >= beta:
                break


    else:
        best = {'position': None, 'score': math.inf}
        for possible_move in positions:
            player.append(possible_move)
            positions.remove(possible_move)
            value = alphabeta(positions, depth + 1, True, a_i_positions, player_positions, alpha, beta)
            value['position'] = possible_move
            if best['score'] > value['score']:
                best = value
            positions.append(possible_move)
            player.remove(possible_move)
            beta = min(beta, value['score'])
            if beta <= alpha:
                break

    return best


def select_algorithm(positions, depth, artificial_intelligence, a_i_positions=[], player_positions=[],
                     alphabeta_choice=False):  # this function is used to select wich algorithm we will compete against
    if alphabeta_choice:
        return alphabeta(positions, depth, True, a_i_positions, player_positions, (-1) * math.inf, math.inf)
    return minimax(positions, depth, True, a_i_positions, player_positions)


def define_sign(number, sign='X'):  # this is the click function of the GUI Buttons
    global player, AI, AI_wins, player_wins
    global AI_turn, alphabeta_choice
    time_move_start = datetime.datetime.now()
    if available_positions.count(number) == 0:  # if no more moves, end game
        return
    if AI_turn:  # determine who is to move
        sign = AI_sign
    else:
        sign = player_sign
    if number == 11:  # for every button, we'll check who is to move an will add the position in his array
        if AI_turn:
            AI.append(number)
        else:
            player.append(number)
        button_1_1.config(text=sign)
    if number == 12:
        if AI_turn:
            AI.append(number)
        else:
            player.append(number)
        button_1_2.config(text=sign)
    if number == 13:
        if AI_turn:
            AI.append(number)
        else:
            player.append(number)
        button_1_3.config(text=sign)
    if number == 21:
        if AI_turn:
            AI.append(number)
        else:
            player.append(number)
        button_2_1.config(text=sign)
    if number == 22:
        if AI_turn:
            AI.append(number)
        else:
            player.append(number)
        button_2_2.config(text=sign)
    if number == 23:
        if AI_turn:
            AI.append(number)
        else:
            player.append(number)
        button_2_3.config(text=sign)
    if number == 31:
        if AI_turn:
            AI.append(number)
        else:
            player.append(number)
        button_3_1.config(text=sign)
    if number == 32:
        if AI_turn:
            AI.append(number)
        else:
            player.append(number)
        button_3_2.config(text=sign)
    if number == 33:
        if AI_turn:
            AI.append(number)
        else:
            player.append(number)
        button_3_3.config(text=sign)

    available_positions.remove(number)  # we'll remove the position from available position because it was taken
    AI_turn = not AI_turn

    if AI_turn:  # if we moved, now it's AI time to move, and it'll choose
        AI_move = select_algorithm(available_positions, 0, True, AI, player, alphabeta_choice)['position']
        define_sign(AI_move)
        time_move_done = datetime.datetime.now()
        showinfo("AI time to move", "AI moved in " + str(
            time_move_done - time_move_start))  # to calculate the time to move, I used the started time - the time  the move was done

    if lost(player):  # verify if someone has lost, to can stop the game
        showinfo("Game result", "Player has lost, AI has won")
        AI_wins += 1
    elif lost(AI):
        showinfo("Game result", "AI has lost, Player has won")
        player_wins += 1
    elif not (available_positions or lost(player) or lost(AI)):
        showinfo("Game result", "It's a draw")


def reverse_sign(sign):  # the reverse sign
    if sign == 'X':
        return '0'
    else:
        return 'X'


def draw_table(artificial=[], artificial_sign='X', player1=[],
               player1_sign='O'):  # the drawing table function  for the console playing
    table = []
    for i in range(34):
        if artificial.count(i):
            table.append(artificial_sign)
        elif player1.count(i):
            table.append(player1_sign)
        else:
            table.append('_')

    string = ""
    for i in range(11, 14):
        string = string + "  " + table[i]
    print(string)
    string = ""
    for i in range(21, 24):
        string = string + "  " + table[i]
    print(string)
    string = ""
    for i in range(31, 34):
        string = string + "  " + table[i]
    print(string)


def play(positions, artificial, player1):  # playing console function
    global AI_sign, player_sign, alphabeta_choice
    print("If you want to exit the game, please insert an invalid number")  # if you want to end the game
    while positions or winner(player1) or winner(artificial):  # while we can still play, we play

        time_move_start = datetime.datetime.now()
        your_move = int(input("Your move: "))
        if available_positions.count(your_move) == 0:  # check 'till the move is valid
            while available_positions.count(your_move) == 0:
                exit_option = input("If you want to close the game, just type 'exit' :")
                if exit_option == "exit":
                    exit(0)
                your_move = int(input("Your move was already taken, please choose another: "))
        time_move_done = datetime.datetime.now()  # to calculate the time to move, I used the started time - the time the move was done
        print("You moved in " + str(time_move_done - time_move_start))
        player1.append(your_move)  # adding the position
        positions.remove(your_move)  # remove the position

        if not positions:  # if that was the last available position
            break

        time_move_start = datetime.datetime.now()
        artificial_move = select_algorithm(positions, 0, True, artificial, player1, alphabeta_choice)[
            'position']  # here we choose the search algorithm we are facing
        time_move_done = datetime.datetime.now()
        print("AI moved in " + str(
            time_move_done - time_move_start))  # to calculate the time to move, I used the started time - the time the move was done
        print("AI move is: " + str(artificial_move))
        artificial.append(artificial_move)
        positions.remove(artificial_move)

        draw_table(artificial, AI_sign, player1, player_sign)  # show me how the table looks like
        if lost(player1):
            print("Player has lost, AI has won")  # determine the winner
            exit(0)
        elif lost(artificial):
            print("AI has lost, Player has won")
            exit(0)

            # the last check
    if lost(player1):
        print("Player has lost, AI has won")
    elif lost(AI):
        print("AI has lost, Player has won")
    else:
        print("It's a draw")
    draw_table(artificial, AI_sign, player1, player_sign)


if __name__ == "__main__":

    # You'll have to choose how to play
    print("You will compete against:\n 1) MiniMax Algorithm \n 2) AlphaBeta Pruning\n your choice is( 1 / 2): ")
    alphabeta_choice = int(input())
    player_sign = input("Your sign is( X/ 0): ")
    AI_sign = reverse_sign(player_sign)
    if alphabeta_choice == 1:
        print("You will compete against the MiniMax Algorithm and your sign is: " + player_sign)
    else:
        print("You will compete against the Alpha Beta Prunning Algorithm and your sign is: " + player_sign)

    console_line_or_GUI = input("The way to play: console/ GUI: ")
    i = 0
    textPlayer = "Player : " + player_sign + "  Wins: " + str(player_wins) + " "
    label_1 = Label(root, text=textPlayer, font="times 15")
    label_1.grid(row=0, column=1)
    textAI = "AI : " + AI_sign + "  Wins: " + str(AI_wins) + "  "
    label_2 = Label(root, text=textAI, font="times 15")
    label_2.grid(row=0, column=2)
    button_1_1.grid(row=1, column=1)
    button_1_2.grid(row=1, column=2)
    button_1_3.grid(row=1, column=3)
    button_2_1.grid(row=2, column=1)
    button_2_2.grid(row=2, column=2)
    button_2_3.grid(row=2, column=3)
    button_3_1.grid(row=3, column=1)
    button_3_2.grid(row=3, column=2)
    button_3_3.grid(row=3, column=3)
    player.clear()
    AI.clear()

    if console_line_or_GUI == "GUI":
        while available_positions:
            root.mainloop()
    else:
        play(available_positions, AI, player)
