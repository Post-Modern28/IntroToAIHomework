import random
from statistics import mode
from datetime import datetime


def generate_random_grid() -> dict:
    words_placement = {}
    for word in words:
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


def count_adjacency_components(adjacency_matrix, pick_random=None):
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
    if pick_random:
        biggest_component_num = random.randint(1, max(visited))
    for i in range(len(adjacency_matrix)):
        if visited[i] == biggest_component_num:
            big_component.append(i)
    return cur_comp-1, big_component


def validate_intersections(word_1: str, word_1_info: list, word_2: str, word_2_info: list, common_points: list):
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

    # if t1 == t2
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


def build_adjacency_matrix(words_positions: dict):
    adjacency_matrix = [[0 for _ in range(len(words_positions))] for __ in range(len(words_positions))]
    word_items = list(words_positions.items())
    for i in range(len(words_positions)):
        for j in range(i + 1, len(words_positions)):
            intersection = word_intersection(*word_items[i], *word_items[j])
            intersection_validation = validate_intersections(*word_items[i], *word_items[j], intersection)
            if intersection_validation > 0:
                adjacency_matrix[i][j] = adjacency_matrix[j][i] = 1
    return adjacency_matrix


def evaluate_fitness(words_positions: dict):
    fit = 0
    adjacency_matrix = [[0 for _ in range(len(words_positions))] for __ in range(len(words_positions))]
    word_items = list(words_positions.items())
    for i in range(len(words_positions)):
        for j in range(i+1, len(words_positions)):
            par1 = check_parallelism(*word_items[i], *word_items[j])
            par2 = check_parallelism(*word_items[j], *word_items[i])
            word1 = word_items[i][0]
            word2 = word_items[j][0]
            x1, y1, t1 = word_items[i][1]
            x2, y2, t2 = word_items[j][1]
            if (par1 < 0 or par2 < 0) and t1 == t2 and not (x1 == x2 or y1 == y2):
                flag = 0
                for k in range(len(words_positions)):
                    if k == i or k == j or word_items[k][1][2] == t1:
                        continue
                    if word_intersection(*word_items[i], *word_items[k]) and\
                            word_intersection(*word_items[j], *word_items[k])\
                            and validate_intersections(*word_items[i], *word_items[k],
                                                       word_intersection(*word_items[i], *word_items[k])) >= 0\
                            and validate_intersections(*word_items[j], *word_items[k],
                                                       word_intersection(*word_items[j], *word_items[k])) >= 0:
                        if not t1:
                            if x1 + len(word1)-1 == x2 or x2 + len(word2)-1 == x1:
                                flag = 1
                                break
                        else:
                            if y1 + len(word1)-1 == y2 or y2 + len(word2)-1 == y1:
                                flag = 1
                                break
                if flag:
                    fit -= par1 + par2
            fit += par1 + par2
            intersection = word_intersection(*word_items[i], *word_items[j])
            intersection_validation = validate_intersections(*word_items[i], *word_items[j], intersection)
            fit += intersection_validation
            if intersection_validation > 0:
                adjacency_matrix[i][j] = adjacency_matrix[j][i] = 1
    adjacency_components_num, biggest_component = count_adjacency_components(adjacency_matrix)
    fit -= (adjacency_components_num-1) * 500

    return fit


def select_parents(population: list, num_parents: int):
    fitness_scores = [evaluate_fitness(words_info) for words_info in population]
    indices = [*range(len(fitness_scores))]
    lst = [(a, b) for a, b in zip(fitness_scores, indices)]
    lst.sort(key=lambda pair: pair[0], reverse=True)
    best_indices = [lst[i][1] for i in range(num_parents)]
    best = [population[i] for i in best_indices]
    return best


def construct_grid(words_info: dict):
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


def find_biggest_component(words_positions, pick_random=None):
    word_items = list(words_positions.items())
    adjacency_matrix = build_adjacency_matrix(words_positions)
    adjacency_components_num, biggest_component = count_adjacency_components(adjacency_matrix, pick_random)

    component = {}
    for i in range(len(words_positions)):
        word, word_info = word_items[i]
        if i in biggest_component:
            component[word] = word_info[::]
    return component


def convert_to_probabilities(scores):
    max_score = 2*min(scores)

    # Convert the scores to positive values
    pos_scores = [(-max_score + score) / 100 for score in scores]

    # Calculate the sum of all scores
    total_score = sum(pos_scores)

    # Divide each score by the sum to get the probabilities
    probs = [score / total_score for score in pos_scores]

    return probs


def select_element(probabilities):
    # Generate a random number between 0 and 1
    rand_num = random.random()

    # Initialize the cumulative probability to 0
    cum_prob = 0

    # Iterate over the probabilities and add them up until the cumulative probability is greater than the random number
    for i, prob in enumerate(probabilities):
        cum_prob += prob
        if cum_prob > rand_num:
            return i


def mutate(word_info, mutations_num=1, move_component=None):
    words = list(word_info.keys())
    new_gen = {key: word_info[key][::] for key in word_info}
    for i in range(mutations_num):
        mutated_key = random.choice(words)
        change_type = random.randint(1, 2)
        if move_component:
            change_type = 4
        if change_type == 1:
            new_gen[mutated_key][2] = (word_info[mutated_key][2] + 1) % 2  # change orientation of the word
        for word in words:
            flag2 = 0
            x1, y1, t1 = word_info[word]
            x2, y2, t2 = new_gen[mutated_key]
            if word != mutated_key and t1 != t2:
                common_letters = list(set(mutated_key).intersection(set(word)))
                for letter in common_letters:
                    idx1 = word.index(letter)
                    idx2 = mutated_key.index(letter)
                    flag = 0
                    if t1:
                        if 0 <= x1 - idx2 and x1 - idx2 + len(mutated_key) < 19:
                            new_gen[mutated_key][0] = x1 - idx2
                            new_gen[mutated_key][1] = y1 + idx1
                            flag = 1
                    else:
                        if 0 <= y1 - idx2 and y1 - idx2 + len(mutated_key) < 19:
                            new_gen[mutated_key][0] = x1 + idx1
                            new_gen[mutated_key][1] = y1 - idx2
                            flag = 1
                    if flag:
                        flag2 = 1
                        break
            if flag2:
                break
        if change_type == 4:
            component_to_move = find_biggest_component(word_info, pick_random=True)
            x_top, x_bottom, y_left, y_right = define_movement_borders(component_to_move)
            top_bottom = random.randint(0, 1)
            left_right = random.randint(0, 1)
            if top_bottom:
                shift_x = 0
                if x_top:
                    shift_x = random.randint(0, x_top)
                diff_x = shift_x - x_top
            else:
                shift_x = random.randint(x_bottom, 19)
                diff_x = shift_x - x_bottom
            if left_right:
                shift_y = 0
                if y_left:
                    shift_y = random.randint(0, y_left)
                diff_y = shift_y - y_left
            else:
                shift_y = random.randint(y_right, 19)
                diff_y = shift_y - y_right
            for word in component_to_move:
                component_to_move[word][0] += diff_x
                component_to_move[word][1] += diff_y
                new_gen[word] = component_to_move[word][:]
    return new_gen


def define_movement_borders(component):
    y_left = 19
    x_top = 19
    y_right = 0
    x_bottom = 0
    for word in component:
        word_info = component[word]
        x, y, t = word_info
        x_top = min(x_top, x)
        y_left = min(y_left, y)
        if not t:
            x_bottom = max(x_bottom, x+len(word)-1)
        else:
            y_right = max(y_right, y+len(word)-1)
    return x_top, x_bottom, y_left, y_right


GRID_SIZE = 20
for i in range(1, 101):
    start_time = datetime.now()
    with open(f'/inputs/input{i}.txt', 'r') as f:
        words = f.read().splitlines()
    print(f"Running test {i}")
    POP_SIZE = 250
    population = [generate_random_grid() for _ in range(POP_SIZE)]
    parents = select_parents(population, num_parents=POP_SIZE)
    epoch = 0
    maxfit = float('-inf')
    last_update = 0
    while maxfit < 0:
        print(epoch)
        TOP_BEST = 30
        children = []
        NUM_CHILDREN = POP_SIZE
        SECOND_CHANGE = 80
        if len(words) < 9:
            STRATEGY_CHANGE_POINT = 16
        else:
            STRATEGY_CHANGE_POINT = 21
        if epoch < STRATEGY_CHANGE_POINT:
            for p1 in range(TOP_BEST):
                parent1 = parents[p1]
                for p2 in range(p1 + 1, POP_SIZE-1):
                    parent2 = parents[p2]
                    child = crossover(parent1, parent2)
                    child = mutate(child, random.randint(1, 2))
                    if child not in children and child not in parents:
                        children.append(child)
        elif STRATEGY_CHANGE_POINT <= epoch < SECOND_CHANGE:
            fitness = [evaluate_fitness(i) for i in parents]
            probas = convert_to_probabilities(fitness)
            for _ in range(TOP_BEST):
                p1 = select_element(probas)
                p2 = select_element(probas)
                parent1 = parents[p1]
                parent2 = parents[p2]
                biggest_comp = [find_biggest_component(i) for i in parents]
                child = good_crossover(parent1, parent2, biggest_comp[p1], biggest_comp[p2])
                child2 = good_crossover(parent2, parent1, biggest_comp[p2], biggest_comp[p1])
                child = mutate(child, random.randint(0, 3))
                if child not in children and child not in parents:
                    children.append(child)
                if child2 not in children and child2 not in parents:
                    children.append(child2)
        else:
            for p1 in range(TOP_BEST):
                adj_matr = build_adjacency_matrix(parents[p1])
                comp_num = count_adjacency_components(adj_matr)[0]
                if comp_num == 2:
                    for i in range(10):
                        child = mutate(parents[p1], move_component=True)
                        if evaluate_fitness(child) > evaluate_fitness(parents[p1]) and child not in children and child not in parents:
                            children.append(child)
                        child2 = mutate(child)
                        if child2 not in children and child2 not in parents:
                            children.append(child2)
                else:
                    child = mutate(parents[p1])
                    if child not in children and child not in parents:
                        children.append(child)
        parents = select_parents(parents+children, POP_SIZE)
        if evaluate_fitness(parents[0]) > maxfit:
            last_update = epoch
            maxfit = evaluate_fitness(parents[0])
        epoch += 1
        if epoch - last_update > 350:  # start over if not succeeded after a long time
            print("Start over")
            print("Best outcome:")
            print_grid(construct_grid(parents[0]))
            population = [generate_random_grid() for _ in range(POP_SIZE)]
            parents = select_parents(population, num_parents=POP_SIZE)
            maxfit = float('-inf')
            epoch = 0
            last_update = 0

        # Uncomment if you need to see partial results
        # if epoch % 100 == 0:
        #     for k in range(1):
        #         print_grid(construct_grid(parents[k]))
        #         print()

    best_grid = construct_grid(parents[0])
    best_info = parents[0]
    maxfit = evaluate_fitness(parents[0])
    with open(f"/outputs/output{i}.txt", "w") as f:
        for word in words:
            x, y, t = best_info[word]
            t = (t + 1) % 2  # in my program 0 is vertical, 1 is horizontal, but the task requires it vice versa
            f.write(f'{x} {y} {t}\n')
    print_grid(best_grid)
    end_time = datetime.now()
    print(f'Done in {end_time - start_time}')
