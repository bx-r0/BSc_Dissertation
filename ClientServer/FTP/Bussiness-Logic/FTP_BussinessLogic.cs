using System;
using ClientServer.FTP;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace FTP.Bussiness_Logic
{
    [TestClass]
    public class FTP_BL
    {
        FTPServer server;

        /// <summary>
        /// Startup for every test
        /// </summary>
        [TestInitialize]
        public void TestStartUp()
        {
            server = new FTPServer();
        }

        [TestMethod]
        public void Create_Object()
        {
            //creation done in startup method
        }

        /// <summary>
        /// Test that starts performs the server setup
        /// </summary>
        [TestMethod]
        public void ServerStartup()
        {
            server.Setup();
        }

        /// <summary>
        /// Tests starting the server
        /// </summary>
        [TestMethod]
        public void ServerStart()
        {
            server.Setup();
            server.Start();
        }

        /// <summary>
        /// Starts ther server and stops the server
        /// </summary>
        [TestMethod]
        public void ServerStartStop()
        {
            server.Setup();
            server.Start();
            server.Stop();
        }
    }
}
