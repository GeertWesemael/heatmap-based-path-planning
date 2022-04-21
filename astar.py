import map
import heapq
from collections import defaultdict

import path


def get_neighbors(coordinate, map):
    return map.get_free_neighbors_coordinates(coordinate)


def h_cost(current, end):
    (xc, yc) = current
    (xe, ye) = end
    return abs(xe - xc) + abs(ye - yc)


def g_cost(current, start):
    (xc, yc) = current
    (xs, ys) = start
    return abs(xs - xc) + abs(ys - yc)


def reconstruct_path(came_from, current_co):
    final_path = [current_co]
    while current_co in came_from.keys():
        current_co = came_from[current_co]
        final_path.insert(0, current_co)
    return final_path


def a_star(map, start_co, end_co, distance=1):
    f_score = 0 + h_cost(start_co, end_co)
    open_list = [(f_score, start_co)]
    heapq.heapify(open_list)

    came_from = {}

    g_score = defaultdict(lambda: 1000000000)
    g_score[start_co] = 0

    f_score = defaultdict(lambda: 1000000000)
    f_score[start_co] = h_cost(start_co, end_co)

    while len(open_list) != 0:
        (f_score_current, current_co) = heapq.heappop(open_list)
        if current_co == end_co:
            return reconstruct_path(came_from, current_co)

        for neighbor_co in get_neighbors(current_co, map):
            new_g_score = g_score[current_co] + distance
            if new_g_score < g_score[neighbor_co]:
                came_from[neighbor_co] = current_co
                g_score[neighbor_co] = new_g_score
                new_f_score = new_g_score + h_cost(neighbor_co, end_co)
                f_score[neighbor_co] = new_f_score

                if neighbor_co not in open_list:
                    heapq.heappush(open_list, (new_f_score, neighbor_co))
    print("Error: goal never reached")


def path_to_path_object(path_in_list, start_time):
    path_dict = {}
    for e in path_in_list:
        path_dict[start_time] = e
        start_time = start_time + 1
    return path.Path(path_dict)
