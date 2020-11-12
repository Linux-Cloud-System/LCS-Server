import os
import math

def getFileData(dataDirectory, fileName):
    with open(os.path.join(dataDirectory, fileName), 'rb') as file:
        data = file.read(int(getFileSize(dataDirectory, fileName)))
        return data
    
def getFileSize(dataDirectory, fileName):
    fileSize = os.path.getsize(os.path.join(dataDirectory, fileName))
    return str(fileSize).encode()

def isFileExists(fileName):
    return os.path.exists(os.path.join(dataDirectory, fileName))

def recvFileData(clientSocket, fileSize):
    print("fileData receiving")
    
    fileData = b""
    while True: # receive all data
        part = clientSocket.recv(int(fileSize))
        fileData += part
                
        if len(fileData) == int(fileSize): # last data
            break

    return fileData
    
def fileUpload(dataDirectory, fileName, fileData):    
    with open(os.path.join(dataDirectory, fileName), "wb+") as file: # file Open with byte write        
        file.write(fileData) # write file
        
def splitFile(fileData):
    n = math.ceil(len(fileData)/4)
    return [fileData[i:i+n] for i in range(0, len(fileData), n)]