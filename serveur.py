import socket
import time
import psutil
import subprocess

def serveur():

    print('démarrage du serveur...')                # IP et port du serveur
    host = '0.0.0.0' #socket.gethostname()
    port = 10017

    server_socket = socket.socket()

    try :
        server_socket.bind((host, port))
    except socket.gaierror:
        print("informations incorrectes")
    else:
        time.sleep(2)
        print('serveur démarré')
        print(host, port)

        server_socket.listen(2)
        conn, address = server_socket.accept()
        print("connexion depuis" + str(address))

        time.sleep(2)

        msg = ''
        while msg != 'kill':                                                    #Les commande ne sont que pour OS windows
            data = conn.recv(1024).decode()
            if data == "IP" or  data == "OS" or data == "NAME":                 #commande IP, Os et NAME
                if data == 'OS':
                    cmd = 'ver'
                elif data == 'IP':
                    cmd = 'ipconfig | findstr /i "ipv4" '
                elif data == "NAME":
                    cmd = 'hostname'
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='cp850', shell=True) #execute shell command
                #cmd = shell command
                cmd = p.stdout.read()  #put into a variable the result of the command
                conn.send(cmd.encode())  #send the result to the client
            if data == "CPU":                                                   #commande CPU
                cpu = f"Utilisation de CPU : {psutil.cpu_percent()} %"
                conn.send(cpu.encode())
            if data == "RAM":
                total = f"RAM totale : {round(((psutil.virtual_memory()[0]) / 1000000000),2)} Go"           #pour arrondir à 0.1 près
                libre = f"RAM libre : {round(((psutil.virtual_memory()[4]) / 1000000000),2)} Go"
                utilise = f"RAM utilisés : {round(((psutil.virtual_memory()[3]) / 1000000000),2)} Go"
                conn.send(total.encode())
                conn.send(libre.encode())
                time.sleep(0.2)
                conn.send(utilise.encode())
            if data == 'disconnect' or data == 'reset':
                ok = 'ok, bye !'                            #confirmation automatique du serveur
                conn.send(ok.encode())
                print("Depuis le client: " + str(data))
                print('client déconnecté')
                if data == 'reset':                          #reémarrage du serveur
                    print('redémarrage du serveur...')
                    conn.close()
                    time.sleep(0.5)
                    print('démarrage du serveur...')
                    host = '127.0.0.1'
                    port = 10017
                    server_socket = socket.socket()
                    server_socket.bind((host, port))
                    time.sleep(0.5)
                    print('serveur démarré')
                server_socket.listen(2)                     #le serveur reécoute
                conn, address = server_socket.accept()
                print("connexion depuis" + str(address))

            if data == 'kill':                              #pour kill le serveur avec confirmation automatique
                msg = 'kill'
                print("Depuis le client: " + str(data))
                ok = "j'arrête !"
                conn.send(ok.encode())

                time.sleep(0.5)

        conn.close()                    #fermeture du serveur



if __name__ == '__main__' :
    serveur()
