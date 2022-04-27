import math
import world
import actor
import path
import map_
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt


def heatmap(world, start_time=None, end_time=None, sample_rate=1, scale=1):
    def get_coordinates_to_check(scale, co):
        (x, y) = co
        to_check = []
        for i in range(1, scale + 1):
            x_lo = x - 0.707 * 0.5 * i  # 0,70 ~~< 1/sqrt(2) circle
            x_hi = x + 0.707 * 0.5 * i
            y_lo = y - 0.707 * 0.5 * i
            y_hi = y + 0.707 * 0.5 * i
            to_check.append((round(x_lo), round(y_lo)))
            to_check.append((round(x_hi), round(y_lo)))
            to_check.append((round(x_lo), round(y_hi)))
            to_check.append((round(x_hi), round(y_hi)))

            if i > 1:
                x_lo = x - 0.999 * 0.5 * i
                x_hi = x + 0.999 * 0.5 * i
                y_lo = y - 0.999 * 0.5 * i
                y_hi = y + 0.999 * 0.5 * i
                to_check.append((round(x_lo), round(y)))
                to_check.append((round(x_hi), round(y)))
                to_check.append((round(x), round(y_lo)))
                to_check.append((round(x), round(y_hi)))
        return to_check

    acs = world.actors
    hm = np.zeros(np.array(world.map_.matrix).shape)
    for a in acs:
        if start_time is None:
            t = a.path.get_start_time()
        else:
            t = start_time
        if end_time is None:
            till = a.path.get_end_time()
        else:
            till = end_time
        while t <= till:
            loc_at = a.path.get_location_at(t)
            if loc_at is None:
                t += sample_rate
                continue
            co = get_coordinates_to_check(scale, loc_at)
            add = []
            for i in co:
                (x, y) = i
                if x < 0 or y < 0 or x >= len(hm[0]) or y >= len(hm):
                    continue
                else:
                    if i not in add:
                        add.append(i)
            for i in add:
                (x, y) = i
                hm[y][x] += sample_rate
            t += sample_rate
    return hm


def visualize_heatmap(heatmap):
    ax = sns.heatmap(heatmap, linewidth=0.5, annot=True)
    plt.show()
