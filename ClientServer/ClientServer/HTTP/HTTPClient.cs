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
        private const string serverAddress = "http://127.0.0.1:80/";

        //One client create and init
        private static readonly HttpClient client = new HttpClient();

        public async static Task<string> POST(object values)
        {
            return "";
        }

        public async static Task<string> GET()
        {
            //The value to return
            string value = "";
            try
            {
                //Sends the response
                HttpResponseMessage response = await client.GetAsync(serverAddress + "data/");
                
                if (response.IsSuccessStatusCode)
                {
                    value = await response.Content.ReadAsStringAsync();
                }
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

    }
}
