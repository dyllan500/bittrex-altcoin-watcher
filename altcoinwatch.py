from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu
import sys
from urllib.request import urlopen
import json
import time
import os
import multiprocessing

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):

        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        exitAction = menu.addAction("Exit")
        self.setContextMenu(menu)
        
        menu.triggered.connect(self.exit)

    def exit(self):
        QApplication.exit()
        return quit()


def main(image):
    app = QApplication(sys.argv)
    w = QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon(image), w)
    trayIcon.show()
    sys.exit(app.exec())

def notifier():
        n = []
        p = []
        try:
            # add the path to the text file containing the alticoin symbols and sell point
	    with open('', 'r') as file:
                m = file.read()
                m = m.split('\n')
                file.close()
                num = len(m) / 2
                num2 = len(m)
                y = 0
                while y < num2:
                    if y % 2 == 0:
                        n.append(m[y].upper())
                    y = y + 1
                y = 0
                while y < num2:
                    if y % 2 != 0:
                        p.append(m[y])
                    y = y + 1
        except:
            os.system('notify-send ' + 'Error no crypt.txt file')
            os.system('spd-say "Error no text file exiting"')
            time.sleep(30)
            exit()
        while True:
            try:
                with urlopen('https://bittrex.com/api/v1.1/public/getmarketsummaries') as data:
                    rdata = json.loads(data.read().decode("utf-8"))
                x = 0
                while x < num:
                    if x == num:
                        x = x - 1
                    for i in rdata['result']:
                        if i['MarketName'] == 'BTC-{}'.format(n[x]):
                            if float('{:f}'.format(i['Last'])) >= float(p[x]):
                                notify = ('{:f}'.format(i['Last']) + " btc")
                                os.system('notify-send ' + str(notify))
                                os.system('spd-say "sell {}"'.format(n[x]))
                            x = x + 1
                            if x == num:
                                break
            except:
                os.system('notify-send ' + 'Error Connection')
                os.system('spd-say "Error No Connection"')
            time.sleep(900)



if __name__ == '__main__':
    try:
        # add path to your icon of choice here in the on '' 
    	on=''
    except:
        os.system('notify-send ' + 'no icon file')
    p = multiprocessing.Process(target=notifier)
    p.daemon = True
    p.start()
    main(on)
    quit()