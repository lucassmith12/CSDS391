# Lucas Smith
# Homework 8
# LJS174

import random, csv
from time import sleep
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import List


random.seed(8675309)

dimensions = ["sepal_length","sepal_width","petal_length","petal_width"]

def raw_iris_data() -> List:
    with open('./Homework9/irisdata.csv') as csvfile:
        # remove the headers
        data = list(csv.reader(csvfile, delimiter=","))[1:]
        # remove setosas (first group)
        data = [row for row in data if row[4] != 'setosa']
        return data

def iris_data_floats() -> List:
        data = raw_iris_data()
        float_rows = list()
        for row in data:
            new_row = [float(i) for i in row[:4]]
            new_row.append(row[4])
            float_rows.append(new_row)
        return float_rows

# includes species as final col    
def iris_lengths_widths() -> List:
     data = iris_data_floats()
     return [row[2:] for row in data]
     

    
def plot_iris_data() -> None:
    data = iris_lengths_widths()
    virginicas = [row for row in data if row[2] == 'virginica']
    versicolors = [row for row in data if row[2] == 'versicolor']
    
    plt.scatter([virginica[0] for virginica in virginicas], [virginica[1] for virginica in virginicas], color='green', marker='*', label='virginicas')
    plt.scatter([versicolor[0] for versicolor in versicolors], [versicolor[1] for versicolor in versicolors], color='blue', marker='x', label='versicolors')

    plt.legend()

    plt.xlabel('Petal length (cm)')
    plt.ylabel('Petal width (cm)')
    plt.title('Virginica and Versicolor Sizes')
    
    # uncomment to run this method by itself
    # plt.show()


def neural_network(neurons: np.ndarray, weights: np.ndarray, bias: float) -> float:
    dot = np.dot(neurons, weights) + bias
    return 1/(1+np.exp(dot * (-1)))

def plot_decision_boundary(weights: List[float], bias: float):
    plot_iris_data()

    x1_range = np.linspace(2, 7)  # Range for petal length
    x2_boundary = -(bias / weights[1]) - (weights[0] / weights[1]) * x1_range  # Compute boundary

    plt.plot(x1_range, x2_boundary, c='black', linestyle='--', label='Decision Boundary')
    
    plt.show()

def plot_3D(weights: List[int], bias: float):
    num = 20
    
    x1_range = np.linspace(2, 7, num)
    x2_range = np.linspace(0, 2, num)
    x1_grid, x2_grid = np.meshgrid(x1_range, x2_range)
    print(np.stack([x1_grid.ravel(), x2_grid.ravel()], axis=1))
    neurons = np.stack([x1_grid.ravel(), x2_grid.ravel()], axis=1)
    
    y = neural_network(neurons, weights, bias).reshape(x1_grid.shape)
    
    
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')  # Create 3D axis
    surface = ax.plot_surface(x1_grid, x2_grid, y, cmap='viridis', alpha=0.8)

    ax.set_xlabel('Petal Length')
    ax.set_ylabel('Petal Width')
    ax.set_zlabel('y (Neural Network Output)')
    ax.set_title('3D Plot of Neural Network Output Function')

    fig.colorbar(surface, shrink=0.5, aspect=10)

    ax.view_init(elev=15)

    plt.show()

def classifier_test(weights, bias):
    ve = [(5.1,1.6), (4.9,1.5), (3.9,1.1), (4.5,1.5)]
    vi = [(4.8,1.8),(4.9,2),(6.1,2.5),(6.4,2)]
    lengths = [pair[0] for pair in ve] + [pair[0] for pair in vi]
    widths = [pair[1] for pair in ve] + [pair[1] for pair in vi]
    certainties = []
    classifications = []
    for i, pair1 in enumerate(ve):
        certainties.append(np.abs(0.5- neural_network(np.asarray(pair1), weights, bias))*200)
        classifications.append("virginica" if neural_network(np.asarray(pair1), weights, bias) > 0.5 else "versicolor")
        
    for i, pair2 in enumerate(vi):
        certainties.append(np.abs(0.5-neural_network(np.asarray(pair2), weights, bias))*200)
        classifications.append("virginica" if neural_network(np.asarray(pair1), weights, bias) > 0.5 else "versicolor")
        
    df = pd.DataFrame({
        'species': ['versicolor','versicolor','versicolor','versicolor','virginica','virginica','virginica','virginica'],
        'lengths': lengths,
        'widths': widths,
        'classified as': classifications,
        'with certainties (%)': certainties
    })
    print(df)

    x1_range = np.linspace(2, 7)  # Range for petal length
    x2_boundary = -(bias / weights[1]) - (weights[0] / weights[1]) * x1_range  # Compute boundary

    plt.scatter(lengths[:4], widths[:4],color='blue', marker='x', label='versicolors')
    plt.scatter(lengths[4:], widths[4:],color='green', marker='*', label='virginicas')
    plt.plot(x1_range, x2_boundary, color='black', linestyle='--', label='Decision Boundary')
    plt.xlabel('Petal length (cm)')
    plt.ylabel('Petal width (cm)')    
    plt.show()
    



def mn_sq_err(data: List, params: List, classes: dict) -> float:
    # to calc mse, we sum the square of the errors then divide the number of elements
    num_elements = len(data)
    diff_squared = 0
    for vector in data:
        class_index = vector[-1]
        bias = float(params[0])
        diff_squared += np.square(neural_network(np.asarray(vector[:-1]), np.asarray(params[1:]), bias) - classes[class_index])
    return diff_squared / num_elements

def mse_test(bias, weights) -> None:
    
    classes = {'versicolor': 0, 'virginica': 1}
    params = [bias] + weights
    err = mn_sq_err(iris_lengths_widths(), params, classes)
    print(f'Error is {err} when bias is {bias} and weights are {weights}')

def gradient(data: List, weights: List, classes: dict) -> List:
    grade = [0 for _ in weights]
    for item in data:
        # add a 1 for the bias neuron, take out the species
        neurons = item[:-1]
        class_val = classes[item[-1]]
        # bias is the 0th element in the weights array. i know i should have been doing that all along but the assignment is due soon. 
        # if this isnt production swe i dont know what is
        sigmoid = neural_network(np.asarray(neurons), np.asarray(weights[1:]), weights[0])
        scalar = (sigmoid - class_val)*(sigmoid)*(1-sigmoid)

        neurons = [1] + neurons
        for i in range(len(grade)):
            grade[i] += scalar * neurons[i]
    return grade

def gradient_descent() -> None:
    
    weights = [random.random()*-5,random.random()*5, random.random()*-5]
    
    
    classes = {'versicolor': 0, 'virginica': 1}
    iters = range(0,6000)
    errors = [0 for _ in iters]
    data = iris_lengths_widths()
    colors = ['black', 'orange', 'yellow', 'green', 'blue', 'purple']

    
    for i in iters:
        if i % 1000 == 0: 
            x1_range = np.linspace(2, 7)  # Range for petal length
            x2_boundary = -(weights[0] / weights[2]) - (weights[1] / weights[2]) * x1_range  # Compute boundary
            plt.plot(x1_range, x2_boundary, c=colors[i//1000], linestyle='--', label='Decision Boundary')
            plot_iris_data()
            plt.show()
            plt.clf()

            plt.xlabel("Iterations")
            plt.ylabel("Mean squared error")
            plt.plot(iters, errors)
            plt.show()
            
        errors[i] = mn_sq_err(data, weights, classes)
        grades = gradient(data, weights, classes)
        pairs = zip(weights, grades)
        weights = [weight-grade*0.00067 for (weight,grade) in pairs]

        if i>100 and errors[i-100] - errors[i] < 1e-3:
            break 
    print(weights)
    
    

gradient_descent()
