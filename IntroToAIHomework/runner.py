
my_map = [# 0    1    2    3    4    5    6    7    8
          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],    # 0
          [' ', 'P', 'P', 'P', ' ', ' ', ' ', ' ', ' '],    # 1
          ['P', 'H', 'T', 'P', ' ', ' ', ' ', ' ', ' '],    # 2
          ['P', 'P', 'M', 'P', 'P', ' ', ' ', ' ', ' '],    # 3
          [' ', 'P', 'P', 'P', 'I', ' ', ' ', ' ', ' '],    # 4
          [' ', ' ', 'P', ' ', ' ', ' ', ' ', ' ', ' '],    # 5
          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],    # 6
          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],    # 7
          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]    # 8


def transpose_matrix(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(i+1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]


transpose_matrix(my_map)
#print(*my_map, sep='\n')
marvel_x = 1000
marvel_y = 1000
for i in range(9):
    mar_flag = 0
    for j in range(9):
        if my_map[i][j] == "M":
            marvel_x = i
            marvel_y = j
            mar_flag = 1
            break
    if mar_flag == 1:
        break
for i in range(9):
    mar_flag = 0
    for j in range(9):
        if my_map[i][j] == ' ':
            my_map[i][j] = ''
has_shield = False
inf_stone_x = inf_stone_y = 0
game_type = None


def game_one():
    global game_type
    global has_shield
    global inf_stone_x, inf_stone_y
    explored_map = [[set() for _ in range(9)] for __ in range(9)]
    inf_stone_y = int(inf_stone_y)
    x = y = 0
    explored_map[0][0].add("Clear")

    make_move(x, y, explored_map, x, y)
    if not has_shield and "Visited" not in explored_map[inf_stone_x][inf_stone_y]:
        """
        If shield wasn't picked in exploration phase, that means it is surrounded by avengers and cannot be accessed.
        If shield cannot be accessed and stone wasn't visited without it, that means the map is unsolvable.
        """
        print("e -1")
    elif not has_shield:
        # print("Shield wasn't found")
        """
        If shield wasn't picked in exploration phase, that means it is surrounded by avengers and cannot be accessed,
        so the shortest path surely has to avoid avengers
        """
        shortest_path = find_shortest_path_without_shield(explored_map, inf_stone_x, inf_stone_y)
        print(f"e {shortest_path}")
    else:
        """
        If shield was found, then firstly double check cells, because we could pass through Perception zones without 
        shield at first, so new paths might be opened. We will need to calculate 2 possible paths:
        1) picking up a shield and moving through disappeared perception zones
        2) going without a shield, avoiding all perception zones
        """

        shield_x = shield_y = -1
        for i in range(9):
            for j in range(9):
                explored_map[i][j].discard("Visited")
                explored_map[i][j].discard("Danger")
                if "Shield" in explored_map[i][j]:
                    shield_x = i
                    shield_y = j
        make_move(x, y, explored_map, x, y)
        if "Visited" not in explored_map[inf_stone_x][inf_stone_y]:
            # If stone is not accessible even with a shield, then map is unsolvable
            print("e -1")
            return
        path1 = find_shortest_path_without_shield(explored_map, inf_stone_x, inf_stone_y)
        path2 = find_shortest_path_with_shield(explored_map, shield_x, shield_y, inf_stone_x, inf_stone_y)
        min_path = min(path1, path2)
        print(f'e {min_path}')
    # print(*explored_map, sep='\n')


def make_move(x, y, game_map, source_x, source_y):
    print("m", x, y)
    global has_shield

    with open("runner_request.txt", 'w') as f:
        f.write(f'm {x} {y}\n')
    simulate_response()
    game_map[x][y].add("Visited")
    with open("author_response.txt", 'r') as f:
        u = f.readline()
        num_of_dangers = int(u)
        dangers = []
        for i in range(num_of_dangers):
            x_c, y_c, danger_type = f.readline().split()
            x_c = int(x_c)
            y_c = int(y_c)
            dangers.append([x_c, y_c])
            if danger_type == 'S':
                game_map[x_c][y_c].add("Shield")
                game_map[x_c][y_c].add("Clear")
            elif danger_type == "H":
                game_map[x_c][y_c].add("Hulk")
                for xcoord, ycoord in x_squares(x_c, y_c):
                    game_map[xcoord][ycoord].add("Solvable Danger")
            elif danger_type == "I":
                game_map[x_c][y_c].add("Stone")
                game_map[x_c][y_c].add("Clear")
            elif danger_type == "T":
                game_map[x_c][y_c].add("Thor")
                for xcoord, ycoord in surrounding_squares(x_c, y_c):
                    game_map[xcoord][ycoord].add("Solvable Danger")
            elif danger_type == "M":
                game_map[x_c][y_c].add("Captain Marvel")
                for xcoord, ycoord in captain_marvel_zone(x_c, y_c):
                    game_map[xcoord][ycoord].add("Danger")
            elif danger_type == "P":
                game_map[x_c][y_c].add("Danger")
    # u = input()
    # num_of_dangers = int(u)
    # dangers = []
    # for i in range(num_of_dangers):
    #     x_c, y_c, danger_type = input().split()
    #     x_c = int(x_c)
    #     y_c = int(y_c)
    #     dangers.append([x_c, y_c])
    #     if danger_type == 'S':
    #         game_map[x_c][y_c].add("Shield")
    #         game_map[x_c][y_c].add("Clear")
    #         dangers.pop()
    #     elif danger_type == "H":
    #         game_map[x_c][y_c].add("Hulk")
    #         for xcoord, ycoord in x_squares(x_c, y_c):
    #             game_map[xcoord][ycoord].add("Solvable Danger")
    #     elif danger_type == "I":
    #         game_map[x_c][y_c].add("Stone")
    #         game_map[x_c][y_c].add("Clear")
    #         dangers.pop()
    #     elif danger_type == "T":
    #         game_map[x_c][y_c].add("Thor")
    #         for xcoord, ycoord in surrounding_squares(x_c, y_c):
    #             game_map[xcoord][ycoord].add("Solvable Danger")
    #     elif danger_type == "M":
    #         game_map[x_c][y_c].add("Captain Marvel")
    #         for xcoord, ycoord in captain_marvel_zone(x_c, y_c):
    #             game_map[xcoord][ycoord].add("Danger")
    #     elif danger_type == "P":
    #         game_map[x_c][y_c].add("Danger")

    for pair in surrounding_squares(x, y):
        if pair not in dangers:
            x_c = pair[0]
            y_c = pair[1]
            game_map[x_c][y_c].add("Clear")
    if game_type == 2:
        for pair in ear_squares(x, y):
            x_c = pair[0]
            y_c = pair[1]
            if pair not in dangers:
                game_map[x_c][y_c].add("Clear")

    for pair in x_squares(x, y):
        x_c = pair[0]
        y_c = pair[1]
        if "Clear" in game_map[x_c][y_c] and "Visited" not in game_map[x_c][y_c]:
            if "Shield" in game_map[x_c][y_c]:
                has_shield = True
            make_move(x_c, y_c, game_map, x, y)
    print("m", source_x, source_y)
    # u = input()
    # num_of_dangers = int(u)
    # for i in range(num_of_dangers):
    #     x_c, y_c, danger_type = input().split()
    with open("runner_request.txt", 'w') as f:
        f.write(f'm {source_x} {source_y}\n')
    simulate_response()


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
        if elem in my_map[x][y]:
            print(f"You stepped at ({x}, {y}) where enemy resides")
            print("Game over.")
            raise Exception
    if [x, y] not in x_squares(x_prev, y_prev) and [x, y] != [x_prev, y_prev]:
        print(f"Invalid move from ({x_prev}, {y_prev}) to ({x}, {y})")
        raise ZeroDivisionError
    x_prev = x
    y_prev = y
    if ('P' in my_map[x][y] and not has_shield) or [x, y] in captain_marvel_zone(marvel_x, marvel_y):
        print(f"You stepped at ({x}, {y})")
        print(marvel_x, marvel_y)
        print(captain_marvel_zone(marvel_x, marvel_y))
        print("Game over.")
        raise Exception
    dangers = []
    for pair in surrounding_squares(x, y):
        if my_map[pair[0]][pair[1]]:
            if my_map[pair[0]][pair[1]] == 'P' and has_shield and pair not in captain_marvel_zone(marvel_x, marvel_y):
                continue
            dangers.append([pair[0], pair[1], my_map[pair[0]][pair[1]]])
    if game_type == 2:
        for pair in ear_squares(x, y):
            if my_map[pair[0]][pair[1]]:
                if my_map[pair[0]][pair[1]] == 'P' and has_shield and pair not in captain_marvel_zone(marvel_x, marvel_y):
                    continue
                dangers.append([pair[0], pair[1], my_map[pair[0]][pair[1]]])
    with open("author_response.txt", 'w') as f:
        f.write(f'{len(dangers)}\n')
        for i in range(len(dangers)):
            pair = dangers[i]
            f.write(f'{pair[0]} {pair[1]} {pair[2]}\n')


def x_squares(x, y):
    squares = []
    for i in [-1, 1]:
        if 0 <= x+i <= 8:
            squares.append([x+i, y])
        if 0 <= y+i <= 8:
            squares.append([x, y+i])
    return squares


def ear_squares(x, y):
    squares = []
    for i in [-2, 2]:
        if 0 <= x+i <= 8 and 0 <= y+i <= 8:
            squares.append([x+i, y+i])
        if 0 <= x+i <= 8 and 0 <= y-i <= 8:
            squares.append([x+i, y-i])
    return squares


def find_shortest_path_without_shield(game_map, destination_x, destination_y):
    shortest_path_length = float("inf")
    visited = [[0 for _ in range(9)] for __ in range(9)]
    queue = []

    def bfs(x, y, length):
        nonlocal shortest_path_length
        if x == destination_x and y == destination_y:
            shortest_path_length = length
            raise Exception
        visited[x][y] = 1
        for x_c, y_c in x_squares(x, y):
            flag = 0
            for elem in ["Danger", "Solvable Danger", "Hulk", "Thor", "Captain Marvel"]:
                if elem in game_map[x_c][y_c]:
                    flag = 1
                    break
            if not visited[x_c][y_c] and not flag:
                queue.append([x_c, y_c, length+1])
        while queue:
            triplet = queue.pop(0)
            x_c, y_c, path_len = triplet
            if not visited[x_c][y_c]:
                bfs(x_c, y_c, path_len)
    try:
        bfs(0, 0, 0)
    except Exception:
        pass

    return shortest_path_length


def find_shortest_path_with_shield(game_map, shield_x, shield_y, destination_x, destination_y):
    path_to_shield = find_shortest_path_without_shield(game_map, shield_x, shield_y)
    visited = [[0 for _ in range(9)] for __ in range(9)]
    path_from_shield_to_stone = float("inf")
    queue = []

    def bfs(x, y, length):
        nonlocal path_from_shield_to_stone
        if x == destination_x and y == destination_y:
            path_from_shield_to_stone = length
            raise Exception
        visited[x][y] = 1
        for x_c, y_c in x_squares(x, y):
            flag = 0
            for elem in ["Danger", "Hulk", "Thor", "Captain Marvel"]:
                if elem in game_map[x_c][y_c]:
                    flag = 1
                    break
            if not visited[x_c][y_c] and not flag:
                queue.append([x_c, y_c, length+1])
        while queue:
            triplet = queue.pop(0)
            x_c, y_c, path_len = triplet
            if not visited[x_c][y_c]:
                bfs(x_c, y_c, path_len)
    try:
        bfs(shield_x, shield_y, 0)
    except Exception:
        pass
    return path_to_shield + path_from_shield_to_stone


def captain_marvel_zone(x, y):
    arr = surrounding_squares(x, y)
    for i in [-2, 2]:
        if 0 <= x + i <= 8:
            arr.append([x+i, y])
        if 0 <= y + i <= 8:
            arr.append([x, y+i])
    return arr


def runner():
    global game_type
    global inf_stone_x, inf_stone_y
    game_type = int(input())
    inf_stone_y, inf_stone_x = map(int, input().split())
    #inf_stone_x, inf_stone_y = map(int, input().split())
    game_one()
    return


runner()




# def generate_test_cases():
#     for i in range(9):
#         for j in range(9):
#
#     test_map = [['' for _ in range(9)] for __ in range(9)]
#
#     with open("testcases.txt", 'w') as f:
#         f.write(f"{my_map}")
# generate_test_cases()


