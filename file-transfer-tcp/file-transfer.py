import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                 # Reserve a port for your service.

s.bind((host, port))        # Bind to the port
f = open('torecv.png','wb')
s.listen(5)                 # Now wait for client connection.

while True:
    choice = input("Deseja enviar algum arquivo? s/n")

    if choice == 's':
        pass
    elif choice == 'n':
        print("Aguardando conexões")
        c, addr = s.accept()     # Establish connection with client.
        print('Got connection from', addr)
        print("Receiving...")
        l = c.recv(1024)

        print('Nome do arquivo %s', l)
        algo = input()
        while (l):
            print("Receiving...")
            f.write(l)
            l = c.recv(1024)
        f.close()
        print("Done Receiving")
        msg = 'Thank you for connecting'.encode('ascii')
        c.send(msg)
        c.close()                # Close the connection