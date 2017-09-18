#!/usr/bin/python

import socket, sys

port = int(sys.argv[1])

# some useful masks
FIRST_NIBBLE = 15 << 4
SECOND_NIBBLE = 15
FIRST_BYTE = 255 << 24
SECOND_BYTE = 255 << 16
THIRD_BYTE = 255 << 8
FOURTH_BYTE = 255

# create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind(("", port))
while True:
	
	# wait for a client to connect, receive the data into a bytearray
	# buffer
	buffer = bytearray(7)

	nbytes, addr = sock.recvfrom_into(buffer)
	
	# parse the bytearray; first item is the operator
	operator = buffer[0]
	
	# second item is the count
	count = buffer[1]
	
	# third and subsequent items are the values, packed as two
	# nibbles per byte.
	processed = 0
	index = 2
	while processed < count:
		first = (buffer[index] & FIRST_NIBBLE) >> 4
		second = (buffer[index] & SECOND_NIBBLE)
		if processed == 0:
			result = first
		else:
			if operator == 1: result += first
			elif operator == 2: result -= first
			elif operator == 4: result *= first
		
		if processed+1 < count:
			if operator == 1: result += second
			elif operator == 2: result -= second
			elif operator == 4: result *= second
			
		processed += 2
		index += 1
	
	# build the response bytearray, a 4-byte integer.
	response = bytearray(4)
	response[0] = (result & FIRST_BYTE) >> 24
	response[1] = (result & SECOND_BYTE) >> 16
	response[2] = (result & THIRD_BYTE) >> 8
	response[3] = (result & FOURTH_BYTE)

	# send the result back to the client.
	sock.sendto(response, addr)
