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
		# sys.stdout.write(client_socket.recv(1024))
		hasil = client_socket.recv(1024)
		# print hasil
		if hasil.split(" ")[0] == "Maksimum":
			sys.stdout.write('')
		elif hasil.split(" ")[0] == "Menunggu":
			i = 1
			client_socket.send("start")
			os.system('cls')
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
		else:
			# sys.stdout.write(hasil)
			print hasil
			sys.stdout.write('>> ')

except KeyboardInterrupt:
	client_socket.close()
	sys.exit(0)