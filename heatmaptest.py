import numpy as np
import random
import map_
import path
import actor
import world
import astar
import zone
import heatmap
from timefunct import random_time_between_
import robot

matrix_map1 = [[0, 0, 0, 0, 0, 0, 1, 1],
               [0, 1, 1, 1, 0, 0, 0, 1],
               [0, 1, 0, 0, 0, 0, 0, 1],
               [0, 1, 0, 0, 0, 0, 0, 0],
               [0, 1, 0, 0, 0, 0, 0, 0],
               [0, 1, 0, 0, 0, 0, 0, 1],
               [0, 1, 1, 1, 0, 0, 0, 1],
               [0, 0, 0, 0, 0, 0, 1, 1]]

map1 = map_.Map(matrix_map1)

a_zone = zone.Zone("a", "A", [(4, 0), (5, 0)])
b_zone = zone.Zone("b", "B", [(7, 3), (7, 4)])
c_zone = zone.Zone("c", "C", [(4, 7), (5, 7)])
d_zone = zone.Zone("d", "D", [(2, 2), (2, 3), (3, 2), (3, 3)])
e_zone = zone.Zone("e", "E", [(2, 4), (2, 5), (3, 4), (3, 5)])
zones = [a_zone, b_zone, c_zone, d_zone, e_zone]
zone.print_zone(map1, zones)

world1 = world.World(map1)

for _ in range(10):
    actorA = actor.Actor.actor_at_zone(b_zone, random_time_between_(0, 120), map1)
    actorA.walk_to_zone(d_zone)
    actorA.wait(random_time_between_(5, 10))
    actorA.walk_to_zone(b_zone)
    world1.add_actor(actorA)

for _ in range(10):
    actorA = actor.Actor.actor_at_zone(b_zone, random_time_between_(240, 360), map1)
    actorA.walk_to_zone(e_zone)
    actorA.wait(random_time_between_(5, 10))
    actorA.walk_to_zone(b_zone)
    world1.add_actor(actorA)

# for _ in range(10):
#     actorA = actor.Actor.actor_at_zone(e_zone, random_time_between_(240,360), map1)
#     actorA.walk_to_zone(d_zone)
#     actorA.wait(random_time_between_(5,10))
#     actorA.walk_to_zone(e_zone)
#     world1.add_actor(actorA)

# matrix_map1 = [[0, 0, 0, 0, 0, 0, 0, 0],
#                [0, 0, 0, 0, 0, 0, 0, 0],
#                [0, 0, 0, 0, 0, 0, 0, 0],
#                [0, 0, 0, 0, 0, 0, 0, 0],
#                [0, 0, 0, 0, 0, 0, 0, 0],
#                [0, 0, 0, 0, 0, 0, 0, 0],
#                [0, 0, 0, 0, 0, 0, 0, 0],
#                [0, 0, 0, 0, 0, 0, 0, 0]]
#
# map1 = map_.Map(matrix_map1)
# world1 = world.World(map1)

# for _ in range(10):
#     actorA = actor.Actor.actor_at((0,0), random_time_between_(0,120), map1)
#     actorA.walk_to((7,7))
# #     actorA.wait(random_time_between_(5,10))
# #     actorA.walk_to((0,0))
#     world1.add_actor(actorA)
#
# for _ in range(10):
#     actorA = actor.Actor.actor_at((0,4), random_time_between_(0,120), map1)
#     actorA.walk_to((4,7))
#     world1.add_actor(actorA)
#
# for _ in range(10):
#     actorA = actor.Actor.actor_at((4,1),random_time_between_(0,120), map1)
#     actorA.walk_to((7,1))
#     world1.add_actor(actorA)

heatm = heatmap.heatmap(world1,None,None, sample_rate=0.1, scale=1)
heatmap.visualize_heatmap(heatm)

heatm1 = heatmap.heatmap(world1,0,120, sample_rate=0.1, scale=1)
heatmap.visualize_heatmap(heatm1)

heatm2 = heatmap.heatmap(world1,240,360, sample_rate=0.1, scale=1)
heatmap.visualize_heatmap(heatm2)

r = robot.Robot((4, 7), 0, map1)
r.astar_path_plan((4, 0))
r.path.plot_path(map1)

r2 = robot.Robot((4, 7), 0, map1)
r2.weighted_astar_path_plan((4, 0), heatm, 0.5)
r2.path.plot_path(map1)
