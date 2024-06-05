import numpy as np

from nptypes import Matrix, Vector, Vertex


class Space:

    def __init__(self, n: int = 1):
        self.res = 10
        x, y = np.meshgrid(np.linspace(-n, n, self.res), np.linspace(-n, n, self.res))
        plane = np.hstack([np.reshape(x, (x.size, 1)), np.reshape(y, (x.size, 1)), np.zeros((x.size, 1))])
        self.plane: Vertex = self._reorder_vertices(plane).flatten()

    def _reorder_vertices(self, plane: Matrix) -> Matrix:
        """
        i = 0
        ordered_array[0:3] = plane[[0, 1, 10]]
        ordered_array[3:6] = plane[[10, 11, 1]]
        i = 1
        ordered_array[6:9] = plane[[1, 2,  11]]
        ordered_array[9:12] = plane[[11, 12, 2]]
        """
        ordered_array = np.empty((89 * 6, 3), np.float_)
        for i in range(89):
            ordered_array[6 * i: 6 * i + 3] = plane[[i, i + 1, i + self.res]]
            ordered_array[6 * i + 3: 6 * i + 6] = plane[[i + self.res, i + self.res + 1, i + 1]]
        return ordered_array
