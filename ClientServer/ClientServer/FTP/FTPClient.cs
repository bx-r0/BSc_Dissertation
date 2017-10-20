using FluentFTP;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace ClientServer.FTP
{
    class FTPClient
    {
        //# Client
        private FtpClient client;

        //# Connection details 
        private string address = "http://127.0.0.1";
        private int port = 21;
        private string mainDir = "/";


        //# Constructors
        public FTPClient() { }
        public FTPClient(string address)
        {
            this.address = address;
        }

        //# Setup code
        public void Setup()
        {
            //# Creates a new FTP connection
            client = new FtpClient(address);

            //# Attempts a connection
            try
            {
                client.Connect();
            }
            catch (Exception e)
            {
                MessageBox.Show("Error in connection: " + e.Message);
            }

        }


        //# File code

        //# Upload file
        public void Upload(string currentFilePath, string FTPFilePath)
        {
            try
            {
                client.UploadFile(currentFilePath, FTPFilePath);
            }
            catch (Exception e)
            {
                MessageBox.Show(e.InnerException.Message);
            }
        }

        //# Download file
        public void Download()
        {
            throw new NotImplementedException();
        }

        //# Files
        public FtpListItem[] GetAllListing(string uri)
        {
            return client.GetListing(uri);
        }
    }
}
