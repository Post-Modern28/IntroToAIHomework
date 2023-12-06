import time

GRID_SIZE = 20
def construct_grid(words_info):
    grid = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for word in words_info:
        x1, y1, t1 = words_info[word]
        if t1:
            for i, letter in enumerate(word):
                grid[x1][y1+i] = letter
        else:
            for i, letter in enumerate(word):
                grid[x1+i][y1] = letter
    return grid


def print_grid(grid):
    print(*[' '.join(line) for line in grid], sep='\n')


for i in range(1, 100):
    f1 = open(f'inputs/input{i}.txt')
    f2 = open(f'outputs/output{i}.txt')
    info = {}

    for word in f1:
        x, y, t = map(int, f2.readline().split())
        t = not t
        if word[-1:] == '\n':
            word = word[:-1]
        info[word] = [x, y, t]
    print(info)

    print_grid(construct_grid(info))
    f1.close()
    f2.close()
    time.sleep(10)
