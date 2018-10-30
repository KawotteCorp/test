#-*-coding:utf-8-*

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
import socket
import select

class TextColor:
    WARNING = '\033[93m'
    NORMAL = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


server_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_connection.bind(("",5566)) # Choose the number of the port you want
server_connection.listen(5)
print "[+] Waiting for internet connection..."
connected_clients = {}
list_of_our_ip_adresses = ["127.0.0.1"]
while True:
	try:			
		asked_clients,wlist,xlist=select.select([server_connection],[],[],0.05)
	except select.error:
		pass
	else:
		for connection in asked_clients:
			client_connection,infos_client_connection=connection.accept()
			if infos_client_connection[0] not in list_of_our_ip_adresses:
				client_connection.send("@end@")
				client_connection.close()
				print "{}[-] {} TRIED TO CONNECT TO THE SERVER. CONNECTION REFUSED.{}".format(TextColor.WARNING,infos_client_connection[0],TextColor.NORMAL)
				continue
			pseudo = client_connection.recv(20)
			connected_clients[connection]=pseudo
			print "[+] {}{}{} is connected !".format(TextColor.UNDERLINE,connected_clients[connection],TextColor.NORMAL)
	clients_to_read=[]
	try:
		clients_to_read,wlist,xlist=select.select(connected_clients,[],[],0.05)
	except select.error:
		pass
	else:
		for connection in clients_to_read:
			received_msg = connection.recv(1024)
			print received_msg


