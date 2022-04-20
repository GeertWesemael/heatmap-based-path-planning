import numpy as np
import random


# consists of the locations an actor is at all timeframes
class Path:
    def __init__(self, path_dict):
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
        else:
            return None

    @classmethod
    def random_path(cls, fr, to, map):
        path = {}
        (x, y) = random.choice(map.get_locations_of(0))
        path[fr] = (x, y)
        while fr < to:
            fr = fr + 1
            free = map.get_free_neighbors_coordinates((x, y))
            free.append((x, y))
            (x, y) = random.choice(free)
            path[fr] = (x, y)
        return cls(path)

    def print_path(self, map):

        print("path start",end='')
        for p in self.values:
            print(" -> "+str(p),end='')
        print(" -> end")

        co = {}
        for i in self.path_list:
            co[self.path_list[i]] = i
        print_list = np.copy(np.array(map.matrix)).tolist()
        for y in range(len(map.matrix)):
            for x in range(len(map.matrix[0])):
                if map.matrix[y][x] == 1:
                    print_list[y][x] = "#"
                if map.matrix[y][x] == 0:
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
