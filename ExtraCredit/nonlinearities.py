from sklearn import datasets
import numpy as np

iris = datasets.load_iris()

features = np.array(iris['data'])
names = np.array(iris['feature_names'])

