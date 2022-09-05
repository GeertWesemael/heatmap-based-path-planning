import pickle
import numpy as np
import random
import map_
import path
import actor
import robot
import world
import astar
import zone
import actor
import heatmap

with open('geert_output_paths_big_file', 'rb') as f:
    paths_from_file = pickle.load(f)

print(paths_from_file)

matrix_map1 = [
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0]]

map1 = map_.Map(matrix_map1)

world1 = world.World(map1)

for i in paths_from_file:
    current_path = path.Path(i)
    current_actor = actor.Actor(current_path, map1)
    world1.add_actor(current_actor)

heatm = heatmap.Heatmap(world1, sample_rate=1, scale=1)
heatm.visualize_heatmap()

interval_size = 600

heatmaps = heatmap.heatmap_for_each_interval(world1, interval_size, start_time=0, end_time=3*600, sample_rate=1,
                                             scale=1)
heatmap.animate_heatmaps(heatmaps)

a_star_weight_factor = 100
start_loc_robot = (4,0)
end_loc_robot = (4,12)
robot_start_time = 10

r1 = robot.Robot(start_loc_robot, robot_start_time, map1)
r1.weighted_astar_path_plan(end_loc_robot, heatm, a_star_weight_factor)
# coll = r1.evaluate_collisions_worlds(world_tests, sample_r_col)
time = r1.evaluate_time()
r1.path.plot_path(map1)

r1 = robot.Robot(start_loc_robot, robot_start_time, map1)
r1.weighted_astar_path_plan_timeframes(end_loc_robot, heatmaps, a_star_weight_factor)
time = r1.evaluate_time()
r1.path.plot_path(map1)
