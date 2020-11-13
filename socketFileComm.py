import os
import math

def getFileData(dataDirectory, fileName):
    with open(os.path.join(dataDirectory, fileName), 'rb') as file:
        data = file.read(int(getFileSize(dataDirectory, fileName)))
        return data
    
def getFileSize(dataDirectory, fileName):
    return os.path.getsize(os.path.join(dataDirectory, fileName))

def getFileList(dataDirectory):
    return [i for i in os.listdir(dataDirectory)]
    
def getFileCount(dataDirectory):
    return len(getFileList(dataDirectory))
    
    
def isFileExists(dataDirectory, fileName):
    return os.path.exists(os.path.join(dataDirectory, fileName))


def recvFileData(clientSocket, fileSize):
    fileData = b""
    while True: # receive all data
        part = clientSocket.recv(int(fileSize))
        fileData += part
        
        #print(len(part), len(fileData))
        if len(fileData) == int(fileSize): # all data receive
            break

    return fileData

def writeFile(dataDirectory, fileName, fileData):    
    with open(os.path.join(dataDirectory, fileName), "wb+") as file: # file Open with byte write        
        file.write(fileData) # write file
        
def deleteFile(dataDirectory, fileName):
    if isFileExists(dataDirectory, fileName):
        os.remove(os.path.join(dataDirectory, fileName))
        
def splitFile(fileData):
    n = math.ceil(len(fileData)/4) # split file by n
    result = [fileData[i:i+n] for i in range(0, len(fileData), n)] # return splited file list
    if len(result) != 4: # file size is too small
        for i in range(len(result), 4): 
            result[i] = b"" # fill null data in empty list
    return result