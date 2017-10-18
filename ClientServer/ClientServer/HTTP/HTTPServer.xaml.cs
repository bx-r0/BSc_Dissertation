using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace ClientServer.HTTP
{
    /// <summary>
    /// Interaction logic for HTTPServer.xaml
    /// </summary>
    public partial class HTTPServerWindow : Window
    {
        HTTPServer server;
        public static Label Clients;
        public HTTPServerWindow()
        {
            InitializeComponent();
            
            //Added an event that triggers when the window is fully loaded
            Loaded += HTTPServerWindow_Loaded;

            Clients = NumberOfClientsLabel;
        }

        

        private void HTTPServerWindow_Loaded(object sender, RoutedEventArgs e)
        {
            StartServer();
        }

        public void Set_Label(int value)
        {
            NumberOfClientsLabel.Content = value.ToString();
        }

        private void StartServer()
        {
            //Creates a new server a starts it
            server = new HTTPServer();
            Task t = new Task(() => server.Start());

            WindowOutput.Items.Add("SERVER STARTED");
            t.Start();
        }

        private void StopButton_Click(object sender, RoutedEventArgs e)
        {
            //# Sets the loop bool to false
            server.KEEP_RUNNING = false;

            //# Stops any waiting threads
            server.server.Abort();
            WindowOutput.Items.Add("SERVER HAS BEEN STOPPED");
        }
    }
}
