import socket

TELNET_DEFAULT_PORT = 2323 # 23 (mas precisaria de permição de sudo)
TELNET_DEFAULT_BUFFERSIZE = 1024
TELNET_DEFAULT_ENCODING = 'ascii'

IP = socket.gethostbyname(socket.gethostname())
ADDR = (IP, TELNET_DEFAULT_PORT)