import socket
import select
import sys
import os
import pencari
import pickle

server_address = ('127.0.0.1', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

# test_pickle = {'id':'','isi',''}

# read soal
filename = "soal.txt"
with open(filename) as f:
    ambil = f.read()

# split soal
soal = ambil.split("==")
nUser = 0
# nUser.append(3)
# print nUser[0]
MAXUSER = 2

# list pemain
pemain = {}

# state soal
stateSoal = []
# stateSoal.append(0)

# game state
selesai = False

#penjawab = 0
penjawab = []
penjawab_selesai = 0
# penjawab_selesai = []

pemain[nUser] = {'id':'','username':'','nilai':'','room':0}

jumlah_room = 0
room = {}

room[jumlah_room] = {'username':''}

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
                # sementara1 = sock.recv(1024)
                # test_pickle = pickle.loads(sementara1)
                # print test_pickle
                cek = pencari.cariPemain(pemain, sock.getpeername())             
                # print "jumlah pemain= "+str(len(pemain))

                # pemain lama
                if cek:
                    data = sock.recv(1024)
                    data = data.split("\n")[0]
                    if data == "start":
                        # sendToClient = "Pemain: " + pemain[cek-1]['username'] + " sudah siap"
                        if nUser%MAXUSER:
                            if (nUser-1)%MAXUSER==0:
                                sendToClient = "Menunggu " + str((nUser)%MAXUSER) + " pemain lain terhubung"
                            else:
                                sendToClient = "Menunggu " + str((nUser-1)%MAXUSER) + " pemain lain terhubung"
                            sock.send(sendToClient)
                        else:
                            # print "STATE SOAL>>>>>  " + str(stateSoal)
                            # if len(stateSoal) < len(room):
                            if len(stateSoal) < len(room):
                                stateSoal.append(0)
                                penjawab.append(0)   
                            sock.send("Semua pemain sudah terhubung. Kuis akan segera mulai, yakin?")
                    elif data == "ya":
                        sock.send("soal")
                        sock.send(soal[stateSoal[pencari.cariRoom(pemain, sock.getpeername())]])
                        if selesai:
                            j = 0
                            while j < MAXUSER:
                                pemain[j]['nilai'] = 0
                                j+=1
                            selesai = False
                        if penjawab[pencari.cariRoom(pemain, sock.getpeername())] == MAXUSER:
                            penjawab[pencari.cariRoom(pemain, sock.getpeername())] = 0
                        if stateSoal == 0:
                            penjawab_selesai = 0
                    elif data.split(" ")[0] == "jawaban":
                        jawaban_pemain = data.split(" ")[1].split("\n")[0]
                        urutan_pemain = pencari.cariPemain(pemain, sock.getpeername())
                        if jawaban_pemain == soal[stateSoal[pencari.cariRoom(pemain, sock.getpeername())]][-2:-1]:
                            print "jawaban_pemain " + str(penjawab[pencari.cariRoom(pemain, sock.getpeername())] + 1) + " benar"
                            pemain[urutan_pemain-1]['nilai'] += 1
                            if MAXUSER - penjawab[pencari.cariRoom(pemain, sock.getpeername())]:
                                sendToClient = "Menunggu " + str(MAXUSER - penjawab[pencari.cariRoom(pemain, sock.getpeername())]) + " pemain menjawab"
                                sock.send(sendToClient)
                            else:
                                # print "STATE SOAL>>>>>  " + str(stateSoal)
                                sock.send("Semua pemain sudah menjawab soal. Lanjut soal selanjutnya?")

                        else:
                            print "jawaban_pemain " + str(penjawab[pencari.cariRoom(pemain, sock.getpeername())] + 1) + " salah"
                            pemain[urutan_pemain-1]['nilai'] += 0
                            if MAXUSER - penjawab[pencari.cariRoom(pemain, sock.getpeername())]:
                                sendToClient = "Menunggu " + str(MAXUSER - penjawab[pencari.cariRoom(pemain, sock.getpeername())]) + " pemain menjawab"
                                sock.send(sendToClient)
                            else:
                                # print "STATE SOAL>>>>>  " + str(stateSoal)
                                # print "PENJAWAB>>>>>  " + str(penjawab)
                                sock.send("Semua pemain sudah menjawab soal. Lanjut soal selanjutnya?")
                        penjawab[pencari.cariRoom(pemain, sock.getpeername())] += 1
                        if penjawab[pencari.cariRoom(pemain, sock.getpeername())] == MAXUSER:
                            stateSoal[pencari.cariRoom(pemain, sock.getpeername())] += 1
                        print "Nilai Pemain Sementara:"
                        j = 0
                        # while j < MAXUSER:
                        #     print pemain[j]['username'] + " : " + str(pemain[j]['nilai'])
                        #     j+=1
                        while j<len(pemain):
                            if pemain[j]['room'] == pencari.cariRoom(pemain, sock.getpeername()):
                                print pemain[j]['username'] + " : " + str(pemain[j]['nilai'])
                                # if j==MAXUSER
                            j+=1
                        print "***********************\n"
                    elif data == "kirim_jawaban":
                        if MAXUSER - penjawab[pencari.cariRoom(pemain, sock.getpeername())]:
                            sendToClient = "Menunggu " + str(MAXUSER - penjawab[pencari.cariRoom(pemain, sock.getpeername())]) + " pemain menjawab"
                            # print pencari.cariUsername(pemain, sock.getpeername()) + "room yang digunakan= " + str(pencari.cariRoom(pemain, sock.getpeername()))
                            sock.send(sendToClient)
                        else:
                            # print "UDAH SAMPAI DI AKHIR SOAL "
                            if len(soal)-1 == stateSoal[pencari.cariRoom(pemain, sock.getpeername())]:
                                sendToClient = "Nilai Pemain Akhir:"
                                j = 0
                                while j<len(pemain):
                                    if pemain[j]['room'] == pencari.cariRoom(pemain, sock.getpeername()):
                                        print pemain[j]['username'] + " : " + str(pemain[j]['nilai'])
                                        sendToClient = sendToClient + "\n" + pemain[j]['username'] + " : " + str(pemain[j]['nilai'])
                                        # if j==MAXUSER
                                    j+=1
                                # while j < MAXUSER:
                                #     sendToClient = sendToClient + "\n" + pemain[j]['username'] + " : " + str(pemain[j]['nilai'])
                                #     j+=1
                                sendToClient = sendToClient + "\n***********************\nMain lagi? (ya/tidak)"
                                sock.send("Menunggu " + str(MAXUSER - penjawab[pencari.cariRoom(pemain, sock.getpeername())]) + " pemain menjawab"+ "\n\n" +"Permainan selesai\n"+sendToClient)
                                penjawab_selesai+=1
                            else:
                                sock.send("Menunggu " + str(MAXUSER - penjawab[pencari.cariRoom(pemain, sock.getpeername())]) + " pemain menjawab"+ "\n" +"Semua pemain sudah menjawab soal. Lanjut soal selanjutnya?")
                    elif data == "selesai":
                        # print penjawab_selesai
                        if penjawab_selesai%MAXUSER == 0:
                            stateSoal[pencari.cariRoom(pemain, sock.getpeername())] = 0
                            penjawab[pencari.cariRoom(pemain, sock.getpeername())] = 0
                            print "\n************************\n"
                            print "Nilai Pemain Akhir:"
                            j = 0
                            # while j < MAXUSER:
                            #     print pemain[j]['username'] + " : " + str(pemain[j]['nilai'])
                            #     j+=1
                            while j<len(pemain):
                                if pemain[j]['room'] == pencari.cariRoom(pemain, sock.getpeername()):
                                    print pemain[j]['username'] + " : " + str(pemain[j]['nilai'])
                                    # sendToClient = sendToClient + "\n" + pemain[j]['username'] + " : " + str(pemain[j]['nilai'])
                                    # if j==MAXUSER
                                j+=1
                            # while j<len(pemain):
                            #         if pemain[j]['room'] == pencari.cariRoom(pemain, sock.getpeername()):
                            #             print pemain[j]['username'] + " : " + str(pemain[j]['nilai'])
                            #             # sendToClient = sendToClient + "\n" + pemain[j]['username'] + " : " + str(pemain[j]['nilai'])
                            #             # if j==MAXUSER
                            #         j+=1
                            print "\n************************\n"
                            # stateSoal = []
                            # print "STATE SOAL>>>>>  " + str(stateSoal)
                            selesai = True
                            # sock.send("Menunggu " + str(MAXUSER - penjawab) + " pemain menjawab"+ "\n\n" +"Permainan selesai\n"+sendToClient)
                    else:
                        print "Pesan tidak dikenali oleh server."
                        sock.send("Pesan tidak dikenali oleh server.")
                # pemanin baru
                else:

                    # data = sock.recv(1024)
                    # data = data.split("\n")[0]
                    data = sock.recv(1024)
                    data = pickle.loads(data)
                    room[jumlah_room] = {'username':''}
                    room[jumlah_room]['username'] = pencari.cariUsername(pemain, sock.getpeername())
                    # if nUser%MAXUSER == 0:
                        # jumlah_room += 1
                    # print "jumlah room >>>>>>" + str(jumlah_room)
                    # cek max pemain
                    # print "nUser%MAXUSER = " + str(nUser%MAXUSER)
                    # if (nUser-1)%MAXUSER | nUser==1:
                    pemain[nUser] = {'id':'','username':'','nilai':'','room':0}
                    pemain[nUser]['id'] = sock.getpeername()
                    pemain[nUser]['username'] = data['username']
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
                    # print "nUser >>>>  " + str(nUser)
                    if (nUser+1)%MAXUSER == 1:
                        jumlah_room += 1
                        # print "JUMLAH ROOM >>>>  " + str(jumlah_room)
                        pemain[nUser]['room'] = jumlah_room
                        # print "room" + str(pemain[nUser]['room'])
                    else:
                        # print "JUMLAH ROOM >>>>  " + str(jumlah_room)
                        pemain[nUser]['room'] = jumlah_room
                        # user = 0
                        # sendToClient = "Maksimum pemain sudah tercapai (" + str(nUser) + " pemain)"
                        # print sendToClient
                        # sock.send(sendToClient)
                        # print "room" + str(pemain[nUser]['room'])
                    nUser+=1

except KeyboardInterrupt:        
    server_socket.close()
    sys.exit(0)        