using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Controls;

namespace ClientServer
{
    class StatsManager
    {
        public List<Label> ActiveLabels = new List<Label>();

        /// <summary>
        /// This method deals with the dispatching and changing of labels text.
        /// It also saves the label to a list so it can be reset later, this is so the reset can be dynamic
        /// </summary>
        public void ChangeLabelText(Label label, string msg)
        {
            label.Dispatcher.Invoke(() => label.Content = msg);

            //Keeps track of active ones so they can be reset later
            ActiveLabels.Add(label);
        }

        /// <summary>
        /// Puts all the label values back to default
        /// </summary>
        public void ResetAllLabels()
        {
            foreach (Label label in ActiveLabels)
            {
                label.Content = "-";
            }
        }
    }
}
