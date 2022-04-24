import math
import world
import actor
import path
import map_
import numpy as np


def heatmap(world):
    acs = world.actors
    heatmap = np.zeros(np.array(world.map_.matrix).shape)
    print(heatmap)
    for a in acs:
        for t in range(math.floor(a.path.get_start_time()),math.floor(a.path.get_end_time()+1)):
            (x,y) = a.path.get_location_at(t)
            (x,y) = (round(x),round(y))
            heatmap[y][x] = heatmap[y][x] + 1
    print(heatmap)
    return heatmap
