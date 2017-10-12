using ClientServer.FTP;
using ClientServer.HTTP;
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

namespace ClientServer
{
    /// <summary>
    /// Interaction logic for Program.xaml
    /// </summary>
    public partial class Program : Window
    {
        public Program()
        {
            InitializeComponent();
            Arguments();
        }

        /// <summary>
        /// This method grabs the arguments and decides which window to open.
        /// For example passing "-f c" will open the FTP Client window
        /// </summary>
        private void Arguments()
        {
            //Grabs the command line arguments
            string[] args = Environment.GetCommandLineArgs();
            
            try
            {
                switch (args[1])
                {
                    //# FTP
                    case "-f":
                        if (ServerOrClient(args[2]))
                        {
                            //# FTP Server
                            ShowWindow(new FTPServerWindow());
                        }
                        else
                        {
                            //# FTP Client
                            ShowWindow(new FTPClientWindow());

                        }
                        break;
                    //# HTTP
                    case "-h":
                        if (ServerOrClient(args[2]))
                        {
                            //# HTTP Server
                            ShowWindow(new HTTPServerWindow());
                        }
                        else
                        {
                            //# HTTP Client
                            ShowWindow(new HTTPClientWindow());
                        }
                        break;
                    //# INVALID
                    default:
                        Error();
                        break;
                }
            }
            catch (Exception e)
            {
                Error(e.Message);
            }

        }

        /// <summary>
        /// RETURN: --
        /// TRUE: SERVER --
        /// FALSE: CLIENT --
        /// </summary>
        /// <param name="parameter"></param>
        /// <returns></returns>
        private bool ServerOrClient(string parameter)
        {
            //# Server
            if (parameter == "s")
            {
                return true;
            }
            else
            //# Client
            if (parameter == "c")
            {
                return false;
            }
            //# Invalid
            else
            {
                Error("Invalid second parameter passed for FTP");
            }
            return false;
        }

        /// <summary>
        /// Used as a general method to show another window
        /// </summary>
        /// <param name="window"></param>
        private void ShowWindow(Window window)
        {
            window.Show();
            this.Hide();
        }
        
        /// <summary>
        /// Methods used to throw an exception, and print to the console
        /// </summary>
        private void Error()
        {
            string msg = "ERROR: Invalid parameters passed";

            Console.WriteLine(msg);
            throw new Exception(msg);
        }
        private void Error(string extra)
        {
            string msg = $"Invalid parameters passed: {extra}";

            Console.WriteLine(msg);
            throw new Exception(msg);
        }
    }
}
