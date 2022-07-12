import astar
import path
import heatmap
import actor
import math


class Robot:
    def __init__(self, star_pos, start_time, map_, size=1):
        if not (int(star_pos[0]) == star_pos[0] and int(star_pos[1]) == star_pos[1]):
            raise Exception("can't give float coord to astar")
        self.map_ = map_
        self.size = size
        self.path = path.Path.stand_still(start_time, start_time + 1, star_pos)

    def astar_path_plan(self, destination):
        if not (int(destination[0]) == destination[0] and int(destination[1]) == destination[1]):
            raise Exception("can't give float coord to astar")
        last_co = self.path.get_end_location()
        last_time = self.path.get_end_time()
        new_path = astar.path_to_path_object(astar.a_star(self.map_, last_co, destination), last_time)
        self.path.add_to_path_safe(new_path)

    def weighted_astar_path_plan(self, destination, heatmap, factor):
        if not (int(destination[0]) == destination[0] and int(destination[1]) == destination[1]):
            raise Exception("can't give float coord to astar")
        last_co = self.path.get_end_location()
        last_time = self.path.get_end_time()
        new_path = astar.path_to_path_object(astar.weighted_a_star(self.map_, last_co, destination, heatmap, factor),
                                             last_time)
        self.path.add_to_path_safe(new_path)

    def weighted_astar_path_plan_timeframes(self, destination, heatmaps, factor):
        start = self.path.get_end_time()
        for i in heatmaps:
            if i.start_time <= start < i.end_time:
                return self.weighted_astar_path_plan(destination, i, factor)

    def get_collisions(self, world, sample_rate, distance=1):
        collisions = 0
        t = self.path.get_start_time()
        while t < self.path.get_end_time():
            robot_loc = self.path.get_location_at(t)
            for a in world.actors:
                actor_loc = a.path.get_location_at(t)
                if actor_loc is not None and euclidian_distance(robot_loc, actor_loc) <= distance:
                    collisions += 1
            t = t + sample_rate
        return collisions

    def get_time(self):
        return self.path.get_time()

    def evaluate_time(self):
        print(f"time of path = {self.get_time()}")
        return self.get_time()

    def evaluate_collisions(self, world, sample_rate, distance=1):
        r = self.get_collisions(world, sample_rate, distance)
        print(f"amount of collisions = {r}")
        return r

    def evaluate_collisions_worlds(self, worlds, sample_rate, distance=1):
        amount = 0
        for i in worlds:
            amount += self.get_collisions(i, sample_rate, distance)
        r = amount/len(worlds)
        print(f"avg amount of collisions in all the test worlds = {r}")
        return r


    def plan_path_waiting_at_encounter(self, world, destination, sample_rate, distance=2, wait_time=5):
        last_co = self.path.get_end_location()
        last_time = self.path.get_end_time()
        new_path = astar.path_to_path_object(astar.a_star(self.map_, last_co, destination), last_time)
        t = new_path.get_start_time()
        while t < new_path.get_end_time():
            robot_loc = new_path.get_location_at(t)
            for a in world.actors:
                actor_loc = a.path.get_location_at(t)
                if actor_loc is not None and euclidian_distance(robot_loc, actor_loc) <= distance:
                    new_path.insert_waiting(t, wait_time)
                    t = t + wait_time
                    continue
            t = t + sample_rate

        self.path.add_to_path_safe(new_path)


def euclidian_distance(coord1, coord2):
    (x1, y1) = coord1
    (x2, y2) = coord2
    return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
