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

print("Run easy setup")
filename = 'easy_scenario_worlds_'
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

# world1.plot_world(hours=True,fr=hour_min_to_sec(9, 30),to=hour_min_to_sec(13, 0), title="Actors walking towards the center")
#
# # moment heatmaps
# interval = hour_min_to_sec(1, 0)
# start = hour_min_to_sec(9, 0)
# end = hour_min_to_sec(10, 0)
#
# prob_heatmaps = prob_heatmap.heatmap_for_each_interval(list_of_worlds, interval, start_time=start, end_time=end,
#                                                        sample_rate=1, scale=1)
# print(len(prob_heatmaps))
# prob_heatmaps[0].visualize_heatmap()
# hm = prob_heatmaps[0]

def get_value(hm):
    # values_to_check = [(5,2),(5,3),(5,4),(5,5),
    #                    (6,2),(6,3),(6,4),(6,5),
    #                    (7,2),(7,3),(7,4),(7,5)]
    values_to_check = [(6,2),(6,3),(6,4),(6,5)]
    total = 0
    for v in values_to_check:
        total += hm.get_value_at(v)
    return total


uberstart = hour_min_to_sec(9,0)
ubertill = hour_min_to_sec(13,0)
stepsize = hour_min_to_sec(0,1)
interval = hour_min_to_sec(2,0)
i= uberstart

timing_list = []
value_list = []

while i < ubertill:
    prob_heatmaps = prob_heatmap.heatmap_for_each_interval(list_of_worlds, interval, start_time=i, end_time=i+interval,
                                                           sample_rate=1, scale=1)
    hm = prob_heatmaps[0]

    timing_list.append(i)
    value_list.append(get_value(hm))

    i+=stepsize

print(timing_list)
print(value_list)

plt.plot(timing_list,value_list,'b.-')
plt.title("sliding heatmap with interval: " + sec_to_hour_min_string(interval))
plt.show()




# heatmap.animate_heatmaps(prob_heatmaps)

# # prob_heatmap.animate_heatmaps(prob_heatmaps)
# for i in prob_heatmaps:
#     i.visualize_heatmap(title= "heatmap from " + str(sec_to_hour_min_string(i.start_time)) + " to " + str(sec_to_hour_min_string(i.end_time)))


