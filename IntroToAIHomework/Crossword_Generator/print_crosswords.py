import time
from MikhailRomanov import construct_grid
GRID_SIZE = 20



def print_grid(grid):
    print(*[' '.join(line) for line in grid], sep='\n')


for i in range(6, 7):
    f1 = open(f'inputs/input{i}.txt')
    f2 = open(f'outputs/output{i}.txt')
    info = {}

    for word in f1:
        x, y, t = map(int, f2.readline().split())
        t = int(not t)
        if word[-1:] == '\n':
            word = word[:-1]
        info[word] = [x, y, t]
    print(info)

    print_grid(construct_grid(info))
    f1.close()
    f2.close()
    time.sleep(5)
