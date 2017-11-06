using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;

namespace ClientServer.UDP
{
    class UDPServer
    {
        //# Setup
        UdpClient Server = new UdpClient(port);
        public static int port = 1000;

        Image UDP_Image;

        //# Constructor 
        public UDPServer()
        {
           
        }

        public async Task Start()
        {
            try
            {
                int _port = port;

                //IPEndPoint object will allow us to read datagrams sent from any source.
                IPEndPoint RemoteIpEndPoint = new IPEndPoint(0, 0);

                byte[] receiveBytes = NewMethod(ref RemoteIpEndPoint);

                //saves the image
                UDP_Image = BytesToImage(receiveBytes);
                UDP_Image.Save("image.png");

                //END TODO: Make multi request?
                Server.Close();
            }
            catch (Exception e)
            {
                throw;
            }
            
        }

        private byte[] NewMethod(ref IPEndPoint RemoteIpEndPoint)
        {
            byte[] returnBytes = Server.Receive(ref RemoteIpEndPoint);

            //Bool to keep looping
            bool recieving = true;
            while(recieving)
            {
                byte[] newReceieve = Server.Receive(ref RemoteIpEndPoint);
                if (newReceieve.Length == 1)
                {
                    //Check for EOF
                    break;
                }
                else
                {
                   //TODO: Join two byte arrays
                }
            }

            // Blocks until a message returns on this socket from a remote host.
            return returnBytes;
        }

        /// <summary>
        /// Function used to convert a byte array into an Image
        /// </summary>
        /// <param name="bytes"></param>
        /// <returns></returns>
        private Image BytesToImage(byte[] bytes)
        {
            ImageConverter converter = new ImageConverter();
            return (Image)converter.ConvertFrom((byte[])bytes);
        }
    }
}
