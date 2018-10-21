import numpy as np
import matplotlib.pyplot as plt
#原创
def optimizer(data, start_a, start_b, learing_rate):

    a = start_a
    b = start_b
    for num in range(iter_num):
        [a, b] = compute_gradient(a, b, data, learing_rate)

    return [a, b]

def compute_gradient(a, b, data, learing_rate):

    x = data[:, 0]
    y = data[:, 1]

    N = len(data)

    a_gradient = -(2/N)*x*(y - a*x - b)         # 核心
    a_gradient = np.sum(a_gradient, axis=0)     # 核心

    b_gradient = -(2/N)*(y - a*x - b)           # 核心
    b_gradient = np.sum(b_gradient, axis=0)     # 核心

    a = a - learing_rate*a_gradient
    b = b - learing_rate*b_gradient
    print([a,b])
    return [a, b]


if __name__ == '__main__':
    iter_num = 1000
    ini_a = 0
    ini_b = 0
    learing_rate = 0.001

    data = np.loadtxt('data')
    print(data)
    [a, b] = optimizer(data, ini_a, ini_b, learing_rate)
    print([a, b])

    x = data[:, 0]
    y = data[:, 1]
    y_t =a*x + b
    plt.scatter(x, y, color = 'b')
    plt.plot(x, y_t, color = 'r')
    plt.show()
