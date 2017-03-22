# Definition of Iris class
class Iris:
    def __init__(self, sLen, sWid, pLen, pWid, kind):
        self.sepalLen = sLen
        self.sepalWid = sWid
        self.petalLen = pLen
        self.petalWid = pWid
        self.kind = kind

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

#
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


# returns min flower feature from container
def minFlower(container):
    minimum = float('inf')
    for obj in container:
        if obj < minimum:
            minimum = obj
    return minimum


# returns max flower feature from container
def maxFlower(container):
    maximum = float('-inf')
    for obj in container:
        if obj > maximum:
            maximum = obj
    return maximum


def distance(container):
    return maxFlower(container) - minFlower(container)


def median(container):
    container.sort()
    if len(container) % 2:
        return container[len(container)/2]
    else:
        return (container[len(container)/2 - 1] + container[len(container)/2]) / 2.0


def getHalfOfContainer(container, half):
    container.sort()
    if half == 1:
        return container[0:len(container)/2]
    elif half == 2:
        if len(container) % 2:
            return container[len(container)/2 + 1:len(container)]
        else:
            return container[len(container) / 2:len(container)]


def getFirstQuartile(container):
    return median(getHalfOfContainer(container, 1))

def getThirdQuartile(container):
    return median(getHalfOfContainer(container, 2))

def generalizedMean(container, stage):
    total = 0
    for obj in container:
        total += pow(obj, stage)
    return pow(float(total) / len(container), 1.0 / stage)

def geometricMean(container):
    total = 1
    for obj in container:
        total *= obj
    return pow(total, 1.0/len(container))

def arithmeticMean(container):
    return generalizedMean(container, 1)

def harmonicMean(container):
    return generalizedMean(container, -1)

def variance(container):
    total = 0
    average = arithmeticMean(container)
    for value in container:
        total += pow(value - average, 2)
    return float(total)/(len(container) - 1)

def standardDeviation(container):
    return pow(variance(container), 0.5)

def curtosis(container):
    total = 0
    average = arithmeticMean(container)
    standardDev = float(standardDeviation(container))
    for value in container:
        total += pow((value - average)/standardDev, 4)
    n = float(len(container))
    curtosis = n*(n+1)/((n-1)*(n-2)*(n-3))
    curtosis *= total
    curtosis -= (3*pow(n-1, 2))/((n-2)*(n-3))
    return curtosis

print("Srednia arytmetyczna sepal length dla wszystkich irisow = ", arithmeticMean(getSpecifiedIrisData(listOfFlowers, 'sepalLen', '')))
print("Srednia harmoniczna petal length dla Iris-setosa = ", harmonicMean(getSpecifiedIrisData(listOfFlowers, 'petalLen', 'Iris-setosa')))
print("Srednia geometryczna petal length dla Iris-setosa = ", geometricMean(getSpecifiedIrisData(listOfFlowers, 'petalLen', 'Iris-setosa')))
print("Srednia potegowa rzedu 3 petal length dla Iris-setosa = ", generalizedMean(getSpecifiedIrisData(listOfFlowers, 'petalLen', 'Iris-setosa'), 3))
print("Srednia potegowa rzedu 1 petal length dla Iris-setosa = ", generalizedMean(getSpecifiedIrisData(listOfFlowers, 'petalLen', 'Iris-setosa'), 1))
print("Mediana sepal width dla Iris-versicolor = ", median(getSpecifiedIrisData(listOfFlowers, 'sepalWid', 'Iris-versicolor')))
print("Q1 petal width dla Iris-virginica = ", getFirstQuartile(getSpecifiedIrisData(listOfFlowers, 'petalWid', 'Iris-virginica')))
print("Q3 petal width dla Iris-virginica = ", getThirdQuartile(getSpecifiedIrisData(listOfFlowers, 'petalWid', 'Iris-virginica')))
print("Wariancja dla sepal width dla Iris-virginica = ", variance(getSpecifiedIrisData(listOfFlowers, 'sepalWid', 'Iris-virginica')))
print("Odchylenie standardowe dla sepal width dla Iris-virginica = ", standardDeviation(getSpecifiedIrisData(listOfFlowers, 'sepalWid', 'Iris-virginica')))
print("Kurtoza dla sepal width dla Iris-virginica = ", curtosis(getSpecifiedIrisData(listOfFlowers, 'sepalLen', 'Iris-virginica')))

# Drawing chart

# to generate charts install pygal library and uncomment code below

# import pygal
# sepalChart = pygal.XY(stroke=False, x_title='Sepal Length', y_title='Sepal Width')
# sepalChart.title = 'Distribution of sepal'
# sepalChart.add('Iris-setosa', getDataForCharts(listOfFlowers, 'sepal', 'Iris-setosa'))
# sepalChart.add('Iris-versicolor', getDataForCharts(listOfFlowers, 'sepal', 'Iris-versicolor'))
# sepalChart.add('Iris-virginica', getDataForCharts(listOfFlowers, 'sepal', 'Iris-virginica'))
# sepalChart.render_to_file('sepalChart.svg')
#
# petalChart = pygal.XY(stroke=False, x_title='Petal Length', y_title='Petal Width')
# petalChart.title = 'Distribution of petal'
# petalChart.add('Iris-setosa', getDataForCharts(listOfFlowers, 'petal', 'Iris-setosa'))
# petalChart.add('Iris-versicolor', getDataForCharts(listOfFlowers, 'petal', 'Iris-versicolor'))
# petalChart.add('Iris-virginica', getDataForCharts(listOfFlowers, 'petal', 'Iris-virginica'))
# petalChart.render_to_file('petalChart.svg')