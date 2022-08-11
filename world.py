import numpy as np
from matplotlib.collections import LineCollection
from timefunct import sec_to_hour_min_string, sec_to_hour, hour_min_to_sec
import matplotlib.pyplot as plt
from matplotlib.path import Path as Pathmatplotlib
import matplotlib.patches as patches

abc = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


class World:
    def __init__(self, map_):
        self.map_ = map_
        self.actors = []

    def get_map(self):
        return self.map_

    def add_actor(self, actor):
        # #check overlap walls
        # for p in actor.path.values:
        #     (x,y) = p
        #     if self.map.matrix[y][x] == 1:
        #         raise Exception("actor walks through a wall")
        # #check overlap other actors
        # can_add = True
        # for a in self.actors:
        #     for key in a.path.path_list:
        #         value = a.path.path_list[key]
        #         if key in actor.path.keys and actor.path.path_list[key] == value:
        #             raise Exception("can't add actor, because of overlap at time "+ str(key) + " at " + str(actor.path.path_list[key]))
        #             # print("can't add actor, because of overlap")
        #             can_add = False
        #             break
        #     if not can_add:
        #         break
        self.actors.append(actor)

    # def is_free(self, time, co):
    #     if co in self.free_co_list(time):
    #         return True
    #     return False
    #
    # def free_co_list(self, time):
    #     free_co_list = self.map.get_locations_of(0)
    #     for co in free_co_list:
    #         for a in self.actors:
    #             if time in a.path.keys and a.path.path_list[time] == co:
    #                 free_co_list.remove(co)
    #     return free_co_list

    def get_min_time(self):
        min_ = 999999999
        if len(self.actors) == 0:
            return None
        else:
            for a in self.actors:
                for key in a.path.path_list:
                    if key < min_:
                        min_ = key
            return min_

    def get_max_time(self):
        max_ = 0
        if len(self.actors) == 0:
            return None
        else:
            for a in self.actors:
                for key in a.path.path_list:
                    if key > max_:
                        max_ = key
            return max_

    # def print_world(self):
    #     min_ = self.get_min_time()
    #     max_ = self.get_max_time()
    #     if min_ is None or max_ is None:
    #         print("cant find min or max: no actors?")
    #         print(self.actors)
    #         return
    #
    #     last_print = ""
    #
    #     for t in range(min_, max_ + 1):
    #         print_string = ""
    #         print_list = np.copy(np.array(self.map_.matrix)).tolist()
    #         for a_index in range(len(self.actors)):
    #             actor_path = self.actors[a_index].path.path_list
    #             if t in actor_path:
    #                 (x, y) = actor_path[t]
    #                 print_list[y][x] = abc[a_index]
    #
    #         for y in range(len(print_list)):
    #             for x in range(len(print_list[0])):
    #                 if print_list[y][x] == 1:
    #                     print_list[y][x] = "#"
    #                 if print_list[y][x] == 0:
    #                     print_list[y][x] = "."
    #
    #         print_string += "x"
    #         for q in range(len(print_list[0])):
    #             if len(str(q)) > 1:
    #                 print_string += " " + str(q)
    #             else:
    #                 print_string += "  " + str(q)
    #         for y in range(len(print_list)):
    #             print_string += "\n"
    #             if len(str(y)) > 1:
    #                 print_string += str(y)
    #             else:
    #                 print_string += str(y) + " "
    #             for x in range(len(print_list[0])):
    #                 st = str(print_list[y][x])
    #                 if len(st) == 1:
    #                     print_string += "  " + str(print_list[y][x])
    #                 if len(st) == 2:
    #                     print_string += " " + str(print_list[y][x])
    #                 if len(st) > 2:
    #                     print_string += " __"
    #         if last_print != print_string:
    #             print("\nworld at time " + sec_to_hour_min_string(t) + " :\n" + print_string)
    #         last_print = print_string

    def plot_world(self,showborders = False,robots = None, fr = None, to = None, title = None, hours = False):

        def fr_to_list(keys):
            if fr is not None and to is not None:
                print("be aware: any instances outside of fr/to will give a wrong visualization")
                if hours:
                    cols_ = list(map(sec_to_hour, keys)) + [sec_to_hour(fr),sec_to_hour(to)]
                else:
                    cols_ = list(keys) + [fr, to]
            else:
                if hours:
                    cols_ = list(map(sec_to_hour, keys)) + [8, 18]
                else:
                    cols_ = list(keys) + [hour_min_to_sec(8,0),hour_min_to_sec(18,0)]
            return cols_

        fig, ax = plt.subplots()
        if len(self.actors) == 0:
            print("No Actors in this world")
        else:
            #add actors
            for a in self.actors:
                if to is not None and fr is not None:
                    if a.path.get_start_time() > to:
                        continue
                    if a.path.get_end_time() < fr:
                        continue
                data = np.array(a.path.values)

                x = data[:, 0]
                y = data[:, 1]

                cols = fr_to_list(a.path.keys)

                points = np.array([x, y]).T.reshape(-1, 1, 2)
                segments = np.concatenate([points[:-1], points[1:]], axis=1)

                lc = LineCollection(segments, cmap='rainbow')
                lc.set_array(cols)
                lc.set_linewidth(2)
                line = ax.add_collection(lc)
            if not hours:
               fig.colorbar(line, ax=ax, label="time in seconds")
            else:
                fig.colorbar(line, ax=ax, label="time in hours")
        #add robots if i added one
        if robots is not None:
            for r in robots:
                data = np.array(r.path.values)

                x = data[:, 0]
                y = data[:, 1]

                fr_to_list(r.path.keys)

                points = np.array([x, y]).T.reshape(-1, 1, 2)
                segments = np.concatenate([points[:-1], points[1:]], axis=1)

                lc = LineCollection(segments, cmap='rainbow')
                lc.set_array(cols)
                lc.set_linewidth(6)
                line = ax.add_collection(lc)
                print(cols)
            # fig.colorbar(line, ax=ax)

        map_data = np.array(self.map_.get_locations_of(1))
        map_data_borders = np.array(self.map_.get_location_of_borders())

        codes = [
            Pathmatplotlib.MOVETO,
            Pathmatplotlib.LINETO,
            Pathmatplotlib.LINETO,
            Pathmatplotlib.LINETO,
            Pathmatplotlib.CLOSEPOLY,
        ]
        #black
        for i in map_data:
            (y, x) = i
            verts = [
                (x-0.5, y+0.5),
                (x-0.5, y-0.5),
                (x+0.5, y-0.5),
                (x+0.5, y+0.5),
                (x-0.5, y+0.5),
            ]
            pa = Pathmatplotlib(verts, codes)
            patch = patches.PathPatch(pa, facecolor='black', lw=0)
            ax.add_patch(patch)
        #gray
        if showborders:
            for i in map_data_borders:
                (y, x) = i
                verts = [
                    (x-0.5, y+0.5),
                    (x-0.5, y-0.5),
                    (x+0.5, y-0.5),
                    (x+0.5, y+0.5),
                    (x-0.5, y+0.5),
                ]
                pa = Pathmatplotlib(verts, codes)
                patch = patches.PathPatch(pa, facecolor='grey', lw=0)
                ax.add_patch(patch)

        # if len(map_data) != 0:
        #     ax.scatter(map_data[:, 1], map_data[:, 0], marker="s")

        ax.set_xlim(0, len(self.map_.matrix[0])-1)
        ax.set_ylim(0, len(self.map_.matrix)-1)
        ax.set_aspect('equal', adjustable='datalim')
        if title is not None:
            ax.set_title(title)
        plt.gca().invert_yaxis()
        plt.show()