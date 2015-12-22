import socket
import sys

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
		print hasil
		if hasil.split(" ")[0] == "Maksimum":
			sys.stdout.write('')
		else:
			sys.stdout.write('>> ')

except KeyboardInterrupt:
	client_socket.close()
	sys.exit(0)