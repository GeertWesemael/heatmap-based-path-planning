import math
import world
import actor
import path
import map_
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt


def heatmap(world):
    acs = world.actors
    hm = np.zeros(np.array(world.map_.matrix).shape)
    for a in acs:
        for t in range(math.floor(a.path.get_start_time()), math.floor(a.path.get_end_time() + 1)):
            (x, y) = a.path.get_location_at(t)
            (x, y) = (round(x), round(y))
            hm[y][x] = hm[y][x] + 1
    return hm


def heatmap2(world):
    acs = world.actors
    xv = []
    yv = []
    for a in acs:
        for t in range(math.floor(a.path.get_start_time()), math.floor(a.path.get_end_time() + 1)):
            (x, y) = a.path.get_location_at(t)
            xv.append(x)
            yv.append(y)
    ax = sns.kdeplot(x=xv, y=yv, shade=True)
    ax.set_xlim(0, len(world.map_.matrix[0]) - 1)
    ax.set_ylim(0, len(world.map_.matrix) - 1)
    plt.gca().invert_yaxis()
    plt.show()


def heatmap3(world, scale=1):
    acs = world.actors
    hm = np.zeros(np.array(world.map_.matrix).shape)
    for a in acs:
        t = a.path.get_start_time()
        while t <= a.path.get_end_time():
            (x, y) = a.path.get_location_at(t)
            # x = 1.4 => 0.6 on 1 en 0.4 on 2
            x_lo = math.ceil(x) - x  # 2-1.4 = 0.6
            x_hi = 1 - x_lo  # 0.4
            y_lo = math.ceil(y) - y  # 2-1.4 = 0.6
            y_hi = 1 - y_lo  # 0.4
            hm[math.ceil(y)][math.ceil(x)] += y_hi * x_hi * scale
            hm[math.floor(y)][math.ceil(x)] += y_lo * x_hi * scale
            hm[math.ceil(y)][math.floor(x)] += y_hi * x_lo * scale
            hm[math.floor(y)][math.floor(x)] += y_lo * x_lo * scale
            t += scale
    ax = sns.heatmap(hm, linewidth=0.5, annot=True)
    plt.show()


def heatmap4(world, sample_rate=1,scale=1):

    def get_coordinates_to_check(scale,co):
        (x, y) = co
        to_check = []
        for i in range(1,scale+1):
            x_lo = x - 0.707*0.5*i  # 0,70 ~~< 1/sqrt(2) circle
            x_hi = x + 0.707*0.5*i
            y_lo = y - 0.707*0.5*i
            y_hi = y + 0.707*0.5*i
            to_check.append((round(x_lo), round(y_lo)))
            to_check.append((round(x_hi), round(y_lo)))
            to_check.append((round(x_lo), round(y_hi)))
            to_check.append((round(x_hi), round(y_hi)))

            if i>1:
                x_lo = x - 0.999*0.5*i
                x_hi = x + 0.999*0.5*i
                y_lo = y - 0.999*0.5*i
                y_hi = y + 0.999*0.5*i
                to_check.append((round(x_lo), round(y)))
                to_check.append((round(x_hi), round(y)))
                to_check.append((round(x), round(y_lo)))
                to_check.append((round(x), round(y_hi)))
        return to_check

    acs = world.actors
    hm = np.zeros(np.array(world.map_.matrix).shape)
    for a in acs:
        t = a.path.get_start_time()
        while t <= a.path.get_end_time():
            co = get_coordinates_to_check(scale,a.path.get_location_at(t))
            add = []
            for i in co:
                (x, y) = i
                if x < 0 or y < 0 or x >= len(hm[0]) or y >= len(hm):
                    continue
                else:
                    if i not in add:
                        add.append(i)
            for i in add:
                (x, y) = i
                hm[y][x] += sample_rate

            t += sample_rate
    ax = sns.heatmap(hm, linewidth=0.5, annot=True)
    plt.show()

def visualize_heatmap(heatmap):
    ax = sns.heatmap(heatmap, linewidth=0.5)
    plt.show()
