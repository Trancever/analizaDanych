﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IAD1.models
{
    public class Map
    {
        private List<Neuron> neurons = new List<Neuron>();
        Random Random = new Random();

        private int Iteration = 0;
        private int NumIteration = 10000;
        private double Length;        
        private bool isDone = false;
        private int Dimensions;
        private double Influence;
        private double LearningRate;
        private const double StartLearningRate = 1;
        private double NeighbourhoodRadius;
        private double TimeConstant = 0.1;

        public List<Neuron> Neurons
        {
            get { return neurons; }
            set { neurons = value; }
        }

        public bool IsDone
        {
            get { return isDone; }
            set { isDone = value; }
        }

        public Map(int length)
        {
            this.Length = length;
        }

        public void Initialise(List<List<double>> inputVector)
        {
            this.Dimensions = inputVector[0].Count;
            TimeConstant = NumIteration / Length / 2;
            for (int i = 0; i < Length; i++)
            {
                for (int j = 0; j < Length; j++)
                {
                    List<double> weights = new List<double>();
                    for (int x = 0; x < Dimensions; x++)
                    {
                        weights.Add(Random.NextDouble());
                    }
                    neurons.Add(new Neuron(i, j, weights));
                }
            }
        }

        private Neuron FindBestMatchingUnit(List<double> inputVector)
        {
            double lowestDistance = Double.MaxValue;
            int index = 0;

            for(int i = 0; i < Neurons.Count; i++)
            {
                double distance = Neurons[i].CalculateDistance(inputVector);

                if(distance < lowestDistance)
                {
                    lowestDistance = distance;
                    index = i;
                }
            }
            return Neurons[index];
        }

        private double CalculateNeighbourhoodRadius()
        {
            return Length / 2 * Math.Exp(-(double)Iteration / TimeConstant);
        }

        public Tuple<double, int> Kohonen(List<List<double>> inputVector)
        {
            if (Iteration >= NumIteration)
            {
                return new Tuple<double, int>(countError(inputVector), Iteration);
            }

            for (int i = 0; i < 5; i++)
            {
                Iteration++;
                int indexOfUsedData = Random.Next(0, inputVector.Count - 1);
                Neuron Winner = FindBestMatchingUnit(inputVector[indexOfUsedData]);

                NeighbourhoodRadius = CalculateNeighbourhoodRadius();

                foreach (Neuron neuron in neurons)
                {
                    double distanceToBMU = CalculateDistanceBetweenNeurons(Winner, neuron);
                    double width = Math.Pow(NeighbourhoodRadius, 2);
                    if (distanceToBMU < width)
                    {
                        Influence = CalculateInfluence(distanceToBMU, NeighbourhoodRadius);
                        neuron.UpdateWeights(inputVector[indexOfUsedData], LearningRate, Influence);
                    }
                }
                LearningRate = StartLearningRate * Math.Exp(-(double)Iteration * 5 / NumIteration);
            }
            return new Tuple<double, int>(countError(inputVector), Iteration);
        }

        public Tuple<double, int> NeuralGas(List<List<double>> inputVector)
        {
            if (Iteration >= NumIteration)
            {
                return new Tuple<double, int>(countError(inputVector), Iteration); 
            }

            for (int i = 0; i < 5; i++)
            {
                Iteration++;
                int indexOfUsedData = Random.Next(0, inputVector.Count - 1);
                Neuron Winner = FindBestMatchingUnit(inputVector[indexOfUsedData]);

                NeighbourhoodRadius = CalculateNeighbourhoodRadius();
                double width = Math.Pow(NeighbourhoodRadius, 2);
                List<Neuron> sortedNeurons = new List<Neuron>();
                foreach (Neuron neuron in neurons)
                {
                    double distanceToBMU = CalculateDistanceBetweenNeurons(Winner, neuron);
                    if (distanceToBMU < width)
                    {
                        double index = InsertNeuronIntoList(sortedNeurons, neuron, Winner);
                    }
                }

                for (int j = 0; j < sortedNeurons.Count; j++)
                {
                    Influence = 1 - (j / sortedNeurons.Count);
                    sortedNeurons[j].UpdateWeights(inputVector[indexOfUsedData], LearningRate, Influence);
                }
                LearningRate = StartLearningRate * Math.Exp(-(double)Iteration * 5 / NumIteration);
            }
            return new Tuple<double, int>(countError(inputVector), Iteration);
        }

        private int InsertNeuronIntoList(List<Neuron> sortedNeurons, Neuron neuron, Neuron bmu)
        {
            for (int i = 0; i < sortedNeurons.Count; i++)
            {
                if(CalculateDistanceBetweenNeurons(sortedNeurons[i], neuron) < CalculateDistanceBetweenNeurons(sortedNeurons[i], bmu))
                {
                    sortedNeurons.Insert(i, neuron);
                    return i;
                }
            }
            sortedNeurons.Add(neuron);
            return sortedNeurons.Count-1;
        }

        private double CalculateDistanceBetweenNeurons(Neuron first, Neuron second)
        {
            return Math.Pow(first.X - second.X, 2) + Math.Pow(first.Y - second.Y, 2);
        }

        private double CalculateInfluence(double distanceToBMU, double width)
        {
            return Math.Exp(-(Math.Pow(distanceToBMU, 2)) / (2 * Math.Pow(width, 2)));
        }

        double GaussianFunction(double distance, double widthSq)
        {
            if (widthSq > 0)
            {
                double result = distance * distance;
                result /= 2 * widthSq * widthSq;
                result = Math.Exp(-result);
                return result;
            }
            else
            {
                return 0;
            }
        }

        public double countError(List<List<double>> inputVector)
        {
            double error = 0;
            foreach(List<double> dataSample in inputVector)
            {
                foreach (Neuron neuron in Neurons)
                {
                    error += neuron.CalculateDistance(dataSample);
                }
            }
            return error/inputVector.Count;
        }
    }
}
