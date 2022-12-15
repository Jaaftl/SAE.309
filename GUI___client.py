import socket
import time
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QGridLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QFileDialog
import sys
import csv, ipaddress


class Client(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(700, 500)
        self.__thread = None
        self.setWindowTitle("Tchat")


        self.__IP = QLabel("IP : ")
        self.__ip = QLineEdit("127.0.0.1")

        self.__PORT = QLabel("PORT : ")
        self.__port = QLineEdit('10017')

        self.btnconnect = QPushButton("Connect")

        self.lirecsv = QPushButton("open file")

        self.etat = QLabel()
        self.etat.setText('disconnected')
        self.panneau = QTextEdit()
        self.panneau.setEnabled(False)
        self.__text = QLineEdit("")  # Entrée message du client

        self.ajout_message = QPushButton("Add message")
        self.ajout_message.setEnabled(False)
        self.effacer = QPushButton("Clear")
        self.effacer.setEnabled(False)

        layout = QGridLayout()
        layout.addWidget(self.__IP, 0, 0)
        layout.addWidget(self.__ip, 0, 1)
        layout.addWidget(self.lirecsv, 0, 3)
        layout.addWidget(self.__PORT, 1, 0)
        layout.addWidget(self.__port, 1, 1)
        layout.addWidget(self.btnconnect, 2, 1)

        layout.addWidget(self.etat, 3, 0)
        layout.addWidget(self.panneau, 3, 1)
        layout.addWidget(self.__text, 4, 1)
        layout.addWidget(self.ajout_message, 4, 3)
        layout.addWidget(self.effacer, 6, 1)
        self.setLayout(layout)

        self.btnconnect.clicked.connect(self.connexion)
        self.effacer.clicked.connect(self.__effacer)

        self.ajout_message.clicked.connect(self.__envoyer)
        self.lirecsv.clicked.connect(self.__lirecsv)


    def connexion(self):
        x = str(self.etat.text())
        if x == "disconnected":
            try:
                self.__client_socket = socket.socket()
                IP = str(self.__ip.text())
                PORT = int(self.__port.text())
                self.__client_socket.connect((IP, PORT))
            except ConnectionRefusedError:
                print("Server not launched or incorrect information")
                erreur = QMessageBox()
                erreur.setWindowTitle("Error")
                erreur.setText("Server not launched or incorrect information")
                erreur.resize(250, 500)
                erreur.setIcon(QMessageBox.Critical)

                erreur.exec_()
            except ConnectionError:
                print("Connection Error")
                erreur = QMessageBox()
                erreur.setWindowTitle("Error")
                erreur.setText("Connection Error")
                erreur.resize(250, 500)
                erreur.setIcon(QMessageBox.Critical)
                erreur.exec_()

            except OSError:
                print("OS Error")
                erreur = QMessageBox()
                erreur.setWindowTitle("Error")
                erreur.setText("Incorrect IP or port")
                erreur.resize(250, 500)
                erreur.setIcon(QMessageBox.Critical)
                erreur.exec_()

            except TypeError:
                print("Type Error")
                erreur = QMessageBox()
                erreur.setWindowTitle("Error")
                erreur.setText("Incorrect type")
                erreur.resize(250, 500)
                erreur.setIcon(QMessageBox.Critical)
                erreur.exec_()

            else:
                print("connecté au serveur")
                self.etat.setText('connected')
                self.effacer.setEnabled(True)
                self.ajout_message.setEnabled(True)
                self.__thread = threading.Thread(target=self.__msg_du_serv, args=[self.__client_socket])
                self.__thread.start()
                print("thread lancé")
        elif x == "connected":
            pass

    def __envoyer(self):
        x = self.__text.text()
        x = str(x)
        self.__client_socket.send(x.encode())
        self.panneau.append(x)
        self.__text.clear()
        #if x == 'disconnect' or x == 'reset' or x == 'kill':
            #pass

    def __effacer(self):
        self.panneau.setPlainText("")




    def __msg_du_serv(self, conn):
        print('task start')
        data = ""
        while data != 'stop':
            data = conn.recv(1024).decode()
            if data == 'ok, bye !' or data == 'ok, je redémarre !' or data == "j'arrête !":
                self.panneau.append(data)
                time.sleep(0.1)
                data = 'stop'
            else:
                self.panneau.append(data)
                time.sleep(0.1)
        self.__client_socket.close()
        self.etat.setText('disconnected')
        self.effacer.setEnabled(False)
        self.ajout_message.setEnabled(False)
        print("task fini")


    def __lirecsv(self):
        print("open dialog")
        self.open_dialog_box()

    def open_dialog_box(self):
        filename = QFileDialog.getOpenFileName()
        path = str(filename[0])

        '''with open(path) as file:
            reader = csv.reader(file)
            next(reader)
            data = []
            for row in reader:
                row[0] = IP.IPv4Address(row[0])
                data.append(row)

            data.sort()'''

        with open(path) as file:
            reader = csv.reader(file)
            next(reader)
            data = []
            for row in reader:
                row[0] = ipaddress.IPv4Address(row[0])
                data.append(row)

            data.sort()

        print(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Client()
    win.show()
    sys.exit(app.exec_())
