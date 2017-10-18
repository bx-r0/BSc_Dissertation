using NUnit.Framework;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;

namespace ClientServer.Testing
{
    [TestFixture]
    class GeneralFixture
    {
        static Program p;

        [Test]
        public void StartFTPClient()
        {
            //Parameters defined
            string[] args = new string[] { "-f", "c" };

            Task task = new Task(() => Program(args));
            task.Start();

            try
            {
                task.Wait();
            }
            catch (Exception e)
            {
                throw new Exception(e.Message);
            }
        }

        private void Program(string[] args)
        {
            Program p = new Program(args);
            p.Show();
        }
    }
}
