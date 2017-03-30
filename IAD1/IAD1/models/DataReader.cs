using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IAD1.models
{
    public static class DataReader
    {
        public static ObservableCollection<DataSample> LoadData(string file)
        {
            try
            {
                StreamReader reader = File.OpenText(file);
                ObservableCollection<DataSample> list = new ObservableCollection<DataSample>();
                while (!reader.EndOfStream)
                {
                    string[] line = reader.ReadLine().Split(' ');
                    DataSample sample = new DataSample();
                    sample.X = double.Parse(line[0]);
                    sample.Y = double.Parse(line[1]);
                    list.Add(sample);
                }
                reader.Close();
                return list;
            }
            catch (Exception e)
            {
                return new ObservableCollection<DataSample>();
            }
        }
    }
}
