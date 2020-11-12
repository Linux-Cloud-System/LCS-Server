import os
import math

def getFileData(dataDirectory, fileName):
    with open(os.path.join(dataDirectory, fileName), 'rb') as file:
        data = file.read(int(getFileSize(dataDirectory, fileName)))
        return data
    
def getFileSize(dataDirectory, fileName):
    fileSize = os.path.getsize(os.path.join(dataDirectory, fileName))
    return fileSize

def isFileExists(fileName):
    return os.path.exists(os.path.join(dataDirectory, fileName))

def recvFileData(clientSocket, fileSize):
    fileData = b""
    while True: # receive all data
        part = clientSocket.recv(int(fileSize))
        fileData += part
                
        #print(len(part), len(fileData))
        if len(fileData) == int(fileSize): # last data
            break

    return fileData
    
def writeFile(dataDirectory, fileName, fileData):    
    with open(os.path.join(dataDirectory, fileName), "wb+") as file: # file Open with byte write        
        file.write(fileData) # write file
        
def splitFile(fileData):
    n = math.ceil(len(fileData)/4)
    result = [fileData[i:i+n] for i in range(0, len(fileData), n)]
    if len(result) != 4:
        for i in range(len(result), 4):
            result[i] = b""
    return result

def fileDelete():
    fileName = fileComm.recvFileName()
    
    if fileComm.isFileExists(fileName):
        os.remove(os.path.join(dataDirectory, fileName))
    else:
        clientsocket.sendall("There is no file " + fileName)