using FluentFTP;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
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
        private string address = "http://127.0.0.1:21";
       
        //# Constructors
        public FTPClient() { }
        public FTPClient(string address)
        {
            this.address = address;
        }

        //# Setup code
        public bool Setup()
        {
            //# Creates a new FTP connection
            client = new FtpClient(address);

            //# Attempts a connection
            try
            {
                client.Credentials = new NetworkCredential("anonymous", "");
                client.Connect();
                
                return true;
            }
            catch (Exception e)
            {
                MessageBox.Show("Error in connection: " + e.Message);
            }
            return false;
        }
        
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
