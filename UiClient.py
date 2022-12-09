from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QPushButton, QLineEdit
import sys
import socket
import time
import threading


class TextEdit(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i = 0
        self.setWindowTitle("QTextEdit")
        self.resize(300, 270)

        self.textEdit = QTextEdit()
        self.textEdit.setEnabled(False)
        self.__text = QLineEdit("") #Entrée message du client


        self.btnPress1 = QPushButton("Add message")
        self.btnPress2 = QPushButton("Clear")

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.__text)
        layout.addWidget(self.btnPress1)
        layout.addWidget(self.btnPress2)
        self.setLayout(layout)

        self.btnPress1.clicked.connect(self.btnPress1_Clicked)
        self.btnPress2.clicked.connect(self.btnPress2_Clicked)


    def btnPress1_Clicked(self):
        x = self.__text.text()
        x = str(x)
        self.textEdit.append(x)
        self.__text.clear()
#        self.textEdit.setPlainText("Hello PyQt5!\nfrom pythonpyqt.com")




    def btnPress2_Clicked(self):
        self.textEdit.setPlainText("")

if __name__ == '__main__':


###########################################################################
###########################################################################

class Client():
    def __init__(self, ip, port):
        self.__ip = ip
        self.__port = port
        self.__client_socket = socket.socket()
        self.__thread = None


    def connexion(self):
        try:
            self.__client_socket.connect((self.__ip, self.__port))
        except ConnectionRefusedError:
            print("serveur non lancé ou mauvaise information")
        except ConnectionError:
            print("erreur de connection")
        else:
            print("connecté au serveur")

    def comm(self):
        message = ''
        self.__thread = threading.Thread(target=self.msgrcv, args=[self.__client_socket])
        self.__thread.start()
        while message != 'disconnect' or message != 'reset' or message != 'kill':
            message = self.msg()
        self.__thread.join()
        self.__client_socket.close()

    def msg(self):
        #print('task 1 start')
        message = input(" --> ")
        self.__client_socket.send(message.encode())
        time.sleep(1)

    def msgrcv(self, conn):
        data = ""
        while data != 'stop':
            #print('task 2 start')
            data = conn.recv(1024).decode()
            if data == 'ok, bye !' or data == 'ok, je redémarre !' or data == "j'arrête !":
                print(' le serveur: ' + data)
                data = 'stop'
            else:
                print(' le serveur: ' + data)

if __name__ == '__main__':
    
