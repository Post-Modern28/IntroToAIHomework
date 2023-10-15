my_map = [['', 'P', 'T', 'P', '', '', '', '', ''],
          ['', 'P', 'P', 'P', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', ''],
          ['', '', 'P', '', '', '', '', '', ''],
          ['', 'P', 'H', 'P', '', 'S', '', '', ''],
          ['', '', 'P', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', 'I']]

def game_one():
    explored_map = [[set() for i in range(9)] for j in range(9)]
    inf_stone_x, inf_stone_y = map(int, input().split())
    x = y = 0
    has_shield = False
    explored_map[0][0].add("Clear")
    explored_map[inf_stone_x][inf_stone_y].add("Stone")

    make_move(x, y, explored_map, x, y)
    print(*explored_map, sep='\n')
def game_two():
    x = y = 0
    pass


def make_move(x, y, game_map, source_x, source_y):
    print("m", x, y)
    # with open("runner_request.txt", 'w') as f:
    #     f.write(f'm {x} {y}\n')
    # simulate_response()
    # with open("author_response.txt", 'r') as f:
    #     num_of_dangers = int(f.readline())
    #     dangers = []
    num_of_dangers = int(input())
    dangers = []
    for i in range(num_of_dangers):
        x_c, y_c, danger_type = input().split()
        x_c = int(x_c)
        y_c = int(y_c)
        dangers.append([x_c, y_c])
        if danger_type == 'S':
            game_map[x_c][y_c].add("Shield")
        elif danger_type == "H":
            game_map[x_c][y_c].add("Hulk")
        elif danger_type == "I":
            game_map[x_c][y_c].add("Stone")
        elif danger_type == "T":
            game_map[x_c][y_c].add("Thor")
        elif danger_type == "M":
            game_map[x_c][y_c].add("Captain Marvel")
        elif danger_type == "P":
            game_map[x_c][y_c].add("Danger")
    for pair in surrounding_squares(x, y):
        if pair not in dangers:
            x_c = pair[0]
            y_c = pair[1]
            game_map[x_c][y_c].add("Clear")
    game_map[x][y].add("Visited")
    for pair in surrounding_squares(x, y):
        if pair not in dangers:
            x_c = pair[0]
            y_c = pair[1]
            if "Clear" in game_map[x_c][y_c] and "Visited" not in game_map[x_c][y_c]:
                make_move(x_c, y_c, game_map, x, y)
    print("mb", source_x, source_y)


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



def runner():
    n = int(input())
    if n == 1:
        game_one()
    elif n == 2:
        game_two()


    return


if __name__ == "__main__":
    #runner()
    simulate_response()