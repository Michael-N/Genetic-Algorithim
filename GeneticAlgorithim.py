# Code by Michael Naguib
# 9/17/2018 (Studying at TU)

#imports:
import random
import math
from numpy.random import choice

class GeneticAlgorithim():
    def __init__(self,log=False,generations=4,pop_size=10,chromo_length = 4,mutation_rate=0.2,num_range=[0,15],fitness_function=lambda x:0):

        #initilize hyper parameters
        self.population_size = pop_size# must be even
        self.chromosome_length = chromo_length
        self.mutation_rate = mutation_rate
        self.num_range = num_range #the range of possible seed values
        self.population= []
        self.fitness_function = fitness_function #is passed an individual to evaluate
        self.mostFit = Individual()#fitness 0
        self.generations=generations
        self.log = log
        #Begin Main sequence
        self.make_initial_population()
        for i in range(0,self.generations):
            self.compute_next_generation()
            if(self.log):
                print("================================================================================================")
                print("Round              :"+ str(i))
                print("Most Fit Chromosome: "+ str(self.mostFit.chromosome))
                print("Fitness Value      : " + str(self.mostFit.fitness))
                for i in range (0,len(self.population)):
                    print("   ID "+str(i)+":"+str(self.population[i].chromosome))
                    print("   Fit:"+ str(self.population[i].fitness))
    def make_rand_chromosome(self):
        #make a chromosome with random numbers
        start_order=list(range(self.num_range[0],self.num_range[1]))# generate a list of items
        shuffled = random.sample(start_order,len(start_order))#shuffle the items
        return  shuffled[0:self.chromosome_length]#truncate
    def mutate_population(self):
        #mutate the population according to the mutation probability
        for i in range(0,self.population_size):
            if(random.random() <= self.mutation_rate):# select by weighted probability
                self.population[i].mutate()
            continue
    def _select_by_weight(self):
        probs=[]
        for i in range(0,self.population_size):
            probs.append(self.population[i].fitness_ratio)
        return choice(self.population,1,p=probs)[0]
    def cross_over_population(self):
        next_generation = []#to boldly go where no man has gone before
        for i in range(0,int(self.population_size/2)):
            #select parents
            parent1  = self._select_by_weight()
            parent2 = self._select_by_weight()
            #make offspring
            offspring = parent1.cross_over(parent2)
            next_generation  = next_generation + offspring
        self.population = next_generation
    def make_initial_population(self):
        #make a population
        for i in range(0,self.population_size):
            self.population.append(Individual(start_c=self.make_rand_chromosome(),start_f=random.randint(0,100)))
    def find_fitness(self):

        total_fitness=0

        #update the individuals fitness and sum the fitnesses
        for i in range(0, len(self.population)):
            self.population[i].fitness =self.fitness_function(self.population[i])
            if self.population[i].fitness >= self.mostFit.fitness:#keep the fit of all time
                self.mostFit = self.population[i]
            total_fitness+=self.population[i].fitness

        #update the fitness ratios
        sumFitRat = 0
        for i in range(0, len(self.population)):
            self.population[i].fitness_ratio = self.population[i].fitness/total_fitness
    def compute_next_generation(self):
        self.find_fitness()
        self.cross_over_population()
        self.mutate_population()

#The class for creating an individual in the population
class Individual():
    def __init__(self,start_c=[],start_f =1.0):
        # The base being for the genetic algorithm:
        self.chromosome = start_c
        self.fitness = start_f
        self.fitness_ratio = 0
    def mutate(self):
        #mutates an individual by switching two elements:
        c_len = len(self.chromosome)
        index_one= random.randint(0,c_len-1)
        index_two = random.randint(0,c_len-1)
        #switch the items
        temp_item = self.chromosome[index_one]
        self.chromosome[index_one] = self.chromosome[index_two]
        self.chromosome[index_two] = temp_item
    def cross_over(self,other_individual):
        #this function crosses two individuals by selecting two slice points
        #along the chromosomes then returning two offspring.

        #length of the chromosome
        c_len = len(self.chromosome)

        #indicies of the crossover points:
        cp_one_ul = random.randint(0,c_len-1)
        cp_two_ul = random.randint(0,c_len-1 )
        cp_one = min(cp_one_ul, cp_two_ul)
        cp_two = max(cp_one_ul,cp_two_ul)

        #First segment of the chromosome:
        seg_one_one = self.chromosome[0:cp_one]#indivudual one non cross part one
        seg_one_two = other_individual.chromosome[0:cp_one]#indivudual two non cross part one


        #Segment of the chromosome that crosses:
        seg_cross_one = self.chromosome[cp_one:cp_two]#indivudual one cross part
        seg_cross_two = other_individual.chromosome[cp_one:cp_two]#indivudual two cross part

        #Final Segment of the chromosomes
        seg_two_one= self.chromosome[cp_two:c_len]#indivudual one non cross part two
        seg_two_two= other_individual.chromosome[cp_two:c_len]# indivudual two non cross part two


        #print("========== cross ==========")
        #print("rand", str(cp_one), str(cp_two))
        #print(self.chromosome)
        #print(str(seg_one_one) + "+" + str(seg_cross_two) + "+" + str(seg_two_one))
        #print("---------------------------")
        #print(other_individual.chromosome)
        #print(str(seg_one_two)+ "+" + str(seg_cross_one) + "+" + str(seg_two_two))
        #print("===========================")
        #concatanate the chromosome fragments
        parent_avg_fit = (self.fitness + other_individual.fitness)/2
        child_one = Individual(start_c=seg_one_one+seg_cross_one+seg_two_one,start_f=parent_avg_fit)
        child_two = Individual(start_c=seg_one_two+seg_cross_two+seg_two_two,start_f=parent_avg_fit)

        #return the child
        return [child_one,child_two]

if __name__ == "__main__":

    #this genetic algorithim learns that by ordering
    #its chromosomes it gains fitness
    def f(individual):
        r = individual.chromosome
        t = list(r)#make a copy
        t.sort()

        points=0
        for i in range(0,len(t)):
            points += 500-abs(r[i]-t[i])# add so it sorts the list
        return points


    calculation = GeneticAlgorithim(log=True,generations=150,chromo_length=15,pop_size=4,fitness_function=f)