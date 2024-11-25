# Lucas Smith
# Homework 8
# LJS174

import random, csv
import matplotlib.pyplot as plt
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

# includes species as final col    
def iris_lengths_widths() -> List:
     data = raw_iris_data()
     return [row[2:] for row in data]
     
def iris_data_floats() -> List:
        data = raw_iris_data()
        float_rows = list()
        for row in data:
            new_row = [float(i) for i in row[:4]]
            new_row.append(row[4])
            float_rows.append(new_row)
        return float_rows
    
def plot_iris_data() -> None:
    data = iris_lengths_widths()
    virginicas = [row for row in data if row[2] == 'virginica']
    versicolors = [row for row in data if row[2] == 'versicolor']
    
    plt.scatter([float(virginica[0]) for virginica in virginicas], [float(virginica[1]) for virginica in virginicas], color='green', marker='*', label='virginicas')
    plt.scatter([float(versicolor[0]) for versicolor in versicolors], [float(versicolor[1]) for versicolor in versicolors], color='blue', marker='x', label='versicolors')

    plt.legend()

    plt.xlabel('Petal length (cm)')
    plt.ylabel('Petal width (cm)')
    plt.title('Virginica and Versicolor Sizes')

         

def neural_network(neurons: List[int], weights: List[int], bias: float) -> float:
    x = bias
    for neuron, weight in neurons, weights:
        x += neuron*weight
    return 1/(1+np.exp(x*(-1)))

def plot_decision_boundary(weights: List[int], bias: float):
    plot_iris_data()

    x1_range = np.linspace(2, 7)  # Range for petal length
    x2_boundary = -(bias / weights[1]) - (weights[0] / weights[1]) * x1_range  # Compute boundary

    plt.plot(x1_range, x2_boundary, color='black', linestyle='--', label='Decision Boundary')
    plt.show()



weights = [.5,1]
bias = -4
plot_decision_boundary(weights, bias)