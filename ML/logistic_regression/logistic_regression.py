import numpy as np
import matplotlib.pyplot as plt
def cost_function(data, theta0, theta1, theta2, learing_rate, iti_num):
    x1 = data[:, 0]
    x2 = data[:, 1]
    y = data[:, 3]
    current_theta0 = 0
    current_theta1 = 0
    current_theta2 = 0


    for n in range(iti_num):
        [theta0, theta1, theta2] = computer_gradient(data, theta0, theta1, theta2)
        current_theta0 = current_theta0 - theta0
        current_theta1 = current_theta1 - theta1
        current_theta2 = current_theta2 - theta2

def computer_gradient(data, theta0, theta1, theta2):
    x1 = data[:, 0]
    x2 = data[:, 1]
    y = data[:, 3]
    c_theta1 = (theta0 + x1*theta1 + x2*theta2 - y)*x1
    c_theta2 = (theta0 + x1*theta1 + x2*theta2 - y)*x2



if __name__ == '__main__':
    data1 = np.loadtxt('data2.txt' , delimiter=',')
    x = data1[:, 0]
    y = data1[:, 1]

    tp = data1[:, 2]
    a = np.where(tp==0)
    b = np.where(tp==1)
    print(a)
    print(b)

    plt.scatter(x[a], y[a],marker='x', color='r')
    plt.scatter(x[b], y[b], color='b')
    plt.show()

