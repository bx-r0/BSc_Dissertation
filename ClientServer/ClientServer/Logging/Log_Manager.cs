using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Controls;
using System.Windows;
namespace ClientServer.Logging
{
    /// <summary>
    /// Deals with the actual logging of the data
    /// </summary>
    static class Log_Manager
    {
        //This is the single control that will be used to display the log messages
        public static ListBox ServerLogControl;
        
        //Where the log will be saved - Grabs the project directory using the parent of the bin folder. 
        //The bin folder is the Current Directory because it is where the .exe is housed
        static readonly string fileName = Directory.GetParent(Directory.GetCurrentDirectory()).Parent.FullName + @"\Logging\LOG.txt";

        //Will write the log to the output windows using Trace
        public static void Write(LogMessage message)
        {
            string logMessage;
            
            //#---- Exception message
            if (message.ExceptionThrow)
            {
                logMessage = $"{message.Time} - - {message.Exception.Message} - - {message.Message}";

                //# Message box created
                MessageBox.Show($"Exception thrown - \"{message.Exception.ToString().Substring(0, 40)}...\" \n\nPlease see the log for more details");
            }
            else
            //#----- General message
            {
                logMessage = $"{message.Time} - - {message.Message}";
            }

            //#----- Writing to a listbox
            if (ServerLogControl != null)
            {
                ServerLogControl.Dispatcher.Invoke(() => ServerLogControl.Items.Add(logMessage));
            }

            //#----- Other logging
            Trace.Write(logMessage);
            SaveLog(logMessage);
        }
        public static void Write(string message)
        {
            //Used as a stepping stone between the Write methods
            Write(new LogMessage(message));
        }
        
        //Will save the log to a text file
        private static void SaveLog(string msg)
        {
            StreamWriter sr = new StreamWriter(fileName, true);
            sr.WriteLine(msg);
            sr.Close();
        }
    }

    /// <summary>
    /// This is the format for the LogMessage
    /// 
    /// A class was chosen for the potential modularity - more LogMessage formats can be added in the future by adding a new property 
    /// and creating a constructor that deals with that property
    /// </summary>
    class LogMessage
    {
        //# General log
        public LogMessage(string GeneralMessage)
        {
            Message = GeneralMessage;
        }

        //# Exception log
        public LogMessage(Exception ExceptionObj, string GeneralMessage)
        {
            Exception = ExceptionObj;
            Message = GeneralMessage;

            ExceptionThrow = true;
        }
        
        //# Connection log
        //TODO: Add a log that deals with connection details, will need to include and IP etc

        public DateTime Time = DateTime.Now;
        public string Message { get; set; }

        public Exception Exception { get; set; }
        public bool ExceptionThrow = false;
    }
}
