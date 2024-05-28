import numpy as np


class Space:

    def __init__(self, n: int = 1, res: int = 10):
        x, y = np.meshgrid(np.linspace(-n, n, res), np.linspace(-n, n, res))
        self.plane = np.hstack([np.reshape(x, (x.size, 1)), np.reshape(y, (x.size, 1)), np.zeros((x.size, 1))])
