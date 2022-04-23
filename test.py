import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

x= np.linspace(0,1, 100)
y= np.linspace(0,1, 100)
cols = np.linspace(0,1,len(x))
cols2 = np.linspace(0,1,len(x))
y2= np.linspace(0,1, 100) #
x2 = np.linspace(1,0, 100) #


points = np.array([x, y]).T.reshape(-1, 1, 2)
points2 = np.array([x2, y2]).T.reshape(-1, 1, 2) #
segments = np.concatenate([points[:-1], points[1:]], axis=1)
segments2 = np.concatenate([points[:-1], points[1:]], axis=1) #
segments = np.concatenate((segments,segments2))

print(segments)
print(np.concatenate((cols,cols2)))

fig, ax = plt.subplots()
lc = LineCollection(segments2, cmap='viridis')
# lc.set_array(np.concatenate((cols,cols2)))
# lc.set_linewidth(2)
line = ax.add_collection(lc)
# fig.colorbar(line,ax=ax)
plt.show()