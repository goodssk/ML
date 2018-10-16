from functools import reduce

class perceptron:
    def __init__(self, input_num, activation):
        self.activation = activation
        self.weights = [0.0 for _ in range(input_num)]
        self.bias = 0

    def __str__(self):

        #打印学习到的权重、偏置值
        return 'weights\t:%s\nbias\t"%f\n' % (self.weights, self.bias)

    def predict(self, input_vec):

        return self.activation(
            reduce(lambda a, b: a+b,
                   list(map(lambda x, w: x * w,
                            input_vec, self.weights))
                   , 0.0) + self.bias
        )

    def train(self, input_vecs, labels, iteration, rate):
        for i in range(iteration):
            self._one_iteration(input_vecs, labels, rate)

    def _one_iteration(self, input_vecs, labels, rate):

        samples = zip(input_vecs, labels)

        for(input_vec, label) in samples:
            output = self.predict(input_vec)

            self._update_weights(input_vec, output, label, rate)

    def _update_weights(self, input_vec, output, label, rate):
        delta = label - output
        self.weights = list(map(
            lambda x, w: w + rate * delta * x,
            input_vec, self.weights
        ))
        self.bias += rate *delta


def f(x):

    return 1 if x > 0 else 0


def get_training_dataset():
    input_vecs = [[1, 1], [0, 0], [1, 0], [0, 1]]
    lables = [1, 0, 1, 1]
    return input_vecs, lables


def train_and_perceptron():
    p = perceptron(2, f)
    input_vecs, labels = get_training_dataset()
    p.train(input_vecs, labels, 10, 0.1)
    return p


if __name__ == '__main__':
    and_perception = train_and_perceptron()
    print(and_perception)

    print(and_perception.predict([1, 1]))
    print(and_perception.predict([1, 0]))
    print(and_perception.predict([0, 1]))
    print(and_perception.predict([0, 0]))

