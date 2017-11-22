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
        UDPServer server;

        //# Constructor
        public UDPServerWindow()
        {
            InitializeComponent();

            GenerateGrid();
        }

        //# Functions
        private void StartServer()
        {
            //# Starts the servers
            Task t = Task.Factory.StartNew(() => server.Start());
            t.ContinueWith((prev) => LoadGrid());
        }

        //# Buttons 
        private void Start_Click(object sender, RoutedEventArgs e)
        {
            //Makes a new server and starts it
            server = new UDPServer();
            StartServer();

            CanRun(false);
        }
        private void Button_Click(object sender, RoutedEventArgs e)
        {
            Reset_Stats();
            Reset_Grid();
            CanRun(true);
        }

        /// <summary>
        /// This function dynamically generates grid depending on the specified size
        /// </summary>
        /// 
        List<Canvas> Pixels = new List<Canvas>();
        private void GenerateGrid()
        {
            //Grabs the size of the grid
            int GRIDSIZE = UDPServer.GRID_SIZE;

            //Creates the rows and columns
            for (int i = 0; i < GRIDSIZE; i++)
            {
                //Adds a new row and a new row
                grid.RowDefinitions.Add(new RowDefinition());
                grid.ColumnDefinitions.Add(new ColumnDefinition());
            }

            //Creates new canvases and put them in a row and column
            for (int y = 0; y < GRIDSIZE; y++)
            {
                for (int x = 0; x < GRIDSIZE; x++)
                {
                    //Creates a new object
                    Canvas canvas = new Canvas();
                    canvas.Background = Brushes.Beige;

                    //Sets the row and the column values
                    Grid.SetRow(canvas, y);
                    Grid.SetColumn(canvas, x);

                    //Adds the newly created control to the grid
                    Pixels.Add(canvas);
                    grid.Children.Add(canvas);
                }
            }
        }

        /// <summary>
        /// This function uses the correctly received packages to light up elements on the grid
        /// </summary>
        private void LoadGrid()
        {
            try
            {
                //Reset
                lostPackets = 0;

                //Loops round the list of correctly received pixels
                int count = 0;
                foreach (bool pixel in server.GRID_Obtained)
                {
                    Canvas c = Pixels[count];

                    //Changes the colour of the pixel
                    if (pixel)
                    {
                        //CORRECT
                        c.Dispatcher.Invoke(() => c.Background = Brushes.Green);
                    }
                    else
                    {
                        lostPackets++;

                        //INCORRECT
                        c.Dispatcher.Invoke(() => c.Background = Brushes.Red);
                    }

                    //Moves the index along
                    ++count;
                }

                Update_Stats();
            }
            catch (Exception e)
            {
                throw;
            }
        }

        //# Resets
        private void Reset_Grid()
        {
            for (int i = 0; i < UDPServer.GRID_SIZE * UDPServer.GRID_SIZE; i++)
            {
                Canvas c = Pixels[i];

                c.Background = Brushes.Beige;
            }
        }
        private void Reset_Stats()
        {
            foreach (Label label in ActiveStats)
            {
                label.Content = "-";
            }
        }

        //# Stats
        //List of labels that have their values changed, this is to be used when resetting values
        List<Label> ActiveStats = new List<Label>();
        int lostPackets;

        /// <summary>
        /// This method deals with calculating and updating the stats on the GUI
        /// </summary>
        private void Update_Stats()
        {
            //Reset
            ActiveStats.Clear();

            //# Packet Loss value
            //Displays the lost packets
            ChangeLabelText(Data_PacketsLost, lostPackets.ToString());

            //# Packet Loss percentage
            //Displays the lost packets as a percentage
            int total_packets = UDPServer.GRID_SIZE * UDPServer.GRID_SIZE;
            int percent = lostPackets / total_packets * 100;
            string msg = percent + "%";
            ChangeLabelText(Data_LostPacketsPercent, msg);

            //# Displays how many packets should be sent
            ChangeLabelText(Data_TotalPackets, total_packets.ToString());
        }

        /// <summary>
        /// This method deals with the dispatching and changing of labels text
        /// It also saves the label to a list so it can be reset later, this is so the reset can be dynamic
        /// </summary>
        /// <param name="l"></param>
        /// <param name="msg"></param>
        private void ChangeLabelText(Label l, string msg)
        {
            l.Dispatcher.Invoke(() => l.Content = msg);

            //Saves the label to reset later
            ActiveStats.Add(l);
        }
      
        /// <summary>
        /// Method that changes the states of buttons, if the program cannot be run it flips the button states and visa versa
        /// </summary>
        /// <param name="state"></param>
        private void CanRun(bool state)
        {
            Button_Start.IsEnabled = state;
            Button_Restart.IsEnabled = !state;
        }
    }
}
