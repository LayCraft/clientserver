#!/usr/bin/python

import socket, sys

port = int(sys.argv[1])
op = sys.argv[2]        # the operator
values = sys.argv[3:]   # the list of values

# build the data array from the
# commandline arguments.
b = bytearray()

# First byte is the operator
if op == '+':
	b.append(1)
elif op == '-':
	b.append(2)
elif op == '*':
	b.append(4)
else:
	print "Bad operator: " + op
	sys.exit()

# Second byte is the number of items
b.append(len(values))

# Third and subsequent bytes are packed values, with
# two values to a byte, the only exception possibly
# being the last item.

for i in range(0, len(values), 2):
	left = int(values[i]) << 4
	right = int(values[i+1]) if (i+1) < len(values) else 0
	b.append(left + right)
	
# Now send the data over.
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('localhost', port))
s.sendall(b)

# Now receive the response.  It comes as a 4-item bytearray; we have to
# recieve that as a string, convert to a bytearray, and then build a
# 32-bit integer from that!

# receive the string
response = bytearray(4)
s.recv_into(response)
s.close()

# build the 32-bit integer
first = response[0] & 255
second = response[1] & 255
third = response[2] & 255
fourth = response[3] & 255
result = (first << 24) + (second << 16) + (third << 8) + (fourth)
if result >= 2**31: result -= 2**32
print result
