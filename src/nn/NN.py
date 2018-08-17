import numpy as np

HIDDEN_SIZE = 10

class NN(object):

    def __init__(self):
        self.w_dense1 = np.random.uniform(-1.0, 1.0, size=(6, HIDDEN_SIZE))
        self.b_dense1 = np.random.uniform(-1.0, 1.0, size=(HIDDEN_SIZE,))
        self.w_dense2 = np.random.uniform(-1.0, 1.0, size=(HIDDEN_SIZE, 3))
        self.b_dense2 = np.random.uniform(-1.0, 1.0, size=(3,))

    def result(self, x, return_probabilites=False):
        x = np.matmul(x, self.w_dense1) + self.b_dense1
        x = np.matmul(x, self.w_dense2) + self.b_dense2
        
        return x if return_probabilites else np.argmax(x)

    def to_flat(self):
        return np.concatenate([self.w_dense1.flatten(), \
                               self.b_dense1.flatten(), \
                               self.w_dense2.flatten(), \
                               self.b_dense2.flatten()])

def from_flat(self, flat):
    nn = NN()

    loc1 = self.w_dense1.size
    loc2 = loc1 + self.b_dense1.size
    loc3 = loc2 + self.w_dense2.size

    nn.w_dense1 = np.reshape(flat[:loc1], self.w_dense1.shape)
    nn.b_dense1 = np.reshape(flat[loc1:loc2], self.b_dense1.shape)
    nn.w_dense2 = np.reshape(flat[loc2:loc3], self.w_dense2.shape)
    nn.b_dense2 = np.reshape(flat[loc3:], self.b_dense2.shape)

    return nn
