import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                 # Reserve a port for your service.

s.connect((host, port))

f = open('tosend.png','rb')

print('Sending...')
#sending bytes - 1024
l = f.read(1024)
while (l):
    print('Sending...')
    s.send(l)
    l = f.read(1024)

f.close()
print("Done Sending")
s.shutdown(socket.SHUT_WR)                     # Close the socket when done
s.close()