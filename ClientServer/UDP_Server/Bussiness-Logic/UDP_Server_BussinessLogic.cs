using System;
using System.Net;
using ClientServer.UDP;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace UDP_Server.Server.Bussiness_Logic
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

        [TestMethod]
        public void CreateServerObject()
        {
            //Job is performed in start up
        }

        [TestMethod]
        public void StartAndWaitForTimeout()
        {
            server.Start();
        }
    }

}
