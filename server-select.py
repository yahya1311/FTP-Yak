import socket
import select
import sys
import os

server_address = ('127.0.0.1', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

# fungsi cari pemain
def cariPemain(alist, cari):
    found = 0
    for i in range(0,len(alist)):
        if alist[i]['id'] == cari:
            found = i+1
            return found
    return found

# read soal
filename = "daftarkata.txt"
with open(filename) as f:
    kata = f.readlines()

# jumlah pemain
nUser = 0
MAXUSER = 3

# list pemain
pemain = {}

pemain[nUser] = {'id':'','username':'','state':''}

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])
        
        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)        
            
            else:
                cek = cariPemain(pemain, sock.getpeername())             
                # pemain lama
                if cek:
                    data = sock.recv(1024)
                    data = data.split("\n")[0]
                    # print "client: " + str(sock.getpeername()) + " - Mengirim pesan: " + data
                    print "Client: " + pemain[cek-1]['username'] + " mengirim pesan: " + data
                    if data:
                        sock.send("Server has recieved your messages.")
                    else:
                        sock.close()
                        input_socket.remove(sock)
                # pemanin baru
                else:
                    data = sock.recv(1024)
                    data = data.split("\n")[0]
                    # cek max pemain
                    if MAXUSER - nUser:
                        pemain[nUser] = {'id':'','username':'','state':''}
                        pemain[nUser]['id'] = sock.getpeername()
                        pemain[nUser]['username'] = data
                        pemain[nUser]['state'] = 1
                        print "Pemain baru connected: " + pemain[nUser]['username'] + " (Menunggu " + str(MAXUSER - nUser-1) + " pemain lagi)"
                        nUser+=1
                        sendToClient = "Menunggu " + str(MAXUSER - nUser) + " pemain lain terhubung"
                        if data:
                            sock.send(sendToClient)
                        else:
                            sock.close()
                            input_socket.remove(sock)
                    else:
                        sendToClient = "Maksimum pemain sudah tercapai (" + str(nUser) + " pemain)"
                        print sendToClient
                        sock.send(sendToClient)

except KeyboardInterrupt:        
    server_socket.close()
    sys.exit(0)        