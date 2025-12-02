import socket
import sys
# create a socket client object
# create a TCP/IP socket
try:
    mysocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except socket.error as err:
    print("Socket creation failed with error %s" %err)
    sys.exit()

# Take the domani name and get the corresponding IP address
try:
    host=socket.gethostbyname("www.google.com")
except socket.gaierror as err:
    print("Error getting IP address: %s" %err)
    sys.exit()  

mysocket.connect((host,80))
# send a simple HTTP GET request (since its a web server)
# 1.1 is the HTTP version
message="GET / HTTP/1.1\r\n\r\n"
try:
    mysocket.sendall(message.encode())
except socket.error as err:
    print("Error sending data: %s" %err)
    sys.exit()

# receive the response data (up to 4096 bytes)
data=mysocket.recv(1000)
print(data.decode())
# close the socket
mysocket.close()
