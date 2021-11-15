import socket
from threading import Thread

def escutando_clientes(client_sockets, cs):
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    while True:
        try:
            # keep listening for a message from `cs` socket
            msg = cs.recv(1024).decode()
        except Exception as e:
            # client no longer connected
            # remove it from the set
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            # if we received a message, replace the <SEP> 
            # token with ": " for nice printing
            msg = msg.replace("<SEP>", ": ")

        # iterate over all connected sockets
        for client_socket in client_sockets:
            # and send the message
            client_socket.send(msg.encode())

if __name__ == '__main__':
    # server's IP address
    SERVER_HOST = input("Host: ") # "25.43.150.148"
    SERVER_PORT = int(input("Port: ")) # port we want to use

    separator_token = "<SEP>" # we will use this to separate the client name & message

    # initialize list/set of all connected client's sockets
    client_sockets = set()

    # create a TCP socket
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # make the port as reusable port
    s.bind((SERVER_HOST, SERVER_PORT)) # bind the socket to the address we specified
    s.listen(10) # listen for upcoming connections

    print(f"** {SERVER_HOST}:{SERVER_PORT}")

    while True:
        # we keep listening for new connections all the time
        client_socket, client_address = s.accept()
        print(f"[+] {client_address} Novo usuário conectado.")

        # add the new connected client to connected sockets
        client_sockets.add(client_socket)
        # start a new thread that listens for each client's messages
        t = Thread(target=escutando_clientes, args=(client_sockets, client_socket))
        # make the thread daemon so it ends whenever the main thread ends
        t.daemon = True
        # start the thread
        t.start()
    
    # close client sockets
    for cs in client_sockets:
        cs.close()

    # close server socket
    s.close()
