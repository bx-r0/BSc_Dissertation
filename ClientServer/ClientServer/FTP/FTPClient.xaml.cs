using System;
using Microsoft.Win32;
using System.Windows;

namespace ClientServer.FTP
{
    /// <summary>
    /// Interaction logic for FTPClient.xaml
    /// </summary>
    public partial class FTPClientWindow : Window
    {
        //# Variables
        FTPClient client;
        bool fileSelected = false;

        public FTPClientWindow()
        {
            InitializeComponent();

            //# Creates new client
            client = new FTPClient();
            client.Setup();
        }

        //# Buttons
        private void Upload_Click(object sender, RoutedEventArgs e)
        {
            if (fileSelected)
            {
                //Splits the file path by separators
                string[] parts = FileTextBox.Text.Split('\\');
               
                //The last item will be the file name
                string fileName = parts[parts.Length - 1];

                //TODO: Allow the choice of a directory?
                client.Upload(FileTextBox.Text, $"/data/{fileName}");
            }
        }

        private void Browse_Click(object sender, RoutedEventArgs e)
        {
            OpenFileDialog dlg = new OpenFileDialog();

            //# The bool is a flag for if a file was selected or not
            bool? result = dlg.ShowDialog();

            //# File selected
            if (result == true)
            {
                FileTextBox.Text = dlg.FileName;
                fileSelected = true;
            }
            //# File not selected
            else
            {
                if (FileTextBox.Text == "")
                {
                    fileSelected = false;
                }
            }
        }
    }
}
