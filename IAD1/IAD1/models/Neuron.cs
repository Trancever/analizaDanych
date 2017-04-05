using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IAD1.models
{
    public class Neuron
    {
        private List<double> weights = new List<double>();
        private double x;
        private double y;
        private Random Random = new Random();

        public List<double> Weights
        {
            get { return weights; }
            set { weights = value; }
        }

        public double Y
        {
            get { return y; }
            set { y = value; }
        }

        public double X
        {
            get { return x; }
            set { x = value; }
        }

        public Neuron(double x, double y, List<double> weights)
        {
            X = x;
            Y = y;
            Weights = weights;
        }

        public double CalculateDistance(List<double> inputVector)
        {
            double distance = 0;
            for(int i = 0; i < weights.Count; i++)
            {
                distance += Math.Pow(inputVector[i] - weights[i], 2);
            }
            return Math.Sqrt(distance);
        }

        public void UpdateWeights(List<double> inputVector, double learningRate, double influence)
        {
            for (int i = 0; i < Weights.Count; i++)
            {
                weights[i] += learningRate * influence * (inputVector[i] - weights[i]);
            }
        }
    }
}
