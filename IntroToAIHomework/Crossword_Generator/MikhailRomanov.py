import random
from statistics import mode


def generate_random_grid():
    words_placement = {}
    for word in words:
        if len(word) > GRID_SIZE:
            continue
        placement_type = random.randint(0, 1)
        if placement_type:
            x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE - len(word)-1)
        else:
            x, y = random.randint(0, GRID_SIZE - len(word)-1), random.randint(0, GRID_SIZE-1)
        words_placement[word] = [x, y, placement_type]
    return words_placement


def word_intersection(word1, word_info1, word2, word_info2):  # 0 - vertical, 1 - horizontal
    x1, y1, t1 = word_info1
    x2, y2, t2 = word_info2
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


def count_adjacency_components(adjacency_matrix):
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
    biggest_component_num = mode(visited)
    big_component = []
    for i in range(len(adjacency_matrix)):
        if visited[i] == biggest_component_num:
            big_component.append(i)
    return cur_comp-1, big_component


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
        if not t1:
            if (y1 == y2 - 1 or y1 == y2+len(word_2)) and (x1 <= x2 < x1 + len(word_1)):
                score -= 100
        else:
            if (x1 == x2 - 1 or x1 == x2+len(word_2)) and (y1 <= y2 < y1 + len(word_1)):
                score -= 100
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


def evaluate_fitness(words_positions: dict):
    fit = 0
    adjacency_matrix = [[0 for _ in range(len(words_positions))] for __ in range(len(words_positions))]
    word_items = list(words_positions.items())
    for i in range(len(words_positions)):
        for j in range(i+1, len(words_positions)):
            fit += check_parallelism(*word_items[i], *word_items[j])
            intersection = word_intersection(*word_items[i], *word_items[j])
            intersection_validation = validate_intersections(*word_items[i], *word_items[j], intersection)
            fit += intersection_validation
            fit += check_parallelism(*word_items[i], *word_items[j])  # yeah, I check it twice
            if intersection_validation > 0:
                adjacency_matrix[i][j] = adjacency_matrix[j][i] = 1
    adjacency_components_num, biggest_component = count_adjacency_components(adjacency_matrix)

    fit -= (adjacency_components_num-1) * 400

    return fit


def select_parents(population, num_parents):
    fitness_scores = [evaluate_fitness(words_info) for words_info in population]
    indices = [*range(len(fitness_scores))]
    lst = [(a, b) for a, b in zip(fitness_scores, indices)]
    lst.sort(key=lambda pair: pair[0], reverse=True)
    best_indices = [lst[i][1] for i in range(num_parents)]
    best = [population[i] for i in best_indices]
    return best


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
    """
    Prints a crossword in a readable format

    :param grid: array, representing crossword
    :return: None
    """
    print(*[' '.join(line) for line in grid], sep='\n')


def crossover(parent1, parent2):
    # Here is a uniform crossover
    info1 = parent1
    info2 = parent2
    new_gen = {}
    for i in info1.keys():
        coin = random.randint(0, 1)
        if coin:
            new_gen[i] = info1[i][::]
        else:
            new_gen[i] = info2[i][::]
    return new_gen


def modified_crossover(parent1, parent2):
    # Modified uniform crossover
    info1 = parent1
    info2 = parent2
    new_gen = {}
    for i in info1.keys():
        coin = random.randint(0, 9)
        if coin < 8:  # 80 % chance to get DNA of a better parent
            new_gen[i] = info1[i][::]
        else:
            new_gen[i] = info2[i][::]
    return new_gen


def single_point_crossover(parent1, parent2):
    info1 = parent1
    info2 = parent2
    new_gen = {key: info1[key][::] for i, key in enumerate(list(info1.keys())[:len(info1)//2])}
    for key in info2:
        if key not in new_gen:
            new_gen[key] = info2[key][::]
    return new_gen


def good_crossover(parent1, parent2, parent1_big_comp, parent2_big_comp):
    # Picks biggest adjacency components from each parent
    words = list(parent1.keys())
    new_gen = {}
    for word in words:
        if word in parent1_big_comp:
            new_gen[word] = parent1_big_comp[word][::]
        elif word in parent2_big_comp:
            new_gen[word] = parent2_big_comp[word][::]
        else:
            coin = random.randint(0, 1)
            if coin:
                new_gen[word] = parent1[word][::]
            else:
                new_gen[word] = parent2[word][::]
    return new_gen


def find_biggest_component(words_positions):
    adjacency_matrix = [[0 for _ in range(len(words_positions))] for __ in range(len(words_positions))]
    word_items = list(words_positions.items())
    for i in range(len(words_positions)):
        for j in range(i + 1, len(words_positions)):
            intersection = word_intersection(*word_items[i], *word_items[j])
            intersection_validation = validate_intersections(*word_items[i], *word_items[j], intersection)
            if intersection_validation > 0:
                adjacency_matrix[i][j] = adjacency_matrix[j][i] = 1
    adjacency_components_num, biggest_component = count_adjacency_components(adjacency_matrix)

    component = {}
    for i in range(len(words_positions)):
        word, word_info = word_items[i]
        if i in biggest_component:
            component[word] = word_info[::]
    return component


def mutate(word_info, mutations_num=1):
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
    return new_gen


for i in range(1, 101):
    with open(f'inputs/input{i}.txt', 'r') as f:
        words = f.read().splitlines()

    POP_SIZE = 500
    GRID_SIZE = 20
    population = [generate_random_grid() for _ in range(POP_SIZE)]
    parents = select_parents(population, num_parents=POP_SIZE)
    epoch = 0
    maxfit = float('-inf')
    while maxfit < 0:
        # print(epoch)
        TOP_BEST = 25
        children = []
        NUM_CHILDREN = POP_SIZE
        STRATEGY_CHANGE_POINT = 150
        if epoch < STRATEGY_CHANGE_POINT:
            for p1 in range(TOP_BEST):
                parent1 = parents[p1]
                for p2 in range(p1 + 1, NUM_CHILDREN):
                    parent2 = parents[p2]
                    child = crossover(parent1, parent2)
                    child = mutate(child, random.randint(0, 3))
                    if child not in children:
                        children.append(child)
        else:
            biggest_adjacency_components = [find_biggest_component(crossword) for crossword in population]
            for p1 in range(4*TOP_BEST):
                parent1 = parents[p1]
                for p2 in range(p1, 4*TOP_BEST):
                    parent2 = parents[p2]
                    cross_type = [crossover, modified_crossover, single_point_crossover, good_crossover]
                    coin = random.randint(3, 3)  # finally I decided to use the latest crossover
                    cross_function = cross_type[coin]
                    if coin == 3:
                        child = cross_function(parent1, parent2,
                                               biggest_adjacency_components[p1], biggest_adjacency_components[p2])
                    else:
                        child = cross_function(parent1, parent2)
                    if child not in children and child not in parents:
                        children.append(child)
                    child2 = mutate(child, random.randint(1, 2))
                    if child2 not in children:
                        children.append(child)
        parents = select_parents(parents+children, POP_SIZE)
        maxfit = evaluate_fitness(parents[0])
        epoch += 1
        if epoch > 10000:
            population = [generate_random_grid() for _ in range(POP_SIZE)]
            parents = select_parents(population, num_parents=POP_SIZE)
            epoch = 0  # start over if not succeeded after a long time
        # Uncomment if you need to see partial results
        # if epoch % 10 == 0:
        #     for k in range(1):
        #         print_grid(construct_grid(parents[k]))
        #         print()

    best_grid = construct_grid(parents[0])
    best_info = parents[0]
    maxfit = evaluate_fitness(parents[0])
    with open(f"outputs/output{i}.txt", "w") as f:
        for word in words:
            x, y, t = best_info[word]
            t = (t + 1) % 2  # in my program 0 is vertical, 1 is horizontal, but the task requires it vice versa
            f.write(f'{x} {y} {t}\n')
    print_grid(best_grid)
