import zmq
import sys

def whereIs(list,id):
    i=0
    for small in list:
        for element in small:
            if id==element:
                return i
        i+=1
    return -1

def main():
    if len(sys.argv) != 2:
        print("Invalid port")
        exit()

    context = zmq.Context()
    socket = context.socket(zmq.ROUTER)

    port= sys.argv[1]
    socket.bind("tcp://*:{}".format(port))
    print("Started server")

    sessions=[]

    while True:
        ident, op, dest = socket.recv_multipart()
        if op.decode()=="bring":
            i=whereIs(sessions,ident)
            d=whereIs(sessions,dest)
            if d == -1:
                if i!= -1:
                    sessions[i].append(dest)
                else:
                    sessions.append([ident,dest])
                socket.send_multipart([dest ,bytes("connect", 'ascii'), bytes("NA", 'ascii')])
        elif op.decode()=="send":
            i=whereIs(sessions,ident)
            for id in sessions[i]:
                socket.send_multipart([id ,bytes("play", 'ascii'),bytes(str(sessions[i]), 'ascii') ])
        print(sessions)

if __name__ == '__main__':
    main()

"""import zmq
import sys
import os
from math import ceil
IDs={}

IDs["test"]=False

def main():
    if len(sys.argv) != 2:
        print("Error!!!!!")
        exit()

    

    context = zmq.Context()
    s = context.socket(zmq.REP)
    s.bind("tcp://*:{}".format(port))

    #SEGUNDO SOCKET

    while True:
        msg = s.recv_json() #recibir por ese socket
        if msg["op"] == "register":
            if msg["id"] in IDs:
                s.send_json({"flag":False})
            else:
                s.send_json({"flag":True})
                IDs[msg["id"]]=True
        elif msg["op"] == "list":
            temp=[]
            for key in IDs:
                if IDs[key]:
                    temp.append(key)
            s.send_json({"IDs": list(temp)}) #mensaje estructurado, campo IDs tiene lista de usuarios conectados
        elif msg["op"] == "invite":
            if msg["id"] in IDs:
                if IDs[msg["id"]]:
                    s1
                    s.send_json({"answer":"yes"})

                else:
                    s.send_json({"answer":"no"})
            else:
                s.send_json({"answer":"missing"})
        else:
            print("unsupported action!")
            s.send_json({"Error": "Error"})

if __name__ == '__main__':
    main()

#se ejecuta python server.py 4321 /home/utp/Descargas

#Tomar el tamaño el archivo/1024.
"""