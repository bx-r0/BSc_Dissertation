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
        //# Local host for initial testing
        private const string serverAddress = "http://127.0.0.1:80/";

        //One client create and init
        private static readonly HttpClient client = new HttpClient();


        public async static Task<string> GET()
        {
            //The value to return
            string value = "";
            try
            {
                //# Sends the response
                HttpResponseMessage response = await client.GetAsync(serverAddress + "location/");
                
                //# If the response is positive
                if (response.IsSuccessStatusCode)
                {
                    value = await response.Content.ReadAsStringAsync();
                }
                //# If the response is negative
                else
                {
                    MessageBox.Show(response.ReasonPhrase);
                }
            }
            catch (Exception e)
            {
                MessageBox.Show(e.Message);
            }
            return value;
        }

        public async static Task<string> POST(object values)
        {
            return "";
        }
    }
}
