import socket
import sys
import os
import re

# clean the filename string
def clean(badinput):
	pattern = r'\.{2}\/|\;|\/{2}|\:|^\/|\.py'
	if re.search(pattern, badinput):
		return 'BAD'
	else:
		#No character other then regex pattern was found
		goodinput = badinput
		return goodinput
	
# the port defaults to 12345
port = 12345
# the server defaults to localhost
server = "localhost"

BUFFER_SIZE = 1024
verbose= False

# check for port and verbose args
if len(sys.argv) >= 2:
	#first arg is port number
	port = int(sys.argv[1])
if len(sys.argv) == 3 and sys.argv[2]== "-v":
	#optional verbose arg
	verbose = True

# establish connection parameters
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((server, port))
if verbose == True: 
	print "server waiting on port", port

while True:
	# only one connection allowed to the server
	sock.listen(1) 
	# get new socket in tcp
	conn, addr = sock.accept() 
	if verbose == True: 
		print 'server connected to client at {}:{}'.format(addr[0],addr[1])
	#stop listening for requests when server busy
	sock.listen(0)
	
	#return ready state to client
	conn.send("READY")
	
	# collect command
	data = conn.recv(BUFFER_SIZE)
	if verbose == True: 
		print 'server receiving request:', data

	# split the command into filename
	tmp = data.split(' ')
	command = tmp[0] 
	filename = tmp[1]
	
	# check for bad filename
	filename = clean(filename)	
	if filename == "BAD":
		conn.send("ERROR: the filename is illegal")
		continue
	elif command == "GET":
		try:
			#return file size
			filesize = str(os.path.getsize(filename))
		except:
			conn.send("ERROR: {} does not exist".format(filename))
			continue

		#return the client the file size in bytes
		conn.send(filesize)
		
		# check if the client is OK
		data = conn.recv(BUFFER_SIZE)	
		packets = int(filesize)/BUFFER_SIZE

		if verbose == True: print "server sending {} bytes".format(filesize)
		
		# send data
		file = open(filename, 'rb', BUFFER_SIZE)
		i=0
		while i< packets:
			conn.send(file.read(BUFFER_SIZE))
			i+=1

		conn.send("DONE")

	elif command == "PUT":
		# let client know OK to proceed
		conn.send("OK")
		#continue when the client declares they are sending a file but aren't
		try:		
			# get file size
			filesize = int(conn.recv(BUFFER_SIZE))
		except:
			continue

		#tell client filesize is OK
		conn.send("OK")
				
		if verbose == True: 
			print 'server receiving {} bytes'.format(filesize)
		
		#create a file handle

		with open(filename, "wb") as f:
			while filesize > 0:
				data = conn.recv(min(filesize, BUFFER_SIZE))
				f.write(data)
				filesize -= BUFFER_SIZE
			f.close()
		
		conn.send("DONE")
		
	elif command == "DEL":
		if verbose == True: 
			print 'server deleting file', filename
		try:
			# try to delete specified file
			os.remove(clean(filename))
		except:
			conn.send("ERROR: {} does not exist".format(filename))
			continue
			
		conn.send("DONE")
	else:
		if verbose == True: print "ERROR: bad command recieved"

	sock.listen(1)