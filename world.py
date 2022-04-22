import numpy as np

abc = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


class World:
    def __init__(self, map):
        self.map = map
        self.actors = []

    def add_actor(self, actor):
        can_add = True
        for a in self.actors:
            for key in a.path.path_list:
                value = a.path.path_list[key]
                if key in actor.path.keys and actor.path.path_list[key] == value:
                    raise Exception("can't add actor, because of overlap")
                    # print("can't add actor, because of overlap")
                    can_add = False
                    break
            if not can_add:
                break
        self.actors.append(actor)

    def is_free(self, time, co):
        if co in self.free_co_list(time):
            return True
        return False

    def free_co_list(self, time):
        free_co_list = self.map.get_locations_of(0)
        for co in free_co_list:
            for a in self.actors:
                if time in a.path.keys and a.path.path_list[time] == co:
                    free_co_list.remove(co)
        return free_co_list

    def get_min_time(self):
        min_ = 9999
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

    def print_world(self):
        min_ = self.get_min_time()
        max_ = self.get_max_time()
        if min_ is None or max_ is None:
            print("cant find min or max: no actors?")
            print(self.actors)
            return
        for t in range(min_, max_ + 1):
            print_list = np.copy(np.array(self.map.matrix)).tolist()
            for a_index in range(len(self.actors)):
                actor_path = self.actors[a_index].path.path_list
                if t in actor_path:
                    (x, y) = actor_path[t]
                    print_list[y][x] = abc[a_index]

            for y in range(len(print_list)):
                for x in range(len(print_list[0])):
                    if print_list[y][x] == 1:
                        print_list[y][x] = "#"
                    if print_list[y][x] == 0:
                        print_list[y][x] = "."

            print("world at time " + str(t) + " :")
            print("x", end='')
            for q in range(len(print_list[0])):
                if len(str(q)) > 1:
                    print(" " + str(q), end='')
                else:
                    print("  " + str(q), end='')
            for y in range(len(print_list)):
                print("")
                if len(str(y)) > 1:
                    print(y, end='')
                else:
                    print(str(y) + " ", end='')
                for x in range(len(print_list[0])):
                    st = str(print_list[y][x])
                    if len(st) == 1:
                        print("  " + str(print_list[y][x]), end='')
                    if len(st) == 2:
                        print(" " + str(print_list[y][x]), end='')
                    if len(st) > 2:
                        print(" __", end='')
            print("")
