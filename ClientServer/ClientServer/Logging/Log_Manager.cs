using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

//TODO: Commenting for each class
namespace ClientServer.Logging
{
    static class Log_Manager
    {
        //Where the log will be saved - Grabs the project directory using the parent of the bin folder. 
        //The bin folder is the Current Directory because it is where the .exe is housed
        static readonly string fileName = Directory.GetParent(Directory.GetCurrentDirectory()).Parent.FullName + @"\Logging\LOG.txt";

        //Will write the log to the output windows using Trace
        public static void Write(LogMessage message)
        {
            string logMessage;
            
            //# Exception message
            if (message.ExceptionThrow)
            {
                logMessage = $"{message.Time} - - {message.Exception.Message} - - {message.Message}";
            }
            else
            //# General message
            {
                logMessage = $"{message.Time} - - {message.Message}";
            }

            //If there is an exception
            if (message.ExceptionThrow)
            {
                //# Message box created
                MessageBox.Show($"Exception thrown - \"{message.Exception.ToString().Substring(0, 40)}...\" \n\nPlease see the log for more details");
            }
            
            Trace.Write(logMessage);
            SaveLog(logMessage);
        }

        //Will save the log to a text file
        private static void SaveLog(string msg)
        {
            StreamWriter sr = new StreamWriter(fileName, true);
            sr.WriteLine(msg);
            sr.Close();
        }
    }
    
    class LogMessage
    {
        public LogMessage(Exception ExceptionObj, string GeneralMessage)
        {
            Exception = ExceptionObj;
            Message = GeneralMessage;

            ExceptionThrow = true;
        }
        public LogMessage(string GeneralMessage)
        {
            Message = GeneralMessage;
        }

        public DateTime Time = DateTime.Now;
        public Exception Exception { get; set; }
        public string Message { get; set; }

        public bool ExceptionThrow = false;
    }
}
