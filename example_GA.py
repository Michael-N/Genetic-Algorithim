'''
Code By Michael Sherif Naguib
Liscence: MIT open source
Date: 7/8/2019
@University of Tulsa
Description: An example for finding a target string using GeneticAlgorithm2.py; also includes commentary on results
'''

#imports
from GeneticAlgorithm import *

# Begin the main testing of the program:
if __name__ == "__main__":
    # GENETIC ALGORITHM TASK: find this string...
    ''' (fun) targets
    =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        helloworld
        hellodolly
        supercalifragilisticexpialidocious
        hedgehog
        chameleon
        iamrootobeyme
        tobeornottobe
        twobeeornaughttwobee

    '''
    target = "makeitsocommanderdatasaidpiccard"  # is used as a global var in determineFitnessOfGenome
    maxGenerations = 10000000
    mutationProb = 5
    population = 20

    # Implementation specific functions... all of these should be modified to fit the specific problem...
    genomeSize = len(target)


    # fitness function
    def determineFitnessOfGenome(genome):
        # set the fitness val
        fitness = 0
        # award a point for every character and +1 for every character in proper sequence
        lastCharInProperSequence = False
        for i, character in enumerate(genome):
            # correct character
            if (target[i] == character):
                fitness = fitness + 1
                lastCharInProperSequence = True
            else:
                lastCharInProperSequence = False
            # previous character was correct too add a bonus
            if lastCharInProperSequence:
                fitness = fitness + 1
        return fitness


    '''def determineFitnessOfGenomeTwo(genome):#just for expiraments...
        fitness=0
        for i,character in enumerate(genome):
            #correct character
            if(target[i] ==character):
                fitness = fitness + 1
                lastCharInProperSequence = True
            #For english the frequency analysis of the language is known... give a slight reward whenever the frequency of the genome
            #matches that of english... this will help it figure out longer passages faster...
            # an adaptive tool that looks statistically at the length of a passage then given known variances finds frequency then
            #given data about the how the frequency fluctuates normally based on passage size make a rule that
            # awards a point if the frequency distribution falls within a certian tolerance range...
            # but not necessarily if it matches perfectly or 
        return fitness
    '''
    stoppingFitness = determineFitnessOfGenome(target)  # stop when max fitness...
    # log
    log = lambda i: print(str(i["mostFit"]) + "\nGen    :{0}".format(i["generationsComputed"]))


    # make a random gene:
    def randomGene():
        r = random.randint(97, 122)  # inclusive inclusive lower case a-z
        return chr(r)


    # takes a gene and returns the mutated gene...
    def mutationFunction(oldGene):
        # What this does: takes a character and shifts it by a random offset then ensures the character stayes within alpha lowercase
        r = random.randint(0, 26)  # random offset
        return chr(((((ord(
            oldGene) - 97) + r) % 26)) + 97)  # reminiciant of caesar ciphers... could just do random.randint(97,122)


    # Stop function
    def doStop(mostFitOfGeneration):
        # in this case the max fitness for our target is 20
        return mostFitOfGeneration.fitness == stoppingFitness


    # Initilize a new genetic Algorithm: not 10 genes corresponding to 10 characters in the string     helloworld
    #                                   which is the targes specified above in the fitness func
    myGeneticAlgorithm = GeneticAlgorithm(determineFitnessOfGenome, randomGene, mutationFunction, p=population,
                                          g=genomeSize, mutationProb=mutationProb)
    # run the algorithm
    result = myGeneticAlgorithm.main(doStop, generations=maxGenerations,
                                     logFunc=log)  # call with default argument for logging

''' more challenging targets
(opening lines of Aenied in latin...)
armavirumquecanotroiaequiprimusaborisitaliamfatoprofuguslaviniaquevenitlitoramultumilleetterrisiactatusetaltovisuperumsaevaememoremiunonisobiram


Personal Observations:
it seams as if there is a correlation between how many times certain genes can be reused and how switches can affect the population
... genes are not shifted like a slide rule but must all originate from some unique random selection for a gene at that index
thus limiting the gene types (a-z) in this case might make the algorithm do better
there is also a correlation between a population size and how much mutation can occur before the population continually collapses
i also realized that the fitness function can greatly affect how the algorithm searches... you can reward search behaviors too
(what if ... a genetic algorithm created a neural network structure... which in turn was then trained to preform some task and the convergence rate the network achieves is
the fitness for which the genetic algorithm does its searching... )

smaller populations in which the generations results in a higher initial fitness before leveling out... 

also a smarter fitness function would be able to distinguish between different types of fitness and weigh their relative benifits... as well as their compatability
with other genes... 

'''