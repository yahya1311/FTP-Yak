import socket
import sys
import time
import os

server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

sys.stdout.write('Masukkan username: ')

try:
	while True:
		message = sys.stdin.readline()    
		client_socket.send(message)
		hasil = client_socket.recv(1024)
		if hasil.split(" ")[0] == "Maksimum":
			os.system('cls')
			sys.stdout.write('')
		elif hasil.split(" ")[0] == "Menunggu":
			os.system('cls')
			i = 1
			client_socket.send("start")
			while True:
				hasil = client_socket.recv(1024)
				if hasil.split(" ")[0] == "Menunggu":
					time.sleep(1)
					client_socket.send("start")
					os.system('cls')
					print hasil.split("\n")[0] + " (" + str(i) + ")"
					i+=1
				else:
					print hasil.split("\n")[0]
					print "ya/tidak?"
					sys.stdout.write('>> ')
					break
		elif hasil.split("\n")[0] == "soal":
			os.system('cls')
			print client_socket.recv(1024)[:-3]
			message_jawaban = sys.stdin.readline()
			client_socket.send("jawaban " + message_jawaban)
			i = 1
			while True:
				hasil = client_socket.recv(1024)
				if hasil[-1:] == "?":
					print hasil.split("\n")[0]
					os.system('cls')
					print hasil.split("\n")[1]
					print "ya/tidak?"
					sys.stdout.write('>> ')
					break
				elif hasil[-1:] == ")":
					print hasil.split("\n\n")[0]
					os.system('cls')
					print hasil.split("\n\n")[1]
					client_socket.send("selesai")
					sys.stdout.write('>> ')
					break
				elif hasil.split(" ")[0] == "Menunggu":
					time.sleep(1)
					client_socket.send("kirim_jawaban")
					os.system('cls')
					print hasil.split("\n")[0] + " (" + str(i) + ")"
					i+=1
		else:
			print hasil
			sys.stdout.write('>> ')

except KeyboardInterrupt:
	client_socket.close()
	sys.exit(0)