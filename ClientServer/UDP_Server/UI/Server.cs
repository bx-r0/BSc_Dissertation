
using ClientServer.UDP;
using Microsoft.VisualStudio.TestTools.UITesting;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using System.Threading;

namespace UDP.Server.UI
{
    /// <summary>
    /// Summary description for CodedUITest1
    /// </summary>
    [CodedUITest]
    public class UI_UDPServer
    {
        static UDPServerWindow v = new UDPServerWindow();

        public UI_UDPServer()
        {

        }

        //Shared functionality
        public void WaitForTimeout()
        {
            //Waits for timeout lenght
            int timeout = UDPServer.timeOut;
            Thread.Sleep(timeout);
        }

        /// <summary>
        /// Method that runs before every test.
        /// Loads up a fresh window.
        /// </summary>
        [TestInitialize]
        public void StartWindow()
        {
            System.Diagnostics.Process.Start("CMD.exe", "/C ClientServer.exe -u s");
        }

        /// <summary>
        /// Method that runs after every test
        /// </summary>
        [TestCleanup]
        public void CloseWindow()
        {
            //Clicks the close button to close the window
            this.map.Close();
        }

        /// <summary>
        /// Test that clicks the start button and checks if the buttons invert.
        /// When the start button isn't active the restart button should be and visa versa.
        /// </summary>
        [TestMethod]
        public void Start_CheckInvert()
        {
            this.UIMap.Start_Click();
            this.UIMap.Start_InvertCheck();
        }

        /// <summary>
        /// Test that checks the inverting of buttons when Start->Restart. 
        /// When the start button isn't active the restart button should be and visa versa.
        /// </summary>
        [TestMethod]
        public void Restart_CheckInvert()
        {
            // Start click
            this.UIMap.Start_Click();
            this.UIMap.Start_InvertCheck();
            this.UIMap.Restart_Click();
            this.UIMap.Restart_InvertCheck();
        }

        /// <summary>
        /// Test that clicks "Start button and clicks "Restart button"
        /// </summary>
        [TestMethod]
        public void Start_Reset_Click()
        {
            this.UIMap.Start_Click();
            this.UIMap.Restart_Click();
        }

        /// <summary>
        /// Test that clicks the Randomise button
        /// </summary>
        [TestMethod]
        public void Randomise_Click()
        {
            this.UIMap.Randomise();
        }

        /// <summary>
        /// Test that checks that the randomise button resets 
        /// TODO: This check should see the colour of the pixels change
        /// </summary>
        [TestMethod]
        public void RandomiseReset()
        {
            this.UIMap.Randomise();
            this.UIMap.Restart_Click();
        }
        
        /// <summary>
        /// Test that is looking for valid stats when no UDP packets have been recieved 
        /// </summary>
        [TestMethod]
        public void Stat_CheckDefaultStats()
        {
            this.UIMap.Start_Click();
            WaitForTimeout();

            //Expected value = "100%"
            this.UIMap.Assert_CheckPacketLossValue();
        }

        /// <summary>
        /// Test that checks that the "Restart" button resets the PacketLoss value back to default
        /// </summary>
        [TestMethod]
        public void Stat_PacketLoss_Reset()
        {
            this.UIMap.Start_Click();
            WaitForTimeout();
            this.UIMap.Restart_Click(); 

            //Expected value = "-"
            this.UIMap.Assert_CheckPacketLossValueReset();

        }

        /// <summary>
        /// Test that checks that the "Restart" button resets the TotalPackets value back to deafault
        /// </summary>
        [TestMethod]
        public void Stat_TotalPacketsLost_Reset()
        {
            this.UIMap.Start_Click();
            WaitForTimeout();
            this.UIMap.Restart_Click();

            //Expected value = "-"
            this.UIMap.Assert_CheckTotalPacketsValueReset();
        }

        /// <summary>
        /// Test that checks that the "Restart" button resets the TotalPacketsLost value back to deafault
        /// </summary>
        [TestMethod]
        public void Stat_TotalPacketsSent_Reset()
        {
            this.UIMap.Start_Click();
            WaitForTimeout();
            this.UIMap.Restart_Click();

            //Expected value = "-"
            this.UIMap.Assert_CheckTotalSentValueReset();
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
