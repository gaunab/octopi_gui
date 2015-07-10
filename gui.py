#!/usr/bin/env python


from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (QAction, QActionGroup, QApplication, QFrame,
        QLabel, QMainWindow, QMenu, QMessageBox, QSizePolicy, QVBoxLayout,
        QWidget)
        
import octoprint
import json
import requests


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Load Settings from config.json
        self.settings = self.loadSettings()
        # Open Connection to api
        if 'apikey' in self.settings.keys():
            self.octopi = octoprint.Api('octopi.local',self.settings['apikey'])
        else:
            self.octopi = octoprint.Api('octopi.local')

        # Timer for refreshing
        self.timer = QTimer(self);
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.setTimeValue)
        self.timer.start()
        
        # Display Stuff
        widget = QWidget()
        self.setCentralWidget(widget)
        
        topFiller = QWidget()
        topFiller.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.infoLabel = QLabel(
                "<h1>Time Left</h1> ",
                alignment=Qt.AlignCenter)
        self.infoLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        bottomFiller = QWidget()
        bottomFiller.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(5, 5, 5, 5)
        vbox.addWidget(topFiller)
        vbox.addWidget(self.infoLabel)
        vbox.addWidget(bottomFiller)
        widget.setLayout(vbox)
        
        self.setTimeValue()

    def loadSettings(self):
        """ Load Configuration from settings.json """
        try:
            settings = json.load(open("settings.json"))
        except:
            settings = {}

        if type(settings) == list:
# If Settings is list - its assumed that several configs are stored in configfile
            for setting in settings:
                if checkHost(setting["url"]):
                    return setting              # Return the Setting, if Host is reachable

        return settings



    def setTimeValue(self):
        connected,progress = self.octopi.progress()
        print(progress)
        if connected:
            self.infoLabel.setText(u'<h1>Time Left:</h1> %s' %(timestring(progress['printTimeLeft'])))
        else:
            self.infoLabel.setText(u'<h1>Connection Error</h1>')
            
    
def checkHost(hostname):
    """ Check if host is reachable """
    try:
        r = requests.get("http://%s" %(hostname))
    except requests.exceptions.ConnectionError:
        return False
    if r.status_code == 200:
        return True
    else:
        return False


def timestring(sec_elapsed):
    """ Convert duration in Secs to human readable format. If values are large shorter units are not shown """
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60.
     
    if h > 3:
        return "{}h".format(h)
    else:
        if h > 0:
            return "{}h {:>02}m".format(h,m)
        else:
        # Less than one hour
            if m > 10:
               return"{}m".format(m)
            else:
               if m > 0:
                   return "{}m {}s".format(h,s)
               else:
                   return "{}s".format(s)
            
    return "{}:{:>02}:{:>02}".format(h, m, s)
    # End hms_string

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
