using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Windows.Input;
using System.Windows.Forms;
using System.Drawing;
using Microsoft.VisualStudio.TestTools.UITesting;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Microsoft.VisualStudio.TestTools.UITest.Extension;
using Keyboard = Microsoft.VisualStudio.TestTools.UITesting.Keyboard;
using Microsoft.VisualStudio.TestTools.UITest.Common.UIMap;
using ClientServer.UDP;
using System.Threading;

namespace UDP_Server.Live_Tests
{
    /// <summary>
    /// Summary description for CodedUITest1
    /// </summary>
    [CodedUITest]
    public class UDP_Live
    {
        public UDP_Live()
        {
        }

        //Shared functionality
        public void WaitForTimeout()
        {
            //Waits for timeout lenght
            int timeout = UDPServer.timeOut;
            Thread.Sleep(timeout);
        }

        [TestInitialize]
        public void StartWindows()
        {
            System.Diagnostics.Process.Start("CMD.exe", "/C ClientServer.exe -u b");
        }

        [TestCleanup]
        public void CloseWindows()
        {
            this.UIMap.Close_Windows();
        }

        /// <summary>
        /// Tests that is looking for all valid packets to be send over loopback
        /// It then checks the label to make sure all packets are recieved
        /// </summary>
        [TestMethod]
        public void SendAndRecieve_Valid()
        {
            this.UIMap.SendAndRecieve();
            this.WaitForTimeout();

            //Checks packet lost label for "0"
            this.UIMap.Assert_CheckValidSend();
            this.UIMap.Assert_ConnectInvertCheck();
        }

        /// <summary>
        /// Does not send and packets and checks if window shows 100% packet loss
        /// </summary>
        [TestMethod]
        public void SendAndRecieve_Invalid()
        {
            this.UIMap.SendAndRecieve_Invalid();
            WaitForTimeout();

            //Checks the packet loss percentage for "100%"
            this.UIMap.Assert_CheckForAllPacketsLost();
        }

        /// <summary>
        /// Test that performs a valid send, resets then runs again
        /// </summary>
        [TestMethod]
        public void SendAndRecieve_Valid_Twice()
        {
            SendAndRecieve_Valid();
            this.UIMap.RestartWindows();
            SendAndRecieve_Valid();
        }


        /// <summary>
        ///Gets or sets the test context which provides
        ///information about and functionality for the current test run.
        ///</summary>
        public TestContext TestContext
        {
            get
            {
                return testContextInstance;
            }
            set
            {
                testContextInstance = value;
            }
        }
        private TestContext testContextInstance;

        public UIMap UIMap
        {
            get
            {
                if (this.map == null)
                {
                    this.map = new UIMap();
                }

                return this.map;
            }
        }

        private UIMap map;
    }
}
