import numpy as np
import random
import map_
import path
import actor
import world
import astar
import zone

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
    14: (6, 4),
    15: (6, 4.5)
}

map1 = map_.Map(matrix_map1)

test_pad = path.Path(path_a)
assert (test_pad.get_location_at(16) is None)
assert (test_pad.get_location_at(2) is None)
assert (test_pad.get_location_at(6) == (3, 3))
assert (test_pad.get_location_at(6.5) == (3.5, 3.5))
assert (test_pad.get_location_at(12.5) == (4.5, 4))
assert (test_pad.get_location_at(10) == (4, 4))
assert (test_pad.get_location_at(15) == (6, 4.5))
# test_pad.print_path(map1)
test_pad.plot_path(map1)

test_pad_2 = path.Path.stand_still(5, 10, (3, 4))
assert (test_pad_2.get_location_at(5) == (3, 4))
assert (test_pad_2.get_location_at(10) == (3, 4))
assert (test_pad_2.get_location_at(7) == (3, 4))
assert (test_pad_2.get_location_at(7) == (3, 4))
assert (test_pad_2.get_location_at(4.5) is None)
assert (test_pad_2.get_location_at(11) is None)

a_zone = zone.Zone("a","A", [(2,1),(3,1)])
b_zone = zone.Zone("b","B",[(5,1),(6,1)])
c_zone = zone.Zone("c","C", [(3,3)])
zones = [a_zone,b_zone,c_zone]

actorA = actor.Actor.actor_at((1, 1), 1.5, map1)
actorA.walk_to((1, 6))
actorA.wait(5)
actorA.walk_to((6, 6))
actorA.wait_till(30)
actorA.walk_to((6, 2))

actorB = actor.Actor.actor_at((2, 5), 50, map1)
actorB.walk_to_zone(b_zone)
actorB.wait(5)
actorB.walk_to_zone(c_zone)
actorB.wait_till(100)
actorB.walk_to_zone(zone.Zone.combined_zones(zones))
print(actorB.path.path_list)

actorA.plot_path()

world1 = world.World(map1)
world1.add_actor(actorA)
world1.add_actor(actorB)
world1.plot_world()

zone.print_zone(map1,zones)