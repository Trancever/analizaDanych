using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IAD1.models
{
    public static class DataReader
    {
        public static List<List<double>> LoadData(string file)
        {
            try
            {
                StreamReader reader = File.OpenText(file);
                List<List<double>> list = new List<List<double>>();

                var fmt = new NumberFormatInfo();
                fmt.NegativeSign = "-";
                fmt.PositiveSign = "+";

                while (!reader.EndOfStream)
                {
                    string[] line = reader.ReadLine().Split(' ');
                    List<Double> pattern = new List<double>();
                    for(int i = 0; i < line.Length; i++)
                    {
                        pattern.Add(double.Parse(line[i], fmt));
                    }
                    list.Add(pattern);
                }
                reader.Close();
                return list;
            }
            catch (Exception e)
            {
                return new List<List<double>>();
            }
        }
    }
}
