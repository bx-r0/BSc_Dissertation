using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace ClientServer.FTP
{
    class FTPServer
    {
        //# Server
        private TcpListener server;

        //# Connection details


        //# Constructors
        public FTPServer()
        {
            Setup();
        }

        //# Setup
        public void Setup()
        {
            server = new TcpListener(IPAddress.Any, 21);
        }

        //# Start
        public void Start()
        {
            server.Start();
            server.BeginAcceptTcpClient(HandleAcceptTcpClient, server);
        }


        private void HandleAcceptTcpClient(IAsyncResult result)
        {
            TcpClient client = server.EndAcceptTcpClient(result);
            server.BeginAcceptTcpClient(HandleAcceptTcpClient, server);

            // DO SOMETHING.
        }

    }
}
