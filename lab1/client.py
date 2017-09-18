"""
This file expects command line arguments in the form of  
$ client.py [portnum] [operator] [int] [int2] [int...]
"""

LEFT_NIBBLE = 240
RIGHT_NIBBLE = 15

import socket
import sys

def signEncoder(x):
	if x == "+":
		# 0000 0001
		return 1
	elif x == "-":
		# 0000 0010
		return 2
	elif x == "*":
		# 0000 0100
		return 4

##### This section interprets the command line arguments ######

# variable that counts ints
count = 0;

# make a byte array and have a placeholder for length in position 0
buffer = bytearray()
buffer.append(0) # add a space for the operator code
buffer.append(0) # add a space for length of values

# the first is left and the second is right
lr = False;
purgatory = 0;

for x in sys.argv:
	if x == sys.argv[0] or x == sys.argv[1]:
		continue
	elif x == sys.argv[2]:
		buffer[0] = signEncoder(x)
	else:
		x = int(x)
		if lr == False:
			# shift the data four left
			purgatory = x << 4
			lr = True
			count +=1

		elif lr == True:
			temp = purgatory | x
			# append the int to the byte array
			buffer.append(int(temp))
			lr = False
			purgatory=0
			count +=1
if lr == True:
	buffer.append(int(purgatory))
# put the count of all elements into the first spot of the bytearray
buffer[1] = count


##### This section connects to the server ######
port = int(sys.argv[1])
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
sock.connect(("localhost", port))

# send the bytearray to the server
sock.sendall(buffer)


##### This section collects and interprets the response from the server ######
# collect response from the server
response = bytearray(4)
nBytes, addr = sock.recvfrom_into(response)
bytemask = 255

byte0 = response[0]<<24
byte1 = response[1]<<16
byte2 = response[2]<<8
byte3 = response[3]
total = byte0+byte1+byte2+byte3

#compensate for unsigned return
if (total >= 1<<31):
	total = total - 2**32
	
print total

sock.close()