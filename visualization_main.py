import pickle
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
#
# print("Run easy setup")
# filename = 'easy_scenario_worlds_'
# infile = open(filename, 'rb')
# list_of_worlds = pickle.load(infile)
# infile.close()
# print("Unpickled")
#
# world1 = list_of_worlds[0]
# world_test = list_of_worlds[99]
# world_tests = list_of_worlds[10:100]
# print(len(world_tests))
# list_of_worlds = list_of_worlds[0:10]
# print(len(list_of_worlds))
# # test
#
# world1.plot_world(hours=True,fr=hour_min_to_sec(9, 30),to=hour_min_to_sec(13, 0), title="Actors walking towards the center")
#
# # total heatmap
# heatm = heatmap.Heatmap(world1, sample_rate=1, scale=1)
# heatm.visualize_heatmap()
#
# # moment heatmaps
# interval = hour_min_to_sec(0, 10)
# start = hour_min_to_sec(9, 30)
# end = hour_min_to_sec(13, 0)
# heatmaps = heatmap.heatmap_for_each_interval(world1, interval, start_time=start, end_time=end,
#                                              sample_rate=1, scale=1)
# # for i in heatmaps:
# #     i.visualize_heatmap(title= "heatmap from " + str(sec_to_hour_min_string(i.start_time)) + " to " + str(sec_to_hour_min_string(i.end_time)))
# # heatmap.animate_heatmaps(heatmaps)
#
# print("heatmap stuff done")
#
# prob_heatmaps = prob_heatmap.heatmap_for_each_interval(list_of_worlds, interval, start_time=start, end_time=end,
#                                                        sample_rate=1, scale=1)
# # prob_heatmap.animate_heatmaps(prob_heatmaps)
# for i in prob_heatmaps:
#     i.visualize_heatmap(title= "heatmap from " + str(sec_to_hour_min_string(i.start_time)) + " to " + str(sec_to_hour_min_string(i.end_time)))
#
#
# print("prob heatmap stuff done")
#
# map1 = world1.get_map()
# zone_c = zone.Zone("zone_c", "C", [(6, 0)])
# zone_d = zone.Zone("zone_d", "D", [(6, 7)])
# start_loc_robot = zone_d.get_random_location()
# end_loc_robot = zone_c.get_random_location()
#
# path_self_made = {0: (6, 7), 1: (6, 7), 2.4: (5, 6), 3.4: (4, 6), 4.4: (3, 6), 5.4: (2, 6), 6.8: (1, 5), 7.8: (1, 4), 8.8: (1, 3), 9.8: (1, 2), 11.2: (2, 1), 12.2: (3, 1), 13.2: (4, 1), 14.2: (5, 1), 15.6: (6, 0)}
# p = path.Path(path_self_made)
# a_1 = actor.Actor(p, map1)
# a_1.plot_path()
# a_1.print_path()
# a_1.path.plot_path(map1,"example path")
#
#
# world1.actors = []
# path_actor_horizontal = {0:(4,4), 1:(4,4), 2:(4,4), 3:(5,4), 4:(6,4), 5:(7,4), 6:(8,4), 7:(9,4) , 8:(9,4) , 9:(9,4) , 10:(9,4)}
# p_hor = path.Path(path_actor_horizontal)
# a_2 = actor.Actor(p_hor,map1)
# world1.add_actor(a_2)
#
# r = robot.Robot((6,7), 0, map1)
# r.plan_path_waiting_at_encounter(world1, (6,0), 0.1,distance=1,wait_time=2)
# # r.evaluate_collisions_worlds(world_tests, 0.1)
# r.path.plot_path(map1)
# world1.plot_world(robots=[r],fr=0,to=10,title="Robot waiting for actor")
# print(world1.actors[0].path.path_list)
# print(r.path.path_list)
#
# world1.plot_world(hours=True,fr=hour_min_to_sec(8, 0),to=hour_min_to_sec(8, 10))

matrix_map2 = [[1, 1, 1, 1, 1, 1, 1, 0, 1],
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
map2 = map_.Map(matrix_map2)
world2 = world.World(map2)
world2.plot_world()

