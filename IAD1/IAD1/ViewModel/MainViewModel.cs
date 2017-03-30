using GalaSoft.MvvmLight;
using GalaSoft.MvvmLight.Command;
using IAD1.models;
using OxyPlot;
using OxyPlot.Series;
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

        public RelayCommand Start => new RelayCommand(StartSimulation);

        private void StartSimulation()
        {
            Samples = DataReader.LoadData("Resources/" + _filename);
            if(Samples.Count == 0)
            {
                MessageBoxResult result = MessageBox.Show("Data not loaded. Probably the path is wrong!", "Warning", MessageBoxButton.OK, MessageBoxImage.Warning);
            }
            foreach (DataSample value in _samples)
            {
                Points.Add(new ScatterPoint(value.X, value.Y));
            }
        }
    

        public RelayCommand Next => new RelayCommand(NextStep);

        private void NextStep()
        {
            if(_points != null)
            {

            } 
            else
            {
                MessageBoxResult result = MessageBox.Show("First start the simulation!", "Warning", MessageBoxButton.OK, MessageBoxImage.Warning);
            }
        }
    }
}