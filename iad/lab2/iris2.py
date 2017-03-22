import random
import os
from os import system
import errno
from scipy.spatial import distance
# Definition of Iris class
class Iris:
    def __init__(self, sLen, sWid, pLen, pWid, kind):
        self.sepalLen = sLen
        self.sepalWid = sWid
        self.petalLen = pLen
        self.petalWid = pWid
        self.kind = kind
        self.point = ''

# Iris container
listOfFlowers = []

# Reading data from file to container
with open('iris.data') as f:
    for line in f:
        iris = Iris(float(line[0:3]), float(line[4:7]), float(line[8:11]), float(line[12:15]), line[16:len(line)-1])
        listOfFlowers.append(iris)


def getDataForCharts(container, feature, kind):
    list = []
    for iris in container:
        if iris.kind == kind:
            if feature == 'sepal':
                list.append((getattr(iris, 'sepalLen'), getattr(iris, 'sepalWid')))
            elif feature == 'petal':
                list.append((getattr(iris, 'petalLen'), getattr(iris, 'petalWid')))
    return list


def getSpecifiedIrisData(container, feature, kind):
    list = []
    if not kind:
        for iris in container:
            list.append(getattr(iris, feature))
    else:
        for iris in container:
            if iris.kind == kind:
                list.append(getattr(iris, feature))
    return list

def generalizedMean(container, stage):
    total = 0
    for obj in container:
        total += pow(obj, stage)
    return pow(float(total) / len(container), 1.0 / stage)

def arithmeticMean(container):
    return generalizedMean(container, 1)

def variance(container):
    total = 0
    average = arithmeticMean(container)
    for value in container:
        total += pow(value - average, 2)
    return float(total)/(len(container) - 1)

def standardDeviation(container):
    return pow(variance(container), 0.5)

def generateRandom(average, standardDev):
    return random.normalvariate(average, standardDev)

def taxi(point, iris, stage):
    return distance.cityblock([[point[0]], [point[1]], [point[2]], [point[3]]],
                              [[iris.sepalLen], [iris.sepalWid], [iris.petalLen], [iris.petalWid]])

def euklides(point, iris, stage):
    return distance.euclidean([[point[0]], [point[1]], [point[2]], [point[3]]],
                              [[iris.sepalLen], [iris.sepalWid], [iris.petalLen], [iris.petalWid]])

def minkowski(point, iris, stage):
    return distance.minkowski([[point[0]], [point[1]], [point[2]], [point[3]]],
                              [[iris.sepalLen], [iris.sepalWid], [iris.petalLen], [iris.petalWid]], stage)

def chebyshev(point, iris, stage):
    return distance.chebyshev([[point[0]], [point[1]], [point[2]], [point[3]]],
                              [[iris.sepalLen], [iris.sepalWid], [iris.petalLen], [iris.petalWid]])

def cosinus(point, iris, stage):
    return distance.cosine([[point[0]], [point[1]], [point[2]], [point[3]]],
                              [[iris.sepalLen], [iris.sepalWid], [iris.petalLen], [iris.petalWid]])

points = [[],[],[]]

for obj in points:
    obj.append(generateRandom(arithmeticMean(getSpecifiedIrisData(listOfFlowers, 'sepalLen', '')),
                              standardDeviation(getSpecifiedIrisData(listOfFlowers, 'sepalLen', ''))))
    obj.append(generateRandom(arithmeticMean(getSpecifiedIrisData(listOfFlowers, 'sepalWid', '')),
                              standardDeviation(getSpecifiedIrisData(listOfFlowers, 'sepalWid', ''))))
    obj.append(generateRandom(arithmeticMean(getSpecifiedIrisData(listOfFlowers, 'petalLen', '')),
                              standardDeviation(getSpecifiedIrisData(listOfFlowers, 'petalLen', ''))))
    obj.append(generateRandom(arithmeticMean(getSpecifiedIrisData(listOfFlowers, 'petalWid', '')),
                              standardDeviation(getSpecifiedIrisData(listOfFlowers, 'petalWid', ''))))


def setIrisToPoint(container, points, function, stage):
    for obj in container:
        len1 = function(points[0], obj, stage)
        len2 = function(points[1], obj, stage)
        len3 = function(points[2], obj, stage)
        if len1 > len2 and len1 > len3:
            obj.point = 'A'
        elif len2 > len3:
            obj.point = 'B'
        else:
            obj.point = 'C'

def getIrisesByPoint(container, point):
    list = []
    for iris in container:
        if iris.point == point:
            list.append(iris)
    return list

def writeToFile(string, filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filename, 'w') as file:
        file.write(string)

def convertDataToString(container):
    string = ""
    for obj in container:
        string += (str(obj[0]) + " " + str(obj[1]) + "\n")
    return string

def convertPointToString(a, b):
    string = ""
    string += (str(a) + " " + str(b) + "\n")
    return string

#Points A, B, C
writeToFile(convertPointToString(points[0][0], points[0][1]), 'sepalPoints/irisPointA')
writeToFile(convertPointToString(points[1][0], points[1][1]), 'sepalPoints/irisPointB')
writeToFile(convertPointToString(points[2][0], points[2][1]), 'sepalPoints/irisPointC')

writeToFile(convertPointToString(points[0][2], points[0][3]), 'petalPoints/irisPointA')
writeToFile(convertPointToString(points[1][2], points[1][3]), 'petalPoints/irisPointB')
writeToFile(convertPointToString(points[2][2], points[2][3]), 'petalPoints/irisPointC')

# Taxi algorithm
# set iris to right point
setIrisToPoint(listOfFlowers, points, taxi, 1)

#SEPAL
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'sepal', 'Iris-setosa')), 'taxi/sepalIrisSetosaA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'sepal', 'Iris-setosa')), 'taxi/sepalIrisSetosaB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'sepal', 'Iris-setosa')), 'taxi/sepalIrisSetosaC')

writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'sepal', 'Iris-virginica')), 'taxi/sepalIrisVirginicaA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'sepal', 'Iris-virginica')), 'taxi/sepalIrisVirginicaB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'sepal', 'Iris-virginica')), 'taxi/sepalIrisVirginicaC')

writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'sepal', 'Iris-versicolor')), 'taxi/sepalIrisVersicolorA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'sepal', 'Iris-versicolor')), 'taxi/sepalIrisVersicolorB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'sepal', 'Iris-versicolor')), 'taxi/sepalIrisVersicolorC')

#PETAL
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'petal', 'Iris-setosa')), 'taxi/petalIrisSetosaA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'petal', 'Iris-setosa')), 'taxi/petalIrisSetosaB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'petal', 'Iris-setosa')), 'taxi/petalIrisSetosaC')

writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'petal', 'Iris-virginica')), 'taxi/petalIrisVirginicaA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'petal', 'Iris-virginica')), 'taxi/petalIrisVirginicaB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'petal', 'Iris-virginica')), 'taxi/petalIrisVirginicaC')

writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'petal', 'Iris-versicolor')), 'taxi/petalIrisVersicolorA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'petal', 'Iris-versicolor')), 'taxi/petalIrisVersicolorB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'petal', 'Iris-versicolor')), 'taxi/petalIrisVersicolorC')

# Euklides
# set iris to right point
setIrisToPoint(listOfFlowers, points, euklides, 2)

#SEPAL
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'sepal', 'Iris-setosa')), 'euklides/sepalIrisSetosaA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'sepal', 'Iris-setosa')), 'euklides/sepalIrisSetosaB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'sepal', 'Iris-setosa')), 'euklides/sepalIrisSetosaC')

writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'sepal', 'Iris-virginica')), 'euklides/sepalIrisVirginicaA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'sepal', 'Iris-virginica')), 'euklides/sepalIrisVirginicaB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'sepal', 'Iris-virginica')), 'euklides/sepalIrisVirginicaC')

writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'sepal', 'Iris-versicolor')), 'euklides/sepalIrisVersicolorA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'sepal', 'Iris-versicolor')), 'euklides/sepalIrisVersicolorB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'sepal', 'Iris-versicolor')), 'euklides/sepalIrisVersicolorC')

#PETAL
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'petal', 'Iris-setosa')), 'euklides/petalIrisSetosaA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'petal', 'Iris-setosa')), 'euklides/petalIrisSetosaB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'petal', 'Iris-setosa')), 'euklides/petalIrisSetosaC')

writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'petal', 'Iris-virginica')), 'euklides/petalIrisVirginicaA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'petal', 'Iris-virginica')), 'euklides/petalIrisVirginicaB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'petal', 'Iris-virginica')), 'euklides/petalIrisVirginicaC')

writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'petal', 'Iris-versicolor')), 'euklides/petalIrisVersicolorA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'petal', 'Iris-versicolor')), 'euklides/petalIrisVersicolorB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'petal', 'Iris-versicolor')), 'euklides/petalIrisVersicolorC')


# Minkowski rzedu 3
# set iris to right point
setIrisToPoint(listOfFlowers, points, minkowski, 3)

#SEPAL
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'sepal', 'Iris-setosa')), 'minkowski/sepalIrisSetosaA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'sepal', 'Iris-setosa')), 'minkowski/sepalIrisSetosaB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'sepal', 'Iris-setosa')), 'minkowski/sepalIrisSetosaC')

writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'sepal', 'Iris-virginica')), 'minkowski/sepalIrisVirginicaA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'sepal', 'Iris-virginica')), 'minkowski/sepalIrisVirginicaB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'sepal', 'Iris-virginica')), 'minkowski/sepalIrisVirginicaC')

writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'sepal', 'Iris-versicolor')), 'minkowski/sepalIrisVersicolorA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'sepal', 'Iris-versicolor')), 'minkowski/sepalIrisVersicolorB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'sepal', 'Iris-versicolor')), 'minkowski/sepalIrisVersicolorC')

#PETAL
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'petal', 'Iris-setosa')), 'minkowski/petalIrisSetosaA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'petal', 'Iris-setosa')), 'minkowski/petalIrisSetosaB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'petal', 'Iris-setosa')), 'minkowski/petalIrisSetosaC')

writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'petal', 'Iris-virginica')), 'minkowski/petalIrisVirginicaA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'petal', 'Iris-virginica')), 'minkowski/petalIrisVirginicaB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'petal', 'Iris-virginica')), 'minkowski/petalIrisVirginicaC')

writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'petal', 'Iris-versicolor')), 'minkowski/petalIrisVersicolorA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'petal', 'Iris-versicolor')), 'minkowski/petalIrisVersicolorB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'petal', 'Iris-versicolor')), 'minkowski/petalIrisVersicolorC')


# Chebyshev
# set iris to right point
setIrisToPoint(listOfFlowers, points, chebyshev, 3)

#SEPAL
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'sepal', 'Iris-setosa')), 'chebyshev/sepalIrisSetosaA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'sepal', 'Iris-setosa')), 'chebyshev/sepalIrisSetosaB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'sepal', 'Iris-setosa')), 'chebyshev/sepalIrisSetosaC')

writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'sepal', 'Iris-virginica')), 'chebyshev/sepalIrisVirginicaA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'sepal', 'Iris-virginica')), 'chebyshev/sepalIrisVirginicaB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'sepal', 'Iris-virginica')), 'chebyshev/sepalIrisVirginicaC')

writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'sepal', 'Iris-versicolor')), 'chebyshev/sepalIrisVersicolorA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'sepal', 'Iris-versicolor')), 'chebyshev/sepalIrisVersicolorB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'sepal', 'Iris-versicolor')), 'chebyshev/sepalIrisVersicolorC')

#PETAL
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'petal', 'Iris-setosa')), 'chebyshev/petalIrisSetosaA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'petal', 'Iris-setosa')), 'chebyshev/petalIrisSetosaB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'petal', 'Iris-setosa')), 'chebyshev/petalIrisSetosaC')

writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'petal', 'Iris-virginica')), 'chebyshev/petalIrisVirginicaA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'petal', 'Iris-virginica')), 'chebyshev/petalIrisVirginicaB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'petal', 'Iris-virginica')), 'chebyshev/petalIrisVirginicaC')

writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'petal', 'Iris-versicolor')), 'chebyshev/petalIrisVersicolorA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'petal', 'Iris-versicolor')), 'chebyshev/petalIrisVersicolorB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'petal', 'Iris-versicolor')), 'chebyshev/petalIrisVersicolorC')


# Cosinus
# set iris to right point
setIrisToPoint(listOfFlowers, points, cosinus, 0)

#SEPAL
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'sepal', 'Iris-setosa')), 'cosinus/sepalIrisSetosaA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'sepal', 'Iris-setosa')), 'cosinus/sepalIrisSetosaB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'sepal', 'Iris-setosa')), 'cosinus/sepalIrisSetosaC')

writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'sepal', 'Iris-virginica')), 'cosinus/sepalIrisVirginicaA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'sepal', 'Iris-virginica')), 'cosinus/sepalIrisVirginicaB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'sepal', 'Iris-virginica')), 'cosinus/sepalIrisVirginicaC')

writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'sepal', 'Iris-versicolor')), 'cosinus/sepalIrisVersicolorA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'sepal', 'Iris-versicolor')), 'cosinus/sepalIrisVersicolorB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'sepal', 'Iris-versicolor')), 'cosinus/sepalIrisVersicolorC')

#PETAL
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'petal', 'Iris-setosa')), 'cosinus/petalIrisSetosaA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'petal', 'Iris-setosa')), 'cosinus/petalIrisSetosaB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'petal', 'Iris-setosa')), 'cosinus/petalIrisSetosaC')

writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'petal', 'Iris-virginica')), 'cosinus/petalIrisVirginicaA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'petal', 'Iris-virginica')), 'cosinus/petalIrisVirginicaB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'petal', 'Iris-virginica')), 'cosinus/petalIrisVirginicaC')

writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'A'), 'petal', 'Iris-versicolor')), 'cosinus/petalIrisVersicolorA')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'B'), 'petal', 'Iris-versicolor')), 'cosinus/petalIrisVersicolorB')
writeToFile(convertDataToString(getDataForCharts(getIrisesByPoint(listOfFlowers, 'C'), 'petal', 'Iris-versicolor')), 'cosinus/petalIrisVersicolorC')


def generateCharts():
    files = ['taxi', 'euklides', 'minkowski', 'chebyshev', 'cosinus']
    for x in files:
        system('gnuplot -p ' + x + '/sepalIris.gp')
        system('gnuplot -p ' + x + '/petalIris.gp')

generateCharts()