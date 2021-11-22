import socket               # Import socket module
import time
import os

pck_size = 500

def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def connection():
    host = input("Forneca o host: ")
    port = int(input("Forneca a porta de conexao: "))

    file_path = input("Caminho para o arquivo a ser enviado:\n")
    pck_size = int(input("Escolha o tamanho do pacote (500) (1000) (1500): "))

    if(pck_size != 500 and pck_size != 1000 and pck_size != 1500):
        print("Tamanho de pacote invalido...\n")
        exit()
    
    s = socket.socket()
    s.connect((host,port))

    msg = s.recv(1024).decode()
    
    if(msg == "conectado"):
        print("Uhul\n")
        # informações antes do envio do arquivo
        # tamanho do arquivo
        # nome do arquivo + extensao

        file_name = os.path.basename(file_path) 
        file_size = os.path.getsize(file_path)

        print(f'Enviando: {file_name} {file_size} {pck_size}')

        s.send(f'{file_name}/{file_size}/{pck_size}'.encode())

        ready = s.recv(1024).decode()

        if(ready == 'ready'):
            f = open(file_path,'rb')
            l = f.read(pck_size)
            total_packages = (int)(file_size/pck_size)
            cont = 0

            start_time = time.time()
            while (l):
                printProgressBar(cont, total_packages, "Enviando: ","Completo", length= 50)
                s.send(l)
                l = f.read(pck_size)
                cont = cont + 1

            final_time = (time.time() - start_time)

            f.close()
            print(f"Velocidade (bits/s): {(total_packages*pck_size*8)/final_time}")
            print("Done Sending")
            s.shutdown(socket.SHUT_WR)                     # Close the socket when done
            s.close()
    else:
        pass

    
    
def wait_connection():
    s = socket.socket()         # Create a socket object
    host = socket.gethostbyname(socket.gethostname()) # Get local machine name
    port = 3000                 # Reserve a port for your service.

    s.bind((host, port))        # Bind to the port

    s.listen(5)                 # Now wait for client connection.

    print("Aguardando conexão")
    print(f"Sua rede: {host}:{port}")
    c, addr = s.accept()     # Establish connection with client.
    print('Got connection from', addr)
    c.send("conectado".encode())

    desc = c.recv(1024).decode().split('/')
        
    file = open(f'download-{desc[0]}','wb')

    c.send("ready".encode())

    print("Receiving...")
    start_time = time.time()
    l = c.recv(pck_size)
    total_packages = (int)(int(desc[1])/int(desc[2]))
    cont = 0
    pck_count = 1
    while (l):
        printProgressBar(cont, total_packages, "Enviando: ","Completo", length= 50)
        file.write(l)
        l = c.recv(pck_size)
        pck_count = pck_count + 1
        cont=cont+1
    file.close()
    final_time = (time.time() - start_time)
    print(f"file_name: {desc[0]}, file_size: {desc[1]}, pkg_size: {desc[2]}\n")
    msg = 'Thank you for connecting'.encode('ascii')
    c.send(msg)
    c.close()                # Close the connection
    
    print(f"Tempo de corrido: {final_time}")
    print(f"Tamanho do arquivo: {pck_count*pck_size} bytes")
    print(f"Quantidade de pacotes ({pck_size}): {pck_count}")
    print(f"Velocidade (bit/s): {(pck_count*pck_size*8)/final_time}")

while True:
    choice = input("Deseja se conectar ou aguardar uma conexão? conectar/aguardar: ")

    if choice == 'conectar':
        connection()
    elif choice == 'aguardar':
        wait_connection()
    else:
        exit()


