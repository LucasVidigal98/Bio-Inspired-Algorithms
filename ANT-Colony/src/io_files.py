from os import sep


def read_file_dist(name_file):
    file = open(f'..{sep}dist{sep}{name_file}_dist.txt')
    lines = file.readlines()
    dist_tsp = list()

    for line in lines:
        if '#' in line:
            continue

        distance = list()
        for d in line.split():
            distance.append(int(d))
        dist_tsp.append(distance)

    return len(dist_tsp[0]), dist_tsp


def read_file_solution(name_file):
    try:
        file = open(f'..{sep}solution{sep}{name_file}_tsp.txt')
    except:
        return []

    lines = file.readlines()

    solution = list()

    for line in lines:
        if '#' in line:
            continue

        solution.append(int(line)-1)

    return solution
