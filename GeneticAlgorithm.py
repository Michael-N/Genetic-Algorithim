#!./bin/python
'''
Code By Michael Sherif Naguib
license: MIT open source
Date: 12/11/18
@University of Tulsa
Description: a small library for a genetic algorithm..

function:   weighted_choice  code by Stéphane Caron see comment @ code location... takes a list with weighted probabilities and RETURNS an item from the list
            selected based on its probability weight
    param:  seq    the list to draw from
    param:  weights     the weights corresponding to the probabilities of the seq list...

class GeneticAlgorithm
    prop:    self.popSize   holds the value specified for the size of the population   *** see constructor default values that are passed for all of the following props ***
    prop:    self.genomeSize    holds the value that specified the genome size when a instance of GeneticAlgorithm is init.
    prop:    self.randomGeneFunction    can generate a random gene on call
    prop:    self.fitnessFunction   stores the function that determines fitness
    prop:    self.population    stores the population
    prop:    self.populationProbabilityDistribution init as None and this specifies the probs of selection for each individual in the population
                                                    this is computed when fitness is evaluated... 
    prop:   self.mostFitOfAllTime  defaults to 0  in the form of a fake instance of individual class (an individual with an empty genome)
                                    ... stores a copy of the most fit individual of all the generations... 
    prop:   self.populationTotalFitness  defaults to none ... stores the population total fitness so it is not recalculated a bunch of times..
                                         NOTE! this is calculated by the function evalFitnessPopulaton...
    prop:   self.mutationProbability     is the probability that an individual gene in an individual will mutate...
    main:   runs the genetic algorithm passes the most fit after each generation to the logger func  and returns the most fit when finished
        param   stopFunc: Must SPECIFY a function that is passed the most fit individual... then returns true to stop or false to exit
        param   generations=100 by default... number of generations to compute 
        param   logFunc= a function that logs ... is passed data... defaults to printing the data
                         in the form : {"mostFit":self.mostFitOfAllTime,"generationsComputed":currentGen+1}
    constructor:   initilizes a genetic algorithm
        param   fitFunc  = a function that takes a genome list and returns a (numeric) value representing its fitness
        param   randGeneFunc = a function that generates a random VALUE which is the gene for a genome... 
        param   mutationFunc = a function that is passed a gene and returns the mutated gene... 
        param   p = population size int default 10   
        param   g = genome size int default 2
        param   mutationProb = the probability of mutating any one gene in an individual when mutation is computed... ex 5 for 5% also defaults to 5
    method genInitialPop:  generates the initial populaton
    method evalFitnessPop:    evaluates the fitness of the entire population and SETS each child's probability of Selection NOTE! calculates populationTotalFitness... 
        param    fitFunc = a function that takes a genome list and returns a (normalized) value representing its fitness
    method selectTwoFromPop: select two individuals from population based on their probability of selection: Universal stochastic selection... 
                             returns a tuple of the two selected
    method mutatePop:   mutates the population.... (on a gene by gene basis) prob of mutation set as self.mutationProbability
class Individual
    prop:   self.genome stores the genome of the individual
    prop:   self.fitness default None stores the fitness of an individual MUST be a positive numeric value
    prop:   self.probOfSelection default none is set after fitness values ... 
    constructor:   
        param   g = genome list (must have at least 2 items)
    method __str__: to string method...
    method cross:  RETURNS a tuple of 2 child instances seperate from the parents.... 
        param   otherIndividual = (instance of Individual class) number of crossover points is 1
    method mutate: 
        param   mutationFunc = a function that takes a gene as an argument and returnes the mutated gene; WARN defaults to identity function i.e. NO mutation
        param prob = double num default 5%; ex. prob=5 for 5%; is the probability of mutating an individual gene...
    method evalFitness:    
        param    fitFunc = a function that takes a genome list and returns a (normalized) value representing its fitness

'''

#imports 
import random
import copy

#Weighted choice function based on probability distribution:   Code for this function is from https://scaron.info/blog/python-weighted-choice.html 
#                                                              ALL credit for this function to the author Stéphane Caron 
#       I prefered not to simply use the numpy lib but to see how the solution works... 
def weighted_choice(seq, weights):
    assert len(weights) == len(seq)
    assert abs(1. - sum(weights)) < 1e-6

    x = random.random()
    for i, elmt in enumerate(seq):
        if x <= weights[i]:
            return elmt
        x -= weights[i]
#END of the code by Stéphane Caron 
class GeneticAlgorithm:
    def __init__(self,fitFunc,randGeneFunc,mutationFunc,p=10,g=2,mutationProb=5):
        self.popSize=p
        self.genomeSize=g
        self.randomGeneFunction = randGeneFunc
        self.mutationFunction = mutationFunc
        self.mutationProbability = mutationProb
        self.fitnessFunction = fitFunc
        self.populationTotalFitness = None
        self.population=[]
        self.populationProbabilityDistribution = None
        #Make a fake indiviudal and assign a default fitness of 0 and an empty genome
        fakeIndividual = Individual([])
        fakeIndividual.fitness = 0
        self.mostFitOfAllTime = fakeIndividual
    #Compute the Genetic Algorithm: TODO add stopping condition function
    def main(self,stopFunc,generations=100, logFunc=lambda data: print(str(data))):
        #Initilize generation 0 randomly
        currentGen=0
        self.genInitialPop()
        #self.mutatePop() skipped because the genes are random anyway
        self.evalFitnessPop()
        logFunc({"mostFit":self.mostFitOfAllTime,"generationsComputed":currentGen+1})

        #compute the next generation
        while(currentGen<generations):

            #init storage for the new generation:
            newGeneration = []# to boldly go where no one has gone before... these are the voyages of the star ship Enterprise.. [begin theme music]
            #select parents and cross... and append to the new generations
            while(len(newGeneration)<self.popSize):
                parentsTuple = self.selectTwoFromPop(self.populationTotalFitness)
                childrenTuple = parentsTuple[0].cross(parentsTuple[1])
                newGeneration.append(childrenTuple[0])
                newGeneration.append(childrenTuple[1])
            #set the computed generation to be the current population
            self.population = newGeneration
            #mutate the population
            self.mutatePop()
            #Eval the fitness of the population
            self.evalFitnessPop()
            #log the data
            logFunc({"mostFit":self.mostFitOfAllTime,"generationsComputed":currentGen+1})
            #increment the generations
            currentGen = currentGen + 1
            if(stopFunc(self.mostFitOfAllTime)):
                break
        return self.mostFitOfAllTime        
    #generates the intital population
    def genInitialPop(self):
        #Create the individuals
        for i in range(0,self.popSize):
            newGenome = []
            #create each item in the individual's genome
            for j in range(0,self.genomeSize):
                newGenome.append(self.randomGeneFunction())
            #add the individual to the population
            self.population.append(Individual(newGenome))
    #compute fitness
    def evalFitnessPop(self):
        #sum the fitness of the pop...
        totalFitness = 0
        #least fit index:
        leastFitIndex=0
        #calculate the fitness of all the individuals... and check if it is more fit than the fittest of all time
        for i,eachIndividual in enumerate(self.population):
            eachIndividual.evalFitness(self.fitnessFunction)
            totalFitness  =totalFitness + eachIndividual.fitness#sum fitness
            #fittest of all time? if so keep a copy...
            if eachIndividual.fitness > self.mostFitOfAllTime.fitness:
                self.mostFitOfAllTime = copy.deepcopy(eachIndividual)
            #least fit index...
            if(eachIndividual.fitness < self.population[leastFitIndex].fitness):
                leastFitIndex=i
        #UPDATE!!!!NOTE! replace the least fit individual  or a random with the most fit of all time? which will work better?
        #recalculate the total fitness: remove least fit add most fit
        totalFitness = totalFitness - self.population[leastFitIndex].fitness + self.mostFitOfAllTime.fitness
        self.population[leastFitIndex] = copy.deepcopy(self.mostFitOfAllTime)
        
        
        #assign each their probability of selection and store them in a an object list to make lookup faster...
        self.populationProbabilityDistribution = []#reset the list
        for eachIndividual in self.population:
            eachIndividualProb = eachIndividual.fitness/totalFitness
            eachIndividual.probOfSelection = eachIndividualProb
            self.populationProbabilityDistribution.append(eachIndividualProb)       
    #select two individuals from population based on their probability of selection: Universal stochastic selection... returns a tuple of the two selected
    def selectTwoFromPop(self,sumOfFitness):
        #select the first parent
        parentO = weighted_choice(self.population,self.populationProbabilityDistribution)
        #select a canidate for the second
        parentT = weighted_choice(self.population,self.populationProbabilityDistribution)
        #ensure the same parent is not selected twice...
        while(parentT==parentO):
            parentT = weighted_choice(self.population,self.populationProbabilityDistribution)
        return (parentO,parentT)
    #mutates the population according to a integer represented percentage ex. 5 for 5% 
    def mutatePop(self):
        for eachIndividual in self.population:
            eachIndividual.mutate(self.mutationFunction,self.mutationProbability)
class Individual:
    def __init__(self,genome):
        self.genome = genome
        self.fitness = None
        self.probOfSelection = None
    #tostring method
    def __str__(self):
        strTxt = "---------------------------------------------------------------------------\n"
        strTxt = strTxt + "Genome : {0}\nFitness: {1}".format(str(self.genome),str(self.fitness))
        return strTxt
    #Crosses the genes from two individuals
    def cross(self,otherIndividual):
        #crosspoints... i.e the breakpoints for the sections...
        crossPoint = random.randint(1,len(self.genome))
        #pick randomly to the left or right of the crosspoint:
        r = random.randint(0,1)
        ranges = ([0,crossPoint],[crossPoint,len(self.genome)])#left and right respectivly
        selectedRange = ranges[r]
        #create a copy of the parent to be added to the next generation??
        childO = copy.deepcopy(self)
        childT = copy.deepcopy(otherIndividual)
        #cross withine that range
        for i in range(selectedRange[0],selectedRange[1]):
            tmp = childT.genome[i]
            childT.genome[i] = childO.genome[i]
            childO.genome[i] = tmp
        #Set the fitness of the child to None because it is not known yet
        childO.fitness=None
        childT.fitness=None
        #also reset probOfSelection... bc fitness has not assigned it yet
        childO.probOfSelection=None
        childT.probOfSelection=None
        #return the children...
        return (childO,childT)      
    #modifies the genes of this individual
    def mutate(self,mutationFunc = lambda x:x,prob=5):
        for i in range(0,len(self.genome)):
            doMutate= random.randrange(100) < prob
            if(doMutate):
                self.genome[i] = mutationFunc(self.genome[i])
            continue
    #evauluates the fitness of the individual based upon the function
    def evalFitness(self,fitFunc):
        self.fitness = fitFunc(self.genome)

#Begin the main testing of the program:
if __name__ == "__main__":
    #GENETIC ALGORITHM TASK: find this string...
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
    target = "makeitsocommanderdatasaidpiccard"#is used as a global var in determineFitnessOfGenome
    maxGenerations = 10000000
    mutationProb = 5
    population = 20

    #Implementation specific functions... all of these should be modified to fit the specific problem...
    genomeSize=len(target)
    #fitness function
    def determineFitnessOfGenome(genome):
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
    stoppingFitness = determineFitnessOfGenome(target)#stop when max fitness...
    #log
    log = lambda i: print(str(i["mostFit"]) +"\nGen    :{0}".format(i["generationsComputed"]))
    #make a random gene:
    def randomGene():
        r = random.randint(97,122)# inclusive inclusive lower case a-z
        return chr(r)
    #takes a gene and returns the mutated gene...
    def mutationFunction(oldGene):
        #What this does: takes a character and shifts it by a random offset then ensures the character stayes within alpha lowercase
        r = random.randint(0,26)#random offset
        return chr(((((ord(oldGene)-97)+r)%26))+97)#reminiciant of caesar ciphers... could just do random.randint(97,122)
    #Stop function
    def doStop(mostFitOfGeneration):
        #in this case the max fitness for our target is 20 
        return mostFitOfGeneration.fitness == stoppingFitness

    #Initilize a new genetic Algorithm: not 10 genes corresponding to 10 characters in the string     helloworld 
    #                                   which is the targes specified above in the fitness func
    myGeneticAlgorithm = GeneticAlgorithm(determineFitnessOfGenome,randomGene,mutationFunction,p=population,g=genomeSize,mutationProb=mutationProb)
    #run the algorithm
    result = myGeneticAlgorithm.main(doStop,generations=maxGenerations,logFunc=log)#call with default argument for logging
            
''' more challenging targets
(opening lines of Aenied in latin...)
armavirumquecanotroiaequiprimusaborisitaliamfatoprofuguslaviniaquevenitlitoramultumilleetterrisiactatusetaltovisuperumsaevaememoremiunonisobiram


Personal Observations:
it seams as if there is a correlation between how many times certian genes can be reused and how switches can affect the population
... genes are not shifted like a slide rule but must all originate from some unique random selection for a gene at that index
thus limiting the gene types (a-z) in this case might make the algorithm do better
there is also a correlation between a population size and how much mutation can occur before the population continually collapses
i also realized that the fitness function can greatly affect how the algorithm searches... you can reward search behaviors too
(what if ... a genetic algorithm created a neural network structure... which in turn was then trained to preform some task and the convergence rate the network achieves is
the fitness for which the genetic algorithm does its searching... )

also ironically smaller populations in which the generations are thus more quickly computed... for this problem... this results in a higher initial fitness before 
leveling out... 

also a smarter fitness function would be able to distinguish between different types of fitness and weigh their relative benifits... as well as their compatability
with other genes... 

'''
            
            
