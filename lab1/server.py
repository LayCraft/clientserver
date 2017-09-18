import socket
import sys

LEFT_NIBBLE = 15<<4
#print LEFT_NIBBLE
RIGHT_NIBBLE = 15

# this does the math based on whatever operator is passed to it
def mathit(array, operator):
	# 1 2 4  is + - *
	if operator == 1:
		sum = 0
		for x in array:
			sum = x + sum
	elif operator == 2:
		# initial value patch
		sum = array[0]*2
		for x in array:
			sum = sum - x
	elif operator == 4:
		sum = 1
		for x in array:
			sum = x * sum
	else:
		print 'the operator is invalid'
	return sum


# establish connection parameters
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind the port locally to 12345
port = 12345
if len(sys.argv) == 2:
	port = int(sys.argv[1])
sock.bind(("localhost", port))

# make a buffer that is waiting for the data to be passed
buffer = bytearray(12)

while True:
	nBytes, addr = sock.recvfrom_into(buffer)
	# numberBytes portAddress
	response = bytearray(4)

	# collect the type of operator
	operator = int(buffer[0])
	# how many values are in the byte array
	count = int(buffer[1])

	#--------collecting and decompressing

	#this is the array that contains the things to be operated on
	temp = []
	i=0
	j=0
	for x in buffer:
		if j < 2:
			j+=1
			continue
		else:
			if i < count:
				tmp = (x & LEFT_NIBBLE)>>4
				i+=1
				temp.append(tmp)
			if i < count:
				tmp = (x & RIGHT_NIBBLE)
				i+=1
				temp.append(tmp)
	#perform math on the array
	total = mathit(temp, operator)

	bytemask = 255

	#11111111 00000000 00000000 00000000
	response[0] =  ((bytemask << 24) & total)>>24
	#00000000 11111111 00000000 00000000
	response[1] =  ((bytemask << 16) & total)>>16
	#00000000 00000000 11111111 00000000
	response[2] =  ((bytemask << 8) & total)>>8
	#00000000 00000000 00000000 11111111
	response[3] =  (bytemask & total)
	"""
	#test response bytearray
	for x in response:
		print x
	"""
	sock.sendto(response, addr)
