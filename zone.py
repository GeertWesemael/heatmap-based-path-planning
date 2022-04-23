import random


class Zone:
    def __init__(self, name, unique_letter, coordinates):
        self.name = name
        self.coordinates = coordinates
        self.letter = unique_letter

    def get_random_location(self):
        return random.choice(self.coordinates)

    @classmethod
    def combined_zone(cls, zone1, zone2):
        return cls("c-" + zone1.name + "-" + zone2.name, "c", zone1.coordinates + zone2.coordinates)

    @classmethod
    def combined_zones(cls, list_of_zones):
        name = "C"
        coord = []
        for z in list_of_zones:
            name = name + "-" + z.name
            coord = coord + z.coordinates
        return cls(name, "C", coord)


def print_zone(map, list_of_zones):
    print("Zones")
    print("x ", end='')
    for q in range(len(map.matrix[0])):
        if len(str(q)) > 1:
            print(" " + str(q), end='')
        else:
            print("  " + str(q), end='')
    for y in range(len(map.matrix)):
        print("")
        if len(str(y)) > 1:
            print(y, end='')
        else:
            print(str(y) + " ", end='')

        for x in range(len(map.matrix[0])):
            e = map.matrix[y][x]
            co = (x, y)
            isZone = False
            for z in list_of_zones:
                if co in z.coordinates:
                    print("  " + z.letter, end='')
                    if e == 1:
                        raise Exception("zone in wall")
                    isZone = True
            if not isZone:
                if e == 1:
                    print("  " + "#", end='')
                if e == 0:
                    print("  " + ".", end='')
    print("")
