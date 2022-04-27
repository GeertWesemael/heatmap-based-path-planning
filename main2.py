import numpy as np
import random

import heatmap
import map_
import path
import actor
import robot
import world
import astar
import zone
import createactors
import matplotlib.pyplot as plt

from timefunct import sec_to_hour, hour_min_to_sec

# CREATE MAP
matrix_map1 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
     0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
     0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
     0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0,
     0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0,
     0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0,
     0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
     0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
     0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
     1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0,
     0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0,
     0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
     0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1,
     1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1]]

map1 = map_.Map(matrix_map1)

# DEFINE ZONES
wc = zone.Zone("wc", "W", [(1, 7)])
office1 = zone.Zone("office1", "O",
                    [(1, 1), (2, 1), (3, 1), (4, 1), (1, 2), (2, 2), (3, 2), (4, 2), (1, 3), (3, 3), (4, 3), (1, 4),
                     (3, 4), (4, 4), (1, 5), (2, 5), (3, 5), (4, 5)])
office2 = zone.Zone("office2", "o",
                    [(6, 1), (7, 1), (8, 1), (9, 1), (6, 2), (7, 2), (8, 2), (9, 2), (6, 3), (7, 3), (8, 3), (9, 3),
                     (6, 4), (9, 4), (6, 5), (7, 5), (8, 5), (9, 5)])
lounge = zone.Zone("lounge", "L",
                   [(35, 8), (36, 8), (37, 8), (38, 8), (39, 8), (40, 8), (41, 8), (42, 8), (35, 9), (36, 9), (42, 9),
                    (35, 10), (36, 10), (37, 10), (38, 10), (39, 10), (40, 10), (41, 10), (42, 10), (35, 11), (36, 11),
                    (37, 11), (38, 11), (39, 11), (40, 11), (41, 11), (42, 11), (35, 12), (36, 12), (37, 12), (38, 12),
                    (39, 12), (40, 12), (41, 12), (36, 13)])
inbound = zone.Zone("inbound", "I",
                    [(n, 15) for n in range(34, 42 + 1)] + [(n, 16) for n in range(34, 42 + 1)] + [(n, 17) for n in
                                                                                                   range(34,
                                                                                                         42 + 1)] + [
                        (n, 18) for n in range(34, 42 + 1)])
outbound = zone.Zone("outbound", "E",
                     [(30, n) for n in range(1, 7 + 1)] + [(31, n) for n in range(1, 7 + 1)] + [(32, n) for n in
                                                                                                range(1, 7 + 1)] + [
                         (33, n) for n in range(1, 7 + 1)])
storage = zone.Zone("storage", "S",
                    [(n, 9) for n in range(4, 15 + 1)] + [(n, 9) for n in range(18, 29 + 1)] + [(n, 12) for n in
                                                                                                range(4, 15 + 1)] + [
                        (n, 12) for n in range(18, 29 + 1)] + [(n, 13) for n in range(4, 15 + 1)] + [(n, 13) for n in
                                                                                                     range(18,
                                                                                                           29 + 1)] + [
                        (n, 16) for n in range(4, 15 + 1)] + [(n, 16) for n in range(18, 29 + 1)] + [(n, 17) for n in
                                                                                                     range(4,
                                                                                                           15 + 1)] + [
                        (n, 17) for n in range(18, 29 + 1)])
packing = zone.Zone("packing", "P", [(15, 4), (22, 4), (24, 4), (28, 4), (18, 3), (19, 7), (26, 2)])
door = zone.Zone("door", "D", [(13, 0)])

zones = [wc, office1, office2, lounge, inbound, outbound, storage, packing, door]
zone.print_zone(map1, zones)
all_zones = zone.Zone.combined_zones(zones)
zone.print_zone(map1, [all_zones])

# CREATE WORLD & ACTORS
world1 = world.World(map1)
receiver = createactors.actor_with_job("receiver", map1, zones)
packer = createactors.actor_with_job("packer", map1, zones)
forklift = createactors.actor_with_job("forklift", map1, zones)
shipper = createactors.actor_with_job("shipper", map1, zones)

world1.add_actor(receiver)
world1.add_actor(packer)
world1.add_actor(forklift)
world1.add_actor(shipper)
world1.plot_world()

# PRINT HEATMAP
# heatm = heatmap.heatmap(world1,start_time=hour_min_to_sec(14,0),end_time=hour_min_to_sec(15,0), sample_rate=0.1, scale=1)
heatm = heatmap.heatmap(world1, sample_rate=1, scale=1)
heatmap.visualize_heatmap(heatm)

r = robot.Robot((31, 18), hour_min_to_sec(11, 0), map1)
r.astar_path_plan((1, 1))
r.path.plot_path(map1)

r = robot.Robot((31, 18), hour_min_to_sec(11, 0), map1)
r.weighted_astar_path_plan((1, 1), heatm, 1)
r.path.plot_path(map1)

r = robot.Robot((31, 18), hour_min_to_sec(11, 0), map1)
r.weighted_astar_path_plan((1, 1), heatm, 0.01)
r.path.plot_path(map1)

r = robot.Robot((31, 18), hour_min_to_sec(11, 0), map1)
r.weighted_astar_path_plan((1, 1), heatm, 0.001)
r.path.plot_path(map1)

r = robot.Robot((31, 18), hour_min_to_sec(11, 0), map1)
r.weighted_astar_path_plan((1, 1), heatm, 0.0001) #switches path
r.path.plot_path(map1)

r = robot.Robot((31, 18), hour_min_to_sec(11, 0), map1)
r.weighted_astar_path_plan((1, 1), heatm, 0.00001)
r.path.plot_path(map1)
