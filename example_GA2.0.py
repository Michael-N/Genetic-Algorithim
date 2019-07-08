'''
Code By Michael Sherif Naguib
Liscence: MIT open source
Date: 7/8/2019
@University of Tulsa
Description: An example for finding a target string using GeneticAlgorithm2.py
'''
#imports
import random
from GeneticAlgorithm2 import *

#Run the main
if __name__ =="__main__":
    #target
    target="makeitsocommanderdatasaidpiccard"

    #Define the Functions for the genes,mutation, and fitness eval as well as a stopping condition function
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
    myGeneticAlgorithm = GeneticAlgorithm(fitness_func=fit_func,random_gene_func=rand_gene,mutation_func=mut_func,mutation_rate=0.05,population_size=100)

    #run the algorithm (exits if the stop condition is met)
    myGeneticAlgorithm.run(10000000,stop_func,log=True)

    #View the best
    print(str(myGeneticAlgorithm.most_fit_gene))