using ClientServer.HTTP;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
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
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace ClientServer
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class HTTPClientWindow : Window
    {
        public HTTPClientWindow()
        {
            InitializeComponent();
        }

        private async void GET_Click(object sender, RoutedEventArgs e)
        {
            await GetRequest();
        }
        
        async Task GetRequest()
        {
            //# Creates client and grabs response
            HTTPClient client = new HTTPClient();
            HttpResponseMessage output = await client.GET();

            //# Obtains the value
            string value = await output.Content.ReadAsStringAsync();

            //# Adds the value to the list box
            WindowOutput.Items.Add(value);
        }
       
        private void AUTO_Click(object sender, RoutedEventArgs e)
        {
            int maxSeconds = 5;

            //TODO: Create an automatic click
            throw new NotImplementedException();
        }

        private async void SPAM_Click(object sender, RoutedEventArgs e)
        {
            int maxClients = 1000;

            for (int i = 0; i < maxClients; i++)
            {
                await GetRequest();
            }
        }
    }
}
