using ClientServer.Logging;
using System.Windows;

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

            //# Creates the server
            server = new FTPServer();

            //# Sets the output listbox
            //Log_Manager.ServerLogControl = ListBox_ServerLog;
        }
    }
}
