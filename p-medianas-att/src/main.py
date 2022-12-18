from vertice import Vertice
from geneticAlgorithm import generateRandomPopulation, populationFitness, selection, crossingOver
import copy
import math
from localSearch import localSearch


def inputParse():
    with open('input.txt') as file:
        lines = file.readlines()
    allVertices = []
    vertices, medians = lines.pop(0).split()
    for eachLine in lines:
        x, y, cap, demand = eachLine.split()
        vertice = Vertice(float(x), float(y), float(cap), float(demand))
        allVertices.append(vertice)

    return [allVertices, int(vertices), int(medians)]


def getWeakestFitness(population):
    weakest = math.inf
    for solution in (population):
        if solution.fitness < weakest:
            weakest = solution.fitness
    return weakest


def getStrongestFitness(population):
    strongest = -math.inf
    strongestIndice = 0
    for indice, solution in enumerate(population):
        if solution.fitness > strongest:
            strongest = solution.fitness
            strongestIndice = indice
    return strongestIndice, strongest



vertices, numVertices, numMedians = inputParse()

population = generateRandomPopulation(
    copy.deepcopy(vertices), numVertices, numMedians)
populationFitness(population)

fit = getWeakestFitness(population)

populationWithLocalSearch = copy.deepcopy(population)
populationWithoutLocalSearch = copy.deepcopy(population)

for i in range(500):
    father, mother = selection(populationWithLocalSearch)
    father2, mother2 = selection(populationWithoutLocalSearch)

    child = crossingOver(father, mother, copy.deepcopy(vertices))
    child2 = crossingOver(father2, mother2, copy.deepcopy(vertices))

    indice, strongestFit = getStrongestFitness(populationWithLocalSearch)
    indice2, strongestFit2 = getStrongestFitness(populationWithoutLocalSearch)
    if child.fitness < strongestFit:
        optChild = localSearch(child, copy.deepcopy(vertices))
        populationWithLocalSearch.pop(indice)
        populationWithLocalSearch.append(optChild)
    if child2.fitness < strongestFit2:
        populationWithoutLocalSearch.pop(indice2)
        populationWithoutLocalSearch.append(child2)

    fit = getWeakestFitness(populationWithLocalSearch)
    fit2 = getWeakestFitness(populationWithoutLocalSearch)


fit = getWeakestFitness(populationWithLocalSearch)
fit2 = getWeakestFitness(populationWithoutLocalSearch)
print('With localsearch: ', fit)
print('Without localsearch: ', fit2)
