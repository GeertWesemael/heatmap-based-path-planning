import numpy as np
import random
import map_
import path
import actor
import world
import astar
import zone
import createactors
import matplotlib.pyplot as plt

from timefunct import sec_to_hour

matrix_map1 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1],
               [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

map1 = map_.Map(matrix_map1)
# map1.print_map()

wc = zone.Zone("wc","W", [(1,7)])
office1 = zone.Zone("office1","O", [(1,1),(2,1),(3,1),(4,1),(1,2),(2,2),(3,2),(4,2),(1,3),(3,3),(4,3),(1,4),(3,4),(4,4),(1,5),(2,5),(3,5),(4,5)])
office2 = zone.Zone("office2","o", [(6,1),(7,1),(8,1),(9,1),(6,2),(7,2),(8,2),(9,2),(6,3),(7,3),(8,3),(9,3),(6,4),(9,4),(6,5),(7,5),(8,5),(9,5)])
lounge = zone.Zone("lounge","L", [(35,8),(36,8),(37,8),(38,8),(39,8),(40,8),(41,8),(42,8),(35,9),(36,9),(42,9),(35,10),(36,10),(37,10),(38,10),(39,10),(40,10),(41,10),(42,10),(35,11),(36,11),(37,11),(38,11),(39,11),(40,11),(41,11),(42,11),(35,12),(36,12),(37,12),(38,12),(39,12),(40,12),(41,12),(36,13)])
inbound = zone.Zone("inbound","I", [(n, 15) for n in range(34, 42+1)]+[(n, 16) for n in range(34, 42+1)]+[(n, 17) for n in range(34, 42+1)]+[(n, 18) for n in range(34, 42+1)])
outbound = zone.Zone("outbound","E", [(30, n) for n in range(1, 7+1)]+[(31, n) for n in range(1, 7+1)]+[(32, n) for n in range(1, 7+1)]+[(33, n) for n in range(1, 7+1)])
storage = zone.Zone("storage","S", [(n, 9) for n in range(4, 15+1)]+[(n, 9) for n in range(18, 29+1)]+[(n, 12) for n in range(4, 15+1)]+[(n, 12) for n in range(18, 29+1)]+[(n, 13) for n in range(4, 15+1)]+[(n, 13) for n in range(18, 29+1)]+[(n, 16) for n in range(4, 15+1)]+[(n, 16) for n in range(18, 29+1)]+[(n, 17) for n in range(4, 15+1)]+[(n, 17) for n in range(18, 29+1)])
packing = zone.Zone("packing","P", [(15,4),(22,4),(24,4),(28,4),(18,3),(19,7),(26,2)])
door = zone.Zone("door","D", [(13,0)])

zones = [wc,office1,office2,lounge,inbound,outbound,storage,packing,door]
zone.print_zone(map1,zones)
all_zones = zone.Zone.combined_zones(zones)
zone.print_zone(map1,[all_zones])

# combinedzone = zone.Zone.combined_zone(inbound,outbound)
# zone.print_zone(map1,[combinedzone])
#
# actorA = actor.Actor.actor_at((13,0), 1, map1)
# actorA.walk_to_zone(office1)
# actorA.wait(4)
# actorA.walk_to_zone(lounge)
# actorA.wait_till(100)
# actorA.walk_to_zone(office1)

world1 = world.World(map1)

manager = createactors.actor_with_job("manager",map1,zones)
test = actor.Actor.actor_at((42,18),28800,map1)
test.walk_to((42,15))
world1.add_actor(manager)
world1.add_actor(test)
world1.plot_world()
#
# from matplotlib.collections import LineCollection
# data = np.array(manager.path.values)
#
# x = data[:, 0]
# y = data[:, 1]
# cols = list(map(sec_to_hour, manager.path.keys))
#
# points = np.array([x, y]).T.reshape(-1, 1, 2)
# segments = np.concatenate([points[:-1], points[1:]], axis=1)
#
# fig, ax = plt.subplots()
# lc = LineCollection(segments, cmap='viridis')
# lc.set_array(cols)
# lc.set_linewidth(2)
# line = ax.add_collection(lc)
# fig.colorbar(line,ax=ax)
# map_data = np.array(manager.map.get_locations_of(1))
# print(map_data)
# ax.scatter(map_data[:, 1], map_data[:, 0],marker="s")
# ax.set_xlim(0, 43)
# ax.set_ylim(0, 19)
# ax.set_aspect('equal', adjustable='datalim')
# plt.gca().invert_yaxis()
# plt.show()