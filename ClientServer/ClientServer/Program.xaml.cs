using ClientServer.FTP;
using ClientServer.UDP;
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


//================= TODO LIST ======================//
//TODO: Tidy up HTTP and Client server code
//TODO: Add tests for HTTP Server and Client functionality testing
//==================================================//
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
                        switch (ServerOrClient(args[2]))
                        {
                            //# FTP Server
                            case WindowToShow.Server:
                                ShowWindow(new FTPServerWindow());
                                break;
                        } 
                        break;
                    //#UDP
                    case "-u":
                        switch (ServerOrClient(args[2]))
                        {
                            case WindowToShow.Server:
                                ShowWindow(new UDPServerWindow());
                                break;
                            case WindowToShow.Client:
                                ShowWindow(new UDPClientWindow());
                                break;
                            case WindowToShow.Both:
                                ShowTwoWindows(new UDPClientWindow(), new UDPServerWindow());
                                break;
                            default:
                                break;
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

        enum WindowToShow
        {
            Server,
            Client,
            Both,
            Error
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="parameter"></param>
        /// <returns></returns>
        private WindowToShow ServerOrClient(string parameter)
        {
            //# Server
            if (parameter == "s")
            {
                return WindowToShow.Server;
            }
            else
            //# Client
            if (parameter == "c")
            {
                return WindowToShow.Client;
            }
            else
            //# Both
            if (parameter == "b")
            {
                return WindowToShow.Both;
            }
            //# Invalid
            else
            {
                Error("Invalid second parameter passed for FTP");
            }
            //Shouldn't reach here
            return WindowToShow.Error;
        }

        /// <summary>
        /// Used as a general method to show another window
        /// </summary>
        /// <param name="window"></param>
        private void ShowWindow(Window window)
        {
            window.Show();
            Close();
        }
        private void ShowTwoWindows(Window window1, Window window2)
        {
            window1.Show();
            window2.Show();
            Close();
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
