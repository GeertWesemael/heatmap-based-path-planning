import path
import astar


class Actor:
    def __init__(self, path_, world):
        self.path = path_
        self.map = world

    @classmethod
    def actor_at(cls, coordinate, time, world):
        return cls(path.Path({time: coordinate}), world)

    @classmethod
    def random_walking_actor(cls, fr, to, world):
        return cls(path.Path.random_path(fr, to, world), world)

    def walk_to(self, coordinate):
        last_co = self.path.get_end_location()
        last_time = self.path.get_end_time()
        new_path = astar.path_to_path_object(astar.a_star(self.map, last_co, coordinate), last_time)
        self.path.add_to_path_safe(new_path)

    def wait_till(self, time):
        last_time = self.path.get_end_time()
        if time < last_time:
            raise Exception("path that passes waiting moment is present")
        last_co = self.path.get_end_location()
        waiting_path = path.Path.stand_still(last_time, time, last_co)
        self.path.add_to_path_safe(waiting_path)

    def wait(self, timeframe):
        last_time = self.path.get_end_time()
        last_co = self.path.get_end_location()
        waiting_path = path.Path.stand_still(last_time, last_time+timeframe, last_co)
        self.path.add_to_path_safe(waiting_path)
