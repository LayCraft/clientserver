
import socket
import sys


def htmlGet (host, resource):
	# new connection to server
	site = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	site.connect((host,80))
	# send request for resource to server
	request = "GET /" + resource + "\n\n"
	site.send(request)

	# collect request data in content string until end html tag is found
	content = ""
	while "</html>" not in content.lower():
		data = site.recv(BUFFER_SIZE)
		content = content + data
	
	site.close()
	return content

#--------------main program--------------------

BUFFER_SIZE = 1024	

# get request from CLI
url = sys.argv[1]
#parse url into host and resource
url = url.split("http://")
url = url[1].split("/",1)

# collect host and resource for connection
try:
	host = url[0]
	resource = url[1]
except:
	host = url[0]
	resource = "/"

html = htmlGet(host, resource)
html = html.split("\n")

#host and port for rob's text2html service
host = "rtvm.cs.camosun.bc.ca"
port = 10010

# socket connection to server bound to sock
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

# check for ready
data = sock.recv(BUFFER_SIZE)
if data == "READY":
	
	#send html file line by line to the server
	for i in html:
		sock.send(i)
	
	#listen for response and collect it in blocks
	rendered = ""
	while "COMP173 HTML CONVERT COMPLETE" not in rendered:
		rendered += sock.recv(BUFFER_SIZE)

	rendered = rendered[:-30]
	print rendered

#close socket
sock.close()
