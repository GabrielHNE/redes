#! /usr/bin/env python

import socket
import sys
import time
import threading

class Server(threading.Thread):
    def run(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("Server started successfully\n")
        hostname=''
        port=51412

        self.sock.bind((hostname,port))
        self.sock.listen(1)
        
        print("Listening on port %d\n" %port)       
        
        #time.sleep(2)    
        (clientname,address)=self.sock.accept()
        print("Connection from %s\n" % str(address))

        while 1:
            chunk=clientname.recv(4096)            
            print(str(address)+':'+chunk.decode())

class Client(threading.Thread):    
    def connect(self,host,port):
        self.sock.connect((host,port))

    def client(self,msg):               
        sent=self.sock.send(msg.encode())           
        print("Sent\n")

    def run(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        try:
            host=input("Enter the hostname: ")            
            port=int(input("Enter the port: "))
    
        except EOFError:
            print("Error")
            return 1
        
        print("Connecting\n")

        self.connect(host,port)
        print("Connected\n")

        while 1:            
            print("Waiting for message\n")
            msg=input('>>')
            if msg=='exit':
                break
            if msg=='':
                continue
            print("Sending >> ")
            self.client(msg)
        return(1)

if __name__=='__main__':
    
    srv=Server()
    srv.daemon=True
    
    print("Inicializando servidor")
    srv.start()

    time.sleep(1)

    print("Inicializando client")
    cli=Client()
    
    cli.start()