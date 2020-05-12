from random import randint

class Genetic_algorithm:
    def __init__(self, target = "Hello World", chance = 5, amount = 500):
        self.alphabet = "qwertyuiopasdfghjklzxcvbnm ?.!_QWERTYUIOPASDFGHJKLZXCVBNM"
        self.target = target #default set to "Hello World"
        self.chance = chance #mutation chance, default set to 5%
        self.amount = amount #number of entities in a generation, default set to 500
        self.bestfitness = 0
        self.thelist = []
    def randomize_string(self): #creates a random string
        result = ""
        for _ in range(len(self.target)):
            result += self.alphabet[randint(0, len(self.alphabet) - 1)]
        return result
    
    def generate_entities(self): #generates a list of entities
        entitylist = []
        for i in range(self.amount):
            entitylist.append(self.Entity(self.randomize_string(), 0))
            entitylist[i].set_fitness(self.target)
        entitylist.sort(key = lambda x: x.get_fitness(), reverse = True)
        self.bestfitness = entitylist[0].get_fitness()
        self.thelist = entitylist
    
    def create_child(self, entityone, entitytwo): #combines 2 entities to "reproduce"
        randnumber = randint(0, len(self.target) - 1)
        newstring = ""
        for i in range (0, randnumber):
            newstring += entityone.get_solution()[i]
        for i in range (randnumber, len(self.target)):
            newstring += entitytwo.get_solution()[i]
        return self.Entity(newstring, 0)
    
    def mutate(self, entity): #mutates an entity
        current = entity.get_solution()
        newstring = ""
        for i in range(0, len(current)):
            if randint(0,100) <= self.chance:
                newstring += self.alphabet[randint(0, len(self.alphabet) - 1)]
            else:
                newstring += current[i]
        return self.Entity(newstring, 0)
        
    def mutate_population(self): #mutates the population
        newlist = self.thelist[0:self.amount//10]
        for i in range(0, ((self.amount//10) * 9)):
            newlist.append(self.create_child(newlist[randint(0,(self.amount//10) - 1)], newlist[randint(0,(self.amount//10) - 1)]))
        for i in range(1, len(newlist)):
            newlist[i] = self.mutate(newlist[i])
            newlist[i].set_fitness(self.target)
        newlist.sort(key = lambda x: x.get_fitness(), reverse = True)
        self.bestfitness = newlist[0].get_fitness()
        self.thelist = newlist

    class Entity: #entity class
        def __init__(self, solution, fitness):
            self.solution = solution
            self.fitness = fitness
        def get_fitness(self):
            return self.fitness
        def get_solution(self):
            return self.solution
        def set_fitness(self, target):
            correctNum = 0.0
            for i in range(len(target)):
                if self.solution[i] == target[i]:
                    correctNum += 1
            self.fitness = correctNum / len(target)
        def __str__(self):
            return("Fitness: " + str(self.fitness) + ", Solution: " + self.solution)

if __name__ == '__main__':
    world = Genetic_algorithm("Quant_bio_project!")
    world.generate_entities()
    print("Generation 1 = " + str(world.thelist[0]))
    counter = 1
    while world.bestfitness < 1:
        counter+= 1
        world.mutate_population()
        print("Generation " + str(counter) + " = " + str(world.thelist[0]))