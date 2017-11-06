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
        private string _pictureFileName;

        //The maximum size a UDP packet can hold
        private const int ipSize = 65000;

        //# Files
        //Large file
        private string fileName = "castle.png";
        //Small single datagram file
        //private string fileName = "puppy.jpg";

        //# Constructor 
        public UDPClient(string address, int port)
        {
            //TODO: Dynamic file paths
            string path = @"C:\Users\User\Documents\GitHub\Dissertation_Project\ClientServer\ClientServer\UDP\UDP_Images\";

            //Create file dynamic file path
            _pictureFileName =
                path + fileName;

            _address = address;
            _port = port;
        }

        //# Functions
        public void Connect()
        {
            Client = new UdpClient();
            Client.Connect(_address, _port);
            SendImage();
            Disconnect();
        }
        public void Disconnect()
        {
            Client.Close();
        }

        /// <summary>
        /// This method is used to send the specified Image
        /// </summary>
        public void SendImage()
        {
            Image image = Image.FromFile(_pictureFileName);

            byte[] imageBytes = ImageToBytes(image);

            //Larger size
            if (imageBytes.Length > ipSize)
            {
                //If the byte stream is too large cut down the image
                byte[][] split = CutImageIntoChunks(imageBytes);

                //Sends the individual packages
                foreach (byte[] bytes in split)
                {
                    if (bytes != null)
                    {
                        //HACK: This is because packets come in too quickly
                        Thread.Sleep(10);

                        //Sends the data
                        Client.Send(bytes, bytes.Length);
                    }
                    //When a blank value is encountered stop looping
                    else
                    {
                        //Sends the EOF
                        byte[] end = Encoding.ASCII.GetBytes("#");
                        Client.Send(end, 1);

                        break;
                    }
                }
            }
            else
            {
                //Sends the data
                Client.Send(imageBytes, imageBytes.Length);
            }
        }

        /// <summary>
        /// Method used to split down large byte arrays
        /// </summary>
        /// <param name="imageBytes"></param>
        /// <returns></returns>
        private byte[][] CutImageIntoChunks(byte[] imageBytes)
        {
            //Used to hold the chunck
            byte[][] split = new byte[100][];

            for (int i = 0; i < 100; i++)
            {
                //Grabs sections
                byte[] bytes = imageBytes.Skip(i * ipSize).Take(ipSize).ToArray();

                if (bytes.Length < ipSize)
                {
                    split[i] = bytes;
                    break;
                }

                split[i] = bytes;

            }
            return split;
        }

        /// <summary>
        /// This function is used to convert an image into a stream of bytes for sending
        /// </summary>
        /// <param name="image">The image to convert</param>
        /// <returns></returns>
        private byte[] ImageToBytes(Image image)
        {
            ImageConverter coverter = new ImageConverter();
            byte[] bytes = (byte[])coverter.ConvertTo(image, typeof(byte[]));
            return bytes;
        }
    }
}
