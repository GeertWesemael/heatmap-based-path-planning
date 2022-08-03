import pickle
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

val = input("What experiment setup do you want to run? ")
print("Run easy setup")
filename = 'easy_scenario_worlds_1_'
infile = open(filename, 'rb')
list_of_worlds = pickle.load(infile)
infile.close()
print("Unpickled")

world1 = list_of_worlds[0]
world_test = list_of_worlds[99]
world_tests = list_of_worlds[10:100]
print(len(world_tests))
list_of_worlds = list_of_worlds[0:10]
print(len(list_of_worlds))
# test
world1.plot_world()

# total heatmap
heatm = heatmap.Heatmap(world1, sample_rate=1, scale=1)
heatm.visualize_heatmap()

# moment heatmaps
interval = hour_min_to_sec(0, 10)
start = hour_min_to_sec(9, 30)
end = hour_min_to_sec(13, 0)
heatmaps = heatmap.heatmap_for_each_interval(world1, interval, start_time=start, end_time=end,
                                             sample_rate=1, scale=1)
# heatmap.animate_heatmaps(heatmaps)

print("heatmap stuff done")

prob_heatmaps = prob_heatmap.heatmap_for_each_interval(list_of_worlds, interval, start_time=start, end_time=end,
                                                       sample_rate=1, scale=1)
# prob_heatmap.animate_heatmaps(prob_heatmaps)

print("prob heatmap stuff done")

map1 = world1.get_map()
zone_c = zone.Zone("zone_c", "C", [(6, 0)])
zone_d = zone.Zone("zone_d", "D", [(6, 7)])
start_loc_robot = zone_d.get_random_location()
end_loc_robot = zone_c.get_random_location()

r1 = robot.Robot(start_loc_robot, hour_min_to_sec(10, 0), map1)
r1.weighted_astar_path_plan(end_loc_robot, heatm, 1)
r1.evaluate_collisions_worlds(world_tests, 0.1)
r1.path.plot_path(map1, "r1 10h global heatmap")

r1 = robot.Robot(start_loc_robot, hour_min_to_sec(10, 30), map1)
r1.weighted_astar_path_plan(end_loc_robot, heatm, 1)
r1.evaluate_collisions_worlds(world_tests, 0.1)
r1.path.plot_path(map1, "r1 10h30 global heatmap")

r2 = robot.Robot(start_loc_robot, hour_min_to_sec(10, 0), map1)
r2.weighted_astar_path_plan_timeframes(end_loc_robot, heatmaps, 1)
r1.evaluate_collisions_worlds(world_tests, 0.1)
r2.path.plot_path(map1, "r2 10h timeframed heatmap")

r2 = robot.Robot(start_loc_robot, hour_min_to_sec(10, 30), map1)
r2.weighted_astar_path_plan_timeframes(end_loc_robot, heatmaps, 1)
r1.evaluate_collisions_worlds(world_tests, 0.1)
r2.path.plot_path(map1, "r2 10h30 timeframed heatmap")

r3 = robot.Robot(start_loc_robot, hour_min_to_sec(10, 0), map1)
r3.weighted_astar_path_plan_timeframes(end_loc_robot, heatmaps, 1)
r1.evaluate_collisions_worlds(world_tests, 0.1)
r3.path.plot_path(map1, "r3 10h prob timeframed heatmap")

r3 = robot.Robot(start_loc_robot, hour_min_to_sec(10, 30), map1)
r3.weighted_astar_path_plan_timeframes(end_loc_robot, heatmaps, 1)
r1.evaluate_collisions_worlds(world_tests, 0.1)
r3.path.plot_path(map1, "r3 10h30 prob timeframed heatmap")

r4 = robot.Robot(start_loc_robot, hour_min_to_sec(10, 0), map1)
r4.plan_path_waiting_at_encounter(world1, end_loc_robot, 0.1)
r1.evaluate_collisions_worlds(world_tests, 0.1)
r4.path.plot_path(map1, "r4 10h wait")

r4 = robot.Robot(start_loc_robot, hour_min_to_sec(10, 30), map1)
r4.plan_path_waiting_at_encounter(world1, end_loc_robot, 0.1)
r1.evaluate_collisions_worlds(world_tests, 0.1)
r4.path.plot_path(map1, "r4 10h30 wait")