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

def binarySearch(alist, item):
    first = 0
    last = len(alist)-1
    found = False
    while first<=last and not found:
        midpoint = (first + last)//2
        if alist[midpoint].split("\n")[0] == item:
            print "Posisi = " + str(midpoint+1) + "\nKata = " + alist[midpoint].split("\n")[0]
            print "Ketemu"
            found = True
        else:
            if item < alist[midpoint]:
                last = midpoint-1
            else:
                first = midpoint+1
    return found


filename = "daftarkata.txt"
with open(filename) as f:
    kata = f.readlines()

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])
        
        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)        
            
            else:               
                data = sock.recv(1024)
                data = data.split("\n")[0]
                # print sock.getpeername(), data.split("\n")[0]
                print "client: " + str(sock.getpeername()) + " - Cari kata: " + data
                cari = data
                hasil = binarySearch(kata, cari)

                if data:
                    sock.send(str(hasil))
                else:
                    sock.close()
                    input_socket.remove(sock)

except KeyboardInterrupt:        
    server_socket.close()
    sys.exit(0)        