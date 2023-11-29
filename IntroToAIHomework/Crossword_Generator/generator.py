import random
import math
with open('input.txt', 'r') as f:
    words = f.read().splitlines()

POP_SIZE = 500
GRID_SIZE = 20


def sigmoid(x):
    return 1/(1+math.e**-x)


def generate_random_grid():
    grid = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    words_placement = {}
    for word in words:
        if len(word) > GRID_SIZE:
            continue
        placement_type = random.randint(0, 1)
        if placement_type:

            x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE - len(word)-1)
            for i, letter in enumerate(word):
                grid[x][y+i] = letter
        else:
            x, y = random.randint(0, GRID_SIZE - len(word)-1), random.randint(0, GRID_SIZE-1)
            for i, letter in enumerate(word):
                grid[x+i][y] = letter
        words_placement[word] = [x, y, placement_type]
    return grid, words_placement


def word_intersection(word1, word_info1, word2, word_info2):  # 0 - vertical, 1 - horizontal
    x1, y1, t1 = word_info1
    x2, y2, t2 = word_info2
    s1 = set()
    s2 = set()
    if t1:
        s1 = {(x1, i) for i in range(y1, y1+len(word1))}
    else:
        s1 = {(i, y1) for i in range(x1, x1+len(word1))}
    if t2:
        s2 = {(x2, i) for i in range(y2, y2+len(word2))}
    else:
        s2 = {(i, y2) for i in range(x2, x2+len(word2))}
    intersections = []
    for coord in s1:
        if coord in s2:
            intersections.append(coord)
    return intersections


def word_intersection_2(word1, word_info1, word2, word_info2):
    x1, y1, t1 = word_info1
    x2, y2, t2 = word_info2
    if t1 != t2:
        if not t1:
            x1, y1, t1, = word_info2  #make first word horizontal and second vertical
            x2, y2, t2 = word_info1
            word1, word2 = word2, word1
        if x1 <= x2 < x1+len(word1) and y2 <= y1 < y2+len(word2):
            return [(x2, y1)]
        return []
    if t1:
        if x1 != x2:
            return []
        if y1 < y2:
            return [(x1, i) for i in range(y2, y1+len(word1))]
            # do not check whether x2 is greater than x1 + len(word1),
            # because it would just return empty list in that case
        return [(x2, i) for i in range(y1, y2+len(word2))]

    # if not t1:
    if y1 != y2:
        return []
    if x1 < x2:
        return [(i, y1) for i in range(x2, x1+len(word1))]
    return [(i, y1) for i in range(x1, x2+len(word2))]


# def area(x1, y1, x2, y2, x3, y3):
#     return (x2-x1) * (y3-y1) - (y2-y1) * (x3-x1)
#
#
# def intersect_l(a, b, c, d):
#     a, b = min(a, b), max(a, b)
#     c, d = min(c, d), max(c, d)
#     return max(a, c) <= min(b, c)
#
#
# def words_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
#     return intersect_l(x1, x2, x3, x4) and intersect_l(y1, y2, y3, y4) \
#            and area(x1, y1, x2, y2, x3, y3) * area(x1, y1, x2, y2, x4, y4) <= 0 \
#            and area(x3, y3, x4, y4, x1, y1) * area(x3, y3, x4, y4, x2, y2) <= 0
population = [generate_random_grid() for _ in range(POP_SIZE)]


def evaluate_fitness(grid: list, words_positions: dict):

    def validate_intersections(word_1, word_1_info, word_2, word_2_info, common_points):
        score = 0
        x1, y1, t1 = word_1_info
        x2, y2, t2 = word_2_info
        for x, y in common_points:
            if not t1:
                real_letter1 = word_1[x-x1]
            else:
                real_letter1 = word_1[y-y1]
            if not t2:
                real_letter2 = word_2[x-x2]
            else:
                real_letter2 = word_2[y-y2]

            if real_letter1 == real_letter2:
                if t1 == t2:
                    score -= 200
                else:
                    score += 1
            else:
                score -= 100
        return score

    def check_parallelism(word_1, word_1_info, word_2, word_2_info):
        score = 0
        x1, y1, t1 = word_1_info
        x2, y2, t2 = word_2_info
        if t1 != t2:
            return score
        if t1 and x1-1 <= x2 <= x1+1:
            y1_f = y1 + len(word_1)
            y2_f = y2 + len(word_2)
            if y1 <= y2 <= y1_f:
                score -= (y1_f - y2) * 100  # penalty for each intersecting letter
            elif y2 <= y1 <= y2_f:
                score -= (y2_f - y1) * 100
        if not t1 and y1-1 <= y2 <= y1+1:
            x1_f = x1 + len(word_1)
            x2_f = x2 + len(word_2)
            if x1 <= x2 <= x1_f:
                score -= (x1_f - x2) * 100
            elif x2 <= x1 <= x2_f:
                score -= (x2_f - x1) * 100
        return score


    fit = 0
    adjacency_matrix = [[0 for _ in range(len(words_positions))] for __ in range(len(words_positions))]
    word_items = list(words_positions.items())
    for i in range(len(words_positions)):
        for j in range(i+1, len(words_positions)):
            word1, word1_info = word_items[i][0], word_items[i][1]
            word2, word2_info = word_items[j][0], word_items[j][1]
            fit += check_parallelism(*word_items[i], *word_items[j])
            intersection = word_intersection(*word_items[i], *word_items[j])
            if intersection:
                adjacency_matrix[i][j] = adjacency_matrix[j][i] = 1
                fit += validate_intersections(*word_items[i], *word_items[j], intersection)

    def count_adjacency_components():
        visited = [0] * len(adjacency_matrix)
        cur_comp = 1

        def dfs(node):
            visited[node] = cur_comp
            for i in range(len(adjacency_matrix)):
                if adjacency_matrix[node][i] and not visited[i]:
                    dfs(i)
        for i in range(len(adjacency_matrix)):
            if not visited[i]:
                dfs(i)
                cur_comp += 1
        return cur_comp-1

    adjacency_components = count_adjacency_components()

    fit -= (adjacency_components-1) * 400

    return fit


def print_grid(grid):
    print(*[' '.join(l) for l in grid], sep='\n')
# exp_sum = sum(map(math.exp, fitness_scores))
# print(exp_sum)
# sigm = lambda x: math.exp(x) / exp_sum
# probabilities = list(map(sigm, fitness_scores))
# print(probabilities)
# print(fitness_scores)

# Step 4: Select parents for next generation
def select_parents(population, num_parents):
    fitness_scores = [evaluate_fitness(grid, words_info) for grid, words_info in population]
    # print("Max fit is ",max(fitness_scores))
    indices = [*range(len(fitness_scores))]
    lst = [(a, b) for a, b in zip(fitness_scores, indices)]
    lst.sort(key=lambda pair: pair[0], reverse=True)
    # print("Best 10 are", lst[:10])
    best_indices = [lst[i][1] for i in range(num_parents)]
    best = [population[i] for i in best_indices]
    # print("Best are ", [evaluate_fitness(*i) for i in best[:10]])
    return best


parents = select_parents(population, num_parents=POP_SIZE)


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


# Step 5: Create new grids from parents
def crossover(parent1, parent2):
    grid1, info1 = parent1
    grid2, info2 = parent2
    # new_gen = {key: info1[key] for i, key in enumerate(list(info1.keys())[:len(info1)//2])}
    # for key in info2:
    #     if key not in new_gen:
    #         new_gen[key] = info2[key]
    # Here is a uniform crossover
    new_gen = {}
    for i in info1.keys():
        coin = random.randint(0, 1)
        if coin:
            new_gen[i] = info1[i][::]
        else:
            new_gen[i] = info2[i][::]
    new_grid = construct_grid(new_gen)
    return [new_grid, new_gen]


def mutate(grid, word_info, mutations_num=1):
    words = list(word_info.keys())
    new_gen = {key: word_info[key] for key in word_info}
    for i in range(mutations_num):
        mutated_key = random.choice(words)
        change_type = random.randint(1, 3)
        if change_type == 1:
            new_gen[mutated_key][2] = (word_info[mutated_key][2] + 1) % 2
            if new_gen[mutated_key][2] and new_gen[mutated_key][1] + len(mutated_key) > GRID_SIZE-1:
                new_gen[mutated_key][1] = random.randint(0, len(mutated_key)-1)
            if not new_gen[mutated_key][2] and new_gen[mutated_key][0] + len(mutated_key) > GRID_SIZE-1:
                new_gen[mutated_key][0] = random.randint(0, len(mutated_key)-1)
        elif change_type == 2:
            x = random.randint(0, len(mutated_key)-1)
            new_gen[mutated_key][0] = x
        elif change_type == 3:
            y = random.randint(0, len(mutated_key)-1)
            new_gen[mutated_key][1] = y
    grid = construct_grid(new_gen)
    return [grid, new_gen]

NUM_EPOCHS = 2000
epoch = 0
maxfit = float('-inf')
while maxfit < 0:
    children = []
    num_children = POP_SIZE
    for i in range(25):
        parent1 = parents[i]
        for j in range(i+1, num_children):
            parent2 = parents[j]

            child = crossover(parent1, parent2)
            child = mutate(*child, random.randint(0, 3))
            if child not in children:

                children.append(child)
    # print("Best before concatenation:", evaluate_fitness(*parents[0]))
    parents = select_parents(parents+children, POP_SIZE)
    # print("Best after concatenation", evaluate_fitness(*parents[0]))
    maxfit = evaluate_fitness(*parents[0])
    if epoch % 10 == 0:
        print(f"Epoch {epoch}:")
        # print([evaluate_fitness(*i) for i in parents][:10])
        # print([evaluate_fitness(*i) for i in parents][-10:])
        print("Best:")
        print(maxfit)
        print_grid(parents[0][0])
        print("Second:")
        print_grid(parents[1][0])
        print("Third")
        print_grid(parents[2][0])
        print("Fourth")
        print_grid(parents[3][0])
        best_grid = parents[0][0]
        for i in range(1, POP_SIZE):
            if parents[i][1] == parents[i-1][1]:
                print(i, end=' ')
            else:
                print('|', end=' ')
        print()
        epoch += 1

best_grid = parents[0][0]
maxfit = evaluate_fitness(*parents[0])

print(*[' '.join(l) for l in best_grid], sep='\n')
