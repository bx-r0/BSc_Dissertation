using System;
using Microsoft.Win32;
using System.Windows;
using FluentFTP;
using System.Windows.Controls;

namespace ClientServer.FTP
{
    /// <summary>
    /// Interaction logic for FTPClient.xaml
    /// </summary>
    /// 
    [Obsolete()]
    public partial class FTPClientWindow : Window
    {
        //# Variables
        FTPClient client;
        bool fileSelected = false;

        string currentDir = null;

        //# DEBUG
        string testAddress = "ftp://speedtest.tele2.net/";

        //# Constructor
        public FTPClientWindow()
        {
            InitializeComponent();


        }

        //# Buttons
        private void Upload_Click(object sender, RoutedEventArgs e)
        {
            //If the file is selected
            if (fileSelected)
            {
                //Splits the file path by separators
                string[] parts = TextBox_File.Text.Split('\\');

                //The last item will be the file name
                string fileName = parts[parts.Length - 1];

                //TODO: Allow the choice of a directory?
                client.Upload(TextBox_File.Text, $"{currentDir}/{fileName}");
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
                TextBox_File.Text = dlg.FileName;
                fileSelected = true;
            }
            //# File not selected
            else
            {
                if (TextBox_File.Text == "")
                {
                    fileSelected = false;
                }
            }
        }
        private void Connect_Click(object sender, RoutedEventArgs e)
        {
            string address = TextBox_Address.Text;
            string port = TextBox_Port.Text;

            //Default for a port
            if (port.Trim() == "")
            {
                port = "21";
            }

            //Checks if address is valid
            if (address.Trim() == "")
            {
                //Error
                MessageBox.Show("Invalid address entered");
            }
            else
            {

                //# Creates new client
                client = new FTPClient(address);

                //If the client is successful in connection
                if (client.Setup())
                {
                    File_TreeView.MouseDoubleClick += File_TreeView_MouseDoubleClick;
                    LoadFilesIntoTreeView("/");
                }
            }
        }
        
        //# Tree view
        private void LoadFilesIntoTreeView(string uri)
        {
            //# Creates a view item
            TreeViewItem view = new TreeViewItem();
            view.Header = uri;

            //# Saves the current directory
            currentDir = uri;

            //# Grab all the files in the current directory
            foreach (FtpListItem item in client.GetAllListing(uri))
            {
                view.Items.Add(item);
            }

            //# Resets because there will only be one directory selected at one time
            File_TreeView.Items.Clear();

            //Automatically expands the view
            view.IsExpanded = true;

            //# Adds in the view
            File_TreeView.Items.Add(view);
        }

        private void File_TreeView_MouseDoubleClick(object sender, System.Windows.Input.MouseButtonEventArgs e)
        {
            //# Guard
            if (!(File_TreeView.SelectedItem == null))
            {
                //# A messy way to grab uri the directory
                string selectedIndexStr = File_TreeView.SelectedItem.ToString();
                selectedIndexStr = selectedIndexStr.Replace("   ", "/");
                string[] parts = selectedIndexStr.Split('/');

                //Grabs the newest click
                if (selectedIndexStr.StartsWith("DIR"))
                {
                    LoadFilesIntoTreeView(currentDir + parts[1].Trim());
                }
            }
        }

        //Moves to the above directory
        private void UpDirectory_Click(object sender, RoutedEventArgs e)
        {
            if (currentDir != null)
            {   //# Splits the uri into sections
                string[] parts = currentDir.Split('/');

                if (parts.Length >= 2)
                {
                    string parentUri = parts[parts.Length - 2];
                    if (parentUri == "")
                    {
                        LoadFilesIntoTreeView("/");
                    }
                    else
                    {
                        LoadFilesIntoTreeView(parentUri);
                    }


                }
            }
        }

    }
}
