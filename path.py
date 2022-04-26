import math
from matplotlib.collections import LineCollection
from timefunct import sec_to_hour_min_string, sec_to_hour
import numpy as np
import random
import matplotlib.pyplot as plt


# consists of the locations an actor is at all timeframes
def lin_interpol(y1, y2, x1, x2, x):
    return y1 + (x - x1) * ((y2 - y1) / (x2 - x1))


class Path:
    def __init__(self, path_dict):
        if len(path_dict) == 0:
            raise Exception("path has length 0")
        self.path_list = path_dict
        self.keys = list(path_dict)
        self.values = list(path_dict.values())

    def get_start_location(self):
        return self.values[0]

    def get_start_time(self):
        return self.keys[0]

    def get_end_location(self):
        return self.values[-1]

    def get_end_time(self):
        return self.keys[-1]

    def get_present_times(self):
        return self.keys

    def get_location_at(self, timeframe):
        if timeframe in self.path_list:
            return self.path_list[timeframe]
        elif timeframe < self.get_start_time() or self.get_end_time() < timeframe:
            # raise Exception("Current time is not in path")
            return None
        else:
            # the smallest element of self.keys greater than timeframe
            array_ = np.array(self.keys)
            above = array_[array_ > timeframe].min()
            above_loc = self.path_list[above]

            # the largest element of self.keys less than timeframe
            below = array_[array_ < timeframe].max()
            below_loc = self.path_list[below]

            if above_loc == below_loc:
                return above_loc

            # linear interpolation
            xco = lin_interpol(below_loc[0], above_loc[0], below, above, timeframe)
            yco = lin_interpol(below_loc[1], above_loc[1], below, above, timeframe)
            loc = (xco, yco)
            return loc

    def add_to_path(self, path):
        self.path_list = self.path_list | path.path_list
        self.keys = list(self.path_list)
        self.values = list(self.path_list.values())

    def add_to_path_safe(self, path):
        lst = list(path.path_list)
        for p in self.keys:
            if p in lst:
                if path.path_list[p] != self.path_list[p]:
                    raise Exception("can't add path, because overlap is different")
        self.path_list = self.path_list | path.path_list
        self.keys = list(self.path_list)
        self.values = list(self.path_list.values())

    @classmethod
    def stand_still(cls, fr, to, coordinate):
        path = {fr: coordinate, to: coordinate}
        return cls(path)

    @classmethod
    def random_path(cls, fr, to, map_):
        path = {}
        (x, y) = random.choice(map_.get_locations_of(0))
        path[fr] = (x, y)
        while fr < to:
            fr = fr + 1
            free = map_.get_free_neighbors_coordinates((x, y))
            free.append((x, y))
            (x, y) = random.choice(free)
            path[fr] = (x, y)
        return cls(path)

    def print_path(self, map_):

        print("path start", end='')
        for k in self.keys:
            print(" -> time: " + str(k) + " co: " + str(self.path_list[k]), end='')
        print(" -> end")

        co = {}
        for i in range(math.floor(self.get_start_time()), math.floor(self.get_end_time() + 1)):
            co[self.get_location_at(i)] = i
        print_list = np.copy(np.array(map_.matrix)).tolist()
        for y in range(len(map_.matrix)):
            for x in range(len(map_.matrix[0])):
                if map_.matrix[y][x] == 1:
                    print_list[y][x] = "#"
                if map_.matrix[y][x] == 0:
                    print_list[y][x] = "."
                if (x, y) in list(co.keys()):
                    if print_list[y][x] == "#":
                        print("problem: path crosses wall")
                    print_list[y][x] = str(co[(x, y)])

        print("x", end='')
        for q in range(len(print_list[0])):
            print("  " + str(q), end='')
        for y in range(len(print_list)):
            print("")
            print(y, end='')
            for x in range(len(print_list[0])):
                st = str(print_list[y][x])
                if len(st) == 1:
                    print("  " + print_list[y][x], end='')
                if len(st) == 2:
                    print(" " + print_list[y][x], end='')
                if len(st) > 2:
                    print(" __", end='')
        print("")

    def plot_path(self, map_):
        fig, ax = plt.subplots()
        data = np.copy(np.array(self.values))

        x = data[:, 0]
        y = data[:, 1]
        cols = list(self.keys) #map(sec_to_hour,

        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        lc = LineCollection(segments, cmap='rainbow')
        lc.set_array(cols)
        lc.set_linewidth(2)
        line = ax.add_collection(lc)
        fig.colorbar(line, ax=ax)

        map_data = np.array(map_.get_locations_of(1))
        ax.scatter(map_data[:, 1], map_data[:, 0], marker="s")
        ax.set_xlim(0, len(map_.matrix[0])-1)
        ax.set_ylim(0, len(map_.matrix)-1)
        ax.set_aspect('equal', adjustable='datalim')
        plt.gca().invert_yaxis()
        plt.show()