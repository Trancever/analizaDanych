using GalaSoft.MvvmLight;
using GalaSoft.MvvmLight.Command;
using IAD1.models;
using OxyPlot;
using OxyPlot.Series;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Windows;

namespace IAD1.ViewModel
{
    public class MainViewModel3 : ViewModelBase
    {
        public ObservableCollection<DataSample> Samples
        {
            get { return _samples; }
            set
            {
                _samples = value;
                RaisePropertyChanged();
            }
        }

        private ObservableCollection<DataSample> _samples;

        public string Filename
        {
            get { return _filename; }
            set
            {
                _filename = value;
                RaisePropertyChanged();
            }
        }

        private string _filename = "Path to file with data.";

        public ObservableCollection<ScatterPoint> Points
        {
            get { return _points; }
            set
            {
                _points = value;
                RaisePropertyChanged();
            }
        }

        private ObservableCollection<ScatterPoint> _points = new ObservableCollection<ScatterPoint>();

        public ObservableCollection<ScatterPoint> Neurons
        {
            get { return _neurons; }
            set
            {
                _neurons = value;
                RaisePropertyChanged();
            }
        }

        private ObservableCollection<ScatterPoint> _neurons = new ObservableCollection<ScatterPoint>();

        private Map Map;

        private KMeans kmeans;

        public RelayCommand Start => new RelayCommand(StartSimulation);

        private List<List<double>> inputData;

        private void StartSimulation()
        {
            Points.Clear();
            Neurons.Clear();
            kmeans = new KMeans();
            inputData = DataReader.LoadData(Filename);
            if (inputData.Count == 0)
            {
                MessageBoxResult result = MessageBox.Show("Data not loaded. Probably the path is wrong!", "Warning", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }
            kmeans.init(inputData);
            foreach (var value in inputData)
            {
                Points.Add(new ScatterPoint(value[0], value[1]));
            }
            foreach (var cluster in kmeans._clusters)
            {
                Neurons.Add(new ScatterPoint(cluster.X, cluster.Y));
            }

            count = 0;
            Iterator = "Count = " + count.ToString();

            inputData = kmeans.convertData();
        }

        public RelayCommand Next => new RelayCommand(NextStep);

        private void NextStep()
        {
            if (_points != null)
            {
                Points.Clear();
                kmeans.KMeansMethod(inputData);
                inputData = kmeans.convertData();
                foreach (var value in inputData)
                {
                    Points.Add(new ScatterPoint(value[0], value[1]));
                }
            }
            else
            {
                MessageBoxResult result = MessageBox.Show("First start the simulation!", "Warning", MessageBoxButton.OK, MessageBoxImage.Warning);
            }

            count++;
            Iterator = "Count = " + count.ToString();
        }

        public RelayCommand ChooseFile => new RelayCommand(PickFile);

        private void PickFile()
        {
            Microsoft.Win32.OpenFileDialog dlg = new Microsoft.Win32.OpenFileDialog()
            {
                DefaultExt = ".data",
                InitialDirectory = Environment.CurrentDirectory
            };

            Nullable<bool> result = dlg.ShowDialog();

            if (result.HasValue && result.Value)
            {
                _filename = dlg.FileName;
            }
        }

        public RelayCommand OpenKohonenWindow => new RelayCommand(OpenWindow1);

        private void OpenWindow1()
        {
            var window = new MainWindow();
            window.Show();
        }


        private string _iterator { get; set; }
        private int count;

        public string Iterator
        {
            get { return _iterator; }
            set
            {
                _iterator = value;
                RaisePropertyChanged();
            }
        }
    }
}