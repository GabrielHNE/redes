import socket

msgFromClient       = "Lorem ipsum dolor sit amet, consectetur Duis tincidunt purus at diam malesuada blandit. Integer posuere bibendum risus, sit amet maximus mi tincidunt vitae. Sed posuere, lacus quis finibus scelerisque, purus neque auctor mauris, vitae aliquet tortor mi sed magna. Duis laoreet imperdiet accumsan. Cras viverra quam at tempus semper. Sed sit amet egestas erat. Aliquam ut mattis nisi, non fermentum enim. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin vehicula finibus erat, quis commodo nulla consequat bibendum. Cras sapien ex, ornare vitae fermentum eget, consectetur tristique ante. Sed fermentum augue at justo ultricies, sed consectetur urna scelerisque. Nulla semper nec est elementum facilisis. Aliquam egestas est ut erat auctor, in finibus lorem commodo. Suspendisse potenti.Phasellus dapibus et nisl ac elementum. Morbi rutrum vehicula turpis, eget vestibulum enim rutrum sit amet. Praesent eu magna lobortis diam porta accumsan. Mauris eu risus non purus vehicula posuere viverra."
bytesToSend          = str.encode(msgFromClient)
serverAddressPort   = ("25.8.205.36", 20001)
bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

msgFromServer = UDPClientSocket.recvfrom(bufferSize)

msg = "Message from Server {}".format(msgFromServer[0])

print(msg)