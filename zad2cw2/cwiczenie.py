import numpy as np
import jsonpickle.ext.numpy as jsonpickle_numpy
from jsonpickle import encode, decode
import os.path

jsonpickle_numpy.register_handlers()

class BackPropagationNetwork:
    """The back-propagation network"""

    #   Class members
    layerCount = 0
    shape = None
    weights = []
    bias = True
    previousWeightDelta = []

    def __str__(self):
        return "Kształt sieci to - {0}\nWagi - {1}\nBias - {2}".format(self.shape, self.weights, self.bias)

    # Class methods
    def __init__(self, layerSize, bias=True):
        """Initialize the network"""
        self.bias = bias
        self.layerCount = len(layerSize) - 1
        self.shape = layerSize

        self._layerInput = []
        self._layerOutput = []
        self.weights = []
        self.previousWeightDelta = []

        if self.bias:
            for (l1, l2) in zip(layerSize[:-1], layerSize[1:]):
                self.weights.append(np.random.normal(size=(l2, l1+1)))
                self.previousWeightDelta = np.copy(self.weights)
        else:
            for (l1, l2) in zip(layerSize[:-1], layerSize[1:]):
                self.weights.append(np.random.normal(size=(l2, l1)))
                self.previousWeightDelta = np.copy(self.weights)


    # Transform functions
    def sigmoid(self, x, Derivative = False):
        if not Derivative:
            return 1 / (1 + np.exp(-x))
        else:
            out = self.sigmoid(x)
            return out * (1 - out)


    # Run method
    def run(self, input):
        """Run the network based on the input data"""

        InputCases = input.shape[0]

        # Clear out the previous intermediate value lists
        self._layerInput = []
        self._layerOutput = []

        # Run it
        for index in range(self.layerCount):
            # Determine layer input
            if index == 0:
                if self.bias:
                    layerInput = self.weights[0].dot(np.vstack([input.T, np.ones([1, InputCases])]))
                else:
                    layerInput = self.weights[0].dot(input.T)
            else:
                if self.bias:
                    layerInput = self.weights[index].dot(np.vstack([self._layerOutput[-1], np.ones([1, InputCases])]))
                else:
                    layerInput = self.weights[index].dot(self._layerOutput[-1])

            self._layerInput.append(layerInput)
            self._layerOutput.append(self.sigmoid(layerInput))

        return self._layerOutput[-1].T


    # Train Epoch method
    def trainEpoch(self, input, target, trainingRate = 0.9, momentum = 0.0):
        """This method trains the network for one epoch"""

        delta = []
        InputCases = input.shape[0]

        # First run the network
        self.run(input)

        # Calculate our deltas
        for index in reversed(range(self.layerCount)):
            if index == self.layerCount - 1:
                # Compare to the target values
                output_delta = self._layerOutput[index] - target.T
                error = np.sum(output_delta**2)
                delta.append(output_delta * self.sigmoid(self._layerInput[index], True))
            else:
                # Compare to the following layer's delta
                delta_pullback = self.weights[index + 1].T.dot(delta[-1])
                delta.append(delta_pullback[:-1, :] * self.sigmoid(self._layerInput[index], True))

        # Compute weight deltas
        for index in range(self.layerCount):
            delta_index = self.layerCount - 1 - index

            if index == 0:
                if self.bias:
                    layerOutput = np.vstack([input.T, np.ones([1, InputCases])])
                else:
                    layerOutput = input.T
            else:
                if self.bias:
                    layerOutput = np.vstack([self._layerOutput[index - 1], np.ones([1, self._layerOutput[index -1 ].shape[1]])])
                else:
                    layerOutput = self._layerOutput[index - 1]

            weightDelta = np.sum(layerOutput[None,:,:].transpose(2, 0, 1) * delta[delta_index][None, :, :].transpose(2, 1, 0), axis = 0)

            self.weights[index] -= trainingRate * weightDelta + momentum * self.previousWeightDelta[index]
            self.previousWeightDelta[index] = np.copy(weightDelta)

        return error

    def test(self, input, target):
        """It uses run function to calculate forward propagation and also prints some raport to file."""
        delta = []
        InputCases = input.shape[0]

        # First run the network
        output = self.run(input)

        output_string = "Input = {0}\nOutput = {1}\nTarget = {2}\nDelta on last layer of neurons = {3}\nOverall delta on all last layer neurons = {4}"\
            .format(input, output, target, output - target, sum((output - target).T**2))

        iterator = 0
        while(True):
            if not os.path.isfile("raport{0}".format(iterator)):
                break
            iterator += 1

        f = open("raport{0}".format(iterator), 'w')
        f.write(output_string)
        f.close()

        return output


def serializeToJson(object, filename):
    """Serialize network to file"""
    f = open(filename, 'w')
    f.write(encode(object))
    f.close()
    print("Sieć została zapisana do pliku - {0}".format(filename))


def deserializeFromJson(filename):
    """Deserialize network from file"""
    f = open(filename, 'r')
    string = f.read()
    return decode(string=string)


if __name__ == "__main__":

    select = 0
    bpn = BackPropagationNetwork((4, 2, 4))

    while(select != 6):

        print("Wcisnij\n1 aby wczytać sieć z pliku.\n2 aby zapisać sieć do pliku.\n3 aby stworzyć nową sieć.\n4 aby zacząć nauke sieci.\n5 aby testować sieć.\n6 aby zakonczyc")
        select = float(input("Podaj wariant: "))

        if select == 1:
            filename = input("Podaj nazwe pliku z którego chcesz wczytać sieć: ")
            bpn = deserializeFromJson(filename=filename)
            print(bpn)
        elif select == 2:
            filename = input("Podaj nazwe pliku do którego chcesz zapisać sieć: ")
            serializeToJson(object=bpn, filename=filename)
        elif select == 3:

            if "tak" == input("Czy sieć ma zawierać bias? "):
                bias = True
            else:
                bias = False

            bpn = BackPropagationNetwork((4, 2, 4), bias=bias)
            print(bpn)
        elif select == 4:
            learning_rate = float(input("Podaj wartość wspołczynnika nauki: "))
            print("Współczynnik nauki = {0}".format(learning_rate))

            momentum = .0
            if "tak" == input("Czy chcesz uwzględnić człon momentum? "):
                momentum = float(input("Podaj wartość momentum: "))
                print("Wartość momentum = {0}".format(momentum))

            shuffle = False
            if "losowa" == input("Stała czy losowa kolejność wzorców? "):
                shuffle = True
                print("Losowa kolejność wzorców")
            else:
                print("Stała kolejność wzorców")

            dataInput = np.array([[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]])
            dataTarget = np.array([[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]])

            maxIteration = 30000
            minError = 1e-2
            error_list = []
            for i in range(maxIteration+1):

                # Shuffle the lists
                if shuffle:
                    zipped = list(zip(dataInput, dataTarget))
                    np.random.shuffle(zipped)
                    dataInput, dataTarget = zip(*zipped)
                    dataInput = np.array(list(dataInput))
                    dataTarget = np.array(list(dataTarget))

                err = bpn.trainEpoch(input=dataInput, target=dataTarget, momentum=momentum, trainingRate=learning_rate)
                error_list.append(err)
                if err <= minError:
                    print("Minimum error reached at iteration {0}".format(i))
                    break

            print("Wagi po zakończeniu nauki = {0}".format(bpn.weights))

            output_string = ""
            iteration = 1
            for x in error_list:
                output_string += str(iteration) + " " + str(x) + "\n"
                iteration += 1

            file = open('error_data', 'w')
            file.write(output_string)
            file.close()

        elif select == 5:
            inp = input("Podaj input, 4 wartosci oddzielone przecinkami: ")
            string_array = inp.split(",")
            input_array = []
            for value in string_array:
                input_array.append(float(value))

            inp = input("Podaj target output, 4 wartosci oddzielone przecinkami: ")
            string_array = inp.split(",")
            output = []
            for value in string_array:
                output.append(float(value))

            print("Wynik dla {0} jest równy = {1}".format(input_array, bpn.test(np.array([input_array]), np.array([output]))))
        elif select == 6:
            break