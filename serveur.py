
import socket
import time
import psutil
import subprocess

def serveur():

    print('démarrage du serveur...')
    host = '127.0.0.1' #socket.gethostname()
    port = 10000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    time.sleep(2)
    print('serveur démarré')
    print(host, port)

    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("connexion depuis" + str(address))

    time.sleep(2)

    msg = ''
    while msg != 'kill':
        data = conn.recv(1024).decode()
        if data == "IP" or  data == "OS" or data == "NAME":
            if data == 'OS':
                cmd = 'ver'
            elif data == 'IP':
                cmd = 'ipconfig | findstr /i "ipv4" '
            elif data == "NAME":
                cmd = 'hostname'
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='cp850', shell=True)
            cmd = p.stdout.read()
            conn.send(cmd.encode())
            # la sortie et erreur sont récuperées par les attributs stdout et stderr. faite un read()
            #print(f"résultat commande : \n {p.stdout.read()}")
        if data == "CPU":
            cpu = f"Utilisation de CPU : {psutil.cpu_percent()} %"
            conn.send(cpu.encode())
        if data == "RAM":
            total = f"RAM totale : {round(((psutil.virtual_memory()[0]) / 1000000000),2)} Go"
            libre = f"RAM libre : {round(((psutil.virtual_memory()[4]) / 1000000000),2)} Go"
            utilise = f"RAM utilisés : {round(((psutil.virtual_memory()[3]) / 1000000000),2)} Go"
            conn.send(total.encode())
            conn.send(libre.encode())
            time.sleep(0.1)
            conn.send(utilise.encode())
        if data == 'disconnect' or data == 'reset':

            ok = 'ok, bye !'
            conn.send(ok.encode())
            print("Depuis le client: " + str(data))
            print('client déconnecté')
            if data == 'reset':
                print('redémarrage du serveur...')
                conn.close()
                time.sleep(0.5)
                print('démarrage du serveur...')
                host = '127.0.0.1' #socket.gethostname()
                port = 10000
                server_socket = socket.socket()
                server_socket.bind((host, port))
                time.sleep(0.5)
                print('serveur démarré')
            server_socket.listen(2)
            conn, address = server_socket.accept()
            print("connexion depuis" + str(address))

        if data == 'kill':
            msg = 'kill'
            print("Depuis le client: " + str(data))
            ok = "j'arrête !"
            conn.send(ok.encode())

            time.sleep(0.5)

    conn.close()



if __name__ == '__main__' :
    serveur()

