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

        //# Bool for the loop
        public bool KEEP_RUNNING = true;

        //This is used when testing, it makes sure the server doesn't wait for a TCP connection
        public bool DO_NOT_RUN = false;

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
            Setup();

            //# Boolean that keeps the server running
            if (!DO_NOT_RUN)
            {
                do
                {
                    //# This blocks progress while it waits for a request
                    HttpListenerContext serverContext = server.GetContext();

                    //# Spawns a thread to deal with a client
                    Task r = new Task(() => DealWithClientRequest(serverContext));
                    r.Start();
                } while (KEEP_RUNNING);
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

            //The first index will be blank
            string[] split = request.RawUrl.Split('/');

            switch (split[1])
            {
                case ("add"):
                    responseString = Operation(split[2], split[3], Add);
                    break;

                case ("sub"):
                    responseString = Operation(split[2], split[3], Sub);
                    break;

                case("mul"):
                    responseString = Operation(split[2], split[3], Mul);
                    break;

                case ("div"):
                    responseString = Operation(split[2], split[3], Div);
                    break;

                //# Used for the test scripts
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
        }

       /// <summary>
       /// Takes values as strings and parses them 
       /// operation is a passed in function that call the necessary method
       /// </summary>
       /// <param name="num1"></param>
       /// <param name="num2"></param>
       /// <param name="operation"></param>
       /// <returns></returns>
        private string Operation(string num1, string num2, Func<int,int,int> operation)
        {
            int value = operation(int.Parse(num1), int.Parse(num2));
            return value.ToString();
        }

        //Operations
        private int Add(int n1, int n2)
        {
            return n1 + n2;
        }
        private int Sub(int n1, int n2)
        {
            return n1 - n2;
        }
        private int Mul(int n1, int n2)
        {
            return n1 * n2;
        }
        private int Div(int n1, int n2)
        {
            return n1 / n2;
        }
    }
}   
