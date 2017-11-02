from gi.repository import Gtk
import subprocess
import shlex
import getpass
import gi
gi.require_version('Gtk', '3.0')


class Handler:

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def latency_Clicked(self, button):
        self.run_packet_capture("-l 1")

    def packet_loss_Clicked(self, button):
        self.run_packet_capture("-pl 10")

    def run_packet_capture(self, parameters):
        # Elevates user to run packet script
        print("root privileges needed:")
        subprocess.call(shlex.split("sudo python Packet.py " + parameters))
        print("Password: " + getpass.getuser())


class PacketCaptureGTK:

    # Loads and shows the window
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("PacketCaptureWindow.glade")
        builder.connect_signals(Handler())

        win = builder.get_object("window1")
        win.show_all()

        Gtk.main()
