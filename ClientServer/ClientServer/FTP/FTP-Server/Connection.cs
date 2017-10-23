using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace ClientServer.FTP.FTP_Server
{
    class Connection
    {

        //# Vars
        private TcpClient _controlClient;

        private NetworkStream _controlStream;
        private StreamReader _controlReader;
        private StreamWriter _controlWriter;

        private string _username;

        //# Constructor
        public Connection(TcpClient client)
        {
            _controlClient = client;

            _controlStream = client.GetStream();

            //# Creates the new stream objects
            _controlReader = new StreamReader(_controlStream);
            _controlWriter = new StreamWriter(_controlStream);
        }

        //# Handle code
        public void HandleClient(object obj)
        {
            //Response back to the client
            _controlWriter.WriteLine("220 Service Ready.");
            _controlWriter.Flush();

            string line;

            try
            {
                //Loops until there is no more to read
                while (!string.IsNullOrEmpty(line = _controlReader.ReadLine()))
                {
                    //# Setup #//
                    
                    //reset
                    string response = null;

                    string[] command = line.Split(' ');

                    string cmd = command[0].ToUpperInvariant();
                    
                    //If the command.length is greater than 1 make it equal to the command
                    //else make it equal to null
                    string arguments = command.Length > 1 ? line.Substring(command[0].Length + 1) : null;

                    //Checks if the command is just whitespace
                    if (string.IsNullOrWhiteSpace(arguments))
                    {
                        arguments = null;
                    }

                    //# Command action #//
                    
                    if (response == null)
                    {
                        //Switch case for command types - This can be expanded
                        switch (cmd)
                        {
                            case "USER":
                                response = User(arguments);
                                break;
                            case "PASS":
                                response = User(arguments);
                                break;

                            case "CWD":
                                response = ChangeWorkingDirectory(arguments);
                                break;
                            case "CDUP":
                                response = ChangeWorkingDirectory("..");
                                break;
                            case "PWD":
                                response = "257 \"/\" is current directory.";
                                break;
                         
                            case "QUIT":
                                response = "221 Service closing control connection";
                                break;

                            //Default error
                            default:
                                response = "502 Command not implemented";
                                break;
                        }
                    }

                    //# Return of message #//

                    //Used to break out of the loop
                    if (_controlClient == null || !_controlClient.Connected)
                    {
                        break;
                    }
                    else
                    {
                        //Returns the response
                        _controlWriter.WriteLine(response);
                        _controlWriter.Flush();

                        //221 is the quit command
                        if (response.StartsWith("221"))
                        {
                            break;
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                //TODO: error handling
                throw;
            }
        }
        
        //## Commands ##//

        private string ChangeWorkingDirectory(string pathname)
        {
            return "250 Changed to new directory";
        }

        //User login
        private string User(string username)
        {
            _username = username;

            if (username == "anonymous")
            {
                return "230 User logged in";
            }

            return "331 Username okay, need password";
        }
        private string Password(string password)
        { 
            //TODO: implement actual validation
            if (true)
            {
                return "230 User logged in";
            }
            else
            {
                return "530 Not logged in";
            }
        }
    }
}
