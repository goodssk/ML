from neutral_network.perceptron import perceptron
import matplotlib.pyplot as plt

f = lambda x: x


class linear_unit(perceptron):
    def __init__(self, input_num):
        perceptron.__init__(self, input_num, f)

def get_dataset():

    input_vecs = [[5], [3], [8], [1.4], [10.1]]
    lables = [5500, 2300, 7600, 1800, 11400]

    return input_vecs, lables

def train_linex_unit():
    lu = linear_unit(1)

    input_vecs, lables = get_dataset()
    lu.train(input_vecs, lables, 10, 0.01)

    return lu

def plot(linear_unit):
    input_vecs, labels = get_dataset()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(list(map(lambda x: x[0], input_vecs)), labels)
    weights = linear_unit.weights
    bias = linear_unit.bias
    x = range(0, 12, 1)
    y = list(map(lambda x: weights[0]*x + bias, x))
    ax.plot(x, y)
    plt.show()

if __name__ == "__main__":
    linear_unit = train_linex_unit()

    print(linear_unit)

    print(linear_unit.predict([3.4]))
    print(linear_unit.predict([15]))

    plot(linear_unit)