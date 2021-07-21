from colorama import *
import socket
import sys
from threading import Thread
import random
import os
import time
import signal

# Global variables
clients = {}
usernames = []
PID = os.getpid()

def signal_handler(sig, frame):
	os.system("kill -9 {} &>/dev/null".format(PID))
	os.system("clear")

def handle():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((sys.argv[1],int(sys.argv[2])))
	s.listen(5)
	Thread(target=printer).start()

	while True:
		signal.signal(signal.SIGINT, signal_handler)
		connection, client_address = s.accept()
		Thread(target=client_handler, args=(connection, client_address)).start()

def client_handler(connection, client_address):
	try:
		connection.send(b'Type your username: ')
		b = connection.recv(16)
		colors = list(vars(Fore).values())
		username = "\n " + random.choice(colors) + "~ " + b.decode().rstrip() + ": " + Style.RESET_ALL
		usernames.append(username)
		clients[connection] = username

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
	while True:
		banner = Fore.YELLOW + "\n[*] Server running at " + sys.argv[1] + ", port " + sys.argv[2] + Style.RESET_ALL + "\n\n"
		print(banner)
		print(Fore.BLUE + "[*] Clients: \n" + Style.RESET_ALL)

		try:
			for sock in clients.keys():
				if sock.fileno() == -1:
					clients.pop(sock,None)
		except:
			pass

		for user in clients.values():
			print("\t", user.replace(':',''))

		time.sleep(2)
		os.system("clear")

def server_params():
	print( Fore.BLUE + "\n [*] Usage: \n\n\t" + Style.RESET_ALL + 
		Fore.YELLOW + " python3 main.py <SERVER_HOST> <SERVER_PORT>" + Style.RESET_ALL)

if len(sys.argv) == 3:
	handle()
else:
	server_params()
