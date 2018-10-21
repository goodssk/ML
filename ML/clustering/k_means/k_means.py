import numpy as np
import matplotlib.pyplot as plt
import math
#原创
#随机在原有数据中找出k个点作为初始点
def randCent(data, K):
    n = len(data)
    center_point = []
    random = np.random.randint(n, size=K)
    for i in range(K):
        center_point.append(data[random[i],:])

    return center_point

#计算两点之间的距离
def calculate_distance(data, point):
    x = point[0]
    y = point[1]
    x1 = data[0]
    y1 = data[1]
    distance = math.sqrt(pow((x1-x), 2)+pow((y1-y), 2))
    return distance

#画出分好类的图形，直观感受
def plot_point(point, k):
    point_color = ['b', 'r', 'w', 'y', 'g']
    for i in range(k):
        point_i = point[i]
        point_i = np.array(point_i)
        print(point_i)
        x = point_i[:,0]
        y = point_i[:,1]
        print(x)
        print(y)
        plt.scatter(x, y, color = point_color[i])

    plt.show()

#分别求出离k个中心点最近的点，再计算每类新的中心点（所有点的平均数）
def calculate_center_point(data, point, K):
    n = len(data)
    point_distance = []

    distance = []
    for i in range(K):
        distance += [[]]
    for i in range(n):
        for j in range(K):
            point_distance.append(calculate_distance(data[i], point[j]))
        min_count = np.min(point_distance)
        k_point = np.where(np.array(point_distance) == min_count)
        distance[k_point[0][0]].append(data[i, :])
        point_distance = []
    center_point = []
    for i in range(K):
        n = len(distance[i])
        distance_i = distance[i][:]
        center_point_i = np.sum(distance_i, axis=0)/n
        center_point.append(center_point_i)

    return center_point, distance
#进行迭代
def k_mean(data, K, iteration_num):
    point = randCent(data, K)
    n = len(data)
    for i in range(iteration_num):   #进行迭代，不断改变中心点
        point, all_point= calculate_center_point(data, point, K)    #输出k个聚类中心点

    return point, all_point

if __name__ == '__main__':
    data = np.loadtxt('data1.txt', delimiter=',')
    k = 5
    iteration_num = 50
    center_point, all_point= k_mean(data, k, iteration_num)
    plot_point(all_point, k)
    print(center_point)
