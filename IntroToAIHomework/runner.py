import heapq

has_shield = False
inf_stone_x = inf_stone_y = 1000
game_type = None
visited = [[0 for _ in range(9)] for __ in range(9)]
heuristics_map = [[0 for i in range(9)] for j in range(9)]


class MyException(Exception):
    pass


my_map = [
[' ', ' ', 'P', 'S', ' ', ' ', ' ', ' ', ' '],    # 0
[' ', 'P', 'H', 'P', ' ', ' ', ' ', ' ', ' '],    # 1
[' ', ' ', 'P', ' ', ' ', ' ', ' ', ' ', ' '],    # 2
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],    # 3
['P', 'P', 'P', 'P', ' ', ' ', ' ', ' ', ' '],    # 4
['P', 'T', 'P', 'P', 'P', ' ', ' ', ' ', ' '],    # 5
['P', 'P', 'P', 'M', 'P', 'P', ' ', ' ', ' '],    # 6
[' ', ' ', 'P', 'P', 'P', ' ', ' ', ' ', ' '],    # 7
[' ', ' ', 'I', 'P', ' ', ' ', ' ', ' ', ' ']]    # 8
for i in range(9):
    for j in range(9):
        if my_map[i][j] == ' ':
            my_map[i][j] = ''

marvel_x = 1000
marvel_y = 1000
for i in range(9):
    mar_flag = 0
    for j in range(9):
        if my_map[i][j] == "M":
            marvel_x = j
            marvel_y = i
            mar_flag = 1
            break
    if mar_flag == 1:
        break


avoid_shield = True
with_shield = without_shield = float("inf")
def game_one():
    global game_type
    global has_shield
    global inf_stone_x, inf_stone_y
    global avoid_shield
    global with_shield, without_shield
    global visited
    for i in range(9):
        for j in range(9):
            # heuristic will be a Manhattan distance to the cell from infinity stone coordinates
            heuristics_map[i][j] = abs(inf_stone_y - i) + abs(inf_stone_x - j)
    # print(*heuristics_map, sep='\n')
    x = y = 0
    cell_queue = []
    try:
        make_move(heuristics_map[y][x], x, y, cell_queue)
    except MyException:
        pass
    avoid_shield = False
    cell_queue = []
    visited = [[0 for _ in range(9)] for __ in range(9)]
    try:
        make_move(heuristics_map[y][x], x, y, cell_queue)
    except MyException:
        pass
    min_path = min(with_shield, without_shield)
    if min_path > 10**4:
        print("e -1")
    else:
        print(f'e {min_path}')


shield_x = shield_y = 1000

def make_move(sum_of_functions, x, y, q):
    global has_shield, shield_x, shield_y
    global visited
    global avoid_shield
    global with_shield, without_shield
    visited[y][x] = 1
    if sum_of_functions > 10 ** 4:
        print("e -1")
        raise MyException
    if x == inf_stone_x and y == inf_stone_y:
        if avoid_shield:
            without_shield = sum_of_functions

            find_path_to_cell(x, y, 0, 0)
        else:
            with_shield = sum_of_functions
        # print(f"e {sum_of_functions}")
        raise MyException
    if x == shield_x and y == shield_y:
        has_shield = True
        q = []
        visited = [[0 for _ in range(9)] for __ in range(9)]

    visited[y][x] = 1
    # print("m", x, y)
    # u = input()
    # num_of_dangers = int(u)
    with open("runner_request.txt", 'w') as f:
        f.write(f'm {x} {y}\n')
    simulate_response()
    dangers = []
    with open("author_response.txt", 'r') as f:
        u = f.readline()
        num_of_dangers = int(u)
        dangers = []
        for i in range(num_of_dangers):
            x_c, y_c, danger_type = f.readline().split()
            x_c = int(x_c)
            y_c = int(y_c)
            dangers.append([x_c, y_c])
            if danger_type == "S":
                if not avoid_shield:
                    dangers.pop()
                shield_x = x_c
                shield_y = y_c
            elif danger_type == "I":
                dangers.pop()

    # for i in range(num_of_dangers):
    #     x_c, y_c, danger_type = input().split()
    #     x_c = int(x_c)
    #     y_c = int(y_c)
    #     dangers.append([x_c, y_c])
    #     if danger_type == "S":
    #         dangers.pop()
    #         shield_x = x_c
    #         shield_y = y_c
    #     elif danger_type == "I":
    #         dangers.pop()

    for pair in x_squares(x, y):
        x_c = pair[0]
        y_c = pair[1]
        if pair not in dangers and not visited[y_c][x_c]:
            heapq.heappush(q, [sum_of_functions - heuristics_map[y][x] + heuristics_map[y_c][x_c] + 1, x_c, y_c])
    if q:
        top_priority = heapq.heappop(q)
        new_f, new_x, new_y = top_priority
        while visited[new_y][new_x] and q:
            top_priority = heapq.heappop(q)
            new_f, new_x, new_y = top_priority
        # print(f'q = {[top_priority] + q}')
        find_path_to_cell(x, y, new_x, new_y)
        make_move(new_f, new_x, new_y, q)
    else:
        find_path_to_cell(x, y, 0, 0)
        raise MyException


def surrounding_squares(x, y):
    squares = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            x_c = x + i
            y_c = y + j
            if 0 <= x_c <= 8 and 0 <= y_c <= 8:
                squares.append([x_c, y_c])
    return squares


def x_squares(x, y):
    squares = []
    for i in [-1, 1]:
        if 0 <= x + i <= 8:
            squares.append([x + i, y])
        if 0 <= y + i <= 8:
            squares.append([x, y + i])
    return squares


def ear_squares(x, y):
    squares = []
    for i in [-2, 2]:
        if 0 <= x + i <= 8 and 0 <= y + i <= 8:
            squares.append([x + i, y + i])
        if 0 <= x + i <= 8 and 0 <= y - i <= 8:
            squares.append([x + i, y - i])
    return squares


def find_path_to_cell(source_x, source_y, destination_x, destination_y):
    global visited
    visited_cells = [[0 for _ in range(9)] for __ in range(9)]
    move_queue = []
    cell_parent = [[[100, 100] for _ in range(9)] for __ in range(9)]
    cell_parent[destination_y][destination_x] = [destination_x, destination_y]

    def bfs(x, y):

        global visited
        visited_cells[y][x] = 1
        if x == source_x and y == source_y:
            raise Exception
        for x_c, y_c in x_squares(x, y):
            if visited[y_c][x_c] and not visited_cells[y_c][x_c]:
                move_queue.append([x_c, y_c, x, y])
        if move_queue:
            new_x, new_y, parent_x, parent_y = move_queue.pop(0)

            while visited_cells[new_y][new_x] and move_queue:
                new_x, new_y, parent_x, parent_y = move_queue.pop(0)
            cell_parent[new_y][new_x] = [parent_x, parent_y]
            bfs(new_x, new_y)

    try:
        bfs(destination_x, destination_y)
    except:
        pass
    path_to_cell = []
    xc = source_x
    yc = source_y
    # print(*cell_parent, sep='\n', end='\n\n')
    # print(*visited_cells, sep="\n", end="\n\n")
    # print(*visited, sep="\n", end="\n\n")
    while not (xc == destination_x and yc == destination_y):
        path_to_cell.append(cell_parent[yc][xc])
        xc, yc = cell_parent[yc][xc]
    # print(f"Path from {source_x} {source_y} to {destination_x} {destination_y}:")
    # print(*path_to_cell)
    for x_c, y_c in path_to_cell:
        with open("runner_request.txt", 'w') as f:
            f.write(f'm {x_c} {y_c}\n')
        # print(f'mt {x_c} {y_c}')
        simulate_response()
        # print(f'm {x_c} {y_c}')
        # u = int(input())
        # for i in range(u):
        #     danger_info = input()


def captain_marvel_zone(x, y):
    arr = surrounding_squares(x, y)
    for i in [-2, 2]:
        if 0 <= x + i <= 8:
            arr.append([x + i, y])
        if 0 <= y + i <= 8:
            arr.append([x, y + i])
    return arr


x_prev = y_prev = 0


def simulate_response():
    global game_type
    global x_prev, y_prev
    global has_shield
    with open("runner_request.txt", 'r') as f:
        m, x, y = f.readline().split()
        x = int(x)
        y = int(y)
    for elem in ['H', 'M', 'T']:
        if elem in my_map[y][x]:
            print(f"You stepped at ({x}, {y})")
            print("Game over.")
            raise Exception
    if [x, y] not in x_squares(x_prev, y_prev) and [x, y] != [x_prev, y_prev]:
        print(f"Invalid move from ({x_prev}, {y_prev}) to ({x}, {y})")
        raise ZeroDivisionError
    x_prev = x
    y_prev = y
    if ('P' in my_map[y][x] and not has_shield) or [x, y] in captain_marvel_zone(marvel_x, marvel_y):
        print(f"You stepped at ({x}, {y})")
        print("Game over.")
        raise Exception
    dangers = []
    for pair in surrounding_squares(x, y):
        x_c = pair[0]
        y_c = pair[1]
        if my_map[y_c][x_c]:
            if my_map[y_c][x_c] == 'P' and has_shield and pair not in captain_marvel_zone(marvel_x, marvel_y):
                continue
            dangers.append([x_c, y_c, my_map[y_c][x_c]])
    if game_type == 2:
        for pair in ear_squares(x, y):
            if my_map[pair[1]][pair[0]]:
                if my_map[pair[0]][pair[1]] == 'P' and has_shield and pair not in captain_marvel_zone(marvel_x,
                                                                                                      marvel_y):
                    continue
                dangers.append([pair[0], pair[1], my_map[pair[1]][pair[0]]])
    with open("author_response.txt", 'w') as f:
        f.write(f'{len(dangers)}\n')
        for i in range(len(dangers)):
            pair = dangers[i]
            f.write(f'{pair[0]} {pair[1]} {pair[2]}\n')


def runner():
    global game_type
    global inf_stone_x, inf_stone_y
    game_type = int(input())
    inf_stone_x, inf_stone_y = map(int, input().split())
    game_one()
    return


runner()
