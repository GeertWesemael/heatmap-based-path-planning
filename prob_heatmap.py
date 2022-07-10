import math
import world
import actor
import path
import map_
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
from timefunct import sec_to_hour_min_string


class ProbHeatmap:
    def __init__(self, worlds, start_time, end_time, sample_rate=1, scale=1):
        self.worlds = worlds
        self.start_time = start_time
        self.end_time = end_time
        self.sample_rate = sample_rate
        self.scale = scale
        # numpy matrix object
        self.matrix = self.create_heatmap()

    def create_heatmap(self):
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

        # #find earliest and latest time
        # start = 999999999999
        # end = 0
        # for w in self.worlds:
        #     acs = w.actors
        #     for a in acs:
        #         if self.start_time is None and a.path.get_start_time() < start:
        #             start = a.path.get_start_time()
        #         if self.end_time is None and a.path.get_end_time() > end:
        #             end = a.path.get_end_time()
        #         else:
        #             till = self.end_time
        # if self.end_time is not None:
        #     start = self.start_time
        # if self.end_time is not None:
        #     end = self.end_time
        # if start > end:
        #     raise Exception("no correct start or end date")

        t = self.start_time
        till = self.end_time

        timeframe = till - t
        amount_per_timeframe = timeframe / self.sample_rate
        # save one matrix for prob
        hm = np.zeros(np.array(self.worlds[0].map_.matrix).shape)

        while t < till:
            print("creating heatmap at " + sec_to_hour_min_string(t))
            for w in self.worlds:
                acs = w.actors
                # hm_w contains all the positions persons where at this timeframe
                hm_w = np.zeros(np.array(self.worlds[0].map_.matrix).shape)
                for a in acs:
                    loc_at = a.path.get_location_at(t)
                    if loc_at is None:
                        continue
                    co = get_coordinates_to_check(self.scale, loc_at)
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
                        hm_w[y][x] = 1
                # hm is the total sum of people at a certain position at a timeframe in each world
                hm += hm_w
            t += self.sample_rate
        # divide it for each world and the sample rate
        hm = hm/(len(self.worlds)*amount_per_timeframe)
        return hm

    def visualize_heatmap(self):
        ax = sns.heatmap(self.matrix, linewidth=0.5, annot=True, annot_kws={"size": 6})
        plt.show()

    def get_value_at(self, coord):
        (x, y) = coord
        return self.matrix[y][x]

def heatmap_for_each_interval(worlds, interval, start_time, end_time, sample_rate=1, scale=1):
    heatmaps = []
    t = start_time
    while t < end_time:
        heatmaps.append(ProbHeatmap(worlds, t, t + interval, sample_rate, scale))
        t += interval
    return heatmaps

def animate_heatmaps(heatmaps):
    v_min = 999999999999
    v_max = 0
    matrices = [n.matrix for n in heatmaps]
    max_ = np.amax(np.array(matrices))
    min_ = np.amin(np.array(matrices))
    if min_ < v_min:
        v_min = min_
    if max_ > v_max:
        v_max = max_

    fig, ax = plt.subplots()
    fig.set_figheight(5)
    fig.set_figwidth(12)
    for i in range(len(heatmaps)):
        ax.cla()
        im = ax.imshow(matrices[i], vmin=v_min, vmax=v_max, aspect='auto', cmap="magma")
        cb = ax.figure.colorbar(im, ax=ax)
        ax.set_title("from {}".format(str(sec_to_hour_min_string(heatmaps[i].start_time)) + " to " + str(
            sec_to_hour_min_string(heatmaps[i].end_time))))
        for y in range(len(matrices[i])):
            for x in range(len(matrices[i][0])):
                number = heatmaps[i].get_value_at((x, y))
                number = str(number)[0:4]
                text = ax.text(x, y, number, ha="center", va="center", color="w", fontsize="x-small")
        plt.pause(1)
        plt.tight_layout()
        cb.remove()

