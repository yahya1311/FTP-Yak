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
filename = "soal.txt"
with open(filename) as f:
    ambil = f.read()

# split soal
soal = ambil.split("==")

# jumlah pemain
nUser = 0
MAXUSER = 2

# list pemain
pemain = {}

# state soal
stateSoal = 0

# game state
selesai = False

penjawab = 0
penjawab_selesai = 0

pemain[nUser] = {'id':'','username':'','nilai':''}
os.system('cls')
print "Menunggu " + str(MAXUSER) + " pemain terhubung"

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
                    if data == "start":
                        if MAXUSER - nUser:
                            sendToClient = "Menunggu " + str(MAXUSER - nUser) + " pemain lain terhubung"
                            sock.send(sendToClient)
                        else:
                            sock.send("Semua pemain sudah terhubung. Kuis akan segera mulai, yakin?")
                    elif data == "ya":
                        sock.send("soal")
                        sock.send(soal[stateSoal])
                        if selesai:
                            j = 0
                            while j < MAXUSER:
                                pemain[j]['nilai'] = 0
                                j+=1
                            selesai = False
                        if penjawab == MAXUSER:
                            penjawab = 0
                        if stateSoal == 0:
                            penjawab_selesai = 0
                    elif data.split(" ")[0] == "jawaban":
                        jawaban_pemain = data.split(" ")[1].split("\n")[0]
                        urutan_pemain = cariPemain(pemain, sock.getpeername())
                        if jawaban_pemain == soal[stateSoal][-2:-1]:
                            print "jawaban_pemain " + str(penjawab + 1) + " benar"
                            pemain[urutan_pemain-1]['nilai'] += 1
                            if MAXUSER - penjawab:
                                sendToClient = "Menunggu " + str(MAXUSER - penjawab) + " pemain menjawab"
                                sock.send(sendToClient)
                            else:
                                sock.send("Semua pemain sudah menjawab soal. Lanjut soal selanjutnya?")
                        else:
                            print "jawaban_pemain " + str(penjawab + 1) + " salah"
                            pemain[urutan_pemain-1]['nilai'] += 0
                            if MAXUSER - penjawab:
                                sendToClient = "Menunggu " + str(MAXUSER - penjawab) + " pemain menjawab"
                                sock.send(sendToClient)
                            else:
                                sock.send("Semua pemain sudah menjawab soal. Lanjut soal selanjutnya?")
                        penjawab += 1
                        if penjawab == MAXUSER:
                            stateSoal += 1
                        print "Nilai Pemain Sementara:"
                        j = 0
                        while j < MAXUSER:
                            print pemain[j]['username'] + " : " + str(pemain[j]['nilai'])
                            j+=1
                        print "***********************\n"
                    elif data == "kirim_jawaban":
                        if MAXUSER - penjawab:
                            sendToClient = "Menunggu " + str(MAXUSER - penjawab) + " pemain menjawab"
                            sock.send(sendToClient)
                        else:
                            if len(soal)-1 == stateSoal:
                                sendToClient = "Nilai Pemain Akhir:"
                                j = 0
                                while j < MAXUSER:
                                    sendToClient = sendToClient + "\n" + pemain[j]['username'] + " : " + str(pemain[j]['nilai'])
                                    j+=1
                                sendToClient = sendToClient + "\n***********************\nMain lagi? (ya/tidak)"
                                sock.send("Menunggu " + str(MAXUSER - penjawab) + " pemain menjawab"+ "\n\n" +"Permainan selesai\n"+sendToClient)
                                penjawab_selesai+=1
                            else:
                                sock.send("Menunggu " + str(MAXUSER - penjawab) + " pemain menjawab"+ "\n" +"Semua pemain sudah menjawab soal. Lanjut soal selanjutnya?")
                    elif data == "selesai":
                        print penjawab_selesai
                        if penjawab_selesai == MAXUSER:
                            stateSoal = 0
                            penjawab = 0
                            print "Nilai Pemain Akhir:"
                            j = 0
                            while j < MAXUSER:
                                print pemain[j]['username'] + " : " + str(pemain[j]['nilai'])
                                j+=1
                            print "***********************\n"
                            selesai = True
                            # sock.send("Menunggu " + str(MAXUSER - penjawab) + " pemain menjawab"+ "\n\n" +"Permainan selesai\n"+sendToClient)
                    else:
                        print "Pesan tidak dikenali oleh server."
                        sock.send("Pesan tidak dikenali oleh server.")
                # pemanin baru
                else:
                    data = sock.recv(1024)
                    data = data.split("\n")[0]
                    # cek max pemain
                    if MAXUSER - nUser:
                        pemain[nUser] = {'id':'','username':'','nilai':''}
                        pemain[nUser]['id'] = sock.getpeername()
                        pemain[nUser]['username'] = data
                        pemain[nUser]['nilai'] = 0
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