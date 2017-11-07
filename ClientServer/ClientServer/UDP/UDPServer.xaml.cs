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
            StartServer();
            Button_Start.Content = "STARTED";
            Button_Start.IsEnabled = false;
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
                        //INCORRECT
                        c.Dispatcher.Invoke(() => c.Background = Brushes.Red);

                    }

                    //Moves the index along
                    ++count;
                }
            }
            catch (Exception e)
            {
                throw;
            }
        }
    }
}
