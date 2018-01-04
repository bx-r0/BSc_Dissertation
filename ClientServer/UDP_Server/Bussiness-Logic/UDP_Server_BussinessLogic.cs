using System;
using System.Net;
using ClientServer.UDP;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace UDP.Server.Bussiness_Logic
{
    [TestClass]
    public class UDP_Server_BussinessLogic
    {
        UDPServer server;

        [TestInitialize]
        public void TestStartup()
        {
            server = new UDPServer();
        }

        /// <summary>
        /// Tests the creation of the server object
        /// </summary>
        [TestMethod]
        public void CreateServerObject()
        {
            //Job is performed in start up
        }

        /// <summary>
        /// Tests the server can close cleanly from a timeout
        /// </summary>
        [TestMethod]
        public void StartAndWaitForTimeout()
        {
            server.Start();
        }
    }
}
