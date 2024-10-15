# Lucas Smith
# Assignment 6
# LJS174
import typing, random, matplotlib.pyplot as plt
class Bag:
    
    def __init__(self, num_candies: int, candy_prob:int, bag_prob: int):
        self.num_candies = num_candies
        # percentage of cherry candy in the bag
        self.candy_prob = candy_prob
        # a priori probability of pulling this type of bag
        self.bag_prob = bag_prob
        
        # generate candies in the bag
        self.candy_list = [0 for _ in range(num_candies)]
        for i in range(num_candies):
            if i < num_candies*candy_prob:
                self.candy_list[i] = "Cherry"
            else:
                self.candy_list[i] = "Lime"
        random.shuffle(self.candy_list)
    
    def pop(self):
        return self.candies.pop()
    

# function for generating h2 probability graph
def assignment6_problem6c():
    # Creation of an h2 bag
    candies = 10
    cherry_prob = .75
    bag_prob = .2
    h2 = Bag(candies, cherry_prob, bag_prob)
    
    observations = [i for i in range(0, candies+1)]
    post_probs = posterior_probabilities(candies)
    
    h1_probs, h2_probs, h3_probs, h4_probs, h5_probs = zip(*post_probs)

    fig, axes = plt.subplots()
    axes.set_xlabel("Number of observations in d")
    axes.set_ylabel("Posterior probability of hypothesis")

    axes.plot(observations, h1_probs, label='h1')
    axes.plot(observations, h2_probs, label='h2')
    axes.plot(observations, h3_probs, label='h3')
    axes.plot(observations, h4_probs, label='h4')
    axes.plot(observations, h5_probs, label='h5')
    plt.legend(loc='best')
    plt.show()

# finds the posterior probabilties given a bag
def posterior_probabilities(candies):
    h1 = Bag(candies, 1, .1)
    h2 = Bag(candies, .75, .2)
    h3 = Bag(candies, .5, .4)
    h4 = Bag(candies, .25, .2)
    h5 = Bag(candies, 0, .1)
    bag_list = [h1,h2,h3,h4,h5]
    sequence = h2.candy_list
    probabilities = [bag.bag_prob for bag in bag_list]
    likelihoods = [1.0 for _ in bag_list]
    results = [probabilities[:]]
    for n, candy in enumerate(sequence):
        cherry_picked = candy == 'Cherry'
        for i in range(len(bag_list)):
            likelihoods[i] = likelihoods[i]*bag_list[i].candy_prob if cherry_picked else likelihoods[i]*(1-bag_list[i].candy_prob)
            probabilities[i] = likelihoods[i]*bag_list[i].bag_prob

        total = sum(probabilities)
        probabilities = [prob/total for prob in probabilities]

        results.append(probabilities[:])
    return results

def custom():   
    candies = int(input("Enter the number of candies per bag: "))
    bags = int(input("Enter the number of bag varieties: "))
    if bags < 1:
        raise ValueError("Must have at least one bag")
    
    probs = [0 for _ in range(bags)]
    candy_probs = [0 for _ in range(bags)]
    
    for i in range(bags):
        probs[i] = float(input(f"Enter the probability to get bag {i+1} as a decimal 0 <= p <= 1: "))
        candy_probs[i] = float(input(f"Enter the percentage of cherry candies in bag {i+1} as a decimal 0 <= p <= 1: "))
        if(candy_probs[i] < 0 or candy_probs[i] >1 ):
            raise ValueError(f"Probability of bag {i+1} must be between 0 and 1")
    
    if int(sum(probs)) != 1:
        raise ValueError("Probability to get bags must sum to 1")
    
    bag_list = [Bag(candies, candy_probs[i], probs[i]) for i in range(bags)]
    for bag in bag_list:
        print(bag.candy_list) 



    

#Terminal interaction for custom bags
if __name__ == "__main__":
    random.seed(8675309)
    assignment6_problem6c()
    print(assignment6_problem6c)
    
    # function for specific entries
    # custom()

