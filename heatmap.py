import math
import world
import actor
import path
import map_
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
from timefunct import sec_to_hour_min_string


class Heatmap:
    def __init__(self, world, start_time=None, end_time=None, sample_rate=1, scale=1):
        self.world = world
        self.start_time = start_time
        self.end_time = end_time
        self.sample_rate = sample_rate
        self.scale = scale
        # numpy matrix object
        self.matrix = self.create_heatmap()

    #scale is the size of an actor

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

        acs = self.world.actors
        hm = np.zeros(np.array(self.world.map_.matrix).shape)
        for a in acs:
            if self.start_time is None:
                t = a.path.get_start_time()
            else:
                t = self.start_time
            if self.end_time is None:
                till = a.path.get_end_time()
            else:
                till = self.end_time

            while t <= till:
                loc_at = a.path.get_location_at(t)
                if loc_at is None:
                    t += self.sample_rate
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
                    hm[y][x] += self.sample_rate
                t += self.sample_rate
        return hm

    def visualize_heatmap(self,title=None):
        if title is None:
            sns.heatmap(self.matrix, linewidth=0.5, annot=True, annot_kws={"size": 6})
        else:
            sns.heatmap(self.matrix, linewidth=0.5, annot=True, annot_kws={"size": 6}).set(title=title)
        plt.show()


    def get_value_at(self, coord):
        (x, y) = coord
        return self.matrix[y][x]


def heatmap_for_each_interval(world, interval, start_time, end_time, sample_rate=1, scale=1):
    heatmaps = []
    t = start_time
    while t < end_time:
        heatmaps.append(Heatmap(world, t, t + interval, sample_rate, scale))
        t += interval
    return heatmaps

#onnodig sum(np array is goed genoeg)
# def combine_heatmaps(heatmaps):
#     result = heatmaps[0]
#     for i in range(1, len(heatmaps)):
#         result += heatmaps[i]
#     return result

def combine_heatmaps(list_of_heatmap_matrixes):
    return sum(list_of_heatmap_matrixes)/len(list_of_heatmap_matrixes)

# convolution = [,,] or [,,,,]
def combine_heatmaps_using_convolution(heatmaps,convolution):
    if not len(convolution)%2:
        raise Exception("even convolution")
    result = list(heatmaps)
    center_index = math.floor(len(convolution)/2)
    print(len(heatmaps))
    for i in range(len(heatmaps)):
        result[i].matrix = heatmaps[i].matrix * convolution[center_index]
        j = center_index
        while j != 0:
            if i-j >= 0:
                print("bottom")
                result[i].matrix += heatmaps[i - j].matrix * convolution[j - center_index]
            if i+j < len(heatmaps):
                print("top")
                result[i].matrix += heatmaps[i + j].matrix * convolution[j + center_index]
            print(i+j)
            print(i-j)
            j -= 1

    print(heatmaps[0].matrix)
    print(heatmaps[1].matrix)
    print(heatmaps[2].matrix)
    print(result[0].matrix)

    return result



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
                if len(str(number)) > 4:
                    number = "__"
                else:
                    number = str(number)
                text = ax.text(x, y, number, ha="center", va="center", color="w", fontsize="x-small")
        plt.pause(2)
        plt.tight_layout()
        cb.remove()
