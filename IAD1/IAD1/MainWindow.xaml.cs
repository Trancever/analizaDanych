﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

using IAD1.models;

namespace IAD1
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            MainWindow2 window = new MainWindow2();
            window.Show();
            ErrorWindow1 window1 = new ErrorWindow1();
            window1.Show();
            KMeansWindow kMeansWindow = new KMeansWindow();
            kMeansWindow.Show();
        }
    }
}
