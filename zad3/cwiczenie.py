from cmath import sqrt

import numpy as np
import os.path


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


def readDataFromFile(filename):
    input_array = []
    output_array = []
    with open(filename, "r") as f:
        for line in f:
            tmp = line.split(",")
            size = len(tmp)
            inner_input_array = []
            inner_output_array = []
            for x in range(size-3):
                inner_input_array.append(float(tmp[x]))
            for x in range(size-3, size):
                inner_output_array.append(float(tmp[x]))
            input_array.append(inner_input_array)
            output_array.append(inner_output_array)

    return (np.array(input_array), np.array(output_array))



if __name__ == "__main__":

    data_learn_input_file = input("Podaj nazwe pliku z danymi do nauki: ")
    input_learn__data, output_learn_data = readDataFromFile(data_learn_input_file)

    input_size = len(input_learn__data[0])
    output_size = len(output_learn_data[0])
    print(input_size)
    select = 0
    bpn = None

    while(select != 4):

        print("Wcisnij\n1 aby stworzyć Perceptron\n2 aby zacząć nauke sieci.\n3 aby testować sieć.\n4 aby zakonczyc")
        select = int(input("Podaj wariant: "))

        if select == 1:

            if "tak" == input("Czy sieć ma zawierać bias? "):
                bias = True
            else:
                bias = False

            number_of_hidden_neurons = int(input("Podaj ilość neuronów w warstwie ukrytej: "))

            bpn = BackPropagationNetwork((input_size, number_of_hidden_neurons, output_size), bias=bias)
            print(bpn)
        elif select == 2:
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

            maxIteration = 100000
            minError = 1e-5
            error_list = []
            for i in range(maxIteration+1):

                # Shuffle the lists
                if shuffle:
                    zipped = list(zip(input_learn__data, output_learn_data))
                    np.random.shuffle(zipped)
                    dataInput, dataTarget = zip(*zipped)
                    dataInput = np.array(list(dataInput))
                    dataTarget = np.array(list(dataTarget))

                err = bpn.trainEpoch(input=input_learn__data, target=output_learn_data, momentum=momentum, trainingRate=learning_rate)
                if (i % 20) == 0:
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

        elif select == 3:

            output_array = np.zeros((output_size, output_size))

            good_samples = 0
            bad_samples= 0

            data_test_input_file = input("Podaj nazwe pliku z danymi do testowania sieci: ")
            input_test_data, output_test_data = readDataFromFile(data_test_input_file)

            for x in range(len(input_test_data)):
                output = bpn.run(np.array([input_test_data[x]]))
                print(output)
                computed = np.argmax(output)
                original = np.argmax([output_test_data[x]])
                output_array[original][computed] += 1
                if original == computed:
                    good_samples += 1
                else:
                    bad_samples += 1
            print("Dobrze zakwalifikowanych próbek jest {0}, źle jest {1}, {2}% jest dobrze.".format(good_samples, bad_samples, good_samples/(good_samples+bad_samples)*100))
            print(output_array)
        elif select == 4:
            break