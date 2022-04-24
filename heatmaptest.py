import numpy as np
import random
import map_
import path
import actor
import world
import astar
import zone

matrix_map1 = [[1, 1, 1, 0, 0, 1, 1, 1],
               [1, 1, 1, 0, 0, 1, 1, 1],
               [1, 1, 1, 0, 0, 1, 1, 1],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [1, 1, 1, 0, 0, 1, 1, 1],
               [1, 1, 1, 0, 0, 1, 1, 1],
               [1, 1, 1, 0, 0, 1, 1, 1]]

map1 = map_.Map(matrix_map1)

a_zone = zone.Zone("a","A", [(3,0),(4,0)])
b_zone = zone.Zone("b","B",[(7,3),(7,4)])
c_zone = zone.Zone("c","C", [(3,7),(4,7)])
d_zone = zone.Zone("d","D", [(0,3),(0,4)])
zones = [a_zone,b_zone,c_zone,d_zone]
zone.print_zone(map1,zones)

world1 = world.World(map1)

actorA = actor.Actor.actor_at_zone(c_zone,0,map1)
actorA.walk_to_zone(b_zone)
# actorA.walk_to_zone(c_zone)
# actorA.walk_to_zone(b_zone)
# actorA.walk_to_zone(c_zone)
# actorA.walk_to_zone(b_zone)
# actorA.walk_to_zone(c_zone)
# actorA.walk_to_zone(b_zone)
# actorA.walk_to_zone(c_zone)
actorA.plot_path()

world1.add_actor(actorA)

import seaborn as sns
import matplotlib.pylab as plt
from heatmap import heatmap

data = heatmap(world1)
ax = sns.heatmap(data, linewidth=0.5)
plt.show()

# def my_plotter(ax, data1, data2, param_dict):
#     """
#     A helper function to make a graph.
#     """
#     out = ax.plot(data1, data2, **param_dict)
#     return out
#
# data1, data2, data3, data4 = np.random.randn(4, 100)  # make 4 random data sets
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5, 2.7))
# my_plotter(ax1, data1, data2, {'marker': 'x'})
# my_plotter(ax2, data3, data4, {'marker': 'o'});

# actorA = actor.Actor.actor_at((1, 1), 1.5, map1)
# actorA.walk_to((1, 6))
# actorA.wait(5)
# actorA.walk_to((6, 6))
# actorA.wait_till(30)
# actorA.walk_to((6, 2))
#
# actorB = actor.Actor.actor_at((2, 5), 50, map1)
# actorB.walk_to_zone(b_zone)
# actorB.wait(5)
# actorB.walk_to_zone(c_zone)
# actorB.wait_till(100)
# actorB.walk_to_zone(zone.Zone.combined_zones(zones))
# print(actorB.path.path_list)
#
# actorA.plot_path()
#
# world1 = world.World(map1)
# world1.add_actor(actorA)
# world1.add_actor(actorB)
# world1.plot_world()
#
# zone.print_zone(map1,zones)