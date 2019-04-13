#!./bin/python
'''
Code By Michael Sherif Naguib
Liscence: MIT open source
Date: 12/23/18
@University of Tulsa
Description: Seccond attempt at a genetic algorithm... key differences:
             crossing necessarily excludes some genes...
             most fit is not preserved but recorded
             how the genes are encoded matters greatly... preserve data structure
             (IDEA to test: encode data by frequency analysis of english binary tree?)

            Improvements:
                less OOP overhead with individual classes
                more explicit parameter names
'''
#imports
import random
import copy
import tqdm

class GeneticAlgorithm():
    '''
        ## constructor ```__init__(self,fitness_func,random_gene_func,mutation_func,mutation_rate,population_size)```:
        - Creates a new genetic algorithm based on the appropriate criteria
        - ```fitness_func```: a function that takes a gene list as an argument and returns a numerical fitness value
        - ```random_gene_func```: a function that creates and returns a random gene as list
        - ```mutation_func```: a function that takes a gene as an input and modifies the items in that reference
        - ```mutation_rate```: sets the rate at which mutations can occur (probability gene will be passed to the mutation function)
        - ```population_size```: sets the size of the population (must be at least greater than 2)
    '''
    def __init__(self,fitness_func=None,random_gene_func=None,mutation_func=None,mutation_rate=None,population_size=None):
        #testing (confirm type and instance)
        assert(type(fitness_func,) == type(random_gene_func) == type(mutation_func) == type(lambda x:x))
        assert((0<=mutation_rate<=1) and isinstance(mutation_rate,float))
        assert(isinstance(population_size,int))
        #init settings
        self.fitness_func = fitness_func
        self.random_gene_func = random_gene_func
        self.mutation_func = mutation_func
        self.mutation_rate = mutation_rate
        self.population_size = population_size
        #internal variables: (init the first population randomly)
        self.population=self.__generate_random_population()
        self.population_selection_probabilities=[0]*self.population_size
        self.population_fitness_values=[0]*self.population_size
        #collected information (init random)
        self.most_fit_gene= self.random_gene_func()
        self.most_fit_gene_fitness_value = self.fitness_func(self.most_fit_gene)
    '''
        ## method ```run(self,number_of_generations,stop_func,log=False)```:
        - runs the main genetic algorithm and returns the best solution
        - ```number_of_generations```: is the number of generations to compute unless the ```stop_func``` function parameter returns true to stop earlier
        - ```stop_func```: a function that takes a the most fit gene as a parameter and returns True to stop and False to continue
        - ```log```: if True then a progress bar is printed to the screen
    '''
    def run(self,number_of_generations,stop_func,log=False):
        #testing (confirm type and instance)
        assert(isinstance(number_of_generations,int)and number_of_generations>=1)
        assert(type(stop_func)==type(lambda x:x))
        #log? if so use tqdm iterator
        range_vals = tqdm.tqdm(range(0,number_of_generations)) if log else range(0,number_of_generations)
        #compute the generation
        for generation_index in range_vals:
            #print(self.population)
            #do stop?
            if stop_func(self.most_fit_gene):
                break
            #evaluate fitness
            self.__compute_population_fitness_values()
            #Elite-ism ... the most fit from the previous generation replaces the least fit of the next...
            least_fit_index = min(list(enumerate(self.population_fitness_values)), key=lambda val: val[1])[0]
            self.population[least_fit_index] = copy.deepcopy(self.most_fit_gene)
            self.population_fitness_values[least_fit_index] = self.most_fit_gene_fitness_value
            #save a copy of the mostFit of this generation if it is more fit than all previous generations
            most_fit_index = max(list(enumerate(self.population_fitness_values)),key=lambda val: val[1])[0]
            if(self.most_fit_gene_fitness_value <=self.population_fitness_values[most_fit_index]):
                self.most_fit_gene = copy.deepcopy(self.population[most_fit_index])
                self.most_fit_gene_fitness_value = self.population_fitness_values[most_fit_index]
            #compute selection probabilities
            try:
                self.__compute_population_selection_probabilities()
            except(AssertionError):
                #throws an error if divide by 0 --> i.e population selection probabilities are all 0!
                #therefore generate random generation and try again ... continue to the next loop
                self.population = self.__generate_random_population()
                continue
            #compute population crossover (by selection probabilities)
            self.__compute_population_cross()
            #mutate the population
            self.__compute_population_mutation()
    '''
        ## method ```__universal_stochastic_selection(self)```:
        - Chooses at random an index (not index value) in weights based upon the weights themselves
    '''
    @staticmethod
    def __universal_stochastic_selection(weights):
        #ensure the weights sum to 1 up to 3 decimal places... 
        assert(round(sum(weights)*1000)/1000 == 1)
        #weights preserving as the seccond item in each tuple the initial index of the weight
        indexed_weights = list(enumerate(weights))
        #select a random number between 0 and 1:
        r = random.random()
        #preform weighted sampling
        for i in range(0,len(weights)):
            r = r- indexed_weights[i][1]
            if(r<=0):
                #return index
                return indexed_weights[i][0]       
    '''
        ## method ```__compute_population_fitness_values(self)```:
        - updates ```self.population_fitness_values``` with fitness values corresponding to each gene in ```self.population```
    '''
    def __compute_population_fitness_values(self):
        #compute the fitness values
        for i in range(0,self.population_size):
            self.population_fitness_values[i] = self.fitness_func(self.population[i])

    '''
        ## method ```__compute_population_selection_probabilities(self)```:
        - calculates selection probabilities for ```self.population``` based on ```self.population_fitness_values```
    '''
    def __compute_population_selection_probabilities(self):
        #scale the fitness values:
        s = sum(self.population_fitness_values)
        assert(s != 0)
        self.population_selection_probabilities = list(map(lambda val: val/s,self.population_fitness_values ))
    '''
        ## method ```__compute_population_cross(self)```:
        - Preforms crossover on the pupulation creating the new population
    '''
    def __compute_population_cross(self):
        #child population + setup data
        gene_list_length = len(self.population[0])
        child_population=[]
        #compute the population
        for i in range(0,self.population_size//2):
            #crossover point
            crossover_point = random.randint(1,gene_list_length-2)# do not cross at front(0) and at end (length-1)
            #parents (can be identical... ok for now)
            parent_a_index = self.__universal_stochastic_selection(self.population_selection_probabilities)
            parent_b_index = self.__universal_stochastic_selection(self.population_selection_probabilities)
            #prevent identical parents
            while parent_a_index== parent_b_index:
                parent_b_index = self.__universal_stochastic_selection(self.population_selection_probabilities)
            parent_a = self.population[parent_a_index]
            parent_b = self.population[parent_b_index]
            #cross the parents:
            child_gene = parent_a[0:crossover_point] + parent_b[crossover_point:gene_list_length]
            child_gene2 = parent_b[0:crossover_point] + parent_a[crossover_point:gene_list_length]
            #add the children to the population
            child_population.append(child_gene)
            child_population.append(child_gene2)

        self.population = child_population
    '''
        ## method ```__compute_population_mutation(self)```:
        - Mutates the current population according to ```mutation_rate```
    '''
    def __compute_population_mutation(self):
        #iterate through each individual of the population and mutate
        for i in range(0,self.population_size):
            #randomly mutate: weighted probability     #NOTE: this was incorrectly <= ... caused really high mutation rate = population failure
            if (self.mutation_rate >= random.random()):
                #mutate the current element
                self.population[i] = self.mutation_func(self.population[i])
    '''
        ## method ```__generate_random_population(self)```:
        - Returns a random population list using the ```self.random_gene_func``` and determines size based on ```self.population_size```
    '''
    def __generate_random_population(self):
        random_population=[]
        for i in range(0,self.population_size):
            random_population.append(self.random_gene_func())
        return random_population

if __name__ == "__main__":
    #target
    target="makeitsocommanderdatasaidpiccard"
    #Funcs
    def mut_func(oldGene):
        #What this does: takes a character and shifts it by a random offset then ensures the character stayes within alpha lowercase
        r = lambda al: chr(((((ord(al)-97)+random.randint(0,26))%26))+97)#random offset
        return list(map(lambda g: r(g) if random.random()>0.05 else g,oldGene))
    def rand_gene():
        r = lambda x: chr(random.randint(97,122))# inclusive inclusive lower case a-z
        return list(map(r,[None]*len(target)))
    def fit_func(genome):
        #set the fitness val
        fitness=0
        #award a point for every character and +1 for every character in proper sequence
        lastCharInProperSequence=False
        for i,character in enumerate(genome):
            #correct character
            if(target[i] ==character):
                fitness = fitness + 1
                lastCharInProperSequence = True
            else:
                lastCharInProperSequence = False
            #previous character was correct too add a bonus
            if lastCharInProperSequence:
                fitness = fitness + 1
        return fitness
    stoppingFitness = fit_func(target)
    def stop_func(mostFitOfGeneration):
        #in this case the max fitness for our target is 20 
        return fit_func(mostFitOfGeneration) == stoppingFitness
    #make the algorithm
    myGeneticAlgorithm = GeneticAlgorithm(fitness_func=fit_func,random_gene_func=rand_gene,mutation_func=mut_func,mutation_rate=0.05,population_size=20)

    #run the algorithm
    myGeneticAlgorithm.run(10000000,stop_func,log=True)
    print(str(myGeneticAlgorithm.most_fit_gene))


