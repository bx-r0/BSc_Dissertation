using System;
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

namespace ClientServer.UDP
{
    /// <summary>
    /// Interaction logic for UDPClient.xaml
    /// </summary>
    public partial class UDPClientWindow : Window
    {
        //# Client
        UDPClient Client = new UDPClient("192.168.1.10", UDPServer.port);

        //# Constructor
        public UDPClientWindow()
        {
            InitializeComponent();
        }

        //# Connection click
        private void Connect_Click(object sender, RoutedEventArgs e)
        {
            //# Connects
            Client.Connect();
        }
    }
}
