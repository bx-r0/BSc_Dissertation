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
    class UDPClient
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

        //# Functions
        public void Connect()
        {
            Client = new UdpClient();
            Client.Connect(_address, _port);


            //SendImage();
            SendGridPackets();
            Disconnect();
        }
        public void Disconnect()
        {
            Client.Close();
        }
        private void SendUDPPacket(string data)
        {
            //Grabs the bytes encoding in ASCII
            byte[] dataBytes = Encoding.ASCII.GetBytes(data.ToCharArray());

            //Sends the data
            Client.Send(dataBytes, dataBytes.Length);
        }

        /// <summary>
        /// This method sends packets containing a single value that represents their pixel number
        /// </summary>
        private void SendGridPackets()
        {
            List<int> test = new List<int>();

            //Iterates through each element of a grid
            for (int y = 0; y < GRID_SIZE; y++)
            {
                for (int x = 0; x < GRID_SIZE; x++)
                {
                    //Keeps track of the overall index
                    int cellValue = (y * GRID_SIZE) + x;

                    //Sends a packet containing the index
                    SendUDPPacket(cellValue.ToString());
                }
            }
        }
    }
}
