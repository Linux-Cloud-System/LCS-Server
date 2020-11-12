import socket
import os
import socketFileComm as fileComm
import time

serverHost = ""
subHost = ["127.0.0.1", "127.0.0.1", "127.0.0.1"]
Port = 3333
tempPort = [3334, 3335, 3336]
dataDirectory = "/home/pi/Desktop/data/Data" # data directory
                
def fileUpdate():
    print("is it possible?")
    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind((serverHost, Port))
    
    print("Socket Server is listening")
    serverSocket.listen()
    
    while(True):
        print("Waiting for client")
        clientSocket, addr = serverSocket.accept()
        print("Connected by ", addr)
        
        request = clientSocket.recv(512).decode() # download, upload, delete, update
        clientSocket.sendall("ok".encode()) # send "ok"
        print(request)
        
        if request == "upload":
            fileSize = clientSocket.recv(512).decode() # recieve fileSize
            clientSocket.sendall("ok".encode()) # send "ok"
            
            fileName = clientSocket.recv(512).decode() # recieve fileName
            clientSocket.sendall("ok".encode()) # send "ok"
            
            fileData = fileComm.recvFileData(clientSocket, fileSize) # recieve fileData
            
            fileData = fileComm.splitFile(fileData) # split file
            
            fileComm.writeFile(dataDirectory, fileName, fileData[0])
            
            for i in range(2, 5):
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as subSocket:
                    subSocket.connect((subHost[i-2], tempPort[i-2]))
                    
                    subSocket.sendall("upload".encode()) # send "upload"
                    
                    subSocket.recv(2) # receive "ok" == server is ready to receive next data
                    subSocket.sendall(str(len(fileData[i-1])).encode()) # send fileSize
                    
                    subSocket.recv(2) # receive "ok"
                    subSocket.sendall(fileName.encode()) # send fileName
                    
                    subSocket.recv(2) # receive "ok"
                    subSocket.sendall(fileData[i-1]) # send fileData
            
        elif request == "download":
            fileName = clientSocket.recv(512).decode() # recieve fileName
            
            fileSize = fileComm.getFileSize(dataDirectory, fileName)            
            fileData = fileComm.getFileData(dataDirectory, fileName)
            
            for i in range(2, 5):
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as subSocket:
                    subSocket.connect((subHost[i-2], tempPort[i-2]))
            
                    subSocket.sendall("download".encode())
                    
                    subSocket.recv(2)
                    subSocket.sendall(fileName.encode())
                    
                    fileSize = subSocket.recv(512).decode()
                    subSocket.sendall("ok".encode()) # send "ok"
                    
                    fileData += fileComm.recvFileData(subSocket, fileSize)
            
            clientSocket.sendall(str(len(fileData)).encode())
            
            clientSocket.recv(2)
            clientSocket.sendall(fileData)
                    
        elif request == "delete":
            fileDelete()
        elif request == "update":
            fileUpdate()
            