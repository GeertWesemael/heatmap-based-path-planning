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

scenario = 2
amount_actors = 20

# create map and zones
matrix_map1 = [[1, 1, 1, 1, 1, 1, 1, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 1, 1, 1, 1, 1, 0, 1],
               [1, 0, 1, 0, 0, 0, 1, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 1, 0, 0, 0, 1, 0, 1],
               [0, 0, 1, 1, 1, 1, 1, 0, 0],
               [1, 0, 1, 0, 0, 0, 1, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 1, 0, 0, 0, 1, 0, 1],
               [1, 0, 1, 1, 1, 1, 1, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 1, 1, 1, 1, 1, 1, 0, 1]]
map1 = map_.Map(matrix_map1)
zone_a = zone.Zone("zone_a", "A", [(3,3) , (3,4) , (3,5) , (4,3) , (4,4) , (4,5) , (5,3) , (5,4) , (5,5)])
zone_b = zone.Zone("zone_b", "B", [(3,7) , (3,8) , (3,9) , (4,7) , (4,8) , (4,9) , (5,7) , (5,8) , (5,9)])
zone_c = zone.Zone("zone_c", "C", [(7,0)])
zone_d = zone.Zone("zone_d", "D", [(7,12)])
zone_e = zone.Zone("zone_e", "E", [(0,6)])
zone_f = zone.Zone("zone_f", "F", [(8,6)])


zones = [zone_a, zone_b, zone_c, zone_d, zone_e, zone_f]
zone.print_zone(map1, zones)
all_zones = zone.Zone.combined_zones(zones)
world1 = world.World(map1)

# creating diff worlds
list_of_worlds = []
# CREATE WORLDS
for j in range(1000):
    world1 = world.World(map1)

    if scenario == 1:
        profession_zone = None
        door_zone = None
        if j % 2 == 0:
            profession_zone = zone_a
            door_zone = zone_c
        else:
            profession_zone = zone_b
            door_zone = zone_d

        # amount of actors
        for _ in range(amount_actors):
            a = actor.Actor.actor_at_zone(door_zone, random_time_between(9, 45, 10, 15), map1)
            a.walk_to_zone(profession_zone)
            a.wait(random_time_between(0, 5, 0, 10))
            a.walk_to_zone(door_zone)
            a.path.add_noise_to_path(0.5, map1)
            world1.add_actor(a)

    else:
        dense_zone = zone_a
        dense_door = zone_c
        sparse_zone = zone_b
        sparse_door = zone_d
        #amount of actors
        for _ in range(amount_actors):
            #dense zone
            a = actor.Actor.actor_at_zone(dense_door, random_time_between(9, 40, 10, 20), map1)
            a.walk_to_zone(dense_zone)
            a.wait(random_time_between(0, 1, 0, 2))
            a.walk_to_zone(dense_door)
            a.path.add_noise_to_path(0.5, map1)
            world1.add_actor(a)
            #sparse zone
            a = actor.Actor.actor_at_zone(sparse_door, random_time_between(9, 59, 10, 1), map1)
            a.walk_to_zone(sparse_zone)
            a.wait(random_time_between(0, 1, 0, 2))
            a.walk_to_zone(sparse_door)
            a.path.add_noise_to_path(0.5, map1)
            world1.add_actor(a)

    list_of_worlds.append(world1)
    print("World " + str(j) + " was created!")

filename = 'hard_scenario_worlds_' + str(scenario) +'_'+str(amount_actors)
outfile = open(filename,'wb')
pickle.dump(list_of_worlds,outfile)
outfile.close()