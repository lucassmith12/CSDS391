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
        return list(csv.reader(csvfile, delimiter=","))[1:]

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
    setosas = [row for row in data if row[2] == 'setosa']
    virginicas = [row for row in data if row[2] == 'virginica']
    versicolors = [row for row in data if row[2] == 'versicolor']
    
    plt.scatter([float(setosa[0]) for setosa in setosas], [float(setosa[1]) for setosa in setosas], color='red', marker='o', label='setosas')
    plt.scatter([float(virginica[0]) for virginica in virginicas], [float(virginica[1]) for virginica in virginicas], color='green', marker='*', label='virginicas')
    plt.scatter([float(versicolor[0]) for versicolor in versicolors], [float(versicolor[1]) for versicolor in versicolors], color='blue', marker='x', label='versicolors')

    plt.legend()

    plt.xlabel('Petal length (cm)')
    plt.ylabel('Petal width (cm)')
    plt.title('Iris Dataset')

    plt.show()
         

#def neural_network() -> float:
     