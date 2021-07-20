from colorama import *
import socket
import sys
from threading import Thread
import random

clients = []

def handle():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((sys.argv[1],int(sys.argv[2])))
	s.listen(5)

	while True:
		print("\nWaiting for connections")
		connection, client_address = s.accept()
		Thread(target=client_handler, args=(connection, client_address)).start()
		clients.append(connection)

def client_handler(connection, client_address):
	try:
		print("connection from: ", client_address)
		connection.send(b'Type your username: ')
		b = connection.recv(16)
		colors = list(vars(Fore).values())
		username = "\n " + random.choice(colors) + "~ " + b.decode().rstrip() + ": " + Style.RESET_ALL
		print(username)

		while True:
			print(clients)
			data = connection.recv(1024)
			print("Data received: ", data)
			if data:
				dat = username.encode('utf-8') + data
				print("Sending: ", dat)
				print("Sending back the data")
				#connection.sendall(dat)
				for conn in clients:
					if connection is not conn:
						conn.sendall(dat)
			else:
				print("No data to send")
				break
	finally:
		connection.close()

def server_params():
	print( Fore.BLUE + "\n [*] Usage: \n\n\t" + Style.RESET_ALL + 
		Fore.YELLOW + " python3 main.py <SERVER_HOST> <SERVER_PORT>" + Style.RESET_ALL)

if len(sys.argv) == 3:
	handle()
else:
	server_params()