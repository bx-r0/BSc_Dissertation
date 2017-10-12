using NUnit.Framework;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ClientServer.Testing
{
    [TestFixture]
    class HTTPFixture_Client
    {
        //# Connection
        [Test]
        public void HTTP_SucessfulConnection()
        {
            throw new NotImplementedException();
        }

        [Test]
        public void HTTP_UnsucessfulConnection()
        {
            throw new NotImplementedException();
        }

        //# GET
        [Test]
        public void SendGETRequest()
        {
            throw new NotImplementedException();
        }
        
        //# UPDATE
        [Test]
        public void SendUPDATERequest()
        {
            throw new NotImplementedException();
        }
    }

    [TestFixture]
    public class HTTPFixture_Server
    {
        //# Running
        [Test]
        public void StartServer()
        {
            //Could this use a test client to check if it's working?
            throw new NotImplementedException();
        }

        [Test]
        public void StopServer()
        {
            throw new NotImplementedException();
        }

        //# Dealing with requests
        //# GET
        [Test]
        public void GET_Valid()
        {
            throw new NotImplementedException();
        }

        //# UPDATE
        [Test]
        public void UPDATE_Valid()
        {
            throw new NotImplementedException();
        }

        //# Logging
        [Test]
        public void AddToLog_ValidAction()
        {
            throw new NotImplementedException();
        }
        public void AddToLog_Exception()
        {
            throw new NotImplementedException();
        }

        //# Saving
        public void SaveLog()
        {
            throw new NotImplementedException();
        }

        public void SaveDatabase()
        {
            throw new NotImplementedException();
        }

        //# Loading
        public void LoadLog()
        {
            throw new NotImplementedException();
        }
        public void LoadDatabase()
        {
            throw new NotImplementedException();
        }
    }
}
