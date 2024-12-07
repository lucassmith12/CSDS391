from sklearn import datasets, model_selection
from sklearn.discriminant_analysis import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, adjusted_rand_score, classification_report, homogeneity_score

import matplotlib.pyplot as plt
import numpy as np

iris = datasets.load_iris()

X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, random_state=11)

layers, neurons = 10,10

activations = ['identity', 'logistic', 'tanh', 'relu']
sol = 'adam'
results = {}

# Clear our output file
open('./classification_report.txt', 'w').close()


for f_x in activations:
    print(f'Training with function {f_x}')

    clf = MLPClassifier(hidden_layer_sizes=(layers,neurons),  
                        activation=f_x,
                        solver=sol,
                        max_iter=1000,
                        random_state=11)
    
    # Train the model
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    score = accuracy_score(y_test, y_pred)

    results[f_x] = score

    with open('./classification_report.txt', 'a') as f:
        f.write(f"Accuracy with {f_x}: {score:.3f}\n")
        f.write(classification_report(y_test, y_pred, target_names=iris.target_names, zero_division=0))
        f.write("-" * 40 + '\n')

plt.figure(figsize=(8, 5))
plt.bar(results.keys(), results.values(), color=['blue', 'orange', 'green', 'red'])
plt.title(f"Accuracy for Different Activation Functions ({sol})")
plt.xlabel("Activation Function")
plt.ylabel("Accuracy")
plt.ylim(0, 1)
plt.show()

# K-means

clusters = len(set(y))
kmeans = KMeans(n_clusters=clusters, random_state=42)
kmeans.fit(X_train)

km_pred = kmeans.predict(X_test)

ari = adjusted_rand_score(y_test, km_pred)
hmg = homogeneity_score(y_test, km_pred)

with open('./clustering_report.txt', 'w') as f:
    f.write(f'Adjusted Rand Index: {ari:.3f}\n')
    f.write(f'Homogeneity Score: {hmg:.3f}\n')

plt.figure(figsize=(8, 6))
plt.scatter(X_test[:, 0], X_test[:, 1], c=y_pred, cmap='viridis', label='Predicted Clusters', alpha=0.7)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=200, c='red', label='Centroids')
plt.title("K-Means Clustering on Iris Dataset")
plt.xlabel("Sepal length (cm)")
plt.ylabel("Sepal width (cm)")
plt.legend()
plt.show()
