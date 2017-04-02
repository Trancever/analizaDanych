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
    public class MainViewModel : ViewModelBase
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

        public RelayCommand Start => new RelayCommand(StartSimulation);

        private List<List<double>> inputData;

        private void StartSimulation()
        {
            Points.Clear();
            Map = new Map(15);
            inputData = DataReader.LoadData(Filename);
            Map.Initialise(inputData);
            if(inputData.Count == 0)
            {
                MessageBoxResult result = MessageBox.Show("Data not loaded. Probably the path is wrong!", "Warning", MessageBoxButton.OK, MessageBoxImage.Warning);
            }
            foreach (List<double> value in inputData)
            {
                Points.Add(new ScatterPoint(value[0], value[1]));
            }
            foreach (Neuron neuron in Map.Neurons)
            {
                Neurons.Add(new ScatterPoint(neuron.Weights[0], neuron.Weights[1]));
            }
        }
    

        public RelayCommand Next => new RelayCommand(NextStep);

        private void NextStep()
        {
            if(_points != null)
            {
                Neurons.Clear();
                Map.Epoch(inputData);
                foreach (Neuron neuron in Map.Neurons)
                {
                    Neurons.Add(new ScatterPoint(neuron.Weights[0], neuron.Weights[1]));
                }
            }
            else
            {
                MessageBoxResult result = MessageBox.Show("First start the simulation!", "Warning", MessageBoxButton.OK, MessageBoxImage.Warning);
            }
        }

        public RelayCommand ChooseFile => new RelayCommand(PickFile);

        private void PickFile()
        {
            Microsoft.Win32.OpenFileDialog dlg = new Microsoft.Win32.OpenFileDialog()
            {
                DefaultExt = ".data",
                InitialDirectory = Environment.GetFolderPath(Environment.SpecialFolder.Desktop)
            };

            Nullable<bool> result = dlg.ShowDialog();

            if (result.HasValue && result.Value)
            {
                _filename = dlg.FileName;
            }
        }
    }
}