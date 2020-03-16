# GeneticAlgorithm
- Code By Michael Sherif Naguib
- Liscence: MIT open source
- Date: 12/11/18
- @University of Tulsa
- Description: a small library for a genetic algorithm... this is the seccond version of the code after I took more time to think as to how it could be implemented
## About:
- an implememtation of a genetic algorithm; the library code is designed to be used for any specific problem however a string search is implemented here
- the program currently is given a target string for which the fitness function is tailored to provide hints in the form of a fitness value
- this was just a side project to learn more about genetic algorithms...
- also there are some ideas... and realizations I made while messing around with the parameters of the algorithm... 

## Examples
- ```example_G.py``` was run on the target '*make it so commander data said piccard*' (without spaces) 
![exampleGARunning](exampleGA.gif)
- The genome space was all possible letters of the alphabet; 
- The mutation function would simply ofset the character from its order in the alphabet: i.e the letter **a** would be given a random offset ... so for example an offset of 12 would yield the letter **m**
- Genetic algorithms are very good at performing acceptably in many domains across computer science given the right fitness and mutation functions are determined. 

## Documentation: for file ```GeneticAlgorithm.py```
- Description: this file was a first attempt at a genetic algorithm without optimization...
- An example of a String Finder GA for this code is in file ```example_GA.py```
### function:   ```weighted_choice```
- code by Stéphane Caron see comment @ code location... takes a list with weighted probabilities and RETURNS an item from the list selected based on its probability weight
- **param**:  ```seq```    the list to draw from
- **param**:  ```weights```     the weights corresponding to the probabilities of the seq list...

### class ```GeneticAlgorithm```
- **prop**:    ```self.popSize```   holds the value specified for the size of the population   *** see constructor default values that are passed for all of the following props 
- **prop**:    ```self.genomeSize```    holds the value that specified the genome size when a instance of GeneticAlgorithm is init.
- **prop**:    ```self.randomGeneFunction```    can generate a random gene on call
- **prop**:    ```self.fitnessFunction```   stores the function that determines fitness
- **prop**:    ```self.population```    stores the population
- **prop**:    ```self.populationProbabilityDistribution``` init as None and this specifies the probs of selection for each individual in the population
                                                this is computed when fitness is evaluated... 
- **prop**:   ```self.mostFitOfAllTime ``` defaults to 0  in the form of a fake instance of individual class (an individual with an empty genome)
                                ... stores a copy of the most fit individual of all the generations... 
- **prop**:   ```self.populationTotalFitness```  defaults to none ... stores the population total fitness so it is not recalculated a bunch of times..
                                     NOTE! this is calculated by the function evalFitnessPopulaton...
- **prop**:   ```self.mutationProbability```     is the probability that an individual gene in an individual will mutate...
#### method ```main```:   
- runs the genetic algorithm passes the most fit after each generation to the logger func  and returns the most fit when finished
- **param**   ```stopFunc```: Must SPECIFY a function that is passed the most fit individual... then returns true to stop or false to exit
- **param**   ```generations``` =100 by default... number of generations to compute 
- **param**   ```logFunc```= a function that logs ... is passed data... defaults to printing the data
                 in the form : ```python
                 {"mostFit":self.mostFitOfAllTime,"generationsComputed":currentGen+1}
                 ```
#### constructor:   
- initilizes a genetic algorithm
- **param**   ```fitFunc```  = a function that takes a genome list and returns a (numeric) value representing its fitness
- **param**   ```randGeneFunc``` = a function that generates a random VALUE which is the gene for a genome... 
- **param**   ```mutationFunc``` = a function that is passed a gene and returns the mutated gene... 
- **param**   ```p``` = population size int default 10   
- **param**   ```g``` = genome size int default 2
- **param**   ```mutationProb``` = the probability of mutating any one gene in an individual when mutation is computed... ex 5 for 5% also defaults to 5
#### method ```genInitialPop```:  
- generates the initial populaton
####method ```evalFitnessPop```:    
- evaluates the fitness of the entire population and SETS each child's probability of Selection NOTE! calculates populationTotalFitness... 
- **param**    ```fitFunc``` = a function that takes a genome list and returns a (normalized) value representing its fitness
####method ```selectTwoFromPop```: 
- select two individuals from population based on their probability of selection: Universal stochastic selection... 
- returns a tuple of the two selected
####method ```mutatePop```:   
- mutates the population.... (on a gene by gene basis) prob of mutation set as ```self.mutationProbability```
###class Individual
- **prop**:   ```self.genome``` stores the genome of the individual
- **prop**:   ```self.fitness``` default None stores the fitness of an individual MUST be a positive numeric value
- **prop**:   ```self.probOfSelection``` default none is set after fitness values ... 
#### constructor:   
- **param**   ```g``` = genome list (must have at least 2 items)
#### method ```__str__```: 
- to string method...
#### method ```cross```:  
- RETURNS a tuple of 2 child instances seperate from the parents.... 
- **param**   ```otherIndividual``` = (instance of Individual class) number of crossover points is 1
#### method ```mutate```: 
- **param**   ```mutationFunc``` = a function that takes a gene as an argument and returnes the mutated gene; WARN defaults to identity function i.e. NO mutation
- **param** ```prob``` = double num default 5%; ex. prob=5 for 5%; is the probability of mutating an individual gene...
- **method** ```evalFitness```:    
- **param**    ```fitFunc``` = a function that takes a genome list and returns a (normalized) value representing its fitness

## Documentation: for file ```GeneticAlgorithm2.0.py```
- Description: this code has been converted to a less object oriented approach so that it could potentially benefit from distributed computing. 
- Dependancies: tqdm
- An example of a String Finder GA for this code is in file ```example_GA2.py```
### Class ``` GeneticAlgorithm2```:
#### constructor ```__init__(self,fitness_func,random_gene_func,mutation_func,mutation_rate,population_size)```:
- Creates a new genetic algorithm based on the appropriate criteria
- ```fitness_func```: a function that takes a gene list as an argument and returns a numerical fitness value
- ```random_gene_func```: a function that creates and returns a random gene as list
- ```mutation_func```: a function that takes a gene as an input and modifies the items in that reference
- ```mutation_rate```: sets the rate at which mutations can occur (probability gene will be passed to the mutation function)
- ```population_size```: sets the size of the population (must be at least greater than 2)
#### method ```run(self,number_of_generations,stop_func,log=False)```:
- runs the main genetic algorithm and returns the best solution
- ```number_of_generations```: is the number of generations to compute unless the ```stop_func``` function parameter returns true to stop earlier
- ```stop_func```: a function that takes a the most fit gene as a parameter and returns True to stop and False to continue
- ```log```: if True then a progress bar is printed to the screen
#### method ```__universal_stochastic_selection(self)```:
- Chooses at random an index (not index value) in weights based upon the weights themselves
#### method ```__compute_population_fitness_values(self)```:
- updates ```self.population_fitness_values``` with fitness values corresponding to each gene in ```self.population```
#### method ```__compute_population_selection_probabilities(self)```:
- calculates selection probabilities for ```self.population``` based on ```self.population_fitness_values```        
#### method ```__compute_population_cross(self)```:
- Preforms crossover on the pupulation creating the new population
#### method ```__compute_population_mutation(self)```:
- Mutates the current population according to ```mutation_rate```
#### method ```__generate_random_population(self)```:
- Returns a random population list using the ```self.random_gene_func``` and determines size based on ```self.population_size```
        
        
        