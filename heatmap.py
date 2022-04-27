import math
import world
import actor
import path
import map_
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
from timefunct import sec_to_hour_min_string


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


def heatmap_for_each_interval(world, interval, start_time, end_time, sample_rate=1, scale=1):
    heatmaps = []
    t = start_time
    while t < end_time:
        heatmaps.append(heatmap(world, t, t + interval, sample_rate, scale))
        t += interval
    return heatmaps


def visualize_heatmap(heatmap):
    ax = sns.heatmap(heatmap, linewidth=0.5, annot=True, annot_kws={"size": 6})
    plt.show()


def animate_heatmaps(heatmaps, start_time, interval):
    v_min = 999999999999
    v_max = 0
    max_ = np.amax(np.array(heatmaps))
    min_ = np.amin(np.array(heatmaps))
    if min_ < v_min:
        v_min = min_
    if max_ > v_max:
        v_max = max_

    fig, ax = plt.subplots()
    fig.set_figheight(7)
    fig.set_figwidth(18)
    for i in range(len(heatmaps)):
        ax.cla()
        im = ax.imshow(heatmaps[i], vmin=v_min, vmax=v_max, aspect='auto', cmap="magma")
        cb = ax.figure.colorbar(im, ax=ax)
        ax.set_title("from {}".format(str(sec_to_hour_min_string(start_time + i * interval)) + " to " + str(
            sec_to_hour_min_string(start_time + i * interval + interval))))
        for y in range(len(heatmaps[i])):
            for x in range(len(heatmaps[i][0])):
                number = heatmaps[i][y][x]
                if (number).is_integer:
                    number = int(number)
                if len(str(number)) > 4:
                    number = "__"
                else:
                    number = str(number)
                text = ax.text(x, y, number, ha="center", va="center", color="w", fontsize="x-small")
        plt.pause(1)
        plt.tight_layout()
        cb.remove()
