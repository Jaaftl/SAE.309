import socket
import time
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QGridLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QFileDialog
import sys
import csv


class Client(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(700, 500)
        self.__thread = None
        self.setWindowTitle("Tchat")


        self.__IP = QLabel("IP : ")                     #section IP
        self.__ip = QLineEdit("0")

        self.__PORT = QLabel("PORT : ")                 #section port
        self.__port = QLineEdit('0')

        self.btnconnect = QPushButton("Connect")        #button pour connecter

        self.lirecsv = QPushButton("open file")         #button pour ouvrir le fichier csv

        self.etat = QLabel()                            #etat de la connexion
        self.etat.setText('disconnected')
        self.panneau = QTextEdit()                      #la box pour afficher les commande effectués et les réponses du serveur
        self.panneau.setEnabled(False)
        self.__text = QLineEdit("")                     #Entrée message du client

        self.ajout_message = QPushButton("Add message") #ajouter un message
        self.ajout_message.setEnabled(False)            #False car le client est déconnecté
        self.effacer = QPushButton("Clear")             #effacer la box de tchat
        self.effacer.setEnabled(False)                  #False car le client est déconnecté

        layout = QGridLayout()                          #emplacement des widgets
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

        self.btnconnect.clicked.connect(self.connexion)     #actions effectués sur les buttons appuyés
        self.effacer.clicked.connect(self.__effacer)

        self.ajout_message.clicked.connect(self.__envoyer)
        self.lirecsv.clicked.connect(self.__lirecsv)


    def connexion(self):                                #pour se connecter
        x = str(self.etat.text())
        if x == "disconnected":
            try:
                self.__client_socket = socket.socket()
                IP = str(self.__ip.text())
                PORT = int(self.__port.text())
                self.__client_socket.connect((IP, PORT))
            except ConnectionRefusedError:              #Les erreurs si la connexion n'est pas réussi
                print("Server not launched or incorrect information")
                erreur = QMessageBox()
                erreur.setWindowTitle("Error")
                erreur.setText("Server is not launched or incorrect information")
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

            except ValueError:
                print("Type Error")
                erreur = QMessageBox()
                erreur.setWindowTitle("Error")
                erreur.setText("Incorrect type")
                erreur.resize(250, 500)
                erreur.setIcon(QMessageBox.Critical)
                erreur.exec_()

            else:                                           #initioation de la connexion et lancer le thread de récéption message
                print("connecté au serveur")
                self.etat.setText('connected')
                self.effacer.setEnabled(True)
                self.ajout_message.setEnabled(True)
                self.__thread = threading.Thread(target=self.__msg_du_serv, args=[self.__client_socket])
                self.__thread.start()
                print("thread lancé")
        elif x == "connected":
            pass

    def __envoyer(self):                                    #fonction pour envoyer
        x = self.__text.text()
        x = str(x)
        try:
            self.__client_socket.send(x.encode())
        except :
            erreur = QMessageBox()
            erreur.setWindowTitle("Error")
            erreur.setText("Server is unavailable")
            erreur.resize(250, 500)
            erreur.setIcon(QMessageBox.Critical)
            erreur.exec_()
            self.__text.clear()
            erreur = QMessageBox()
            erreur.setWindowTitle("Help")
            erreur.setText("you will be disconnected from the server")
            erreur.resize(250, 500)
            erreur.setIcon(QMessageBox.Information)
            erreur.exec_()

            self.etat.setText('disconnected')
            self.effacer.setEnabled(False)
            self.ajout_message.setEnabled(False)
        else :
            self.panneau.append(x)
            self.__text.clear()

    def __effacer(self):                                    #fonction pour effacer les message envoyés et reçus
        self.panneau.setPlainText("")




    def __msg_du_serv(self, conn):                          #fonction pour recevoir les message
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


    def __lirecsv(self):                                    #fonction pour ouvrir une dialogue pour choisir le fichier csv
        print("open dialog")
        self.open_dialog_box()

    def open_dialog_box(self):                              #fonction pour lire le fichier csv
        filename = QFileDialog.getOpenFileName()
        path = str(filename[0])

        try :
            f = open(path, 'r')   #open csv file
        except :
            print ("the choosen file is incorrect, chose again")
            print("file error")
            erreur = QMessageBox()
            erreur.setWindowTitle("Error")
            erreur.setText("the choosen file is incorrect, chose again")
            erreur.resize(250, 500)
            erreur.setIcon(QMessageBox.Critical)
            erreur.exec_()
            self.__lirecsv()
        else :
            add = csv.reader(f)  # readcthe csv
            x = 1
            for ind in add:  # trasnform it into a list
                self.__ip.setText(
                    str(ind[0]))  # the element from the list ind index 0, is placed into self.__ip wich is a server's ip input
                self.__port.setText(str(ind[1]))  # same thing for server's port
                print(x)
                x = x + 1



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Client()
    win.show()
    sys.exit(app.exec_())
