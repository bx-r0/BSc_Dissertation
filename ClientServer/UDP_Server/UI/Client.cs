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
using ClientServer.UDP;

namespace UDP_Server.Client.UI
{
    /// <summary>
    /// Summary description for CodedUITest1
    /// </summary>
    [CodedUITest]
    public class Client
    {
        static UDPClientWindow v = new UDPClientWindow();

        public Client()
        {
        }

        /// <summary>
        /// Method that runs before every test.
        /// Loads up a fresh window.
        /// </summary>
        [TestInitialize]
        public void StartWindow()
        {
            System.Diagnostics.Process.Start("CMD.exe", "/C ClientServer.exe -u c");
        }

        [TestCleanup]
        public void CloseWindow()
        {
            this.UIMap.Close_ClientWindow();
        }

        /// <summary>
        /// Test that is just a click on the connect button
        /// </summary>
        [TestMethod]
        public void ConnectClick()
        {
            this.UIMap.Connect_Click();
        }

        /// <summary>
        /// Test that clicks the connect button and checks the buttons invert their "Enable"
        /// property
        /// </summary>
        [TestMethod]
        public void Connect_InvertCheck()
        {
            this.UIMap.Connect_Click();
            this.UIMap.Assert_ConnectInvertCheck();
        }

        /// <summary>
        /// Click of connect and then reset
        /// </summary>
        [TestMethod]
        public void RestartClick()
        {
            this.UIMap.Connect_Click();
            this.UIMap.Reset_Click();
        }

        /// <summary>
        /// Connect click, reset click and then a check for the buttons "Enable"
        /// property inverts properly
        /// </summary>
        [TestMethod]
        public void Restart_InvertCheck()
        {
            this.UIMap.Connect_Click();
            this.UIMap.Reset_Click();
            this.UIMap.Assert_ResetCheck();
        }

        /// <summary>
        /// Test enters values into the box and checks they end up in the class
        /// </summary>
        [TestMethod]
        public void TextEntry()
        {
            this.UIMap.Add_LocalHostToTextbox();
        }


        #region Additional test attributes

        // You can use the following additional attributes as you write your tests:

        ////Use TestInitialize to run code before running each test 
        //[TestInitialize()]
        //public void MyTestInitialize()
        //{        
        //    // To generate code for this test, select "Generate Code for Coded UI Test" from the shortcut menu and select one of the menu items.
        //}

        ////Use TestCleanup to run code after each test has run
        //[TestCleanup()]
        //public void MyTestCleanup()
        //{        
        //    // To generate code for this test, select "Generate Code for Coded UI Test" from the shortcut menu and select one of the menu items.
        //}

        #endregion

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
