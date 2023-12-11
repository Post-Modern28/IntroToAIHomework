from queue import PriorityQueue


has_shield = False
inf_stone_x = inf_stone_y = 1000
game_type = None
visited = [[0 for _ in range(9)] for __ in range(9)]
heuristics_map = [[0 for i in range(9)] for j in range(9)]
shield_allowed = False
with_shield = without_shield = float("inf")


class MyException(Exception):
    pass


def play_game():
    global game_type
    global has_shield
    global inf_stone_x, inf_stone_y
    global shield_allowed
    global with_shield, without_shield
    global visited
    for i in range(9):
        for j in range(9):
            # heuristic will be a Manhattan distance to the cell from infinity stone coordinates
            heuristics_map[i][j] = abs(inf_stone_y - i) + abs(inf_stone_x - j)
    x = y = 0
    A_star_queue = PriorityQueue()
    # firstly check the map, avoiding the shield
    try:
        make_move(heuristics_map[y][x], x, y, A_star_queue)
    except MyException:
        pass
    # then check the map with, being permitted to use shield
    shield_allowed = True
    A_star_queue = PriorityQueue()
    visited = [[0 for _ in range(9)] for __ in range(9)]
    try:
        make_move(heuristics_map[y][x], x, y, A_star_queue)
    except MyException:
        pass
    min_path = min(with_shield, without_shield)
    if min_path > 10 ** 4:
        print("e -1")
    else:
        print(f'e {min_path}')


shield_x = shield_y = 1000


def make_move(sum_of_functions, x, y, q):
    global has_shield, shield_x, shield_y
    global visited
    global shield_allowed
    global with_shield, without_shield
    visited[y][x] = 1
    if sum_of_functions > 10 ** 4:
        print("e -1")
        raise MyException
    if x == inf_stone_x and y == inf_stone_y:
        if not shield_allowed:
            without_shield = sum_of_functions
            find_path_to_cell(x, y, 0, 0)
        else:
            with_shield = sum_of_functions
        raise MyException
    if x == shield_x and y == shield_y:
        has_shield = True
        q = PriorityQueue()
        visited = [[0 for _ in range(9)] for __ in range(9)]
    visited[y][x] = 1
    print("m", x, y)
    num_of_dangers = int(input())
    dangers = []
    for i in range(num_of_dangers):
        x_c, y_c, danger_type = input().split()
        x_c = int(x_c)
        y_c = int(y_c)
        dangers.append([x_c, y_c])
        if danger_type == "S":
            if shield_allowed:
                dangers.pop()
            shield_x = x_c
            shield_y = y_c
        elif danger_type == "I":
            dangers.pop()

    for pair in x_squares(x, y):
        x_c = pair[0]
        y_c = pair[1]
        if pair not in dangers and not visited[y_c][x_c]:
            q.put([sum_of_functions - heuristics_map[y][x] + heuristics_map[y_c][x_c] + 1, x_c, y_c])

    if not q.empty():
        top_priority = q.get()
        new_f, new_x, new_y = top_priority
        while visited[new_y][new_x] and not q.empty():
            top_priority = q.get()
            new_f, new_x, new_y = top_priority
        find_path_to_cell(x, y, new_x, new_y)
        make_move(new_f, new_x, new_y, q)
    else:
        find_path_to_cell(x, y, 0, 0)
        raise MyException


def surrounding_squares(x, y):
    """
        returns cells of Moore neighbourhood that belong to the map
    """
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
    """
        returns cells of Von Neumann neighbourhood that belong to the map
    """
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


def captain_marvel_zone(x, y):
    arr = surrounding_squares(x, y)
    for i in [-2, 2]:
        if 0 <= x + i <= 8:
            arr.append([x + i, y])
        if 0 <= y + i <= 8:
            arr.append([x, y + i])
    return arr


def find_path_to_cell(source_x, source_y, destination_x, destination_y):
    global visited
    visited_in_bfs = [[0 for _ in range(9)] for __ in range(9)]
    move_queue = []
    cell_parent = [[[100, 100] for _ in range(9)] for __ in range(9)]
    cell_parent[destination_y][destination_x] = [destination_x, destination_y]

    def bfs(x, y):
        global visited
        visited_in_bfs[y][x] = 1
        if x == source_x and y == source_y:
            raise MyException
        for coord_x, coord_y in x_squares(x, y):
            if visited[coord_y][coord_x] and not visited_in_bfs[coord_y][coord_x]:
                move_queue.append([coord_x, coord_y, x, y])
        if move_queue:
            new_x, new_y, parent_x, parent_y = move_queue.pop(0)
            while visited_in_bfs[new_y][new_x] and move_queue:
                new_x, new_y, parent_x, parent_y = move_queue.pop(0)
            cell_parent[new_y][new_x] = [parent_x, parent_y]
            bfs(new_x, new_y)

    try:
        bfs(destination_x, destination_y)
    except MyException:
        pass
    path_to_cell = []
    xc = source_x
    yc = source_y
    while not (xc == destination_x and yc == destination_y):
        path_to_cell.append(cell_parent[yc][xc])
        xc, yc = cell_parent[yc][xc]
    for x_c, y_c in path_to_cell:
        print(f'm {x_c} {y_c}')
        u = int(input())
        for i in range(u):
            input()


def runner():
    global game_type
    global inf_stone_x, inf_stone_y
    game_type = int(input())
    inf_stone_x, inf_stone_y = map(int, input().split())
    play_game()
    return


runner()
