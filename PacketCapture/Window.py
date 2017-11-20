import fcntl
import os
import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject


class PacketCaptureGTK:
    """A GUI for controlling the Packet.py script"""

    # Loads and shows the window
    def __init__(self):
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

        # Buttons
        self.button_Latency = builder.get_object("Button_latency")
        self.button_PacketLoss = builder.get_object("Button_packet_loss")

        # Labels
        self.label_ARP_active = builder.get_object("Label_ARP_active")

        self.button_Stop = builder.get_object("Button_stop")
        self.button_Stop.set_sensitive(False)  # Stops the button from being clickable

    def arp_window_init(self):
        builder = Gtk.Builder()
        builder.add_from_file("ARP_Settings.glade")
        builder.connect_signals(self)

        # Grabs and saves the window for later
        self.arp_window = builder.get_object("window1")

        #Grabs objects
        self.button_OK = builder.get_object("Button_OK")
        self.button_Cancel = builder.get_object("Button_Cancel")

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
    
        # Bool to check later
        self.arpValuesSet = True
        self.arp_window.hide()

    def ARP_Cancel_Clicked(self, button):
        # Clears the TextBoxes
        for textBox in self.ARP_TextBoxes:
            textBox.set_text("")

        self.arp_window.hide()

    # ----------------------------------------------------------------------------- #

    def run_packet_capture(self, parameters):
        """This method is used to run the Packet.py script"""

        # Toggles the buttons
        self.progressRunning(True)

        # The exact location of the file needs to specified
        file_name = "Packet.py"
        file_path = "/home/user_1/PycharmProjects/Dissertation_Project/PacketCapture/" + file_name

        # Command parameters
        cmd = ['pkexec', 'python', file_path, parameters]

        # Calls the sub procedure
        self.sub_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
        self.sub_outp = ""

        # Non-Block updates the TextView
        GObject.timeout_add(100, self.update_terminal)

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

    def update_terminal(self):
        """Used to pipe terminal output to a TextView"""

        # Grabs the buffer and finds the end
        buffer = self.textView_ConsoleOutput.get_buffer()

        # Grabs the end and marks it for reference
        # the mark will stay at the end of the TextView
        end = buffer.get_end_iter()
        mark = buffer.create_mark('', end, False)

        # Grabs the console output
        bytes = self.non_block_read(self.sub_proc.stdout)

        if bytes is not None:
            # Display the output of the console
            buffer.insert(end, bytes.decode())

            # Keeps the most recent line on screen
            self.textView_ConsoleOutput.scroll_mark_onscreen(mark)

        return self.sub_proc.poll() is None

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
            # Kill needs to be sudo because the sub process is launched from sudo
            os.system('pkexec kill -SIGINT ' + str(self.sub_proc.pid))
        except Exception as e:
            print(e)

    def progressRunning(self, state):
        """Used to toggle the button being enabled, so when a progress is running
        the process buttons should be off and the cancel button enabled and visa versa"""

        # Sets the latency and packet loss buttons sensitivity
        self.button_Latency.set_sensitive(not state)
        self.button_PacketLoss.set_sensitive(not state)

        # Inverts the stop button
        self.button_Stop.set_sensitive(state)

        # Clears the textboxes (GtkEntry) if the stop button has been clicked
        if state is False:
            self.textBox_Latency.set_text("")
            self.textBox_PacketLoss.set_text("")
