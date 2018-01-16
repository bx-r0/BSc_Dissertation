using ClientServer.FTP.FTP_Server;
using ClientServer.Logging;
using FluentFTP;
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
    class FTP_Connection
    {
        //# Vars
        private TcpClient _controlClient;
        private TcpClient _dataClient;

        private Stream _controlStream;
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
        public FTP_Connection(TcpClient client)
        {
            _controlClient = client;

            //Check
            if (!client.Connected)
            {
                throw new Exception("Client disconnected!");
            }

            _controlStream = client.GetStream();

            //# Creates the new stream objects
            _controlReader = new StreamReader(_controlStream);
            _controlWriter = new StreamWriter(_controlStream);
        }

        //#---------MAIN------------#//
        public void HandleClient(object obj)
        {
            //Response back to the client
            _controlWriter.WriteLine(FTP_Responses.ServiceReady);
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

                    //Grabs the command and arguments
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
                        //Logs the connection type
                        Log_Manager.Write($"Handling command: {cmd} {arguments}");

                        //Switch case for command types - This can be expanded
                        switch (cmd)
                        {
                            case "USER":
                                response = User(arguments);
                                break;
                            case "PASS":
                                response = Password(arguments);
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

                            case "RMD":
                                response = DeleteDir(arguments);
                                break;

                            case "DELE":
                                response = DeleteFile(arguments);
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

                            case "RETR":
                                response = Retr(arguments);
                                break;

                            case "LIST":
                                response = List(arguments == null ? _currentDirectory : arguments);
                                break;

                            case "QUIT":
                                response = FTP_Responses.ConnectionClosing;
                                break;

                            //Default error
                            default:
                                response = FTP_Responses.CommandNotImplemented;
                                break;
                        }
                    }

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
                Log_Manager.Write(new LogMessage(ex, "Error when handling FTP client"));
            }
        }
        //#-------------------------#//


        //## ----------------------- Commands --------------------------------- ##//
        //Changes the working directory
        private string ChangeWorkingDirectory(string pathname)
        {
            //If section of the path is specified
            if (!pathname.StartsWith("/"))
            {
                _currentDirectory = _currentDirectory + "/" + pathname;
            }
            //If the whole path is specied
            else
            {
                _currentDirectory = pathname;
            }

            return FTP_Responses.FileActionOK;
        }

        private string ResolvePath(string pathname)
        {
            return new DirectoryInfo(Path.Combine(_currentDirectory, pathname)).FullName;
        }

        //USER
        private string User(string username)
        {
            //Saves the username
            _username = username;

            //Checks for users would go here

            return FTP_Responses.UsernameOKNeedPassword;
        }

        //PASS
        private string Password(string password)
        {
            //No password needed
            return FTP_Responses.UserLoggedIn;
        }

        //DELE
        private string DeleteFile(string pathname)
        {
            //Resolves the path name
            pathname = ResolvePath(pathname);

            //TODO: Add delete functionality
            return FTP_Responses.CommandNotImplemented;
        }

        //RMD
        private string DeleteDir(string pathname)
        {
            //Resolves the path name
            pathname = ResolvePath(pathname);

            //TODO: have dir deleting functionality
            return FTP_Responses.CommandNotImplemented;
        }

        //MKD
        private string MakeDir(string pathname)
        {
            //Resolves the path name
            pathname = ResolvePath(pathname);

            //TODO: Makes a directory
            return FTP_Responses.CommandNotImplemented;
        }

        //STOR
        private string UploadFile(string pathname)
        {
            //TODO: Implemented Upload
            return FTP_Responses.CommandNotImplemented;
        }


        //TYPE - Handles Type coding -- http://www.nsftools.com/tips/RawFTP.htm#TYPE
        private string Type(string arguments)
        {
            string typeCode = "";
            string formatControl = "";

            //# Splits up the argument string
            string[] splitArgs = arguments.Split(' ');
            typeCode = splitArgs[0];
            formatControl = splitArgs.Length > 1 ? splitArgs[1] : null;

            //Sets up for error
            string response = FTP_Responses.Error500;

            switch (typeCode)
            {
                case "L":
                case "E":
                case "A":
                case "I":
                    _transferType = typeCode;
                    response = FTP_Responses.OK;
                    break;
                default:
                    response = FTP_Responses.CommandNotImplementedForParameter;
                    break;
            }

            if (formatControl != null)
            {
                switch (formatControl)
                {
                    case "N":
                        response = FTP_Responses.OK;
                        break;
                    case "T":
                        break;
                    case "C":
                        break;
                    default:
                        response = FTP_Responses.CommandNotImplementedForParameter;
                        break;

                }
            }

            return response;
        }

        //PORT - tells the server to connect to a given sockets
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

            return FTP_Responses.OK;
        }

        //PASV - tells the server to open a port to listen on it
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


            return FTP_Responses.EnteringPassiveMode(address, portArray);
        }

        //LIST - tells the server to list out a given directory
        private string List(string pathname)
        {
            //if no file path is specified we assume the current working directory
            if (pathname == null)
            {
                pathname = _root;
            }

            //Creates the path and checks if it is valid
            pathname = ResolvePath(pathname);

            //Checks the directory can be opened
            if (!CheckDirectoryStatus(pathname))
            {
                return "450: Access to direction is not allowed";
            }

            //Checks if the pathname is a valid pathname
            if (Directory.Exists(pathname))
            {
                //Active
                if (_dataConnectionType == DataConnectionType.Active)
                {
                    _dataClient = new TcpClient();
                    _dataClient.BeginConnect(_dataEndpoint.Address.ToString(), _dataEndpoint.Port, ListCommand, pathname);
                }
                //Passive   
                else
                {
                    _passiveListener.BeginAcceptTcpClient(ListCommand, pathname);
                }

                return FTP_Responses.FileStatusOK;
            }

            //Returns an error is the file path doesn't exist
            return FTP_Responses.FileActionNotTaken;
        }
        private void ListCommand(IAsyncResult result)
        {
            //Closes the connections and grabs the pathname
            string pathname = RetrieveLogic(result);

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
                    DirectoryInfo directory = new DirectoryInfo(dir);

                    //Creates a response string    
                    string line = FTP_Responses.PrintDirectory(directory.Name);


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
                    string line = FTP_Responses.PrintFile(f.Name, f.Length);

                    //Writes data
                    _dataWriter.WriteLine(line);
                    _dataWriter.Flush();
                }
            }

            //CLOSES STREAMS
            _dataClient.Close();
            _dataClient = null;

            _controlWriter.WriteLine(FTP_Responses.SucessfullAction);
            _controlWriter.Flush();
        }

        private bool CheckDirectoryStatus(string pathname)
        {
            try
            {
                IEnumerable<string> test = Directory.EnumerateDirectories(pathname);
                return true;
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
                return false;
            }
        }

        //RETR - tells the server to start downloading a file
        private string Retr(string pathname)
        {
            //Resolves the path name
            pathname = new DirectoryInfo(Path.Combine(_currentDirectory, pathname)).FullName;

            //Error checks
            if (!(Directory.Exists(_currentDirectory) && File.Exists(pathname)))
            {
                return FTP_Responses.FileNotFound;
            }
            if (!CheckFileStatus(pathname))
            {
                return "550: File cannot be opened";
            }

            //Active
            if (_dataConnectionType == DataConnectionType.Active)
            {
                _dataClient = new TcpClient();
                _dataClient.BeginConnect(_dataEndpoint.Address, _dataEndpoint.Port, RetrCommand, pathname);
            }
            //Passive
            else
            {
                _passiveListener.BeginAcceptTcpClient(RetrCommand, pathname);
            }

            return $"150: Opening {_dataConnectionType} mode data transfer for RETR";


        }
        private void RetrCommand(IAsyncResult result)
        {
            //Closes the connections and grabs the pathname
            string pathname = RetrieveLogic(result);

            using (NetworkStream dataStream = _dataClient.GetStream())
            {
                using (FileStream fs = new FileStream(pathname, FileMode.Open, FileAccess.Read))
                {
                    CopyStream(fs, dataStream);

                    _dataClient.Close();
                    _dataClient = null;
                }
            }

            _controlWriter.Write(FTP_Responses.SucessfullAction);
            _controlWriter.Flush();
        }

        /// <summary>
        /// This method checks if a file can be opended
        /// </summary>
        /// <param name="pathname"></param>
        /// <returns></returns>
        private bool CheckFileStatus(string pathname)
        {
            try
            {
                using (FileStream fs = new FileStream(pathname, FileMode.Open, FileAccess.Read))
                {
                    return true;
                }
            }
            catch
            {
                return false;
            }

        }

        /// <summary>
        /// Method uses for the List and Retr command, it will close a connection
        /// then grab the parameter
        /// </summary>
        /// <param name="result"></param>
        /// <returns></returns>
        private string RetrieveLogic(IAsyncResult result)
        {
            // Ending the connection type
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
            return (string)result.AsyncState;
        }

        //## Code from
        //https://www.codeproject.com/articles/380769/creating-an-ftp-server-in-csharp-with-ipv-support
        private static long CopyStream(Stream input, Stream output, int bufferSize)
        {
            byte[] buffer = new byte[bufferSize];
            int count = 0;
            long total = 0;

            while ((count = input.Read(buffer, 0, buffer.Length)) > 0)
            {
                output.Write(buffer, 0, count);
                total += count;
            }

            return total;
        }
        private static long CopyStreamAscii(Stream input, Stream output, int bufferSize)
        {
            char[] buffer = new char[bufferSize];
            int count = 0;
            long total = 0;

            using (StreamReader rdr = new StreamReader(input))
            {
                using (StreamWriter wtr = new StreamWriter(output, Encoding.ASCII))
                {
                    while ((count = rdr.Read(buffer, 0, buffer.Length)) > 0)
                    {
                        wtr.Write(buffer, 0, count);
                        total += count;
                    }
                }
            }

            return total;
        }
        private long CopyStream(Stream input, Stream output)
        {
            if (_transferType == "I")
            {
                return CopyStream(input, output, 4096);
            }
            else
            {
                return CopyStreamAscii(input, output, 4096);
            }
        }
    }
}
