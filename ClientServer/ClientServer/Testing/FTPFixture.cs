using NUnit.Framework;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ClientServer.Testing
{
    [TestFixture]
    class FTPFixture
    {

        //# Connection
        [Test]
        public void FTP_SucessfulConnection()
        {
            throw new NotImplementedException();
        }
        
        [Test]
        public void FTP_UnsucessfullConnection()
        {
            //NOTE: This needs to be handled and not throw an exception
            throw new NotImplementedException();
        }
        

        //# Downloading
        [Test]
        public void DownloadTextFile()
        {
            throw new NotImplementedException();
        }

        [Test]
        public void DownloadImageFile()
        {
            throw new NotImplementedException();
        }

        [Test]
        public void DownloadFolder()
        {
            throw new NotImplementedException();
        }

        [Test]
        public void Download_Invalid_FileDoesNotExist()
        {
            throw new NotImplementedException();
        }


        //# Uploading
        [Test]
        public void UploadFile()
        {
            throw new NotImplementedException();
        }

        [Test]
        public void UploadThenDownload()
        {
            throw new NotImplementedException();
        }


        //# File management
        [Test]
        public void CreateFolder()
        {
            throw new NotImplementedException();
        }

        [Test]
        public void DeleteFolder()
        {
            throw new NotImplementedException();
        }

        [Test]
        public void CreateThenDeleteFolder()
        {
            throw new NotImplementedException();
 
        }
    }
}
