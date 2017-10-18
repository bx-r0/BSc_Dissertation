using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Http;
using System.Net;
using System.Windows;
using System.Windows.Threading;

namespace ClientServer.HTTP
{
    class HTTPServer
    {
        //# Address components
        // + = Localhost
        private const string address = "+";
        private const int port = 80;
        private string socket;
        
        //# String array that holds the prefixes for the server
        private string[] prefixes = new string[] { "/" };
        
        //# Server variable
        public readonly HttpListener server = new HttpListener();

        private int _numberOfClients;
        int numberOfClients
        {
            get { return _numberOfClients; }

            set
            {
                _numberOfClients = value;

                
                Application.Current.Dispatcher.Invoke(() => { HTTPServerWindow.Clients.Content = _numberOfClients.ToString(); });

                
            }
        }

        //# Bool for the loop
        public bool KEEP_RUNNING = true;

        /// <summary>
        /// Setup for the server
        /// </summary>
        public void Setup()
        {
            //# Creates the socket
            socket = $"http://{socket}{address}:{port.ToString()}";

            //# Adds the supported prefixes
            foreach (string prefix in prefixes)
            {
                server.Prefixes.Add($"{socket}{prefix}");
            }

            //# Starts the server
            server.Start();
        }
        
        /// <summary>
        /// Starts the endless execution of the server
        /// </summary>
        public void Start()
        {
            try
            {
                Setup();

                //# Boolean that keeps the server running
                do
                {
                    //# This blocks progress while it waits for a request
                    HttpListenerContext serverContext = server.GetContext();

                    //Increments the number of clients
                    numberOfClients = numberOfClients + 1;
                    
                    //# Spawns a thread to deal with a client
                    Task r = new Task(() => DealWithClientRequest(serverContext));
                    r.Start();
                } while (KEEP_RUNNING);
            }
            catch (Exception e)
            {
                //TODO: Add logging
                MessageBox.Show(e.Message);
            }
            
        }

        /// <summary>
        /// Multi threaded task that will be used to deal with a clients request
        /// </summary>
        /// <param name="serverContext"></param>
        public void DealWithClientRequest(HttpListenerContext serverContext)
        {
            //# Response
            HttpListenerResponse response = serverContext.Response;

            //# Grabs the request data
            HttpListenerRequest request = serverContext.Request;

            //# Switch case to deal with prefixes
            //TODO: Add methods that deal with different prefixes
            //STRUCTURE:
            //      /location/<location_name>
            //
            string responseString = "";
            switch (request.RawUrl)
            {
                case ("/data/"):
                    responseString = "data!";
           
                    break;
                case ("/location/"):
                    responseString = "location!";
                    break;
                    
                case ("/testing"):
                    responseString = "TEST_VALID";
                    break;
                default:
                    responseString = "Error: Non supported prefix";
                    break;
            }
            
            //# Creates a response stream and writes the response to it
            byte[] buffer = Encoding.UTF8.GetBytes(responseString);
            response.ContentLength64 = buffer.Length;
            System.IO.Stream output = response.OutputStream;
            output.Write(buffer, 0, buffer.Length);
            output.Close();

            numberOfClients = numberOfClients - 1;
        }
    }
}
