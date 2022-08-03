import numpy as np
import random
import heatmap
import map_
import path
import actor
import prob_heatmap
import robot
import world
import astar
import zone
import createactors
import matplotlib.pyplot as plt
from timefunct import sec_to_hour, hour_min_to_sec
from timefunct import random_time_between, random_time_between_, sec_to_hour_min_string
import pickle

random.seed(1)

# create map and zones
matrix_map1 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
               [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1]]
map1 = map_.Map(matrix_map1)
zone_a = zone.Zone("zone_a", "A", [(2, 2), (3, 2), (2, 3), (3, 3), (2,4), (3,4), (2,5), (3,5), (2,6), (3,6)])
zone_b = zone.Zone("zone_b", "B", [(7, 2), (8, 2), (7, 3), (8, 3), (7,4), (8,4), (7,5), (8,5), (7,6), (8,6)])
zone_c = zone.Zone("zone_c", "C", [(14, 2), (15, 2), (14, 3), (15, 3), (14,4), (15,4), (14,5), (15,5), (14,6), (15,6)])
door = zone.Zone("door", "D", [(11, 0), (11, 8)])

zones = [zone_a, zone_b, zone_c, door]
zone.print_zone(map1, zones)
all_zones = zone.Zone.combined_zones(zones)

world1 = world.World(map1)

# creating diff worlds
list_of_worlds = []
# CREATE WORLDS
for j in range(100):
    world1 = world.World(map1)
    # ADD ACTORS TO WORLD
    r = random.uniform(0,1)
    profession_zone = None
    if r > 0.9:
        profession_zone = zone_a
    if 0.9 >= r > 0.45:
        profession_zone = zone_b
    if r <= 0.45:
        profession_zone = zone_c

    for _ in range(5):
        a = actor.Actor.actor_at_zone(door, random_time_between(8, 50, 9, 10), map1)
        stop_time = random_time_between(9, 50, 10, 10)
        # first work shift
        while a.path.get_end_time() <= stop_time:
            a.walk_to_zone(profession_zone)
            r = random_time_between(0, 1, 0, 5)
            a.wait(r)
        a.walk_to_zone(door)
        a.path.add_noise_to_path(0.5, map1)
        world1.add_actor(a)

    list_of_worlds.append(world1)
    print("World " + str(j) + " was created!")

filename = 'hard_scenario_worlds_old'
outfile = open(filename,'wb')
pickle.dump(list_of_worlds,outfile)
outfile.close()