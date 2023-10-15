my_map = [['', 'P', 'T', 'P', '', '', '', '', ''],
          ['', 'P', 'P', 'P', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', ''],
          ['', '', 'P', '', '', '', '', '', ''],
          ['', 'P', 'H', 'P', '', 'S', '', '', ''],
          ['', '', 'P', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', 'I']]


my_map = [['', 'P', 'T', 'P', '', '', '', '', ''],
          ['', 'P', 'P', 'P', '', '', '', '', ''],
          ['P', 'H', 'P', '', '', '', '', '', ''],
          ['', 'P', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', 'S', '', '', ''],
          ['', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', 'I']]

my_map = [['', '', '', '', '', '', '', 'P', 'S'],
          ['', '', '', '', '', '', 'P', 'H', 'P'],
          ['', '', '', '', '', '', '', 'P', ''],
          ['', '', '', '', '', '', '', '', ''],
          ['P', 'P', 'P', '', 'P', '', '', '', ''],
          ['P', 'T', 'P', 'P', 'P', 'P', '', '', ''],
          ['P', 'P', 'P', 'P', 'M', 'P', '', '', ''],
          ['', '', '', '', 'P', 'P', 'P', '', ''],
          ['I', '', '', '', '', 'P', '', '', '']]

my_map = [['', '', '', '', '', '', '', 'P', 'S'],
          ['', '', '', '', '', '', 'P', 'P', 'P'],
          ['', '', '', '', '', 'P', 'P', 'M', 'P'],
          ['', '', '', '', '', '', 'P', 'P', 'P'],
          ['P', 'P', 'P', 'P', '', '', '', 'P', ''],
          ['P', 'T', 'P', 'H', 'P', '', '', '', 'I'],
          ['P', 'P', 'P', 'P', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '']]

has_shield = False
inf_stone_x = inf_stone_y = 0


def game_one():
    global has_shield
    global inf_stone_x, inf_stone_y
    explored_map = [[set() for i in range(9)] for j in range(9)]
    inf_stone_y = int(inf_stone_y)
    x = y = 0
    explored_map[0][0].add("Clear")
    #explored_map[inf_stone_x][inf_stone_y].add("Stone")

    make_move(x, y, explored_map, x, y)
    if not has_shield and "Visited" not in explored_map[inf_stone_x][inf_stone_y]:
        """
        If shield wasn't picked in exploration phase, that means it is surrounded by avengers and cannot be accessed.
        If shield cannot be accessed and stone wasn't visited without it, that means the map is unsolvable.
        """
        print("e -1")
    elif not has_shield:
        """
        If shield wasn't picked in exploration phase, that means it is surrounded by avengers and cannot be accessed,
        so the shortest path surely has to avoid avengers
        """
        shortest_path = find_shortest_path_without_shield(explored_map)
        print(f"e {shortest_path}")
    #print(*explored_map, sep='\n')


def game_two():
    x = y = 0
    pass


def make_move(x, y, game_map, source_x, source_y):
    global has_shield

    with open("runner_request.txt", 'w') as f:
        f.write(f'm {x} {y}\n')
    simulate_response()

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
            elif danger_type == "P":
                if has_shield:
                    game_map[x_c][y_c].add("Unsolvable Danger")
                game_map[x_c][y_c].add("Danger")

    for pair in surrounding_squares(x, y):
        if pair not in dangers:
            x_c = pair[0]
            y_c = pair[1]
            game_map[x_c][y_c].add("Clear")
    game_map[x][y].add("Visited")
    for pair in x_squares(x, y):
        x_c = pair[0]
        y_c = pair[1]
        if "Clear" in game_map[x_c][y_c] and "Visited" not in game_map[x_c][y_c]:
            if "Shield" in game_map[x_c][y_c]:
                has_shield = True
            make_move(x_c, y_c, game_map, x, y)
    #print("mb", source_x, source_y)


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


def simulate_response():
    with open("runner_request.txt", 'r') as f:
        m, x, y = f.readline().split()
        x = int(x)
        y = int(y)
    for elem in ['H', 'M', 'T', 'P']:
        if elem in my_map[x][y]:
            print("Game over.")
            raise Exception
    dangers = []
    for pair in surrounding_squares(x, y):
        if my_map[pair[0]][pair[1]]:
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


def find_shortest_path_without_shield(game_map):
    shortest_path_length = float("inf")
    visited = [[0 for i in range(9)] for j in range(9)]
    queue = []

    def bfs(x, y, length):
        nonlocal shortest_path_length
        if x == inf_stone_x and y == inf_stone_y:
            shortest_path_length = length
            raise Exception
        visited[x][y] = 1
        for x_c, y_c in x_squares(x, y):
            if not visited[x_c][y_c] and "Danger" not in game_map[x_c][y_c] and "Hulk" not in game_map[x_c][y_c]\
                    and "Thor" not in game_map[x_c][y_c] and "Captain Marvel" not in game_map[x_c][y_c]:
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



def runner():
    global inf_stone_x, inf_stone_y
    n = int(input())
    inf_stone_x, inf_stone_y = map(int, input().split())
    if n == 1:
        game_one()
    elif n == 2:
        game_two()


    return


if __name__ == "__main__":
    runner()
