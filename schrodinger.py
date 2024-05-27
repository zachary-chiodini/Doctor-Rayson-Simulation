import numpy as np
from nptyping import Float, NDArray, Shape


Matrix = NDArray[Shape['*, 3'], Float]
Vector = NDArray[Shape['3'], Float]


class Particle:

    def __init__(self, c0=1, m0=1, p0=0, r0=np.zeros(3), s0=0):
        self.c0 = c0
        self.m0 = m0
        self.p0 = p0
        self.r0 = r0
        self.s0 = s0

    @staticmethod
    def delta(X: Matrix, r: Vector = np.zeros(3), a=1) -> Matrix:
        X[:, 2] = np.exp(-a * np.linalg.norm(X - r, axis=1)**2)
        return X


class Wave(Particle):

    def packet(self):
        pass


class Potential:

    def __init__(self, r0=np.zeros(3)):
        self.r0 = r0

    def exponential(self, X: Matrix) -> Matrix:
        X[:, 2] = np.exp(np.linalg.norm(X - self.r0))
        return X
