
import structure
import socket
import threading
import sys

server_data = []
clients = []
threads = []

running = True

#--Gotta add message length to command header
#--use global locked queue to send things between threads (included in python)
#--see: async io 

#Client thread class
#--Python's threads don't run concurrently.
class clientThread(threading.Thread):

	def __init__(self,conn,address):
		
		threading.Thread.__init__(self)
		
		self.connection = conn
		self.address = address
		#--Don't do this, shared mutable data like this can become easily corrupted
		clients.append(self)
		threads.append(self)
		
	def run(self):
		
		global running
		
		print(f"Created client for {self.address}")
		
		while(running):
			message = "1{(0:text|Bob Boblaw)}\n".encode("UTF-8")
			self.connection.send(message)
			
			#--Arg is bytes recieved, doesn't always work bc of data rerouteing and other stuff.
			data = self.connection.recv(1024)
			#print("Server recieved: %s" % data)
			server_data.append((self,data))
				
		print("Closed a client")
		
#Connecting thread class
class connectingThread(threading.Thread):

	def __init__(self,threadID):
		
		print("Initializing")
		
		threading.Thread.__init__(self)
		self.threadID = threadID
		
		self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		
		hostname = socket.gethostname() #Some black magic fuckery to get the local IP
		#
		HOST = "127.0.0.1"   #socket.gethostbyname(hostname)
		PORT = 1337

		self.server.bind((HOST,PORT))
		self.server.settimeout(20)
		
		threads.append(self)
		
	def run(self):
		
		global running
		
		print("Running")
		
		#--parameter is backlog of connections in queue. This may have to be modified later
		self.server.listen(1)
		
		while(running):
			
			try:
				#--Lots of things can go wrong here: read/write timeouts, heartbeats, external idle kills etc...
				conn,address = self.server.accept()
				
				for client in clients:
					
					if client.connection != conn:
						
						print("Connected to " + address[0])
						message_to_send = "Hello Beautiful!\n".encode("UTF-8")
						conn.send(message_to_send)
				
				#Create a new client, automatically adding it to the clients list
				new_client = clientThread(conn,address)
				new_client.daemon = True
				new_client.start()
				
				#Clears the connection and the address for the next loop
				conn = 0
				address = 0
			
			except Exception as e:
				print(e)
				
		conn.close()
		print("Closed listener")
		
class safetyThread(threading.Thread):
		
		def __init__(self):
			
			threading.Thread.__init__(self)
			
			threads.append(self)
		
		def run(self):
			
			global running
			
			while(running):
				
				user_input = input()
			
				if(user_input == "q"):
					running = False
			
		
#Multithreading. One thread is now always listening for new connections and client data

thread = connectingThread(1)
thread.daemon = True
thread.start()

safety = safetyThread()
safety.daemon = True
safety.start()

while(running):

	for index, data in enumerate(server_data):
		
		sending_client = data[0]
		data_sent = data[1]
		print(f"{sending_client.address}:{data_sent}")
		
		if data_sent == "FFFF{(0:text|bye)}":
			
			message == "thanks"
			sending_client.connection.send(message)
			
			sending_client.connection.close()
			clients.pop(clients.get_index(sending_client))
		
		for client in clients:
			
			if client != sending_client:
				
				message = f"{sending_client.address[0]}:{data_sent}\n".encode("UTF-8")
				client.send(message)
			
		server_data.pop(index)

print("Shutting down")	
	
sys.exit()
		

		
		
		
		
	


	
	
	
	
	
