using System;
using ClientServer.UDP;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace UDP_Server.Bussiness_Logic
{
    [TestClass]
    public class UDP_BussinessLogic
    {
        UDPClient client;

        [TestInitialize]
        public void MakeObject()
        {
            client = new UDPClient("127.0.0.1", 8888);
        }

        /// <summary>
        /// Test that creates a new client object 
        /// </summary>
        [TestMethod]
        public void CreateClient()
        {
           //TestInit performs opperation
        }

        /// <summary>
        /// Test that connects the client and then disconnects
        /// </summary>
        [TestMethod]
        public void Connect_Disconnect()
        {
            client.Connect();
            client.Disconnect();
        }

        /// <summary>
        /// Test that sends a udp packet
        /// </summary>
        [TestMethod]
        public void SendPacket()
        {
            client.Connect();
            client.SendUDPPacket("test");
            client.Disconnect();
        }

        /// <summary>
        /// Test that checks if the amount of udp packets sent match the grid size correctly
        /// </summary>
        [TestMethod]
        public void SendPacketsForGrid()
        {
            client.Connect();
            client.SendGridPackets();

            //Checks if the correct number of packets were sent
            int expected = UDPClient.GRID_SIZE * UDPClient.GRID_SIZE;
            int actual = client.test_GridCount;
            Assert.AreEqual(expected, actual);

            client.Disconnect();
        }
    }
}
