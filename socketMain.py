import socket
import os
import socketFileComm as fileComm

serverHost = ""
subHost = ["127.0.0.1", "127.0.0.1", "127.0.0.1"]
Port = 3333
subPort = [3334, 3335, 3336]
dataDirectory = "/home/pi/Desktop/data/Data" # local data storage
bufferSize = 1024
    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket: # open server socket
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    serverSocket.bind((serverHost, Port))
    
    print("Socket Server is listening")
    serverSocket.listen()
    
    while(True):
        print("Waiting for client")
        clientSocket, addr = serverSocket.accept()
        print("Connected by ", addr)
        
        request = clientSocket.recv(bufferSize).decode() # download, upload, delete, list
        print(request)
        
        if request == "upload":
            # communication with client
            clientSocket.sendall("ok".encode()) # send "ok"
            
            fileSize = clientSocket.recv(bufferSize).decode() # recieve fileSize
            clientSocket.sendall("ok".encode()) # send "ok"
            
            fileName = clientSocket.recv(bufferSize).decode() # recieve fileName
            clientSocket.sendall("ok".encode()) # send "ok"
            
            fileData = fileComm.recvFileData(clientSocket, fileSize) # recieve fileData
            
            fileData = fileComm.splitFile(fileData) # split file
            
            fileComm.writeFile(dataDirectory, fileName, fileData[0])
            
            # communication with subNode
            for i in range(2, 5):
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as subSocket:
                    subSocket.connect((subHost[i-2], subPort[i-2]))
                    
                    subSocket.sendall("upload".encode()) # send "upload"
                    
                    subSocket.recv(2) # receive "ok" == ready to receive next data
                    subSocket.sendall(str(len(fileData[i-1])).encode()) # send fileSize
                    
                    subSocket.recv(2) # receive "ok"
                    subSocket.sendall(fileName.encode()) # send fileName
                    
                    subSocket.recv(2) # receive "ok"
                    subSocket.sendall(fileData[i-1]) # send fileData
            
        elif request == "download":
            # communication with client
            clientSocket.sendall("ok".encode()) # send "ok"
            
            fileName = clientSocket.recv(bufferSize).decode() # recieve fileName
            
            fileSize = fileComm.getFileSize(dataDirectory, fileName) # get fileSize from local storage        
            fileData = fileComm.getFileData(dataDirectory, fileName) # get fileData from local storage
            
            # communication with subNode
            for i in range(2, 5):
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as subSocket: # open socket with subNode
                    subSocket.connect((subHost[i-2], subPort[i-2])) # connect with subNode
            
                    subSocket.sendall("download".encode()) # send download
                    
                    subSocket.recv(2) # receive "ok"
                    subSocket.sendall(fileName.encode()) # send FileName
                    
                    fileSize = subSocket.recv(bufferSize).decode() # receive fileSize
                    subSocket.sendall("ok".encode()) # send "ok"
                    
                    fileData += fileComm.recvFileData(subSocket, fileSize) # get FileData from each subNode
            
            clientSocket.sendall(str(len(fileData)).encode()) # send total fileSize to client
            
            clientSocket.recv(2) # receive "ok"
            clientSocket.sendall(fileData) # send fileData
            
        elif request == "delete":
            clientSocket.sendall("ok".encode()) # send "ok"
            
            fileName = clientSocket.recv(bufferSize).decode() # recieve fileName
            
            fileComm.deleteFile(dataDirectory, fileName)
            
            for i in range(2, 5):
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as subSocket: # open socket with subNode
                    subSocket.connect((subHost[i-2], subPort[i-2])) # connect with subNode
                    
                    subSocket.sendall("delete".encode()) # send delete
                    
                    subSocket.recv(2)
                    subSocket.sendall(fileName.encode())
                    
        elif request == "list": # file count, file list
            clientSocket.sendall(str(fileComm.getFileCount(dataDirectory)).encode()) # send file count
            
            for fileName in fileComm.getFileList(dataDirectory): # get each fileName
                clientSocket.recv(2) # receive "ok"
                clientSocket.sendall(fileName.encode()) # send each fileName