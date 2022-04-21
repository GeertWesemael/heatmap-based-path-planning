import numpy as np
import random
import map
import path
import actor
import world
import astar

matrix_map1 = [[1, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 0, 0, 1, 0, 0, 1],
               [1, 0, 0, 0, 1, 0, 0, 1],
               [1, 0, 0, 0, 1, 0, 0, 1],
               [1, 0, 0, 1, 1, 0, 0, 1],
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

# map1 = map.Map(matrix_map1)
# print("get_locations_of: ", end='')
# print(map1.get_locations_of(1))
# n = (1, 1)
# print("get_free_neighbors_coordinates at " + str(n) + " is :", end='')
# print(map1.get_free_neighbors_coordinates(n))
#
# actor1 = actor.Actor.random_walking_actor(0, 10, map1)
# actor1.path.print_path(map1)
#
# path2 = path.Path({4: (1, 1), 5: (1, 2), 6: (1, 1)})
# actor2 = actor.Actor(path2, map1)
#
# map1.print_map()
#
# world1 = world.World(map1)
# world1.add_actor(actor1)
# world1.add_actor(actor2)
# world1.print_world()
# print(world1.free_co_list(6))
# print(world1.is_free(6, (1, 1)))
#
# path3 = astar.path_to_path_object(astar.a_star(map1, (1, 1), (6, 1), 1), 0)
# path3.print_path(map1)
# path3.add_to_path(path2)
# path3.print_path(map1)

# actor3 = actor.Actor(path3, map1)
# world1.add_actor(actor3)
# world1.print_world()

map1 = map.Map(matrix_map1)
map1.print_map()

actorA = actor.Actor.actor_at((1,1), 1, map1)
actorA.walk_to((6,1))
actorA.wait(4)
actorA.walk_to((3,3))
actorA.wait_till(30)
actorA.walk_to((1,1))

world1 = world.World(map1)

world1.add_actor(actorA)
world1.print_world()

