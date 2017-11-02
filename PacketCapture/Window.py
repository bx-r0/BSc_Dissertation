import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Handler:

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def latency_Clicked(self, button):
        # TODO: Add latency logic here
        print("L")

    def packet_loss_Clicked(self, button):
        # TODO: Add packet loss logic here
        print("P")


class PacketCaptureGTK:
    """This is an Hello World GTK application"""

    # Loads and shows the window
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("PacketCaptureWindow.glade")
        builder.connect_signals(Handler())

        win = builder.get_object("window1")
        win.show_all()

        Gtk.main()


