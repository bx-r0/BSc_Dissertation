using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Http;
using System.Net;
using System.Windows;

namespace ClientServer.HTTP
{
    class HTTPServer
    {
        private const string address = "+";
        private const int port = 80;
        private string socket = "http://";
        
        private string[] prefixes = new string[] { "/" };
        public HttpListener server = new HttpListener();

        //Bool for the loop
        public bool RUNNING = true;

        public void Setup()
        {
            //Creates the socket
            socket = $"{socket}{address}:{port.ToString()}";

            //Adds the suported prexies
            foreach (string prefix in prefixes)
            {
                server.Prefixes.Add($"{socket}{prefix}");
            }
        }

        public async Task Start()
        {
            try
            {
                Setup();

                while (RUNNING)
                {
                    //Starts the server
                    server.Start();

                    //This blocks progress while it waits
                    HttpListenerContext serverContext = server.GetContext();

                    //Request
                    HttpListenerRequest request = serverContext.Request;

                    //Response
                    HttpListenerResponse response = serverContext.Response;

                    string responseString = "Hello!";
                    byte[] buffer = Encoding.UTF8.GetBytes(responseString);

                    // Get a response stream and write the response to it.
                    response.ContentLength64 = buffer.Length;
                    System.IO.Stream output = response.OutputStream;
                    output.Write(buffer, 0, buffer.Length);

                    output.Close();
                }
            }
            catch (Exception e)
            {
                MessageBox.Show(e.Message);
                //Output("ERROR: " + e.Message);
            }
            
        }

    }
}
