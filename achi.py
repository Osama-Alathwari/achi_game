import tkinter as tk

positions_adjacency = {
    (0, 0): [(0, 1), (1, 0), (1, 1)],
    (0, 1): [(0, 0), (0, 2), (1, 1)],
    (0, 2): [(0, 1), (1, 2), (1, 1)],
    (1, 0): [(0, 0), (2, 0), (1, 1)],
    (1, 1): [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
    (1, 2): [(0, 2), (2, 2), (1, 1)],
    (2, 0): [(1, 0), (2, 1), (1, 1)],
    (2, 1): [(2, 2), (2, 0), (1, 1)],
    (2, 2): [(1, 2), (2, 1), (1, 1)],
}

player = "black"
com = "yellow"
white = "white"
playerCounter = 4
position_of_picked_button = (-1, -1)
player_score = {com: 1, player: -1}
pick = True  # To prevent player from moving more than one piece

####################################


def create_board(frame):
    # Creating 3x3 board
    board = [[None] * 3 for _ in range(3)]

    for i in range(3):
        for j in range(3):
            cell = tk.Button(
                frame,
                bg="white",
                height=5,
                width=10,
                command=lambda i=i, j=j: click(i, j, board, frame),
            )
            cell.grid(row=i, column=j, padx=10, pady=10)
            board[i][j] = cell  # type: ignore
    return board


####################################


def reset_board(board, frame):
    global playerCounter, position_of_picked_button, pick
    for i in range(3):
        for j in range(3):
            board[i][j]["bg"] = "white"
            board[i][j].config(state="normal")

    label["text"] = "Achi Game"
    label["bg"] = "white"
    playerCounter = 4
    position_of_picked_button = (-1, -1)
    pick = True


####################################


root = tk.Tk()
root.title("Achi Game")

label = tk.Label(text="", width=22)
label.pack(side="top")

label = tk.Label(text="Achi Game", bg="white", font=("consolas", 20), width=22)
label.pack(side="top")

reset_button = tk.Button(
    root, text="Reset", bg="gray", command=lambda: reset_board(board, frame)
)
reset_button.pack(side="bottom", fill="x", padx=10, pady=10)


frame = tk.Frame(root, bg="white")
frame.pack(padx=10, pady=10)
board = create_board(frame)
####################################


def click(x, y, board, frame):
    w, flag = user_click_conditions((x, y), board)
    print(f"player counter {playerCounter}")
    if flag:
        print("w is not none", w)
        if not (check_winer(w)):
            (sc, white_pos, com_pos) = alphabeta_run(board)
            if sc:
                w = change_color(white, white_pos, board)
                w = change_color(com, com_pos, board)
                check_winer(w)
            else:
                print("Game Over")
        else:
            return False

    else:
        print("#" * 50)
        print("waiting for player to finish his move")
        print("#" * 50)


def alphabeta_run(borad):
    comCounter = 0
    for i in range(3):
        for j in range(3):
            if board[i][j]["bg"] == com:
                comCounter += 1

    if comCounter == 4:
        return alphabeta_move2(borad)
    else:
        return alphabeta_move(borad)


def alphabeta_move(borad):
    scores = []
    pos = []

    alpha = -10
    beta = 10

    for x in range(3):
        for y in range(3):
            if borad[x][y]["bg"] == "white":
                borad[x][y]["bg"] = com
                sc = alphabeta(borad, False, alpha, beta)

                if alpha < sc:
                    alpha = sc

                scores.append(sc)
                pos.append((x, y))
                borad[x][y]["bg"] = "white"

    index = scores.index(max(scores))
    sce = scores[index]
    p = pos[index]
    return (scores, p, p)


def get_adjacency_position(x, y, board):
    empty_nodes = []
    print(f"empty nodes before for {x,y} : {empty_nodes}")

    for empty_node in positions_adjacency[(x, y)]:
        i, j = empty_node
        if board[i][j]["bg"] == white:
            print(f"empty node : {empty_node}")
            empty_nodes.append(empty_node)
        else:
            print(f"full node : {empty_node}")

    print(f"empty nodes after for {x,y}: {empty_nodes}")
    return empty_nodes


def alphabeta_move2(board):
    scores = []
    next_pos = []
    old_pos = []

    alpha = -10
    beta = 10

    player_positions = {}
    com_positions = {}

    for x in range(3):
        for y in range(3):
            if board[x][y]["bg"] == com:
                empty_adjacent_positions = get_adjacency_position(x, y, board)
                com_positions[(x, y)] = empty_adjacent_positions
            elif board[x][y]["bg"] == player:
                empty_adjacent_positions = get_adjacency_position(x, y, board)
                player_positions[(x, y)] = empty_adjacent_positions
            else:
                continue

    print(f"com pos : {com_positions}")
    print(f"player pos : {player_positions}")
    for k, v in com_positions.items():
        if v != []:
            sc = alphabeta2(
                board,
                com_positions,
                player_positions,
                list(com_positions.keys()),
                list(player_positions.keys()),
                True,
                alpha,
                beta,
            )
            print(sc)
            if alpha < sc:
                alpha = sc

            scores.append(sc)
            old_pos.append(k)
            next_pos.append(v[0])

    index = scores.index(max(scores))
    sce = scores[index]
    com_pos = next_pos[index]
    white_pos = old_pos[index]
    return (scores, white_pos, com_pos)


def alphabeta2(
    board,
    com_positions,
    player_positions,
    com_positions_temp,
    player_positions_temp,
    ismax,
    alpha,
    beta,
):
    score = score_fun()

    if score != None:
        return score

    if ismax:
        return alphabeta_max2(
            board,
            com_positions,
            player_positions,
            com_positions_temp,
            player_positions_temp,
            alpha,
            beta,
        )

    else:
        return alphabeta_min2(
            board,
            com_positions,
            player_positions,
            com_positions_temp,
            player_positions_temp,
            alpha,
            beta,
        )


def alphabeta_max2(
    board,
    com_positions,
    player_positions,
    com_positions_temp,
    player_positions_temp,
    alpha,
    beta,
):
    best = -10
    print(f"com_positions_temp : {com_positions_temp}")
    if com_positions_temp != []:
        c = com_positions_temp.pop()
        x, y = c
        adj = get_adjacency_position(x, y, board)
        if adj != []:
            i, j = adj[0]
            board[x][y]["bg"] = white
            board[i][j]["bg"] = com
            sc = alphabeta2(
                board,
                com_positions,
                player_positions,
                com_positions_temp,
                player_positions_temp,
                False,
                alpha,
                beta,
            )

            board[x][y]["bg"] = com
            board[i][j]["bg"] = white

            if sc > best:
                best = sc

            if best > alpha:
                alpha = best

            if alpha >= beta:
                return best

    return best


def alphabeta_min2(
    board,
    com_positions,
    player_positions,
    com_positions_temp,
    player_positions_temp,
    alpha,
    beta,
):
    best = 10
    print(f"player_position_temp : {player_positions_temp}")
    if player_positions_temp != []:
        p = player_positions_temp.pop(0)
        x, y = p
        adj = get_adjacency_position(x, y, board)
        if adj != []:
            i, j = adj[0]
            board[x][y]["bg"] = white
            board[i][j]["bg"] = player
            sc = alphabeta2(
                board,
                com_positions,
                player_positions,
                com_positions_temp,
                player_positions_temp,
                True,
                alpha,
                beta,
            )

            board[x][y]["bg"] = player
            board[i][j]["bg"] = white

            if sc < best:
                best = sc

            if best < beta:
                beta = best

            if beta <= alpha:
                return best

    return best


def alphabeta(borad, ismax, alpha, beta):
    score = score_fun()

    if score != None:
        return score

    if ismax:
        return alphabeta_max(borad, alpha, beta)

    else:
        return alphabeta_min(borad, alpha, beta)


def alphabeta_max(borad, alpha, beta):
    best = -10
    for x in range(3):
        for y in range(3):
            if borad[x][y]["bg"] == "white":
                borad[x][y]["bg"] = com

                sc = alphabeta(borad, False, alpha, beta)

                borad[x][y]["bg"] = "white"
                if sc > best:
                    best = sc

                if best > alpha:
                    alpha = best

                if alpha >= beta:
                    return best

    return best


def alphabeta_min(borad, alpha, beta):
    best = 10
    for x in range(3):
        for y in range(3):
            if borad[x][y]["bg"] == "white":
                borad[x][y]["bg"] = player
                sc = alphabeta(borad, True, alpha, beta)
                borad[x][y]["bg"] = "white"

                if sc < best:
                    best = sc

                if best < beta:
                    beta = best

                if beta <= alpha:
                    return best

    return best


def user_click_conditions(pos, board):
    global pick, playerCounter, position_of_picked_button
    x, y = pos
    flag = True
    if board[x][y]["bg"] == white:
        if playerCounter > 0:
            if position_of_picked_button[0] == -1:
                print(f"position of picked item : {position_of_picked_button}")
                playerCounter -= 1
                flag = True
                position_of_picked_button = (-1, -1)
                print(f"position after : {position_of_picked_button}")
                return change_color(player, pos, board), flag
            elif position_of_picked_button != pos:
                if check_adjacency_nodes(position_of_picked_button, pos):
                    print(f"position of picked item : {position_of_picked_button}")
                    playerCounter -= 1
                    flag = True
                    position_of_picked_button = (-1, -1)
                    print(f"position after : {position_of_picked_button}")
                    return change_color(player, pos, board), flag
                else:
                    return None, False
            else:
                return None, False
        else:
            if position_of_picked_button[0] != -1:
                if check_adjacency_nodes(position_of_picked_button, pos):
                    playerCounter += 1
                    flag = True
                    position_of_picked_button = (-1, -1)
                    return change_color(player, pos, board), flag
                else:
                    return None, False
            else:
                return None, False

    elif board[x][y]["bg"] == player:
        if playerCounter == 0:
            if position_of_picked_button[0] == -1:
                board[x][y]["bg"] = white
                playerCounter += 1
                position_of_picked_button = pos
                print(f"position of picked item : {position_of_picked_button}")
                flag = False
                return None, flag
            else:
                return None, False
        else:
            return None, False

    else:
        flag = False
        return None, flag


def change_color(color, pos, board):
    x, y = pos
    board[x][y]["bg"] = color
    return score_fun()


def change(pos):
    global playerCounter, player, pick, position_of_picked_button
    x, y = pos
    flag = False  # To prevent computer from playing while the player is moving his position
    if board[x][y]["bg"] == "white":
        flag = True
        if playerCounter > 0:
            board[x][y]["bg"] = player
            playerCounter -= 1
            pick = True

        else:
            label["text"] = "You are out  of pieces"
            label["bg"] = "red"

    elif board[x][y]["bg"] == player:
        if playerCounter <= 0:
            if pick:
                flag = False
                board[x][y]["bg"] = "white"
                playerCounter += 1
                label["text"] = "Achi Game"
                label["bg"] = "white"
                pick = False
                print(f"Player Counter : {playerCounter}")
                position_of_picked_button = (x, y)

    else:
        label["text"] = "You Can't choose this position"
        label["bg"] = "red"
        flag = False

    return (score_fun(), flag)


def score_fun():
    for i in range(3):
        if (
            board[i][0]["bg"] == board[i][1]["bg"] == board[i][2]["bg"]
            and board[i][0]["bg"] != "white"
        ):
            pl = board[i][0]["bg"]
            return player_score[pl]

    for i in range(3):
        if (
            board[0][i]["bg"] == board[1][i]["bg"] == board[2][i]["bg"]
            and board[2][i]["bg"] != "white"
        ):
            pl = board[0][i]["bg"]
            return player_score[pl]

    if (
        board[0][0]["bg"] == board[1][1]["bg"] == board[2][2]["bg"]
        and board[2][2]["bg"] != "white"
    ):
        pl = board[0][0]["bg"]
        return player_score[pl]

    if (
        board[2][0]["bg"] == board[1][1]["bg"] == board[0][2]["bg"]
        and board[0][2]["bg"] != "white"
    ):
        pl = board[0][2]["bg"]
        return player_score[pl]

    is_tie = sum(1 for x in range(3) for y in range(3) if board[x][y]["bg"] == "white")
    if is_tie == 0:
        return 0


def check_adjacency_nodes(cur_pos, next_pos):
    global positions_adjacency
    if next_pos in positions_adjacency[cur_pos]:
        return True

    else:
        return False


def check_winer(w):
    if w is not None:
        if w == 1:
            label.config(text=("Computer won"))
            label.config(background="red")
            result_style("red", com)
        elif w == -1:
            label.config(background="green")
            label.config(text=("YOU won"))
            result_style("green", player)
        else:
            label.config(background="#ff7301")
            label.config(text=("Tie!"))
            result_style("#ff7301", "white")
        return True
    else:
        return False


def result_style(color, player):
    for x in range(3):
        for y in range(3):
            board[x][y].config(state="disabled")
            if board[x][y]["bg"] == player:
                board[x][y].config(bg=color)  # type: ignore


root.mainloop()
