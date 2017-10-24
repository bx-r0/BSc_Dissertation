using ClientServer.FTP.FTP_Server;
using System;
using System.Collections.Generic;
using System.IO;
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
            Start();
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

        //# Stop
        public void Stop()
        {
            if (server != null)
            {
                server.Stop();
            }
        }

        //# Handling code
        private void HandleAcceptTcpClient(IAsyncResult result)
        {
            TcpClient client = server.EndAcceptTcpClient(result);

            //Restarts the async method
            server.BeginAcceptTcpClient(HandleAcceptTcpClient, server);

            //Creates a new connection obj
            Connection connection = new Connection(client);

            //Sets of a new thread
            Task t = Task.Run(() => connection.HandleClient(client));
        }

    }
}
