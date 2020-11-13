import socket
import socketFileComm as fileComm

HOST = ""
PORT = 3334
dataDirectory = "/home/pi/Desktop/data/Data2" # data directory

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind((HOST, PORT))
    
    print("Socket Server is listening")
    serverSocket.listen()
    
    while True:
        print("Waiting for client")
        clientSocket, addr = serverSocket.accept()
        print("Connected by ", addr)
        
        request = clientSocket.recv(512).decode() # download, upload, delete, update
        clientSocket.sendall("ok".encode()) # send "ok"
        
        if request == "upload":
            fileSize = clientSocket.recv(512).decode() # recieve fileSize
            clientSocket.sendall("ok".encode()) # send "ok"
            
            fileName = clientSocket.recv(512).decode() # recieve fileName
            clientSocket.sendall("ok".encode()) # send "ok"
            
            fileData = fileComm.recvFileData(clientSocket, fileSize) # recieve fileData

            fileComm.writeFile(dataDirectory, fileName, fileData)
            
        elif request == "download": # download
            fileName = clientSocket.recv(512).decode()
            
            fileSize = fileComm.getFileSize(dataDirectory, fileName)
            clientSocket.sendall(str(fileSize).encode())
            
            clientSocket.recv(2)
            fileData = fileComm.getFileData(dataDirectory, fileName)
            clientSocket.sendall(fileData)
            
            
        elif request == "delete":
            fileName = clientSocket.recv(512).decode()
            
            fileComm.deleteFile(dataDirectory, fileName)         
            
        #elif request == "update":    