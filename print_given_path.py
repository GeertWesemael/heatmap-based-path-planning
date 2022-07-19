import map_
import path
import ast

val = 1

if val == 1:

    matrix_map1 = [[1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                   [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                   [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                   [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                   [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                   [1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                   [1, 1, 1, 1, 1, 1, 0, 1, 1, 1]]

    map1 = map_.Map(matrix_map1)

name = input("zet hier de path string:")
dictionary = ast.literal_eval(name)

p = path.Path(dictionary)
p.plot_path(map1)