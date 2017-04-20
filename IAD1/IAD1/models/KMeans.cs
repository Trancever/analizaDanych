using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IAD1.models
{
    public class KMeans
    {
        private int _numberOfClusters = 3;
        int maxCount = 1000;
        int ct = 0;
        bool changed = true;
        bool success = true;

        public List<MyDataPoint> _rawDataToCluster = new List<MyDataPoint>();
        public List<MyDataPoint> _normalizedDataToCluster = new List<MyDataPoint>();
        public List<MyDataPoint> _clusters = new List<MyDataPoint>();

        public List<List<double>> convertData()
        {
            var c = 0;
            var tmp = new List<List<double>>();
            foreach (var point in _normalizedDataToCluster)
            {
                tmp.Add(new List<double>());
                tmp[c].Add(point.X);
                tmp[c].Add(point.Y);
                ++c;
            }
            return tmp;
        }

        public void init(List<List<double>> inputData)
        {
            InitilizeRawData(inputData);

            for (int i = 0; i < _numberOfClusters; i++)
            {
                _clusters.Add(new MyDataPoint() { Cluster = i });
            }

            _normalizedDataToCluster = _rawDataToCluster;

            InitializeCentroids();

            
        }


        public void KMeansMethod(List<List<double>> inputData)
        {
            InitilizeRawData(inputData);

            if (ct < maxCount)
            {
                ++ct;
                success = UpdateDataPointMeans();
                changed = UpdateClusterMembership();
            }
        }

        private void InitilizeRawData(List<List<double>> inputData)
        {
            _rawDataToCluster = new List<MyDataPoint>();
            foreach (var data in inputData)
            {
                var tmp = new MyDataPoint(data[0], data[1]);
                _rawDataToCluster.Add(tmp);
            }
        }



        private void InitializeCentroids()
        {
            Random random = new Random(_numberOfClusters);
            for (int i = 0; i < _numberOfClusters; ++i)
            {
                _normalizedDataToCluster[i].Cluster = _rawDataToCluster[i].Cluster = i;
            }
            for (int i = _numberOfClusters; i < _normalizedDataToCluster.Count; i++)
            {
                _normalizedDataToCluster[i].Cluster = _rawDataToCluster[i].Cluster = random.Next(0, _numberOfClusters);
            }
        }

        private bool UpdateDataPointMeans()
        {
            if (EmptyCluster(_normalizedDataToCluster)) return false;

            var groupToComputeMeans = _normalizedDataToCluster.GroupBy(s => s.Cluster).OrderBy(s => s.Key);
            int clusterIndex = 0;
            double X = 0.0;
            double Y = 0.0;
            foreach (var item in groupToComputeMeans)
            {
                foreach (var value in item)
                {
                    X += value.X;
                    Y += value.Y;
                }
                _clusters[clusterIndex].X = X / item.Count();
                _clusters[clusterIndex].Y = Y / item.Count();
                clusterIndex++;
                X = 0.0;
                Y = 0.0;
            }
            return true;
        }

        private bool UpdateClusterMembership()
        {
            bool changed = false;

            double[] distances = new double[_numberOfClusters];

            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < _normalizedDataToCluster.Count; ++i)
            {

                for (int k = 0; k < _numberOfClusters; ++k)
                    distances[k] = ElucidanDistance(_normalizedDataToCluster[i], _clusters[k]);

                int newClusterId = MinIndex(distances);
                if (newClusterId != _normalizedDataToCluster[i].Cluster)
                {
                    changed = true;
                    _normalizedDataToCluster[i].Cluster = _rawDataToCluster[i].Cluster = newClusterId;
                    sb.AppendLine("Data Point >> Height: " + _rawDataToCluster[i].X + ", Weight: " +
                                   _rawDataToCluster[i].Y + " moved to Cluster # " + newClusterId);
                }
                else
                {
                    sb.AppendLine("No change.");
                }
                sb.AppendLine("------------------------------");

            }
            if (changed == false)
                return false;
            if (EmptyCluster(_normalizedDataToCluster)) return false;
            return true;
        }

        private bool EmptyCluster(List<MyDataPoint> data)
        {
            var emptyCluster = data.GroupBy(s => s.Cluster).OrderBy(s => s.Key).Select(g => new { Cluster = g.Key, Count = g.Count() });

            foreach (var item in emptyCluster)
            {
                if (item.Count == 0)
                {
                    return true;
                }
            }
            return false;
        }

        private void NormalizeData()
        {
            double XSum = 0.0;
            double YSum = 0.0;
            foreach (MyDataPoint dataPoint in _rawDataToCluster)
            {
                XSum += dataPoint.X;
                YSum += dataPoint.Y;
            }
            double XMean = XSum / _rawDataToCluster.Count;
            double YMean = YSum / _rawDataToCluster.Count;
            double sumX = 0.0;
            double sumY = 0.0;
            foreach (MyDataPoint dataPoint in _rawDataToCluster)
            {
                sumX += Math.Pow(dataPoint.X - XMean, 2);
                sumY += Math.Pow(dataPoint.Y - YMean, 2);
                //sumWeight += (dataPoint.Weight - weightMean) * (dataPoint.Weight - weightMean);

            }
            double XSD = sumX / _rawDataToCluster.Count;
            double YSD = sumY / _rawDataToCluster.Count;
            foreach (MyDataPoint dataPoint in _rawDataToCluster)
            {
                _normalizedDataToCluster.Add(new MyDataPoint()
                {
                    X = (dataPoint.X - XMean) / XSD,
                    Y = (dataPoint.Y - YMean) / YSD
                });
            }
        }

        private double ElucidanDistance(MyDataPoint dataPoint, MyDataPoint mean)
        {
            double sumSquaredDiffs = 0.0;
            sumSquaredDiffs = Math.Pow(dataPoint.X - mean.X, 2);
            sumSquaredDiffs += Math.Pow(dataPoint.Y - mean.Y, 2);
            return Math.Sqrt(sumSquaredDiffs);
        }

        private int MinIndex(double[] distances)
        {
            int indexOfMin = 0;
            double smallDist = distances[0];
            for (int k = 0; k < distances.Length; ++k)
            {
                if (distances[k] < smallDist)
                {
                    smallDist = distances[k];
                    indexOfMin = k;
                }
            }
            return indexOfMin;
        }




    }
}
