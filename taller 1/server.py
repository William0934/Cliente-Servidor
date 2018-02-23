import zmq
import sys
import os
from math import ceil

bufferSize=int(1024*1024)

def loadFiles(path):
    files = {}
    dataDir = os.fsencode(path) #path lo convierte a un objeto de datos en el sistema operativo
    for file in os.listdir(dataDir):
        filename = os.fsdecode(file)
        print("Loading {}".format(filename))
        files[filename] = file
    return files

def main():
    if len(sys.argv) != 3:
        print("Error!!!!!")
        exit()

    directory = sys.argv[2]
    port= sys.argv[1]

    context = zmq.Context()
    s = context.socket(zmq.REP)
    s.bind("tcp://*:{}".format(port))

    files = loadFiles(directory)

    while True:
        msg = s.recv_json() #recibir por ese socket
        if msg["op"] == "list":
            s.send_json({"files": list(files.keys())}) #mensaje estructurado, campo files tiene lista, ubicacion archivo como valor
        elif msg["op"] == "size":            
            filename = msg["file"]
            if filename in files:
               temp=os.path.getsize(directory+filename)
               temp=ceil(temp/bufferSize)
               s.send_string(str(temp))
            else:
                print ("no existe")
                s.send_string("-1")            
        elif msg["op"] == "download":
            filename = msg["file"]
            if filename in files:
                f=open(directory + filename,"rb")
                f.seek(msg["part"]*bufferSize)
                ms=f.read(bufferSize)
                s.send(ms)
            else:
                print ("no existe")
        else:
            print("unsupported action!")


if __name__ == '__main__':
    main()

#se ejecuta python server.py 4321 /home/utp/Descargas

#Tomar el tamaño el archivo/1024.
