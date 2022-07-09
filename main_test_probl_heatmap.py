import numpy as np
import random
import map_
import path
import actor
import prob_heatmap
import robot
import world
import astar
import zone
import actor

matrix_map1 = [[1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
               [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
               [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
               [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
               [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
               [1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
               [1, 1, 1, 1, 1, 1, 0, 1, 1, 1]]

### TEST ERRODE ###
map1 = map_.Map(matrix_map1)
map1_borders = map_.Map(map1.get_borders())
map1_borders.matrix = map1.get_borders()
list_of_worlds = []

world1 = world.World(map1)
a = actor.Actor.actor_at((1,1),0, map1)
a.walk_to((1,6))
a.path.insert_waiting(2,5)
world1.add_actor(a)
list_of_worlds.append(world1)

# world1 = world.World(map1)
# a = actor.Actor.actor_at((1,1),0, map1)
# a.walk_to((1,6))
# # a.path.add_noise_to_path(2,map1)
# world1.add_actor(a)
# list_of_worlds.append(world1)

prob_heatmaps = prob_heatmap.heatmap_for_each_interval(list_of_worlds, 10, start_time=0, end_time=30,
                                                       sample_rate=1, scale=1)
prob_heatmap.animate_heatmaps(prob_heatmaps)

#percentage of time
# divided by the amount of time not by the sample rate, ami right?
