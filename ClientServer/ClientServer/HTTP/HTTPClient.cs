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
        private HttpClient client = new HttpClient();

        //# Local host for initial testing
        private static string _address = $"http://127.0.0.1:{_port}/";
        private static int _port = 80;

        //# Constructors
        public HTTPClient(){ }
        public HTTPClient(string address)
        {
            _address = address;
        }
        
        //# Task for client tasks
        public async Task<HttpResponseMessage> GET()
        {
            HttpResponseMessage response = null;
            try
            {
                //# Sends the response
                response = await client.GetAsync(_address);
            }
            catch (Exception)
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
                response = await client.PostAsync(_address, content);
            }
            catch (Exception)
            {
                //TODO: Log message
            }


            return response;
        }
    }
}
