using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;
using System.Timers;

namespace ClientServer.UDP
{
    class UDPServer
    {
        //# Setup
        UdpClient Server = new UdpClient(port);
        public static int port = 1000;

        //Timeout in ms
        private const int timeOut = 5000;
       
        //# Size of the grid
        public const int GRID_SIZE = UDPClient.GRID_SIZE;
        public bool[] GRID_Obtained = new bool[GRID_SIZE * GRID_SIZE];

        //# Constructor 
        public UDPServer()
        {
        }

        /// <summary>
        /// What runs when the server is started
        /// </summary>
        /// <returns></returns>
        public async Task Start()
        {
            try
            {
                int _port = port;

                //IPEndPoint object will allow us to read datagrams sent from any source.
                IPEndPoint RemoteIpEndPoint = new IPEndPoint(0, 0);

                //Image_Processing(ref RemoteIpEndPoint);
                Grid_Processing(ref RemoteIpEndPoint);

                Server.Close();
            }
            catch (Exception e)
            {
                throw;
            }

        }

        //# Reading grid packages
        private void Grid_Processing(ref IPEndPoint RemoteIpEndPoint)
        {
            try
            {
                //Sets a timeouts
                Server.Client.ReceiveTimeout = timeOut;

                //Loops and receives the incoming packets
                while (true)
                {
                    byte[] returnBytes = Server.Receive(ref RemoteIpEndPoint);

                    //Grabs the value
                    int value = int.Parse(Encoding.ASCII.GetString(returnBytes));

                    //Sets the value to received
                    GRID_Obtained[value] = true;
                }
            }
            //This is where the program will end up after a timeout
            catch (Exception e)
            {
                //TODO: Handle exception
            }
        }
    }
}
