using ClientServer.HTTP;
using NUnit.Framework;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace ClientServer.Testing
{
    [TestFixture]
    class HTTPFixture_Client
    {
        //# Testing variables
        string validAddress = "http://httpbin.org";
        string invalidAddress = "http://shdajshdakjhsdahjsdhajsdh.io";

        //# GET
        public HttpResponseMessage GET(string address)
        {
            //# Creates the client with a custom URL
            HTTPClient client = new HTTPClient(address);

            //# Sets of the GET thread
            var t = Task.Run(() => client.GET());
            t.Wait();

            //# Obtains the result
            return t.Result;
        }
        [Test]
        public void SendGETRequest_ValidAddress()
        {
            //# Creates client and grabs response
            HttpResponseMessage msg = GET(validAddress + "/get");
            Assert.IsTrue(msg.IsSuccessStatusCode);
        }
        [Test]
        public void SendGETRequest_InvalidAddress()
        {
            //# Creates client and grabs response
            HttpResponseMessage msg = GET(invalidAddress);
            Assert.IsTrue(msg == null);
        }
        [Test]
        public void SendGETRequest_CheckExactResponse()
        {
            //# Starts and runs a server
            HTTPServer server = new HTTPServer();
            server.KEEP_RUNNING = false; //Makes sure it only runs once
            new Task(() => server.Start()).Start();
          
            //# Creates client and makes response
            HttpResponseMessage msg = GET("http://127.0.0.1:80/testing");
            Assert.IsTrue(msg.IsSuccessStatusCode);

            //# Reads content from response
            var t = Task.Run(() => msg.Content.ReadAsStringAsync());
            t.Wait();

            //# Checks if the response string is exactly what it should be
            string responseStr = t.Result;
            Assert.IsTrue(responseStr == "TEST_VALID");
        }


        //# UPDATE
        public HttpResponseMessage UPDATE(string address, object values)
        {
            //# Creates the client with a custom URL
            HTTPClient client = new HTTPClient(address);

            //# Sets of the GET thread
            var t = Task.Run(() => client.UPDATE(values));
            t.Wait();

            //# Obtains the result
            return t.Result;
        }
        [Test]
        public void SendUPDATERequest_ValidAddress()
        {
            //# Creates a client and returns the response
            HttpResponseMessage msg = UPDATE(validAddress + "/post", 2);
            Assert.IsTrue(msg.IsSuccessStatusCode);
        }
        [Test]
        public void SendUPDATERequest_InValidAddress()
        {
            //# Creates a client and returns the response
            HttpResponseMessage msg = UPDATE(invalidAddress, 2);
            Assert.IsTrue(msg == null);
        }

        //#TIMEOUTS
        //TODO: Timeout tests
    }

    [TestFixture]
    public class HTTPFixture_Server
    {
        //# Running
        [Test]
        public void StartServer()
        {
            HTTPServer server = new HTTPServer();
        }

        //# GET
        [Test]
        public void GET_Valid()
        {
            //# Creates a new server
            HTTPServer server = new HTTPServer();
            server.KEEP_RUNNING = false;
            new Task(() => server.Start()).Start();

            //# Creates a new client and sends a GET request
            HTTPClient client = new HTTPClient();
            new Task(() => client.GET()).Start();
        }

        //# UPDATE
        [Test]
        public void UPDATE_Valid()
        {
            //# Creates a new server
            HTTPServer server = new HTTPServer();
            server.KEEP_RUNNING = false;
            new Task(() => server.Start()).Start();

            //# Creates a new client and sends a GET request
            HTTPClient client = new HTTPClient();
            new Task(() => client.UPDATE(4)).Start();
        }

        //-Update received and check for saved value

        //# LOGGING

        //# SAVING - Data needs to be persistent
    }
}
