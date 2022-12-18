from solution import Solution
import copy
import random


def genNeighbors(child, vertices):
    neighborhood = []
    for index, median in enumerate(child.medians):
        num = random.randrange(len(vertices))
        medians = copy.deepcopy(child.medians)
        medians[index] = vertices[num]
        newNeighbor = Solution()
        newNeighbor.initChild(medians, copy.deepcopy(vertices))
        neighborhood.append(newNeighbor)
    return neighborhood


def firstImproviment(neighborhood, middle):
    for neighbor in neighborhood:
        if neighbor.fitness < middle.fitness:
            return neighbor
    return False


def localSearch(child, vertices):
    neighborhood = genNeighbors(child, vertices)
    middle = child
    neighbor = firstImproviment(neighborhood, middle)
    while (neighbor):
        neighborhood = genNeighbors(neighbor, vertices)
        middle = neighbor
        neighbor = firstImproviment(neighborhood, middle)
    return middle
