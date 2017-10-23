using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace ClientServer.FTP.FTP_Server
{
    class Connection
    {
        //# Vars
        private TcpClient _controlClient;
        private TcpClient _dataClient;

        private NetworkStream _controlStream;
        private StreamReader _controlReader;
        private StreamWriter _controlWriter;

        private StreamWriter _dataWriter;
        private StreamReader _dataReader;

        private TcpListener _passiveListener;

        private string _username;
        private string _currentDirectory = "/";
        private readonly string _root = "/";

        //Used to define what mode the FTP server is transferring in
        private enum DataConnectionType
        {
            Passive,
            Active
        }
        private DataConnectionType _dataConnectionType = DataConnectionType.Active;

        private IPEndPoint _dataEndpoint;

        //Defines what type the file transfer will be
        private string _transferType;

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
                                response = $"257 /{_currentDirectory} is current directory.";
                                break;

                            case "TYPE":
                                response = Type(arguments);
                                break;

                            case "PORT":
                                response = Port(arguments);
                                break;
                            case "PASV":
                                response = Pasv();
                                break;

                            case "LIST":
                                response = List(arguments == null ? _currentDirectory : arguments);
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
                MessageBox.Show(ex.Message);
            }
        }

        //## ----------------------- Commands --------------------------------- ##//
        //Changes the working directory
        private string ChangeWorkingDirectory(string pathname)
        {
            _currentDirectory = pathname;

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

        //Handles Type coding -- http://www.nsftools.com/tips/RawFTP.htm#TYPE
        private string Type(string arguments)
        {
            string typeCode = "";
            string formatControl = "";

            //# Splits up the argument string
            string[] splitArgs = arguments.Split(' ');
            typeCode = splitArgs[0];
            formatControl = splitArgs.Length > 1 ? splitArgs[1] : null;

            string response = "500: ERROR";

            switch (typeCode)
            {
                case "L":
                case "E":
                case "A":
                case "I":
                    _transferType = typeCode;
                    response = "200: OK";
                    break;
                default:
                    response = "504: Command not implemented for the parameter";
                    break;
            }

            if (formatControl != null)
            {
                switch (formatControl)
                {
                    case "N":
                        response = "200: OK";
                        break;
                    case "T":
                        break;
                    case "C":
                        break;
                    default:
                        response = "504: Command not implemented for the parameter";
                        break;

                }
            }

            return response;
        }

        //Tells the server to connect to a given sockets
        private string Port(string arguments)
        {
            string[] argumentSplit = arguments.Split(',');

            //Checks if the current architecture is LittleEndian
            if (BitConverter.IsLittleEndian)
            {
                Array.Reverse(argumentSplit);
            }

            //Converts all the values in the string array to bytes
            byte[] addressValues = Array.ConvertAll(argumentSplit, delegate (string str) { return byte.Parse(str); });

            byte[] ipAddress = addressValues.Take(4).ToArray();
            byte[] port = addressValues.Skip(4).Take(2).ToArray();

            //Assigns the dataEndPoint
            _dataEndpoint = new IPEndPoint(new IPAddress(ipAddress), BitConverter.ToInt16(port, 0));

            return "200 OK";
        }

        //Tells the server to open a port to listen on it
        private string Pasv()
        {
            //Changes the connection type
            _dataConnectionType = DataConnectionType.Passive;

            //Starts the passive listener
            IPAddress local = ((IPEndPoint)_controlClient.Client.LocalEndPoint).Address;

            //0 as a port parameter specifies that the port does not matter
            _passiveListener = new TcpListener(local, 0);
            _passiveListener.Start();

            //# Returns the address and port
            IPEndPoint localEndpoint = ((IPEndPoint)_passiveListener.LocalEndpoint);

            byte[] address = localEndpoint.Address.GetAddressBytes();
            short port = (short)localEndpoint.Port;

            byte[] portArray = BitConverter.GetBytes(port);

            if (BitConverter.IsLittleEndian)
                Array.Reverse(portArray);


            return $"227 Entering Passive Mode ({address[0]},{address[1]},{address[2]},{address[3]},{portArray[0]},{portArray[1]})";
        }

        //LIST command tells the server to list out a given directory
        private string List(string pathname)
        {
            //if no file path is specified we assume the current working directory
            if (pathname == null)
            {
                pathname = _root;
            }

            //Creates the path and checks if it is valid
            pathname = new DirectoryInfo(Path.Combine(_currentDirectory, pathname)).FullName;
            
            //Checks if the pathname is a valid pathname
            if (Directory.Exists(pathname))
            {
                //Active
                if (_dataConnectionType == DataConnectionType.Active)
                {
                    _dataClient = new TcpClient();
                    _dataClient.BeginConnect(_dataEndpoint.Address.ToString(), _dataEndpoint.Port, Connection_Logic, pathname);
                }
                //Passive   
                else
                {
                    _passiveListener.BeginAcceptTcpClient(Connection_Logic, pathname);
                }

                return string.Format("150 Opening {0} mode data transfer for LIST", _dataConnectionType);
            }

            //Returns an error is the file path doesn't exist
            return "450 Requested file action not taken";
        }
        private void Connection_Logic(IAsyncResult result)
        {
            //Ending the connection type 
            //Active
            if (_dataConnectionType == DataConnectionType.Active)
            {
                _dataClient.EndConnect(result);
            }
            //Passive
            else
            {
                _dataClient = _passiveListener.EndAcceptTcpClient(result);
            }

            //Grabs the directory listing
            string pathname = (string)result.AsyncState;
            

            using (NetworkStream dataStream = _dataClient.GetStream())
            {
                //## DIRECTORIES ##//
                IEnumerable<string> directories = Directory.EnumerateDirectories(pathname);

                //Defines new streams
                _dataReader = new StreamReader(dataStream, Encoding.ASCII);
                _dataWriter = new StreamWriter(dataStream, Encoding.ASCII);

                //Writes the files
                foreach (string dir in directories)
                {
                    DirectoryInfo d = new DirectoryInfo(dir);
                    
                    //Creates a response string    
                    string line = string.Format("drwxr-xr-x    2 2003     2003     {0,8} {1}", "4096", d.Name);


                    //Writes data
                    _dataWriter.WriteLine(line);
                    _dataWriter.Flush();
                }

                //## FILES ##//
                IEnumerable<string> files = Directory.EnumerateFiles(pathname);

                foreach (string file in files)
                {
                    FileInfo f = new FileInfo(file);

                    //Creates response string   
                    string line = string.Format("-rw-r--r--    2 2003     2003     {0,8} {1}", f.Length, f.Name);

                    //Writes data
                    _dataWriter.WriteLine(line);
                    _dataWriter.Flush();
                }
            }


            //CLOSES STREAMS
            _dataClient.Close();
            _dataClient = null;

            _controlWriter.WriteLine("226 Transfer complete");
            _controlWriter.Flush();
        }
    }
}
