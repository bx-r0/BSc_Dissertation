using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Http;

namespace ClientServer.HTTP
{
    class HTTPClient
    {
        private const string serverAddress = "";

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

            //Sends the response
            HttpResponseMessage response = 
                await client.GetAsync(serverAddress);

            if (response.IsSuccessStatusCode)
            {
                value = await response.Content.ReadAsStringAsync();
            }
            else
            {
                //TODO: LOGGING
            }
            return value;
        }

    }
}
