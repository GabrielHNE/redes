from io import BufferedReader
import socket               # Import socket module
import time
import os
import math

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

def openFile(file_path): 
    '''
    '''
    file_namebase = os.path.basename(file_path) 
    file_size = os.path.getsize(file_path)

    file = open(file_path,'rb')

    return  (file, file_namebase, file_size)

def connection():
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    host = input("Forneca o host: ")
    port = int(input("Forneca a porta de conexao: ")) # Reserve a port for your service.

    file_path = input("Caminho para o arquivo a ser enviado:\n")
    pck_size = int(input("Escolha o tamanho do pacote (500) (1000) (1500): "))

    if(pck_size != 500 and pck_size != 1000 and pck_size != 1500):
        print("Tamanho de pacote invalido...\n")
        exit()
 
    conn = (host, port)

    file, file_namebase, file_size = openFile(file_path)
    
    # primeiro batch enviado
    s.sendto(f'{file_namebase}/{file_size}/{pck_size}'.encode(), conn)

    message = s.recvfrom(1024) # aguardando mensagem de continuação
    msg = message[0].decode()

    if(msg != "continue"):
        print("Servidor não continuou a conexão por algum motivo. Finalizando!")
        exit()
        
    total_packages = math.ceil((file_size/pck_size))

    print(f"Quantidade total de pacotes a serem enviados: {total_packages}")

    batch = 8
    flag = True
    sair = False

    l = file.read(pck_size)
    cont = 0
    start_time = time.time()
    while (l):
        printProgressBar(cont, total_packages, "Enviando: ","Completo", length= 50)
        
        cont = cont + 1
        s.sendto(l, conn)
        l = file.read(pck_size)
            
    final_time = (time.time() - start_time)
    file.close()
    
    #printa log de informações
    print("Tempo decorrido {0:.3f}".format(final_time))
    print(f'Pacotes enviados ({pck_size}): {cont}')
    print("Velocidade (bits/s): {0:.3f}".format(((cont*pck_size*8)/final_time)/(10**6)))
    print("Arquivo enviado...")

def wait_connection():
    host = input("Forneca o host: ")
    port = int(input("Forneca a porta de conexao: ")) # Reserve a port for your service.
    
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)         # Create a socket object
    s.bind((host, port))        # Bind to the port

    print(f"Sua rede: {host}:{port}")
    print("Aguardando conexões")

    # Pega o 1 batch de conexao
    data = s.recvfrom(1024)
    msg_arr = data[0].decode().split('/') # recupera as informações dp 1 batch
    address = data[1]

    s.sendto("continue".encode(),address) #confirma o recebimento
    
    file_name = msg_arr[0]
    file_size = int(msg_arr[1])
    buffer = int(msg_arr[2])

    file = open(f'./downloads/{file_name}','wb')

    print(f"{file_name} {file_size} {buffer}")

    # Etapa 3
    total_packages = math.ceil((file_size/buffer))

    batch = 8

    cont_pck = 0
    size_rec = 0
    # Listen for incoming datagrams
    start_time = time.time()
    while(size_rec != file_size):
        
        printProgressBar(cont_pck, total_packages, "Recebendo: ","Completo", length= 50)
        bytesAddressPair = s.recvfrom(buffer)
        cont_pck = cont_pck + 1

        bytes = bytesAddressPair[0]
        assert address == bytesAddressPair[1]

        file.write(bytes)
        size_rec += len(bytes)
        
    final_time = (time.time() - start_time)
    file.close()
    
    print("Tempo decorrido: {0:.3f}".format(final_time))
    print(f"Tamanho do arquivo recebido: {size_rec} bytes")
    print(f"Quantidade de pacotes: {cont_pck} ({buffer})")
    print("Velocidade (bit/s): {0:.3f}".format(((cont_pck*buffer*8)/final_time)/(10**6)))
    print("Arquivo recebido")
    
while True:
    choice = input("Deseja se conectar ou aguardar uma conexão? conectar/aguardar: ")

    if choice == 'conectar':
        connection()
    elif choice == 'aguardar':
        wait_connection()
    else:
        exit()


