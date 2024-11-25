# Lucas Smith
# Homework 8
# LJS174

import random
import matplotlib.pyplot as plt

random.seed(8675309)

def iris_data():
    with open('./irisdata.csv') as csvfile:
        rows = list(csv.reader(csvfile, delimiter=","))[1:]
        float_rows = list()
        for row in rows:
            new_row = [float(i) for i in row[:4]]
            new_row.append(row[4])
            float_rows.append(new_row)
        return float_rows