# Lucas Smith
# Homework 8
# LJS174
import csv, random, matplotlib.pyplot as plt

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
        
        
def initialize_means(k: int):
    irises = iris_data()
    # select k random data points to initialize as mean 
    k_means = list()
    for _ in range(k):
        index = random.randint(0, len(irises))
        k_means.append(irises[index])
        irises.remove(irises[index])
    return k_means

def kmeans_update(k_means: list[list], data_points: list[list], dimensions: list[int]):
    assignments = [[] for _ in range(len(k_means))]
    
    distortion = 0
    for X in data_points:
        distances = []
        for mean in k_means:
            distance = 0
            for idx, value in enumerate(X):
                if isinstance(value, str) or idx not in dimensions:  
                    continue
                distance += (value - mean[idx]) ** 2  
            distances.append(distance)  
        mean_index = distances.index(min(distances))  
        assignments[mean_index].append(X)  
        distortion += min(distances)

    new_k_means = []
    
    for cluster in assignments:
        if len(cluster) == 0: # skip if unassigned
            new_k_means.append(k_means[assignments.index(cluster)])  # keep the old one
            continue
        
        
        new_center = []
        num_points = len(cluster)
        for dim in range(len(cluster[0])):  
            sum_dim = 0
            for point in cluster:
                if isinstance(point[dim], str):
                    continue  
                sum_dim += point[dim]
            new_center.append(sum_dim / num_points) 
        
        new_k_means.append(new_center)  
    
    return new_k_means, assignments, distortion

def kmeans_cluster_plot(means: list, data: list, dimensions, max_iters: int):
    for _ in range(max_iters):
        # note distortion is before the new assignments were made
        means, assignments, distortion = kmeans_update(means, data, dimensions)
    
    colors = ['red', 'green', 'blue']
    
    for i, group in enumerate(assignments):
        data = []
        for item in group:
            data.append((item[2], item[3]))

        x_points, y_points = zip(*data)
        plt.scatter(x_points, y_points, color=colors[i], label=f'Group {i}')
    
    for i, mean in enumerate(means):
        cluster_center = (mean[2], mean[3])
        plt.scatter(*cluster_center, color='yellow', s=100, label= f'Mean {i}')  

    dimensions = ["sepal_length","sepal_width","petal_length","petal_width"]
    for d, dim in enumerate(dimensions[2:]):
        maxes = []
        mins = []
        
        for i, group in enumerate(assignments):
            maxes.append(max(iris[d+2] for iris in group))
            mins.append(min(iris[d+2] for iris in group))
        
        overlaps = []

        for i in range(len(maxes) - 1):
            for j in range(i + 1, len(mins)):
                if len(groups) == 2 or i == 2 or j == 2 or (i == 1 and j==0 or i== 0 and j ==2):
                    print(maxes[i], mins[j], (maxes[i] + mins[j]) / 2)
                    overlaps.append((i, j, (maxes[i] + mins[j]) / 2))
        print(overlaps)

        for i, j, overlap in overlaps:
            if d==0:
                plt.axvline(overlap, color='red', linestyle='--')
            else:
                plt.axhline(overlap, color='blue', linestyle='--')


    plt.xlabel('petal_length')
    plt.ylabel('petal_width')
    plt.title('Data Points and Cluster Center')
    plt.legend()

    plt.show()

    return means, assignments, distortion






def kmeans(means: list, data: list, dimensions, max_iters: int):
    distortions = []

    for _ in range(max_iters):
        # note distortion is before the new assignments were made
        means, assignments, distortion = kmeans_update(means, data, dimensions)
        distortions.append(distortion)
    
    x = range(len(distortions))

    plt.plot(x, distortions, marker='o')

    plt.xlabel('Iteration')
    plt.ylabel('Distortion')

    plt.title(f'Distortion After the ith Iteration for K={len(means)}')

    plt.show()

    return means, assignments, distortions

means, assignments, distortions = kmeans_cluster_plot(initialize_means(2), iris_data(), [2,3], 30)

