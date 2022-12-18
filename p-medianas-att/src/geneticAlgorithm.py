from solution import Solution
import random
import copy


def generateRandomPopulation(vertices, numVertices, numMedians):
    population = []
    for i in range(100):
        newSolution = Solution()
        newSolution.randomize(copy.deepcopy(vertices), numMedians)
        population.append(newSolution)
    return population


def populationFitness(population):
    for solution in population:
        solution.calculateFitness()


def selection(population):
    father, mother = None, None
    numOfChosen = 4
    selectedSolutions = []
    for count in range(numOfChosen):
        randPosition = random.randrange(numOfChosen)
        solution = population[randPosition]
        selectedSolutions.append(solution)
    father = selectedSolutions[0]
    mother = selectedSolutions[1]
    for i in range(2, numOfChosen):
        if selectedSolutions[i].fitness > father.fitness:
            mother = father
            father = selectedSolutions[i]
        else:
            if selectedSolutions[i].fitness > mother.fitness:
                mother = selectedSolutions[i]
    return father, mother


def mutation(childMedians, allVertices, numMedians):
    choice = random.randrange(0, 2)
    modifiedMedian = random.randrange(0, len(childMedians))
    if choice == 1:
        childMedians.pop(modifiedMedian)
        chosenPostion = random.randrange(0, len(allVertices))
        while len(childMedians) != numMedians:
            newMedian = allVertices.pop(chosenPostion)
            if validateMedians(childMedians, newMedian):
                childMedians.append(newMedian)
            chosenPostion = random.randrange(0, len(allVertices))


def crossingOver(father, mother, allVertices):
    childMedians = []
    fatherMedians = father.medians
    motherMedians = mother.medians
    numMedians = len(father.medians)
    for fatherMedian in fatherMedians:
        for motherMedian in motherMedians:
            if fatherMedian.id == motherMedian.id:
                childMedians.append(copy.deepcopy(fatherMedian))
    while len(childMedians) != numMedians:
        chosenPostion = random.randrange(0, numMedians)
        choice = random.randrange(0, 2)
        if choice == 1:
            if validateMedians(childMedians, fatherMedians[chosenPostion]):
                newMedian = copy.deepcopy(
                    fatherMedians[chosenPostion])
                childMedians.append(newMedian)

        else:
            if validateMedians(childMedians, motherMedians[chosenPostion]):
                newMedian = copy.deepcopy(
                    motherMedians[chosenPostion])
                childMedians.append(newMedian)

    child = Solution()
    mutation(childMedians, copy.deepcopy(allVertices), numMedians)
    for i in childMedians:
        assert(i.cap == i.capReal)
    child.initChild(childMedians, copy.deepcopy(allVertices))
    return child


def validateMedians(child, newMedian):
    for median in child:
        if newMedian.id == median.id:
            return False
    return True
