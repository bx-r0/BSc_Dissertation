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
using ClientServer.FTP;
using System.Threading;


//TODO: Tests need to be added to simulate FTP usage
namespace FTP.Live_Tests
{
    /// <summary>
    /// Set of tests that are used to test the FTP section in a live enviorment
    /// </summary>
    [CodedUITest]
    public class FTP_Live
    {
        static FTPServerWindow v = new FTPServerWindow();

        public FTP_Live()
        {

        }

        [TestInitialize]
        public void TestStartUp()
        {
            Start_FTPServer();
            Start_FileZilla();
        }

        public void Start_FileZilla()
        {
            System.Diagnostics.Process.Start("filezilla.exe");
        }

        public void Start_FTPServer()
        {
            System.Diagnostics.Process.Start("CMD.exe", "/K ClientServer.exe -f s");

        }


        /// <summary>
        /// Tests FileZilla connecting to the FTP Server
        /// </summary>
        [TestMethod]
        public void Valid_Connect()
        {
            this.UIMap.FTP_ValidConnect();

            //Checks for the directory "/" in the listing 
            this.UIMap.FTP_CheckDirectoryHasBeenListed();

            this.UIMap.Assert_CheckForErrorConnecting();
        }

        /// <summary>
        /// Test that downloads a file a checks it completes sucessfully
        /// </summary>
        [TestMethod]
        public void DownloadFile()
        {
            throw new NotImplementedException();
        }

        /// <summary>
        /// Test that checks the server can handle starting a download and interupting it
        /// </summary>
        [TestMethod]
        public void StartDownload_ThenStop()
        {
            throw new NotImplementedException();
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
