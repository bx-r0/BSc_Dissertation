using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Net.Sockets;
using System.Reflection;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace ClientServer.UDP
{
    public class UDPClient
    {
        //# Setup
        UdpClient Client;

        //# Connection details
        private string _address;
        private int _port;

        //Used to specify how large the grid on the server is
        //It will automatically change, and how many elements the grid contains
        public const int GRID_SIZE = 64; 

        //# Constructor 
        public UDPClient(string address, int port)
        {
            _address = address;
            _port = port;
        }

        public void Run()
        {
            Connect();
            SendGridPackets();
            Disconnect();
        }

        //# Functions
        public void Connect()
        {
            Client = new UdpClient();
            Client.Connect(_address, _port);
        }
        public void Disconnect()
        {
            Client.Close();
        }
        public void SendUDPPacket(string data)
        {
            //Grabs the bytes encoding in ASCII
            byte[] dataBytes = Encoding.ASCII.GetBytes(data.ToCharArray());

            //Sends the data
            Client.Send(dataBytes, dataBytes.Length);
        }

        //Testing variable that is used to check if the correct about of packets are sent
        public int test_GridCount;
        /// <summary>
        /// This method sends packets containing a single value that represents their pixel number
        /// </summary>
        public void SendGridPackets()
        {
            test_GridCount = 0;

            //Iterates through each element of a grid
            for (int y = 0; y < GRID_SIZE; y++)
            {
                for (int x = 0; x < GRID_SIZE; x++)
                {
                    //Keeps track of the overall index
                    int cellValue = (y * GRID_SIZE) + x;

                    //Sends a packet containing the index
                    SendUDPPacket(cellValue.ToString());

                    //TESTING
                    test_GridCount++;
                }
            }
        }
    }
}
