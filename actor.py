import path
import astar


class Actor:
    def __init__(self, path_, map_):
        self.path = path_
        self.map_ = map_
        self.invulnerable = 0

    def set_invulnerable(self,number):
        self.invulnerable = number

    def reduce_invulnerable(self,number):

        self.invulnerable = self.invulnerable - number
        if self.invulnerable < 0:
            self.invulnerable = 0

    def is_vulnerable(self):
        if self.invulnerable <= 0:
            return True
        else:
            return False


    @classmethod  # stand still at least 1 sec
    def actor_at(cls, coordinate, time, map_):
        return cls(path.Path.stand_still(time, time + 1, coordinate), map_)

    @classmethod
    def actor_at_zone(cls, zone, time, map_):
        return cls(path.Path.stand_still(time, time + 1, zone.get_random_location()), map_)

    @classmethod
    def random_walking_actor(cls, fr, to, map_):
        return cls(path.Path.random_path(fr, to, map_), map_)

    def walk_to_zone(self, zone):
        self.walk_to(zone.get_random_location())

    def walk_to(self, coordinate):
        if int(coordinate[0]) == coordinate[0] and int(coordinate[1]) == coordinate[1]:
            last_co = self.path.get_end_location()
            last_time = self.path.get_end_time()
            new_path = astar.path_to_path_object(astar.a_star_hallways(self.map_, last_co, coordinate), last_time)
            self.path.add_to_path_safe(new_path)
        else:
            raise Exception("can't give float coord to astar")

    def wait_till(self, time):
        last_time = self.path.get_end_time()
        if time < last_time:
            self.path.print_path(self.map_)
            raise Exception("path that passes waiting moment is present, wait till: "+str(time)+" , last_time in path: " +str(last_time)+" , path printed above ")
        last_co = self.path.get_end_location()
        waiting_path = path.Path.stand_still(last_time, time, last_co)
        self.path.add_to_path_safe(waiting_path)

    def wait(self, timeframe):
        last_time = self.path.get_end_time()
        last_co = self.path.get_end_location()
        waiting_path = path.Path.stand_still(last_time, last_time + timeframe, last_co)
        self.path.add_to_path_safe(waiting_path)

    def print_path(self):
        self.path.print_path(self.map_)

    def plot_path(self):
        self.path.plot_path(self.map_)
