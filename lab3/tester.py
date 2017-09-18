import socket

urlHost = "http://blog.tonycode.com/tonyprimerano"
urlResource = "/tonyprimerano"

BUFFER_SIZE = 1024

site = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
site.connect((urlHost,80))
request = "GET " + urlResource + "\n\n"
print request

site.send(request)
print "request sent"

html = site.recv(2048)
print html

