import numpy as np
import random
import map
import path
import actor

matrix_map1 = [[1, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 1],
               [1, 1, 1, 1, 1, 1, 1, 1]]

path_a = {
    4: (1, 1),
    5: (2, 2),
    6: (3, 3),
    7: (4, 4),
    12: (4, 4),
    14: (6, 4)
}

map1 = map.Map(matrix_map1)
print("get_locations_of: ", end='')
print(map1.get_locations_of(1))
n = (1,1)
print("get_free_neighbors_coordinates at "+ str(n)+ " is :", end='')
print(map1.get_free_neighbors_coordinates(n))


actor1 = actor.Actor.random_walking_actor(0, 10, map1)
actor1.path.print_path(map1)

# actor2 = Actor.random_walking_actor(0, 10, map1)
# print(actor2.path)

map1.print_map()
