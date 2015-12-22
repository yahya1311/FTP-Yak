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

soal = {}

# fungsi cari pemain
def cariPemain(alist, cari):
    found = 0
    for i in range(0,len(alist)):
        if alist[i]['id'] == cari:
            found = i+1
            return found
    return found

# read soal
filename = "soal.txt"
with open(filename) as f:
    ambil = f.read()

# split soal
splitsoal = ambil.split("==")

# masukin soal ke dalam dictionary "soal"
i = 0
while i < len(splitsoal):
    tempsoal = splitsoal[i].split("\n")
    soal[i] = tempsoal[0:6]
    #soal
    j = 0
    while j < 5:
        print soal[i][j]
        j+=1
    #jawaban
    print soal[i][5]    
    i+=1

# jumlah pemain
nUser = 0
MAXUSER = 3

# list pemain
pemain = {}

pemain[nUser] = {'id':'','username':'','state':''}
os.system('cls')

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
                    # print "Pemanin: " + pemain[cek-1]['username'] + " mengirim pesan: " + data
                    if data == "start":
                        # sendToClient = "Pemain: " + pemain[cek-1]['username'] + " sudah siap"
                        if MAXUSER - nUser:
                            sendToClient = "Menunggu " + str(MAXUSER - nUser) + " pemain lain terhubung"
                            sock.send(sendToClient)
                        else:
                            sock.send("Semua pemain sudah terhubung. Kuis akan segera mulai, yakin?")
                    elif data == "ya":
                        sock.send("Ya")
                    else:
                        print "Pesan tidak dikenali oleh server."
                        sock.send("Pesan tidak dikenali oleh server.")
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
