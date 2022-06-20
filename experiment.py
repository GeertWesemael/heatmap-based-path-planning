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
from timefunct import random_time_between, random_time_between_, sec_to_hour_min_string

val = input("What experiment setup do you want to run? ")
if val == "1":
    print("Run easy setup")

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

    # spawn and move actors
    for i in range(3):
        start_time = hour_min_to_sec(9 + i, 50)
        end_time = hour_min_to_sec(10 + i, 10)
        for _ in range(20):
            a = actor.Actor.actor_at_zone(zone_b, random_time_between_(start_time, end_time), map1)
            a.walk_to_zone(zone_a)
            a.wait(random_time_between_(10, 600))
            a.walk_to_zone(zone_b)
            # add randomness to walk
            a.path.add_noise_to_path(1, map1)
            world1.add_actor(a)

    # test
    world1.plot_world()

    #total heatmap
    heatm = heatmap.Heatmap(world1, sample_rate=1, scale=1)
    heatm.visualize_heatmap()

    #moment heatmaps
    interval = hour_min_to_sec(0, 10)
    start = hour_min_to_sec(9, 30)
    end = hour_min_to_sec(13, 0)
    heatmaps = heatmap.heatmap_for_each_interval(world1, interval, start_time=start, end_time=end,
                                                 sample_rate=1, scale=1)
    heatmap.animate_heatmaps(heatmaps)

    r1 = robot.Robot(zone_d.get_random_location(),hour_min_to_sec(10,0),map1)
    r1.weighted_astar_path_plan(zone_c.get_random_location(),heatm,1)
    r1.evaluate_collisions(world1, 0.1)
    r1.path.plot_path(map1,"r1 10h global heatmap")

    r1 = robot.Robot(zone_d.get_random_location(),hour_min_to_sec(10,30),map1)
    r1.weighted_astar_path_plan(zone_c.get_random_location(),heatm,1)
    r1.evaluate_collisions(world1, 0.1)
    r1.path.plot_path(map1,"r1 10h30 global heatmap")

    r2 = robot.Robot(zone_d.get_random_location(),hour_min_to_sec(10,0),map1)
    r2.weighted_astar_path_plan_timeframes(zone_c.get_random_location(),heatmaps,1)
    r2.evaluate_collisions(world1, 0.1)
    r2.path.plot_path(map1,"r2 10h timeframed heatmap")

    r2 = robot.Robot(zone_d.get_random_location(),hour_min_to_sec(10,30),map1)
    r2.weighted_astar_path_plan_timeframes(zone_c.get_random_location(),heatmaps,1)
    r2.evaluate_collisions(world1, 0.1)
    r2.path.plot_path(map1,"r2 10h30 timeframed heatmap")
