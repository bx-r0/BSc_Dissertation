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
using System.Windows.Threading;

namespace ClientServer.UDP
{
    /// <summary>
    /// Interaction logic for UDPServer.xaml
    /// </summary>
    public partial class UDPServerWindow : Window
    {
        //# Connection definition
        UDPServer server = new UDPServer();

        //# Constructor
        public UDPServerWindow()
        {
            InitializeComponent();
        }

        //# Functions
        private void StartServer()
        {
            //# Starts the servers
            Task t = Task.Factory.StartNew(() => server.Start());
            t.ContinueWith((prev) => LoadPhoto());
        }

        /// <summary>
        /// Used to load the photo after a transfer
        /// </summary>
        private void LoadPhoto()
        {
            //# Creates a bitmap image from file
            BitmapImage bitmap = new BitmapImage(new Uri(@"image.png", UriKind.Relative));

            //This make the bitmap image UI safe
            bitmap.Freeze();

            //# Needed to stop 
            Image_TransferedImage.Dispatcher.Invoke(() => Image_TransferedImage.Source = bitmap);
        }

        //# Buttons 
        private void Start_Click(object sender, RoutedEventArgs e)
        {
            StartServer();
            Button_Start.Content = "STARTED";
            Button_Start.IsEnabled = false;
        }
    }
}
