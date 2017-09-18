"""
This file expects command line arguments in the form of  
$ client.py [server] [portnum] [operation] [filename]

python lab2client.py localhost 12345 PUT amazonia.jpg
"""

import string 
import os

LEFT_NIBBLE = 240
RIGHT_NIBBLE = 15

import socket
import sys

try:
	# collect command line args
	BUFFER_SIZE = 1024
	server = sys.argv[1]
	port = int(sys.argv[2])
	command = sys.argv[3].upper()
	filename = sys.argv[4]
	filesize = 0
except:
	print 'ERROR: malformed command line argument'
	sys.exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
sock.connect((server, port))

#wait for ready
data = sock.recv(BUFFER_SIZE)

if data == "READY":
	#send command and filename
	data = command + " " + filename
	sock.send(data)


	if command == "GET":		
		#filesize to collect
		filesize = sock.recv(BUFFER_SIZE)
		
		# if the filesize isn't an int, print the error message
		try:
			filesize = int(filesize)
			# prepare to receive file
			file = open(filename, 'wb')
		except:
			# print error message
			print filesize
			sys.exit()
			
		sock.send("OK")	
		print "client recieving file {} ({} bytes)".format(filename,filesize)

		try:
		
			while filesize > 0:
				data = sock.recv(min(filesize, BUFFER_SIZE))
				file.write(data)
				filesize -= BUFFER_SIZE
			file.close()
			# server confirms the file is complete
			data = sock.recv(4)
			if data == "DONE":
				print "Complete"
			else:
				print "Incomplete. {} of {} recieved.".format(tally,filesize)
				print "DONE was expected. '{}' was recieved".format(data)
		except:
			print sys.exc_info[0]
			print sys.exc_info[1]			
			sys.exit()
			
	elif command == "PUT":
		# check for server ready
		data = sock.recv(BUFFER_SIZE)
		if data == "OK":
			try:
				filesize = str(os.path.getsize(filename))
			except:
				print "Error: cannot find file to send"
				sys.exit()
				
			#give the server the file size in bytes
			sock.send(filesize)
			
			# check if the server is OK
			data = sock.recv(BUFFER_SIZE)	
			packets = int(filesize)/BUFFER_SIZE+1
			file = open(filename, 'rb', BUFFER_SIZE)
			print "client sending file {} ({} bytes)".format(filename,filesize)
			i=0
			while i< packets:
				sock.send(file.read(BUFFER_SIZE))
				i+=1

			# server file confirmation
			data = sock.recv(BUFFER_SIZE)
			if data == "DONE":
				print "Complete"
			else:
				print data
	
	elif command == "DEL":
		data = sock.recv(BUFFER_SIZE)
		print "client deleting file " + filename
		if data == "DONE":
			print "Complete"
		else:
			print data			
			
sock.close()

