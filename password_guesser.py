from random import randint
import argparse
import matplotlib.pyplot as plt 

class Genetic_algorithm:
    def __init__(self, target="Hello World", chance=5, entities=500):
        self.alphabet = "qwertyuiopasdfghjklzxcvbnm ?.!_QWERTYUIOPASDFGHJKLZXCVBNM"
        self.target = target  # default set to "Hello World"
        self.chance = chance  # mutation chance, default set to 5%
        self.entities = entities  # number of entities in a generation, default set to 500
        self.bestfitness = 0
        self.population = []

    def get_max(self):
        return self.population[0]

    def random_string(self):  # creates a random string
        result = ""
        for _ in range(len(self.target)):
            result += self.alphabet[randint(0, len(self.alphabet) - 1)]
        return result

    def initialize_pop(self):  # generates a list of entities
        entitylist = []
        for i in range(self.entities):
            entitylist.append(self.Entity(self.random_string(), 0))
            entitylist[i].set_fitness(self.target)
        entitylist.sort(key=lambda x: x.get_fitness(), reverse=True)
        self.bestfitness = entitylist[0].get_fitness()
        self.population = entitylist

    def create_child(self, entityone, entitytwo):  # combines 2 entities to "reproduce"
        randnumber = randint(0, len(self.target) - 1)
        newstring = ""
        for i in range(0, randnumber):
            newstring += entityone.get_string()[i]
        for i in range(randnumber, len(self.target)):
            newstring += entitytwo.get_string()[i]
        return self.Entity(newstring, -1)

    def mutate(self, entity):  # mutates an entity
        current = entity.get_string()
        newstring = ""
        for i in range(0, len(current)):
            if randint(0, 100) <= self.chance:
                newstring += self.alphabet[randint(0, len(self.alphabet) - 1)]
            else:
                newstring += current[i]
        return self.Entity(newstring, 0)

    def update_population(self):  # mutates the population
        tenth = self.entities//10 
        newlist = self.population[0:tenth] #selects the top 10% of the population to reproduce
        for i in range(0, ((tenth) * 9)): 
            newlist.append(self.create_child(newlist[randint(
                0, tenth - 1)], newlist[randint(0, tenth - 1)]))
        for i in range(1, len(newlist)):
            newlist[i] = self.mutate(newlist[i])
            newlist[i].set_fitness(self.target)
        newlist.sort(key=lambda x: x.get_fitness(), reverse=True)
        self.bestfitness = newlist[0].get_fitness()
        self.population = newlist

    class Entity:  # entity class
        def __init__(self, string, fitness):
            self.string = string
            self.fitness = fitness

        def get_fitness(self):
            return self.fitness

        def get_string(self):
            return self.string

        def set_fitness(self, target):
            correctNum = 0.0

            if self.string == target:
                self.fitness = 1
                return

            for i in range(len(target)):
                if self.string[i] == target[i]:
                    correctNum += 1
            self.fitness = correctNum / len(target)

        def __str__(self):
            return("Fitness: {:.4f}, String: {}".format(self.fitness, self.string))


def generate_graph(y, title, xlabel = 'Generation', ylabel = 'Fitness', g_type = 1):
    # x axis values 
    # corresponding y axis values 
    x = []
    for i in range(len(y)):
        x.append(i+1)
    
    # plotting the points  
    if g_type == 1:
        plt.plot(x, y) 
    elif g_type == 2:
        plt.plot(x, y, color='blue', linestyle='dashed', linewidth = 2, 
        marker='o', markerfacecolor='red', markersize=8) 
    
    # naming the x axis 
    plt.xlabel(xlabel) 
    # naming the y axis 
    plt.ylabel(ylabel) 
    
    # giving a title to my graph 
    plt.title(title) 
    
    # function to show the plot 
    plt.show() 


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('string', metavar='string', type=str,
                    help='The string to be searched')
    parser.add_argument('-m',dest='chance', type=int, required = False, default = 5,
        help="The percentage chance of a mutation. Default is 5%.")
    parser.add_argument('-e',dest='entities', type=int, required = False, default = 500,
        help="The number of entities. Default is 500.")
    parser.add_argument('-t',dest='times', type=int, required = False, default = 1,
        help="The number of times to run the algorithm. Default is 1.")
    parser.add_argument('--silent',dest='silent', action='store_true', required = False,
        help="Set this flag if you want to run in silent mode and evaluate performance over time.")

    args = parser.parse_args()

    runs = []

    for i in range(args.times):
        world = Genetic_algorithm(args.string, args.chance, args.entities)
        world.initialize_pop()
        counter = 0
        fitness_values = []
        while world.bestfitness < 1:
            counter += 1
            world.update_population()
            if not args.silent:
                print("Generation {} = {}".format(str(counter), world.get_max()))
            fitness_values.append(world.get_max().get_fitness())

        runs.append(counter)
        if not args.silent:
            generate_graph(fitness_values, "Guessing Performance (Run {})".format(i+1))
    
    if args.silent:
        generate_graph(runs, "Performace over multiple runs", xlabel = "Run", ylabel = "Generations", g_type=2)