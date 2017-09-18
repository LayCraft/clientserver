The earlier labs are generally terrible and don't come with error checking and other things. Lab5 is a rebuild of the client server application in java. The python and java versions in lab4 and lab5 should be able to talk.

Perhaps this isn't the best code but is shows where I was at programming-wise in mid-2015.

------------------------------

Here are some instructions for running the lab4 version:
First set the server to listen on port 12345 and run verbose. The default port is 12345
>  python lab4server.py 12345 -v

Then run the client. It supports the commands GET, PUT, and DEL.
>  python lab4client.py localhost 12345 PUT amazonia.jpg
