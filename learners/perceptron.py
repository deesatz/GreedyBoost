"""
    Identical to Perceptron implementation of Chen 2012.
"""

import numpy as np


def _snorm(w):
    return np.linalg.norm(w)


class Perceptron(object):

    def __init__(self, classes):
        if set(classes) != set([-1.0, 1.0]):
            raise ValueError
        self.w = None

    def reset(self, x):
        self.w = np.zeros(x.shape)

    def raw_predict(self, x):
        if self.w is None:
            self.reset(x)

	#print (np.matrix(self.w).shape)
	#print (self.w.shape,x.shape, (np.transpose(np.matrix(x)).shape))
        prod = np.matrix(self.w) * np.matrix(x).T
        norm = _snorm(self.w)
	#print (norm.shape)
        if norm > 1.0:
            return prod / norm
        return prod

    def predict(self, x):
        #print self.raw_predict(x)
        if self.raw_predict(x) > 0.0:
            return 1.0
        return -1.0

    def partial_fit(self, x, y, sample_weight=1.0):
        if self.raw_predict(x) * y <= 0.0:
            self.w = self.w + sample_weight * y * x
