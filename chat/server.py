import zmq
import sys
import os
from math import ceil
IDs={}

IDs["test"]=False

def main():
    if len(sys.argv) != 2:
        print("Error!!!!!")
        exit()

    port= sys.argv[1]

    context = zmq.Context()
    s = context.socket(zmq.REP)
    s.bind("tcp://*:{}".format(port))


    while True:
        msg = s.recv_json() #recibir por ese socket
        if msg["op"] == "register":
            if msg["id"] in IDs:
                s.send_json({"flag":False})
            else:
                s.send_json({"flag":True})
                IDs[msg["id"]]=True
                print(IDs)

        elif msg["op"] == "list":
            temp=[]
            for key in IDs:
                if IDs[key]:
                    temp.append(key)
            s.send_json({"IDs": list(temp)}) #mensaje estructurado, campo IDs tiene lista de usuarios conectados
        
        else:
            print("unsupported action!")
            s.send_json({"Error": "Error"})

if __name__ == '__main__':
    main()

#se ejecuta python server.py 4321 /home/utp/Descargas

#Tomar el tamaño el archivo/1024.
