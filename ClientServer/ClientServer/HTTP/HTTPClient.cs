using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Http;
using System.Windows;

namespace ClientServer.HTTP
{
    class HTTPClient
    {
        private static readonly HttpClient client = new HttpClient();

        public HTTPClient()
        {

        }
        public HTTPClient(string address)
        {
            serverAddress = address;
        }
        
        //# Local host for initial testing
        private string serverAddress = "http://127.0.0.1:80/";
        
        //# Task for client tasks
        public async Task<HttpResponseMessage> GET()
        {
            HttpResponseMessage response = null;
            try
            {
                //# Sends the response
                response = await client.GetAsync(serverAddress);
            }
            catch (Exception e)
            {
                //TODO:Log message
            }

            return response;
        }
        public async Task<HttpResponseMessage> UPDATE(object value)
        {
            HttpResponseMessage response = null;
            try
            {
                //# Creates a content object
                var content = new StringContent(value.ToString());

                //# Sends the response
                response = await client.PostAsync(serverAddress, content);
            }
            catch (Exception e)
            {
                //TODO: Log message
            }


            return response;
        }

       
    }

   
}
