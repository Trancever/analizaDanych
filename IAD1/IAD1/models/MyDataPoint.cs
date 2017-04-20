using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IAD1.models
{
    public class MyDataPoint
    {
        public double X { get; set; }
        public double Y { get; set; }
        public double Cluster { get; set; }

        public MyDataPoint() { }
        public MyDataPoint(double x, double y)
        {
            X = x;
            Y = y;
            Cluster = 0;
        }
    }
}
