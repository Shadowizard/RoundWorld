

import socket
from threading import Thread
from socketserver import ThreadingMixIn


class ClientThread(Thread):

	def __init__(self,ip,port):
		Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.running = True
		print(f"[+] New server socket thread started for {ip} : {port}")


	def run(self):
		#client update loop
		while self.running:
			#get data
			data = conn.recv(2048)
			print(f"Server received data: {data}")

			#check for disconnect
			if data == b'FFFF{(0:text|bye)}':
				print("Disconnect Sequence")
			
				break
				
		
			
			
			#echo data
			conn.send(data)
			
		#disconnect stuff goes here
		threads.remove(self)
		conn.close()
			
	def abort(self):
		print("Killing thread...")
		self.running = False


TCP_IP = 'localhost'
TCP_PORT = 7777
BUFFER_SIZE = 128

#setup server
tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

while True:
	print(threads)
	tcpServer.listen(4)
	print("Multithreaded Python server : Waiting for connections from TCP clients...")
	#get accept
	(conn, (ip,port)) = tcpServer.accept()
	#if found, create client thread
	newthread = ClientThread(ip,port)
	newthread.start()
	#append thread to threads
	threads.append(newthread)
	
	print(f"Threads: {len(threads)}")
	
for t in threads:
	t.abort()
	
