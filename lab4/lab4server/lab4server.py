import socket
import sys
import os
import re
import threading
import Queue
import time

# create ClientHandler class
class ClientHandler(threading.Thread):

	# write constructor that extends threading
	def __init__ (self, conn):
		threading.Thread.__init__(self)
		self.conn = conn
	def run(self):
		#return ready state to client
		self.conn.send("READY")
	
		# collect command
		data = self.conn.recv(BUFFER_SIZE)
		if verbose == True: 
			print 'server receiving request:', data

		# split the command into filename
		tmp = data.split(' ')
		command = tmp[0] 
		filename = tmp[1]
	
		# check for bad filename
		filename = clean(filename)	
		if filename == "BAD":
			self.send("ERROR: the filename is illegal")
			return
		elif command == "GET":
			try:
				#return file size
				filesize = str(os.path.getsize(filename))
			except:
				self.conn.send("ERROR: {} does not exist".format(filename))
				return
			#return the client the file size in bytes
			self.conn.send(filesize)
		
			# check if the client is OK
			data = self.conn.recv(BUFFER_SIZE)	
			packets = int(filesize)/BUFFER_SIZE

			if verbose == True: print "server sending {} bytes".format(filesize)
		
			# send data
			file = open(filename, 'rb', BUFFER_SIZE)
			i=0
			while i< packets:
				self.conn.send(file.read(BUFFER_SIZE))
				i+=1

			self.conn.send("DONE")

		elif command == "PUT":
			# let client know OK to proceed
			self.conn.send("OK")
			#return when the client declares they are sending a file but aren't
			try:		
				# get file size
				filesize = int(self.conn.recv(BUFFER_SIZE))
			except:
				return

			#tell client filesize is OK
			self.conn.send("OK")
				
			if verbose == True: 
				print 'server receiving {} bytes'.format(filesize)

			with open(filename, "wb") as f:
				while filesize >= 0:
					data = self.conn.recv(min(filesize, BUFFER_SIZE))
					f.write(data)
					filesize -= BUFFER_SIZE
				f.close()

			self.conn.send("DONE")
			print "done"
			
		elif command == "DEL":
			if verbose == True: 
				print 'server deleting file', filename
			try:
				# try to delete specified file
				os.remove(clean(filename))
			except:
				self.conn.send("ERROR: {} does not exist".format(filename))
				return
			
			self.conn.send("DONE")
		else:
			if verbose == True: print "ERROR: bad command recieved"

# Manager
class Manager(threading.Thread):
	# write constructor
	def __init__ (self):
		threading.Thread.__init__(self)
		#make a new queue that holds all the queued threads
		self.q = Queue.Queue()
		# make a new thread
		self.running = set()
		
	def run(self):
		while True:
			kick = []	

			#iterate through running
			for t in self.running:
				if not t.isAlive(): 
					kick.append(t)
				
			for t in kick:
				#remove all elements in the list from set
				self.running.remove(t)
			
			#if q is empty wait a second and restart loop
			if self.q.empty():
				time.sleep(1)
				continue
				
			#if q has an item
			if len(self.running) == MAX_SIZE:
				time.sleep(1)
				continue
					
			#if there is space, remove next client thread from the queue
			t= self.q.get()
			t.start()
			self.running.add(t)

	def add(self, t):
		#add the thread to running set
		self.q.put(t) 
		print "Added thread to queue"

# clean the filename string
def clean(badinput):
	pattern = r'\.{2}\/|\;|\/{2}|\:|^\/|\.py'
	if re.search(pattern, badinput):
		return 'BAD'
	else:
		#No character other then regex pattern was found
		goodinput = badinput
		return goodinput

#default variables
port = 12345
MAX_SIZE = 5
BUFFER_SIZE = 1024
verbose= True
server = "localhost"

# check for port and verbose args

if len(sys.argv) == 3 and sys.argv[2]== "-v":
	#optional verbose arg
	verbose = True
	
if len(sys.argv) > 1:
	port = int(sys.argv[1])	
if len(sys.argv) > 2:
	MAX_SIZE = int(sys.argv[2])
	

# establish connection parameters
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((server, port))
sock.listen(5)
# instantiate the manager class
manager = Manager()
manager.start()

if verbose == True: 
	print "server waiting on port", port
while True:
	# get new socket in tcp
	conn, addr = sock.accept() 
	if verbose == True: 
		print 'server connected to client at {}:{}'.format(addr[0],addr[1])
	
	t = ClientHandler(conn)
	manager.add(t)
	