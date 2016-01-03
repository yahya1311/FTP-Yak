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
def cariPemain(cari):
    found = 0
    for i in range(0,len(pemain)):
        if pemain[i]['id'] == cari:
            found = i+1
            return found
    return found

def cariUsername(idPemain):
    for i in range(0,len(pemain)):
        if pemain[i]['id'] == idPemain:
            return pemain[i]['username']

# read soal
filename = "soal.txt"
with open(filename) as f:
    ambil = f.read()

# split soal
soal = ambil.split("==")


# masukin soal ke dalam dictionary "soal"
# soal = {}

# i = 0
# while i < len(splitsoal):
    # tempsoal = splitsoal[i].split("\n")
    # soal[i] = tempsoal[0:6]
    #soal
    # j = 0
    # while j < 5:
        # print soal[i][j]
        # j+=1
    #jawaban
    # print soal[i][5]    
    # i+=1

# count user per room
# user = 0

# jumlah pemain
# nUser = []
nUser = 0
# nUser.append(3)
# print nUser[0]
MAXUSER = 2

# list pemain
pemain = {}

# state soal
stateSoal = []
# stateSoal.append(0)

penjawab = 0

pemain[nUser] = {'id':'','username':'','nilai':'','room':''}

jumlah_room = 0
room = {}

room[jumlah_room] = {'username':''}
# os.system('cls')

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])
        
        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)        
                
            else:
                cek = cariPemain(sock.getpeername())             
                print "jumlah pemain= "+str(len(pemain))

                # pemain lama
                if cek:
                    data = sock.recv(1024)
                    data = data.split("\n")[0]
                    

                    # print "client: " + str(sock.getpeername()) + " - Mengirim pesan: " + data
                    # print "Pemanin: " + pemain[cek-1]['username'] + " mengirim pesan: " + data
                    if data == "start":
                        # sendToClient = "Pemain: " + pemain[cek-1]['username'] + " sudah siap"
                        if nUser%MAXUSER:
                            if (nUser-1)%MAXUSER==0:
                                sendToClient = "Menunggu " + str((nUser)%MAXUSER) + " pemain lain terhubung"
                            else:
                                sendToClient = "Menunggu " + str((nUser-1)%MAXUSER) + " pemain lain terhubung"
                            
                            sock.send(sendToClient)
                        else:
                            stateSoal.append(0)
                            sock.send("Semua pemain sudah terhubung. Kuis akan segera mulai, yakin?")
                    elif data == "ya":
                        sock.send("soal")
                        # j = 0
                        # sock.send(soal[stateSoal][1]+"\n")
                        # print soal[stateSoal]
                        sock.send(soal[stateSoal])
                        if penjawab == MAXUSER:
                            penjawab = 0
                        # print "Nilai Pemain Sementara:"
                        # while j < MAXUSER:
                        #     print pemain[j]['username'] + " : " + str(pemain[j]['nilai'])
                        #     j+=1
                        # while j < 5:
                        #     sock.send(soal[stateSoal][j]+"\n")
                        #     j+=1
                    elif data.split(" ")[0] == "jawaban":
                        jawaban_pemain = data.split(" ")[1].split("\n")[0]

                        # print "-" + data.split(" ")[1] + "-" + soal[stateSoal][-2:-1] + "-"
                        # print jawaban_pemain == soal[stateSoal][-2:]
                        urutan_pemain = cariPemain(sock.getpeername())
                        if jawaban_pemain == soal[stateSoal][-2:-1]:
                            print "jawaban_pemain " + str(penjawab + 1) + " benar"
                            pemain[urutan_pemain-1]['nilai'] += 1
                            # sock.send("Menunggu_Jawaban_Pemain_Lain")
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

                    elif data == "kirim_jawaban":
                        if MAXUSER - penjawab:
                            sendToClient = "Menunggu " + str(MAXUSER - penjawab) + " pemain menjawab"
                            sock.send(sendToClient)
                        else:
                            sock.send("Menunggu " + str(MAXUSER - penjawab) + " pemain menjawab"+ "\n" +"Semua pemain sudah menjawab soal. Lanjut soal selanjutnya?")
                    else:
                        print "Pesan tidak dikenali oleh server."
                        sock.send("Pesan tidak dikenali oleh server.")
                # pemanin baru
                else:

                    data = sock.recv(1024)
                    data = data.split("\n")[0]
                    room[jumlah_room] = {'username':''}
                    room[jumlah_room]['username'] = cariUsername(sock.getpeername())
                    # if nUser%MAXUSER == 0:
                        # jumlah_room += 1
                    print "jumlah room >>>>>>" + str(jumlah_room)
                    # cek max pemain
                    print "nUser%MAXUSER = " + str(nUser%MAXUSER)
                    # if (nUser-1)%MAXUSER | nUser==1:
                    pemain[nUser] = {'id':'','username':'','nilai':'','room':''}
                    pemain[nUser]['id'] = sock.getpeername()
                    pemain[nUser]['username'] = data
                    pemain[nUser]['nilai'] = 0
                    if nUser%MAXUSER==0:

                        print "Pemain baru connected: " + pemain[nUser]['username'] + " (Menunggu " + str((nUser%MAXUSER)+1) + " pemain lagi)"
                    else:
                        print "Pemain baru connected: " + pemain[nUser]['username'] + " (Menunggu " + str((nUser%MAXUSER)-1) + " pemain lagi)"    
                    
                    # print nUser
                    # user+=1
                    sendToClient = "Menunggu " + str(nUser%MAXUSER) + " pemain lain terhubung"
                    if data:
                        sock.send(sendToClient)
                    else:
                        sock.close()
                        input_socket.remove(sock)
                    if (nUser-1)%MAXUSER == 0:
                        pemain[nUser]['room'] = jumlah_room
                    else:
                        jumlah_room += 1
                        # user = 0
                        # sendToClient = "Maksimum pemain sudah tercapai (" + str(nUser) + " pemain)"
                        # print sendToClient
                        # sock.send(sendToClient)
                    nUser+=1

except KeyboardInterrupt:        
    server_socket.close()
    sys.exit(0)        