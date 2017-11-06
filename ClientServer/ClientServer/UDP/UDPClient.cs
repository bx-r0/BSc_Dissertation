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
        private const int ipSize = 10000;

        //# Files
        //Large file
        //private string fileName = "castle.png";
        //Small single datagram file
        private string fileName = "puppy.jpg";

        //# Constructor 
        public UDPClient(string address, int port)
        {
            //TODO: Dynamic file paths
            string path = @"C:\Users\afray\Documents\GitHub\Dissertation_Project\ClientServer\ClientServer\UDP\UDP_Images\";

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

                //Sends the EOF
                byte[] end = Encoding.ASCII.GetBytes("#");
                Client.Send(end, 1);
            }
        }

        /// <summary>
        /// Method used to split down large byte arrays
        /// </summary>
        /// <param name="imageBytes"></param>
        /// <returns></returns>
        private byte[][] CutImageIntoChunks(byte[] imageBytes)
        {
            //Used to hold the chunk
            List<byte[]> split = new List<byte[]>();

            //Loops until a break
            bool splitLoop = true;
            int count = 0;
            while(splitLoop)
            {
                //Grabs sections
                byte[] bytes = imageBytes.Skip(count * ipSize).Take(ipSize).ToArray();

                if (bytes.Length < ipSize)
                {
                    //Adds to the list
                    split.Add(bytes);
                    splitLoop = false;
                    break;
                }

                //Adds to the list
                split.Add(bytes);
                ++count;
            }
            
            //Turns the list to an array
            return split.ToArray();
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
