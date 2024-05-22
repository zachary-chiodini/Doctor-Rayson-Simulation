import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from scipy.spatial import Delaunay

from schrodinger import Wave


class Space:

    def __init__(self, n: int = 1, res: int = 100):
        x, y = np.meshgrid(np.linspace(-n, n, res), np.linspace(-n, n, res))
        r = np.hstack([np.reshape(x, (x.size, 1)), np.reshape(y, (x.size, 1)), np.zeros((x.size, 1))])
        self.map = Delaunay(r, incremental=True, qhull_options='QJ')

    def update_map(self, points):
        self.map.add_points(points - self.map.points)


s = Space()
s.update_map(Wave.delta(s.map.points))

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_trisurf(s.map.points[:, 0], s.map.points[:, 1], s.map.points[:, 2], triangles=s.map.simplices)
plt.show()
