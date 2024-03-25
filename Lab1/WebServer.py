from socket import *
import sys


SERVER_PORT = int(sys.argv[1])

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost', SERVER_PORT))
serverSocket.listen(1)

print("The server is ready to receice")

while 1:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()

    rec_file = sentence.split()[1][1:]
    
    try:
        f = open(rec_file, 'rb')
        content = f.read()
        if("html" in rec_file):
            response = "\nHTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        elif("png" in rec_file):
            response = "\nHTTP/1.1 200 OK\r\nContent-Type: image/png\r\n\r\n"

        connectionSocket.sendall(response.encode())
        connectionSocket.sendall(content)
        connectionSocket.close()
    
    except FileNotFoundError:
        response = "\nHTTP/1.1 404 File not found\r\n\r\n"
        content = "<h1><head><center> 404 not found </center></head></h1>"

        connectionSocket.sendall(response.encode())
        connectionSocket.sendall(content.encode())
        connectionSocket.close()

