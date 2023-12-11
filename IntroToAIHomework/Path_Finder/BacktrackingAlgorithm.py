

has_shield = False
inf_stone_x = inf_stone_y = 1000
game_type = None


def play_game():
    global game_type
    global has_shield
    global inf_stone_x, inf_stone_y
    inf_stone_x = inf_stone_y = 1000
    explored_map = [[set() for _ in range(9)] for __ in range(9)]
    x = y = 0
    explored_map[0][0].add("Clear")
    # starting exploration
    make_move(x, y, explored_map, x, y)
    shield_x = shield_y = 1000
    for i in range(9):
        for j in range(9):
            explored_map[i][j].discard("Visited")
            explored_map[i][j].discard("Danger")
            explored_map[i][j].discard("Clear")
            if "Shield" in explored_map[i][j]:
                shield_y = i
                shield_x = j
            if "Stone" in explored_map[i][j]:
                inf_stone_y = i
                inf_stone_x = j
    """ Since we could pick up a shield while exploring,
        it could impact on the cells that were initially dangerous, so we double check
        the whole area to find all cells that are safe with shield and dangerous
        without it (if we didn't pick up a shield, nothing will change)
    """
    make_move(x, y, explored_map, x, y)
    for i in range(9):
        for j in range(9):
            if "Stone" in explored_map[i][j]:
                inf_stone_y = i
                inf_stone_x = j
                if "Danger" in explored_map[i][j]:
                    print("e -1")  # actually, this is the case of invalid map
                    return
    """ If after second exploration the stone wasn't found, that means the map is
        unsolvable"""
    if inf_stone_y > 10:
        print('e -1')
        return
    # starting exploitation
    map1 = [[0 for _ in range(9)] for __ in range(9)]
    map2 = [[0 for _ in range(9)] for __ in range(9)]
    for y in range(9):
        for x in range(9):
            if "Danger" in explored_map[y][x] or "Solvable Danger" in explored_map[y][x]:
                map1[y][x] = -1
            if "Danger" in explored_map[y][x]:
                map2[y][x] = -1
    path1 = shortest_path_length(map1, (0, 0), (inf_stone_x, inf_stone_y))
    path_to_shield = shortest_path_length(map1, (0, 0), (shield_x, shield_y))
    path2 = path_to_shield + shortest_path_length(map2, (shield_x, shield_y), (inf_stone_x, inf_stone_y))
    min_path = min(path1, path2)
    print(f'e {min_path}')


def make_move(x, y, game_map, source_x, source_y):
    """
    :param x: current x coordinate
    :param y: current y coordinate
    :param game_map: map for exploration
    :param source_x: x coordinate of a parent cell
    :param source_y: y coordinate of a parent cell
    :return: None
    """
    print("m", x, y)
    global has_shield
    num_of_dangers = int(input())
    dangers = []
    for i in range(num_of_dangers):
        x_c, y_c, danger_type = input().split()
        x_c = int(x_c)
        y_c = int(y_c)
        dangers.append([x_c, y_c])
        if danger_type == "S":
            game_map[y_c][x_c].add("Shield")
            dangers.pop()
        elif danger_type == "H":
            game_map[y_c][x_c].add("Hulk")
            game_map[y_c][x_c].add("Danger")
            for xcoord, ycoord in x_squares(x_c, y_c):
                game_map[ycoord][xcoord].add("Solvable Danger")
        elif danger_type == "I":
            game_map[y_c][x_c].add("Stone")
            dangers.pop()
        elif danger_type == "T":
            game_map[y_c][x_c].add("Thor")
            game_map[y_c][x_c].add("Danger")
            for xcoord, ycoord in surrounding_squares(x_c, y_c):
                game_map[ycoord][xcoord].add("Solvable Danger")
        elif danger_type == "M":
            game_map[y_c][x_c].add("Captain Marvel")
            game_map[y_c][x_c].add("Danger")
        elif danger_type == "P":
            game_map[y_c][x_c].add("Danger")

    for pair in surrounding_squares(x, y):
        if pair not in dangers:
            x_c = pair[0]
            y_c = pair[1]
            game_map[y_c][x_c].add("Clear")
    if game_type == 2:
        for pair in ear_squares(x, y):
            x_c = pair[0]
            y_c = pair[1]
            if pair not in dangers:
                game_map[y_c][x_c].add("Clear")
    game_map[y][x].add("Visited")
    for pair in x_squares(x, y):
        x_c = pair[0]
        y_c = pair[1]
        if "Clear" in game_map[y_c][x_c] and "Danger" not in game_map[y_c][x_c] and "Visited" not in game_map[y_c][x_c]:
            if "Shield" in game_map[y_c][x_c]:
                has_shield = True
            make_move(x_c, y_c, game_map, x, y)
    print("m", source_x, source_y)
    u = input()
    num_of_dangers = int(u)
    for i in range(num_of_dangers):
        input()


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


def shortest_path_length(matrix, init, dest):
    init_x = init[0]
    init_y = init[1]

    n = len(matrix)
    if init[0] > n or dest[0] > n:
        return float("inf")

    visited = [[False] * n for _ in range(len(matrix))]
    shortest = [[float('inf') for _ in range(n)] for __ in range(n)]
    shortest[init[1]][init[0]] = 0

    def backtrack(x, y, dist):
        nonlocal shortest, dest
        if shortest[y][x] < dist or shortest[dest[1]][dest[0]] < dist:
            return
        shortest[y][x] = dist
        if (x, y) == dest:
            return
        for new_x, new_y in x_squares(x, y):

            if visited[new_y][new_x] or matrix[new_y][new_x] == -1:
                continue
            visited[new_y][new_x] = True
            backtrack(new_x, new_y, dist + 1)
            visited[new_y][new_x] = False

    visited[init_y][init_x] = True
    backtrack(init_x, init_y, 0)
    return shortest[dest[1]][dest[0]]


def runner():
    global game_type
    global inf_stone_x, inf_stone_y
    game_type = int(input())
    inf_stone_x, inf_stone_y = map(int, input().split())
    play_game()
    return


runner()
