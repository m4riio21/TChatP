from colorama import *
import socket
import sys
from threading import Thread
import random
import os

clients = []
usernames = []

def handle():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((sys.argv[1],int(sys.argv[2])))
	s.listen(5)

	while True:
		banner = Fore.YELLOW + "\n[*] Server running at " + sys.argv[1] + ", port " + sys.argv[2] + Style.RESET_ALL + "\n\n"
		Thread(target=printer).start()
		connection, client_address = s.accept()
		Thread(target=client_handler, args=(connection, client_address)).start()
		clients.append(connection)

def client_handler(connection, client_address):
	try:
		connection.send(b'Type your username: ')
		b = connection.recv(16)
		colors = list(vars(Fore).values())
		username = "\n " + random.choice(colors) + "~ " + b.decode().rstrip() + ": " + Style.RESET_ALL
		usernames.append(username)

		while True:
			data = connection.recv(1024)
			if data:
				dat = username.encode('utf-8') + data
				#connection.sendall(dat)
				for conn in clients:
					if connection is not conn:
						conn.sendall(dat)
			else:
				break
	finally:
		connection.close()

def printer():
	banner = Fore.YELLOW + "\n[*] Server running at " + sys.argv[1] + ", port " + sys.argv[2] + Style.RESET_ALL + "\n\n"
	os.system("clear")
	print(banner)
	print(Fore.BLUE + "[*] Clients: \n\n" + Style.RESET_ALL)
	for user in usernames:
		print("\t", user)


def server_params():
	print( Fore.BLUE + "\n [*] Usage: \n\n\t" + Style.RESET_ALL + 
		Fore.YELLOW + " python3 main.py <SERVER_HOST> <SERVER_PORT>" + Style.RESET_ALL)

if len(sys.argv) == 3:
	handle()
else:
	server_params()