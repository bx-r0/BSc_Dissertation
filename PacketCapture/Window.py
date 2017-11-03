import getpass
import subprocess

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class PacketCaptureGTK:

        # Loads and shows the window
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("PacketCaptureWindow.glade")
        builder.connect_signals(self)

        win = builder.get_object("window1")
        win.show_all()

        # Grabs and saves objects
        self.textBox_Latency = builder.get_object("TextBox_Latency")
        self.textBox_PacketLoss = builder.get_object("TextBox_PacketLoss")

        Gtk.main()
    # --------------------------Control Events------------------------------------- #

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def latency_Clicked(self, button):
        error_message = "Latency value entered is incorrect, it needs to be in the range of 1-1000ms"
        value = self.textBox_Latency.get_text()

        # Checks if the value is a valid int a checks for it's range
        if self.validation(value, 1, 1000):
                self.run_packet_capture("-l " + str(value))
        else:
            print(error_message)

    def packet_loss_Clicked(self, button):
        error_message = "Packet loss value entered is incorrect, it needs to be in the range of 1-100!"
        value = self.textBox_PacketLoss.get_text()

        # Checks if it is a valid int and if its within a specified range
        if self.validation(value, 1, 100):
                self.run_packet_capture("-pl " + str(value))
        else:
            print(error_message)
    # ----------------------------------------------------------------------------- #

    # # Method runs the sub process to manipulate packets
    def run_packet_capture(self, parameters):
                # Elevates user to run packet script
                print("root privileges needed:")
                self.packet = subprocess.Popen(['sudo', 'python', 'Packet.py', parameters])
                print("Password: " + getpass.getuser())

    # # Helper method used to check the validity of a value
    def validation(self, string, start, stop):
        try:
            integer = int(string)

            # Checks for the validation range
            if start < integer < stop:
                return True
            else:
                return False

        except ValueError:
            return False


