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
using System.Windows.Shapes;

namespace ClientServer.FTP
{
    /// <summary>
    /// Interaction logic for FTPServer.xaml
    /// </summary>
    public partial class FTPServerWindow : Window
    {
        //# Variables
        FTPServer server;

        //# Constructor
        public FTPServerWindow()
        {
            InitializeComponent();

            server = new FTPServer();
        }
    }
}