using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ClientServer.FTP.FTP_Server
{
    class FTP_Responses
    { 
        //1xx
        /// <summary>
        /// 150
        /// </summary>
        public static readonly string FileStatusOK = "150: File status ok; about to open data connection";

        //2xx
        /// <summary>
        /// 200
        /// </summary>
        public static readonly string OK = "200: OK";
        /// <summary>
        /// 220
        /// </summary>
        public static readonly string ServiceReady = "220: Service ready for new user";
        /// <summary>
        /// 221
        /// </summary>
        public static readonly string ConnectionClosing = "221: Service closing control connection";
        /// <summary>
        /// 227
        /// </summary>
        /// <param name="address"></param>
        /// <param name="portArray"></param>
        /// <returns></returns>
        public static string EnteringPassiveMode(byte[] address, byte[] portArray)
        {
            return $"227: Entering Passive Mode ({address[0]},{address[1]},{address[2]},{address[3]},{portArray[0]},{portArray[1]})";
        }
        /// <summary>
        /// 226
        /// </summary>
        public static readonly string SucessfullAction = "226: Requesting action successful, closing connection";
        /// <summary>
        /// 230
        /// </summary>
        public static readonly string UserLoggedIn = "230: User logged in";
        /// <summary>
        /// 250
        /// </summary>
        public static readonly string FileActionOK = "250: Requested file action okay, completed";
        
        //3xx
        /// <summary>
        /// 331
        /// </summary>
        public static readonly string UsernameOKNeedPassword = "331: Username okay, need password";

        //4xx
        /// <summary>
        /// 450
        /// </summary>
        public static readonly string FileActionNotTaken = "450: Requested file action not taken";

        //5xx
        /// <summary>
        /// 500
        /// </summary>
        public static readonly string Error500 = "500: Error";
        /// <summary>
        /// 502
        /// </summary>
        public static readonly string CommandNotImplemented = "502: Command not implemented";
        /// <summary>
        /// 504
        /// </summary>
        public static readonly string CommandNotImplementedForParameter = "504: Command not implemented for that parameter";
        /// <summary>
        /// 530
        /// </summary>
        public static readonly string UserNotLoggedIn = "530: Not logged in";
        /// <summary>
        /// 550
        /// </summary>
        public static readonly string FileNotFound = "550: File not found";


        //Directory printing format
        public static string PrintDirectory(string name)
        {
            return string.Format("drwxr-xr-x    2 2003     2003     {0,8} {1}", "4096", name);
        }
        
        //File printing format
        public static string PrintFile(string name, long size)
        {
            return string.Format("-rw-r--r--    2 2003     2003     {0,8} {1}", size, name);
        }
    }
}
