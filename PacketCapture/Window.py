# GLADE Packets
import sys
import gtk
import gtk.glade

class HelloWorldGTK:
    """This is an Hello World GTK application"""


def __init__(self):

    # Set the Glade file
    self.gladefile = "PacketCaptureWindow.glade"
    self.wTree = gtk.glade.XML(self.gladefile)

    # Get the Main Window, and connect the "destroy" event
    self.window = self.wTree.get_widget("MainWindow")
    self.window.show()
    if (self.window):
        self.window.connect("destroy", gtk.main_quit)


