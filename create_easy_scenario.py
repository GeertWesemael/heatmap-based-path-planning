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
matrix_map1 = [[1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
               [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
               [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
               [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
               [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
               [1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
               [1, 1, 1, 1, 1, 1, 0, 1, 1, 1]]
map1 = map_.Map(matrix_map1)
zone_a = zone.Zone("zone_a", "A", [(3, 3), (3, 4), (4, 3), (4, 4)])
zone_b = zone.Zone("zone_b", "B", [(9, 2), (9, 3), (9, 4), (9, 5)])
zone_c = zone.Zone("zone_c", "C", [(6, 0)])
zone_d = zone.Zone("zone_d", "D", [(6, 7)])
zones = [zone_a, zone_b, zone_c, zone_d]
zone.print_zone(map1, zones)
all_zones = zone.Zone.combined_zones(zones)

world1 = world.World(map1)

# creating diff worlds
list_of_worlds = []
# CREATE WORLDS
for j in range(100):
    world1 = world.World(map1)
    # ADD ACTORS TO WORLD
    for i in range(3):
        start_time = hour_min_to_sec(9 + i, 50)
        end_time = hour_min_to_sec(10 + i, 10)
        for _ in range(10):
            a = actor.Actor.actor_at_zone(zone_b, random_time_between_(start_time, end_time), map1)
            a.walk_to_zone(zone_a)
            a.wait(random_time_between_(10, 600))
            a.walk_to_zone(zone_b)
            # add randomness to walk
            a.path.add_noise_to_path(0.5, map1)
            world1.add_actor(a)
    list_of_worlds.append(world1)
    print("World " + str(j) + " was created!")

filename = 'easy_scenario_worlds'
outfile = open(filename,'wb')
pickle.dump(list_of_worlds,outfile)
outfile.close()