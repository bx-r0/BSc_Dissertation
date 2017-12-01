import fcntl
import os
import subprocess
import gi
import queue
import _thread

from LocalNetworkScan import *
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject

# Add to this list to add or remove filters for the packet manipulation
target_protcols = ['TCP', 'UDP', 'ICMP']

# Gets the directory of the current file
filepath = os.path.dirname(os.path.abspath(__file__))

class PacketCaptureGTK:
    """A GUI for controlling the Packet.py script"""

    # Loads and shows the window
    def __init__(self):
        self.running = False

        self.main_window_init()
        self.arp_window_init()
        Gtk.main()

    def main_window_init(self):
        # Creates the builder and loads the UI from the glade file
        builder = Gtk.Builder()
        builder.add_from_file("PacketCaptureWindow.glade")
        builder.connect_signals(self)

        win = builder.get_object("window1")
        win.show_all()

        # Grabs and saves objects
        self.textBox_Latency = builder.get_object("TextBox_Latency")
        self.textBox_PacketLoss = builder.get_object("TextBox_PacketLoss")
        self.textView_ConsoleOutput = builder.get_object("TextView_ConsoleOutput")
        self.TextView_ArpOutput = builder.get_object("TextView_ArpOutput")

        # Buttons
        self.button_Latency = builder.get_object("Button_latency")
        self.button_PacketLoss = builder.get_object("Button_packet_loss")

        # Labels
        self.label_ARP_active = builder.get_object("Label_ARP_active")

        # Combo Box
        self.comboBox_packetFilter = builder.get_object("ComboBox_PacketFilter")
        iface_list_store = Gtk.ListStore(GObject.TYPE_STRING)
        for item in target_protcols:  # Creates the lists
            iface_list_store.append([item])
        self.comboBox_packetFilter.set_model(iface_list_store)
        self.comboBox_packetFilter.set_active(0)

        # Others
        self.checkBox_packetFilter = builder.get_object("CheckBox_PacketFilter")
        self.button_Stop = builder.get_object("Button_stop")

    def arp_window_init(self):
        builder = Gtk.Builder()
        builder.add_from_file("ARP_Settings.glade")
        builder.connect_signals(self)

        # Grabs and saves the window for later
        self.arp_window = builder.get_object("window1")

        #Grabs objects
        self.button_OK = builder.get_object("Button_OK")
        self.button_Cancel = builder.get_object("Button_Cancel")
        self.button_localHost = builder.get_object("Button_GetLocalHosts")

        self.levelbar_localHost = builder.get_object("LevelBar_GetLocalHosts")

        # Puts the textBoxes into a list for easy traversal later
        self.ARP_TextBoxes = []
        self.ARP_TextBoxes.append(builder.get_object("TextBox_Interface"))
        self.ARP_TextBoxes.append(builder.get_object("TextBox_VictimIP"))
        self.ARP_TextBoxes.append(builder.get_object("TextBox_RouterIP"))

    # --------------------------Control Events------------------------------------- #

    def onStop_Clicked(self, button):
        """Runs when the stop button is clicked"""
        self.progressRunning(False)
        self.clean_close()

    def onDeleteWindow(self, *args):
        """Event that runs when the window is closed"""

        if self.running:
            self.clean_close()

        Gtk.main_quit(*args)

    def latency_Clicked(self, button):
        """Event that runs when the latency button is clicked"""

        error_message = \
            "Latency value entered is incorrect, it needs to be in the range of 1-1000ms"
        value = self.textBox_Latency.get_text()

        # Checks if the value is a valid int a checks for it's range
        if self.validation(value, 1, 1000):
            self.run_packet_capture("-l " + str(value))
        else:
            print(error_message)

    def packet_loss_Clicked(self, button):
        """Event that runs when the packet loss button is clicked"""

        error_message = \
            "Packet loss value entered is incorrect, it needs to be in the range of 1-100!"

        value = self.textBox_PacketLoss.get_text()

        # Checks if it is a valid int and if its within a specified range
        if self.validation(value, 1, 100):
            self.run_packet_capture("-z " + str(value))
        else:
            print(error_message)

    def ARP_Clicked(self, button):
        self.arp_window.show_all()

    def ARP_OK_Clicked(self, button):
        # All the output from the TextBoxes are store in the list, the order is:
        # [Interface, VictimIP, RouterIP]
        self.arp_valuesList = []

        # Sets the values and clears the boxes
        for textBox in self.ARP_TextBoxes:
            self.arp_valuesList.append(textBox.get_text())
            textBox.set_text("")

        # Changing ID
        self.label_ARP_active.set_text("ARP Active!")
        self.arp_window.hide()

        # Sets the stop button to on
        self.button_Stop.set_sensitive(True)

        # Starts running the ARP Spoof
        parameters = "-i {0} -t {1} -r {2} -v".format(self.arp_valuesList[0], self.arp_valuesList[1], self.arp_valuesList[2])
        self.run_arp_spoof(parameters)

    def ARP_Cancel_Clicked(self, button):
        # Clears the TextBoxes
        for textBox in self.ARP_TextBoxes:
            textBox.set_text("")

        self.arp_window.hide()

    def onPacketFilter_Checked(self, checkBox):
        self.comboBox_packetFilter.set_sensitive(checkBox.get_active())

    def getLocalHosts_Clicked(self, button):
        active = scan_for_active_hosts()
        self.levelbar_localHost.set_value(1)

    # ----------------------------------------------------------------------------- #

    def run_packet_capture(self, parameters):
        """This method is used to run the Packet.py script"""

        # Toggles the buttons
        self.progressRunning(True)

        parameter_list = [parameters]

        # If the filter packet is toggled
        if self.checkBox_packetFilter.get_active():
            index = self.comboBox_packetFilter.get_active()
            model = self.comboBox_packetFilter.get_model()

            # Grab the selected item
            item = model[index]

            # Adds the selected item
            parameter_list.append("-t " + item[0])

        # The exact location of the file needs to specified

        # Command parameters
        cmd = ['pkexec', 'python', filepath + '/Packet.py']
        cmd = cmd + parameter_list

        # Calls the sub procedure
        self.packet_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
        self.packet_outp = ""

        # Non-Block updates the TextView
        GObject.timeout_add(100, self.update_terminal, self.textView_ConsoleOutput, self.packet_proc)

    def run_arp_spoof(self, parameters):
        """Runs the spoofing when called"""

        # Runs the arp spoofing
        cmd = ['pkexec', 'python', filepath + '/ArpSpoofing.py']
        cmd = cmd + parameters.split()  # Splits the parameter string into a list

        # Calls the sub procedure
        self.arp_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
        self.arp_outp = ""

        # Non-Block updates the TextView
        GObject.timeout_add(100, self.update_terminal, self.TextView_ArpOutput, self.arp_proc)

    @staticmethod
    def validation(string, start, stop):
        """This function is used to validate the passed parameter values
            it checks if the value can be parsed as an int and a range is
            specified that is must be within"""

        try:
            # Parsing
            integer = int(string)

            # Checks for the validation range
            if start <= integer <= stop:
                return True
            else:
                return False
        except ValueError:
            return False

    def update_terminal(self, TextView, sub_proc):
        """Used to pipe terminal output to a TextView"""

        buffer = TextView.get_buffer()

        # Grabs the end and marks it for reference
        # the mark will stay at the end of the TextView
        end = buffer.get_end_iter()
        mark = buffer.create_mark('', end, False)

        # Grabs the console output
        bytes = self.non_block_read(sub_proc.stdout)

        if bytes is not None:
            # Display the output of the console
            buffer.insert(end, bytes.decode())

            # Keeps the most recent line on screen
            TextView.scroll_mark_onscreen(mark)

        return sub_proc.poll() is None

    @staticmethod
    def non_block_read(output):
        """Code for this was taken from @torfbolt answer on:
        https://stackoverflow.com/questions/17038063/show-terminal-output-in-a-gui-window-using-python-gtk
        """
        fd = output.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        try:
            return output.read()
        except:
            return ''

    def clean_close(self):
        """Function that is designed to stop the subprocess as cleanly as possible"""
        try:

            # Checks if the variables have been assigned and therefore if the process are running
            packet = False
            arp = False
            if hasattr(self, 'packet_proc'):
                if self.packet_proc is not None:
                    packet = True

            if hasattr(self, 'arp_proc'):
                if self.arp_proc is not None:
                    arp = True

            # Kill needs to be run from root because the sub process is launched from sudo
            # Runs the command together
            if packet and arp:
                os.system('pkexec kill -SIGINT ' + str(self.packet_proc.pid) + ' ' + str(self.arp_proc.pid))
                self.packet_proc.kill()
                self.arp_proc.kill()
            # Just kills the packet proc
            elif packet:
                os.system('pkexec kill -SIGINT ' + str(self.packet_proc.pid))
                self.packet_proc.kill()
            # Just kill the arp proc
            elif arp:
                os.system('pkexec kill -SIGINT ' + str(self.arp_proc.pid))
                self.arp_proc.kill()

        except Exception as e:
            print(e)

    def progressRunning(self, state):
        """Used to toggle the button being enabled, so when a progress is running
        the process buttons should be off and the cancel button enabled and visa versa"""

        # Keeps track of value
        self.running = state

        # Sets the latency and packet loss buttons sensitivity
        self.button_Latency.set_sensitive(not state)
        self.button_PacketLoss.set_sensitive(not state)

        # Inverts the stop button
        self.button_Stop.set_sensitive(True)

        # Clears the textboxes (GtkEntry) if the stop button has been clicked
        if state is False:
            self.textBox_Latency.set_text("")
            self.textBox_PacketLoss.set_text("")
