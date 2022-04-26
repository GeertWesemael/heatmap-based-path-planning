import astar
import path


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
