import pickle

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
from openpyxl import load_workbook

##################################

val = 1
experiment = "prob_tf"  # total,tf,prob_tf,wait

########### easy setup ###########
robot_start_time = hour_min_to_sec(10, 0)
interval = 1 #hour_min_to_sec(0, 1)
start = hour_min_to_sec(9, 30)
end = hour_min_to_sec(11, 0)
start_loc_robot = (6, 7)
end_loc_robot = (6, 0)

# ########### hard setup ###########
# robot_start_time = hour_min_to_sec(9, 30)
# interval = hour_min_to_sec(0, 10)
# start = hour_min_to_sec(8, 30)
# end = hour_min_to_sec(10, 30)
# start_loc_robot = (0, 4)
# end_loc_robot = (17, 4)

###################################
# adjustable param
a_star_weight_factor = 90
amount_of_sample_worlds = 10
amount_of_test_worlds = 90

###################################
# standard parameters (don't touch)
sample_r_col = 0.1
sample_r_wait = 0.1
distance_robot = 2
wait_time = 5
###################################

filename = ''
if val == 1:
    print("Run easy setup")
    filename = 'easy_scenario_worlds'

if val == 2:
    print("Run medium setup")
    filename = 'medium_scenario_worlds'

if val == 3:
    print("Run hard setup")
    filename = 'hard_scenario_worlds'

if filename == '':
    print("No correct value given")

# Unpickle
infile = open(filename, 'rb')
list_of_worlds = pickle.load(infile)
infile.close()
print("Unpickled")

# read all test worlds
world1 = list_of_worlds[0]
world_test = list_of_worlds[amount_of_sample_worlds + amount_of_test_worlds - 1]
world_tests = list_of_worlds[amount_of_sample_worlds:amount_of_sample_worlds + amount_of_test_worlds]
list_of_worlds = list_of_worlds[0:amount_of_sample_worlds]
print(f"number of worlds used: {len(list_of_worlds)} / number of test worlds: {len(world_tests)}")

print("plotting the world")
# world1.plot_world()

coll = None
time = None
r1 = None
heatm = None
heatmaps = None
prob_heatmaps = None

if experiment == "total":
    print("total heatmap")
    heatm = heatmap.Heatmap(world1, sample_rate=1, scale=1)
    # heatm.visualize_heatmap()

if experiment == "tf":
    print("moment heatmap")
    heatmaps = heatmap.heatmap_for_each_interval(world1, interval, start_time=start, end_time=end, sample_rate=1,
                                                 scale=1)
    # heatmap.animate_heatmaps(heatmaps)

if experiment == "prob_tf":
    print("moment prob_heatmap")
    prob_heatmaps = prob_heatmap.heatmap_for_each_interval(list_of_worlds, interval, start_time=start, end_time=end,
                                                           sample_rate=1, scale=1)
    # prob_heatmap.animate_heatmaps(prob_heatmaps)


#################################################################################
for value in range(1, 50):
    print("start value " + str(value))
    a_star_weight_factor = value

    print("finding robot paths")
    map1 = world1.get_map()

    if experiment == "total":
        r1 = robot.Robot(start_loc_robot, robot_start_time, map1)
        r1.weighted_astar_path_plan(end_loc_robot, heatm, a_star_weight_factor)
        coll = r1.evaluate_collisions_worlds(world_tests, sample_r_col)
        time = r1.evaluate_time()
        #r1.path.plot_path(map1, "r1 10h global heatmap")

    if experiment == "tf":
        r1 = robot.Robot(start_loc_robot, robot_start_time, map1)
        r1.weighted_astar_path_plan_timeframes(end_loc_robot, heatmaps, a_star_weight_factor)
        coll = r1.evaluate_collisions_worlds(world_tests, sample_r_col)
        time = r1.evaluate_time()
        #r1.path.plot_path(map1, "r2 10h timeframed heatmap")

    if experiment == "prob_tf":
        r1 = robot.Robot(start_loc_robot, robot_start_time, map1)
        r1.weighted_astar_path_plan_timeframes(end_loc_robot, prob_heatmaps, a_star_weight_factor)
        coll = r1.evaluate_collisions_worlds(world_tests, sample_r_col)
        time = r1.evaluate_time()
        #r1.path.plot_path(map1, "r3 10h prob timeframed heatmap")

    if experiment == "wait":
        r1 = robot.Robot(start_loc_robot, robot_start_time, map1)
        r1.plan_path_waiting_at_encounter(world1, end_loc_robot, sample_r_wait, distance_robot, wait_time)
        coll = r1.evaluate_collisions_worlds(world_tests, sample_r_col)
        time = r1.evaluate_time()
        #r1.path.plot_path(map1, "r4 10h wait")

    # Write data to TXT file
    # Open a file with access mode 'a'
    file_object = open('results.txt', 'a')
    # Append 'hello' at the end of file
    file_object.write(f'world: {val}, start: {sec_to_hour_min_string(start)}, end: {sec_to_hour_min_string(end)}, '
                      f'interval: {sec_to_hour_min_string(interval)}, r_start: {sec_to_hour_min_string(robot_start_time)}, '
                      f'wf: {a_star_weight_factor}, s_w: {amount_of_sample_worlds}, t_w: {amount_of_test_worlds}, '
                      f'exp: {experiment}, coll: {coll}, time: {time}')
    file_object.write('\n')
    # Close the file
    file_object.close()

    # eddit spreadsheet
    workbook = load_workbook(filename="results.xlsx")

    sheet = workbook.active
    new_row = sheet.max_row + 1

    sheet.cell(row=new_row, column=1).value = val
    sheet.cell(row=new_row, column=2).value = sec_to_hour_min_string(start)
    sheet.cell(row=new_row, column=3).value = sec_to_hour_min_string(end)
    sheet.cell(row=new_row, column=4).value = sec_to_hour_min_string(interval)
    sheet.cell(row=new_row, column=5).value = sec_to_hour_min_string(robot_start_time)
    sheet.cell(row=new_row, column=6).value = a_star_weight_factor
    sheet.cell(row=new_row, column=7).value = amount_of_sample_worlds
    sheet.cell(row=new_row, column=8).value = amount_of_test_worlds
    sheet.cell(row=new_row, column=9).value = experiment
    sheet.cell(row=new_row, column=10).value = coll
    sheet.cell(row=new_row, column=11).value = time
    sheet.cell(row=new_row, column=12).value = str(r1.path.path_list)

    workbook.save(filename="results.xlsx")

# r1 = robot.Robot(start_loc_robot, hour_min_to_sec(10, 0), map1)
# r1.weighted_astar_path_plan(end_loc_robot, heatm, a_star_weight_factor)
# r1.evaluate_collisions_worlds(world_tests, sample_r_col)
# r1.evaluate_time()
# r1.path.plot_path(map1, "r1 10h global heatmap")
#
# r1 = robot.Robot(start_loc_robot, hour_min_to_sec(10, 30), map1)
# r1.weighted_astar_path_plan(end_loc_robot, heatm, a_star_weight_factor)
# r1.evaluate_collisions_worlds(world_tests, sample_r_col)
# r1.evaluate_time()
# r1.path.plot_path(map1, "r1 10h30 global heatmap")
#
# r2 = robot.Robot(start_loc_robot, hour_min_to_sec(10, 0), map1)
# r2.weighted_astar_path_plan_timeframes(end_loc_robot, heatmaps, a_star_weight_factor)
# r2.evaluate_collisions_worlds(world_tests, sample_r_col)
# r2.evaluate_time()
# r2.path.plot_path(map1, "r2 10h timeframed heatmap")
#
# r2 = robot.Robot(start_loc_robot, hour_min_to_sec(10, 30), map1)
# r2.weighted_astar_path_plan_timeframes(end_loc_robot, heatmaps, a_star_weight_factor)
# r2.evaluate_collisions_worlds(world_tests, sample_r_col)
# r2.evaluate_time()
# r2.path.plot_path(map1, "r2 10h30 timeframed heatmap")
#
# r3 = robot.Robot(start_loc_robot, hour_min_to_sec(10, 0), map1)
# r3.weighted_astar_path_plan_timeframes(end_loc_robot, heatmaps, a_star_weight_factor)
# r3.evaluate_collisions_worlds(world_tests, sample_r_col)
# r3.evaluate_time()
# r3.path.plot_path(map1, "r3 10h prob timeframed heatmap")
#
# r3 = robot.Robot(start_loc_robot, hour_min_to_sec(10, 30), map1)
# r3.weighted_astar_path_plan_timeframes(end_loc_robot, heatmaps, a_star_weight_factor)
# r3.evaluate_collisions_worlds(world_tests, sample_r_col)
# r3.evaluate_time()
# r3.path.plot_path(map1, "r3 10h30 prob timeframed heatmap")
#
# r4 = robot.Robot(start_loc_robot, hour_min_to_sec(10, 0), map1)
# r4.plan_path_waiting_at_encounter(world1, end_loc_robot, sample_r_wait)
# r4.evaluate_collisions_worlds(world_tests, sample_r_col)
# r4.evaluate_time()
# r4.path.plot_path(map1, "r4 10h wait")
#
# r4 = robot.Robot(start_loc_robot, hour_min_to_sec(10, 30), map1)
# r4.plan_path_waiting_at_encounter(world1, end_loc_robot, sample_r_wait)
# r4.evaluate_collisions_worlds(world_tests, sample_r_col)
# r4.evaluate_time()
# r4.path.plot_path(map1, "r4 10h30 wait")

# factor of heatmaps??
# sample rate of prob heatmap??
# sample rate of other heatmap??
#
# if val == "2":
#     print("Run medium (warehouse) setup")
#
#     # create map and zones
#     matrix_map1 = [
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
#          0,
#          0, 0, 0, 0, 0, 0],
#         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
#          0,
#          0, 0, 0, 0, 0, 0],
#         [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
#          0,
#          0, 0, 0, 0, 0, 0],
#         [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0,
#          0,
#          0, 0, 0, 0, 0, 0],
#         [1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0,
#          0,d
#          0, 0, 0, 0, 0, 0],
#         [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0,
#          0,
#          0, 0, 0, 0, 0, 0],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
#          0,
#          0, 0, 0, 0, 0, 0],
#         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
#          1,
#          1, 1, 1, 1, 1, 1],
#         [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
#          0,
#          0, 0, 0, 0, 0, 1],
#         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#          1,
#          1, 1, 1, 1, 0, 1],
#         [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0,
#          0,
#          0, 0, 0, 0, 0, 1],
#         [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0,
#          0,
#          0, 0, 0, 0, 0, 1],
#         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
#          0,
#          0, 0, 0, 0, 1, 1],
#         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0,
#          1,
#          1, 1, 1, 1, 1, 1],
#         [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1,
#          1,
#          1, 1, 1, 1, 1, 1],
#         [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
#          0,
#          0, 0, 0, 0, 0, 1],
#         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#          0,
#          0, 0, 0, 0, 0, 1],
#         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#          0,
#          0, 0, 0, 0, 0, 1],
#         [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
#          0,
#          0, 0, 0, 0, 0, 1],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
#          1,
#          1, 1, 1, 1, 1, 1]]
#     map1 = map_.Map(matrix_map1)
#
#     # DEFINE ZONES
#     wc = zone.Zone("wc", "W", [(1, 7)])
#     office1 = zone.Zone("office1", "O",
#                         [(1, 1), (2, 1), (3, 1), (4, 1), (1, 2), (2, 2), (3, 2), (4, 2), (1, 3), (3, 3), (4, 3), (1, 4),
#                          (3, 4), (4, 4), (1, 5), (2, 5), (3, 5), (4, 5)])
#     office2 = zone.Zone("office2", "o",
#                         [(6, 1), (7, 1), (8, 1), (9, 1), (6, 2), (7, 2), (8, 2), (9, 2), (6, 3), (7, 3), (8, 3), (9, 3),
#                          (6, 4), (9, 4), (6, 5), (7, 5), (8, 5), (9, 5)])
#     lounge = zone.Zone("lounge", "L",
#                        [(35, 8), (36, 8), (37, 8), (38, 8), (39, 8), (40, 8), (41, 8), (42, 8), (35, 9), (36, 9),
#                         (42, 9),
#                         (35, 10), (36, 10), (37, 10), (38, 10), (39, 10), (40, 10), (41, 10), (42, 10), (35, 11),
#                         (36, 11),
#                         (37, 11), (38, 11), (39, 11), (40, 11), (41, 11), (42, 11), (35, 12), (36, 12), (37, 12),
#                         (38, 12),
#                         (39, 12), (40, 12), (41, 12), (36, 13)])
#     inbound = zone.Zone("inbound", "I",
#                         [(n, 15) for n in range(34, 42 + 1)] + [(n, 16) for n in range(34, 42 + 1)] + [(n, 17) for n in
#                                                                                                        range(34,
#                                                                                                              42 + 1)] + [
#                             (n, 18) for n in range(34, 42 + 1)])
#     outbound = zone.Zone("outbound", "E",
#                          [(30, n) for n in range(1, 7 + 1)] + [(31, n) for n in range(1, 7 + 1)] + [(32, n) for n in
#                                                                                                     range(1, 7 + 1)] + [
#                              (33, n) for n in range(1, 7 + 1)])
#     storage = zone.Zone("storage", "S",
#                         [(n, 9) for n in range(4, 15 + 1)] + [(n, 9) for n in range(18, 29 + 1)] + [(n, 12) for n in
#                                                                                                     range(4,
#                                                                                                           15 + 1)] + [
#                             (n, 12) for n in range(18, 29 + 1)] + [(n, 13) for n in range(4, 15 + 1)] + [(n, 13) for n
#                                                                                                          in
#                                                                                                          range(18,
#                                                                                                                29 + 1)] + [
#                             (n, 16) for n in range(4, 15 + 1)] + [(n, 16) for n in range(18, 29 + 1)] + [(n, 17) for n
#                                                                                                          in
#                                                                                                          range(4,
#                                                                                                                15 + 1)] + [
#                             (n, 17) for n in range(18, 29 + 1)])
#     packing = zone.Zone("packing", "P", [(15, 4), (22, 4), (24, 4), (28, 4), (18, 3), (19, 7), (26, 2)])
#     door = zone.Zone("door", "D", [(13, 0)])
#
#     zones = [wc, office1, office2, lounge, inbound, outbound, storage, packing, door]
#     zone.print_zone(map1, zones)
#     all_zones = zone.Zone.combined_zones(zones)
#
#     world1 = world.World(map1)
#
#     # creating diff worlds
#     list_of_worlds = []
#     # CREATE WORLDS
#     for j in range(11):
#         world1 = world.World(map1)
#         for _ in range(2):
#             receiver = createactors.actor_with_job("receiver", map1, zones)
#             world1.add_actor(receiver)
#         for _ in range(5):
#             packer = createactors.actor_with_job("packer", map1, zones)
#             world1.add_actor(packer)
#         for _ in range(1):
#             forklift = createactors.actor_with_job("forklift", map1, zones)
#             world1.add_actor(forklift)
#         for _ in range(2):
#             shipper = createactors.actor_with_job("shipper", map1, zones)
#             world1.add_actor(shipper)
#         list_of_worlds.append(world1)
#         print("World " + str(j) + " was created!")
#
#     # The test world is used to count the amount of collisions
#     # The 10 first worlds are used for the probability heatmap
#     # The first one is used for the other tests
#     world1 = list_of_worlds[0]
#     world_test = list_of_worlds[10]
#     list_of_worlds = list_of_worlds[0:10]
#
#     # test
#     world1.plot_world()
#
#     # total heatmap
#     heatm = heatmap.Heatmap(world1, sample_rate=1, scale=1)
#     heatm.visualize_heatmap()
#
#     # moment heatmaps
#     interval = hour_min_to_sec(0, 10)
#     start = hour_min_to_sec(9, 30)
#     end = hour_min_to_sec(13, 0)
#     heatmaps = heatmap.heatmap_for_each_interval(world1, interval, start_time=start, end_time=end,
#                                                  sample_rate=1, scale=1)
#     heatmap.animate_heatmaps(heatmaps)
#
#     print("heatmap stuff done")
#
#     prob_heatmaps = prob_heatmap.heatmap_for_each_interval(list_of_worlds, interval, start_time=start, end_time=end,
#                                                            sample_rate=1, scale=1)
#     prob_heatmap.animate_heatmaps(prob_heatmaps)
#
#     print("prob heatmap stuff done")
#
#     start_loc_robot = (31, 18)
#     end_loc_robot = (1, 1)
#
#     r1 = robot.Robot(start_loc_robot, hour_min_to_sec(15, 0), map1)
#     r1.weighted_astar_path_plan(end_loc_robot, heatm, 1)
#     r1.evaluate_collisions(world_test, 0.1)
#     r1.path.plot_path(map1, "r1 15h global heatmap")
#
#     r1 = robot.Robot(start_loc_robot, hour_min_to_sec(12, 30), map1)
#     r1.weighted_astar_path_plan(end_loc_robot, heatm, 1)
#     r1.evaluate_collisions(world_test, 0.1)
#     r1.path.plot_path(map1, "r1 12h30 global heatmap")
#
#     r2 = robot.Robot(start_loc_robot, hour_min_to_sec(15, 0), map1)
#     r2.weighted_astar_path_plan_timeframes(end_loc_robot, heatmaps, 1)
#     r2.evaluate_collisions(world_test, 0.1)
#     r2.path.plot_path(map1, "r2 15h timeframed heatmap")
#
#     r2 = robot.Robot(start_loc_robot, hour_min_to_sec(12, 30), map1)
#     r2.weighted_astar_path_plan_timeframes(end_loc_robot, heatmaps, 1)
#     r2.evaluate_collisions(world_test, 0.1)
#     r2.path.plot_path(map1, "r2 12h30 timeframed heatmap")
#
#     r3 = robot.Robot(start_loc_robot, hour_min_to_sec(15, 0), map1)
#     r3.weighted_astar_path_plan_timeframes(end_loc_robot, heatmaps, 1)
#     r3.evaluate_collisions(world_test, 0.1)
#     r3.path.plot_path(map1, "r3 15h prob timeframed heatmap")
#
#     r3 = robot.Robot(start_loc_robot, hour_min_to_sec(12, 30), map1)
#     r3.weighted_astar_path_plan_timeframes(end_loc_robot, heatmaps, 1)
#     r3.evaluate_collisions(world_test, 0.1)
#     r3.path.plot_path(map1, "r3 12h30 prob timeframed heatmap")
#
#     r4 = robot.Robot(start_loc_robot, hour_min_to_sec(15, 0), map1)
#     r4.plan_path_waiting_at_encounter(world1, end_loc_robot, 0.1)
#     r4.evaluate_collisions(world_test, 0.1)
#     r4.path.plot_path(map1, "r4 15h wait")
#
#     r4 = robot.Robot(start_loc_robot, hour_min_to_sec(12, 30), map1)
#     r4.plan_path_waiting_at_encounter(world1, end_loc_robot, 0.1)
#     r4.evaluate_collisions(world_test, 0.1)
#     r4.path.plot_path(map1, "r4 12h30 wait")
#
#     # factor of heatmaps??
#     # sample rate of prob heatmap??
#     # sample rate of other heatmap??
#
# if val == "3":
#     print("Run hard setup")
#
#     # create map and zones
#     matrix_map1 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
#                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#                    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
#     map1 = map_.Map(matrix_map1)
#     zone_a = zone.Zone("zone_a", "A", [(n, 1) for n in range(1, 6 + 1)]
#                        + [(n, 2) for n in range(1, 6 + 1)]
#                        + [(n, 3) for n in range(1, 6 + 1)]
#                        + [(n, 4) for n in range(1, 6 + 1)]
#                        + [(n, 5) for n in range(1, 6 + 1)])
#
#     zone_b = zone.Zone("zone_b", "B", [(n, 10) for n in range(5, 5 + 5)]
#                        + [(n, 11) for n in range(5, 5 + 5)]
#                        + [(n, 12) for n in range(5, 5 + 5)])
#
#     zone_c = zone.Zone("zone_c", "C", [(n, 1) for n in range(11, 7 + 11)]
#                        + [(n, 2) for n in range(11, 7 + 11)]
#                        + [(n, 3) for n in range(11, 7 + 11)]
#                        + [(n, 4) for n in range(11, 7 + 11)])
#
#     zone_d = zone.Zone("zone_d", "D", [(n, 8) for n in range(13, 5 + 13)]
#                        + [(n, 9) for n in range(13, 5 + 13)]
#                        + [(n, 10) for n in range(13, 5 + 13)]
#                        + [(n, 11) for n in range(13, 5 + 13)])
#     zones = [zone_a, zone_b, zone_c, zone_d]
#     zone.print_zone(map1, zones)
#     all_zones = zone.Zone.combined_zones(zones)
#
#     world1 = world.World(map1)
#
#     # creating diff worlds
#     list_of_worlds = []
#     # CREATE WORLDS
#     for j in range(11):
#         world1 = world.World(map1)
#         # ADD ACTORS TO WORLD
#         for i in range(3):
#             start_time = hour_min_to_sec(9 + i, 50)
#             end_time = hour_min_to_sec(10 + i, 10)
#             for _ in range(20):
#                 a = actor.Actor.actor_at_zone(zone_b, random_time_between_(start_time, end_time), map1)
#                 a.walk_to_zone(zone_a)
#                 a.wait(random_time_between_(10, 600))
#                 a.walk_to_zone(zone_b)
#                 # add randomness to walk
#                 a.path.add_noise_to_path(1, map1)
#                 world1.add_actor(a)
#         list_of_worlds.append(world1)
#         print("World " + str(j) + " was created!")
