import socket
import sys
import RPi.GPIO as GPIO

# create a socket client object
# create a TCP/IP socket
try:
    mysocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except socket.error as err:
    print("Socket creation failed with error %s" %err)
    sys.exit()

try:
    # Bind the socket to localhost on port 80   
    mysocket.bind(('localhost', 80))
except socket.error as err:
    print("Socket binding failed with error %s" %err)
    sys.exit()  

# Enable the server to accept connections (max 5 queued connections)
mysocket.listen(5)
print("Socket is listening for incoming connections...")

# create a Live server
while True:
    conn, addr = mysocket.accept()
    print("Connection established with:", addr)
    #receive data from the client
    data = conn.recv(1000)
    if   not data:
        break
    print("Received data:", data.decode())
    #send data back to the client
    conn.sendall(data)

# control some LEDs here
led_pin = 14  # Example GPIO pin number

if data.decode().strip() == b"on": # it is a byte string
    print("Turning LED ON")
    GPIO.output(led_pin, True)
elif data.decode().strip() == b"off":
    print("Turning LED OFF")
    GPIO.output(led_pin, False)

conn.close()
# close the socket
mysocket.close()