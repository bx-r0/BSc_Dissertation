using ClientServer.FTP.FTP_Server;
using System;
using System.Net;
using System.Net.Sockets;
using System.Threading.Tasks;
using ClientServer.Logging;

namespace ClientServer.FTP
{
    public class FTPServer
    {
        //# Server
        private TcpListener server;
        
        //# Constructors
        public FTPServer()
        {
            Setup();
            Start();
        }

        //# Setup
        public void Setup()
        {
            try
            {
                server = new TcpListener(IPAddress.Any, 21);
            }
            catch (Exception exception)
            {
                Log_Manager.Write(new LogMessage(exception, "## Setup() ##"));
            }
          
        }

        //# Start
        public void Start()
        {
            try
            {
                server.Start();
                server.BeginAcceptTcpClient(HandleAcceptTcpClient, server);
                Log_Manager.Write(new LogMessage("Server started"));
            }
            catch (Exception exception)
            {
                Log_Manager.Write(new LogMessage(exception, "## Start() ##"));
            }
            
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
            FTP_Connection connection = new FTP_Connection(client);

            //Sets of a new thread
            Task t = Task.Run(() => connection.HandleClient(client));
        }
    }
}