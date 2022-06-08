import numpy as np


class Map:
    def __init__(self, matrix):
        self.matrix = matrix

    def print_map(self):
        print("x ", end='')
        for q in range(len(self.matrix[0])):
            if len(str(q)) > 1:
                print(" " + str(q), end='')
            else:
                print("  " + str(q), end='')
        for y in range(len(self.matrix)):
            print("")
            if len(str(y)) > 1:
                print(y, end='')
            else:
                print(str(y) + " ", end='')

            for x in range(len(self.matrix[0])):
                e = self.matrix[y][x]
                if e == 1:
                    print("  " + "#", end='')
                if e == 0:
                    print("  " + ".", end='')
        print("")

    def get_locations_of(self, value):
        locations = []
        numpy_matrix = np.matrix(self.matrix)
        for x in range(len(numpy_matrix)):
            i = numpy_matrix[x]
            j = np.where(i == value)[1]
            for y in j:
                locations.append((x, y))
        return locations

    def get_location_of_borders(self):
        locations = []
        numpy_matrix = np.matrix(self.get_borders())
        for x in range(len(numpy_matrix)):
            i = numpy_matrix[x]
            j = np.where(i == 1)[1]
            for y in j:
                locations.append((x, y))
        return locations

    # def get_neighbors_coordinates(self, coordinate):
    #     neighbors = []
    #     (xco, yco) = coordinate
    #     if xco - 1 >= 0:
    #         neighbors.append((xco - 1, yco))
    #     if yco - 1 >= 0:
    #         neighbors.append((xco, yco - 1))
    #     if xco + 1 < len(self.matrix[0]):
    #         neighbors.append((xco + 1, yco))
    #     if yco + 1 < len(self.matrix):
    #         neighbors.append((xco, yco + 1))
    #     return neighbors

    def get_free_neighbors_coordinates(self, coordinate):
        neighbors = []
        (xco, yco) = coordinate

        distance = 1
        # next to
        if xco - 1 >= 0 and self.matrix[yco][xco - 1] == 0:
            neighbors.append(((xco - 1, yco),distance))
        if yco - 1 >= 0 and self.matrix[yco - 1][xco] == 0:
            neighbors.append(((xco, yco - 1),distance))
        if xco + 1 < len(self.matrix[0]) and self.matrix[yco][xco + 1] == 0:
            neighbors.append(((xco + 1, yco),distance))
        if yco + 1 < len(self.matrix) and self.matrix[yco + 1][xco] == 0:
            neighbors.append(((xco, yco + 1),distance))

        distance = 1.4
        # diagonal
        if xco - 1 >= 0 and yco - 1 >= 0 and self.matrix[yco - 1][xco - 1] == 0:
            neighbors.append(((xco - 1, yco - 1),distance))
        if xco + 1 < len(self.matrix[0]) and yco + 1 < len(self.matrix) and self.matrix[yco + 1][xco + 1] == 0:
            neighbors.append(((xco + 1, yco + 1),distance))
        if xco + 1 < len(self.matrix[0]) and yco - 1 >= 0 and self.matrix[yco - 1][xco + 1] == 0:
            neighbors.append(((xco + 1, yco - 1),distance))
        if xco - 1 >= 0 and yco + 1 < len(self.matrix) and self.matrix[yco + 1][xco - 1] == 0:
            neighbors.append(((xco - 1, yco + 1),distance))

        return neighbors

    ######
    #
    # i-1 j-1      i-1   j      i-1 j+1
    # i   j-1      i     j      i   j+1s
    # i+1 j-1      i+1   j      i+1 j+1
    #
    def get_borders(self):
        m = self.matrix
        new_m = np.zeros(np.array(m).shape)
        for i in range(len(m)):
            for j in range(len(m[0])):
                if m[i][j] == 1:
                    new_m[i][j] = 1
                    if i != 0:
                        new_m[i - 1][j] = 1
                        if j != 0:
                            new_m[i - 1][j - 1] = 1
                        if j != len(m[0]) - 1:
                            new_m[i - 1][j + 1] = 1
                    if i != len(m) - 1:
                        new_m[i + 1][j] = 1
                        if j != 0:
                            new_m[i + 1][j - 1] = 1
                        if j != len(m[0]) - 1:
                            new_m[i + 1][j + 1] = 1
                    if j != 0:
                        new_m[i][j - 1] = 1
                    if j != len(m[0]) - 1:
                        new_m[i][j + 1] = 1
        for i in range(len(m)):
            for j in range(len(m[0])):
                if new_m[i][j] == m[i][j]:
                    new_m[i][j] = 0
        return new_m
