import zmq
import sys
import threading
import os

numberOfBytes=5

def migrate(reqSocket,context,files,fingerTable):
    for key in fingerTable:
        temp=fingerTable[key]
        reqSocket.connect("tcp://{}:{}".format(temp[0], temp[1]))
        reqSocket.send_json({"op":"save","data":" por implementar"})
        ans=reqSocket.recv_json()
        reqSocket.close()
        reqSocket = context.socket( zmq.REQ )

def getNext(identity,keys):
    print (identity)
    for key in keys:
        if key>int(identity):
            return str(key)
    return str(keys[0])

def askFiles(reqSocket,context,identity,fingerTable):
    if len(fingerTable)>0:
        temp=fingerTable.keys()
        keys=[]
        for key in temp:
            keys.append(int (key))
        keys=sorted(keys)
        next=getNext(identity,keys)
        temp = fingerTable[next]
        arg = "tcp://{}:{}".format(temp[0],temp[1])
        print ('askFiles to ',arg)
        reqSocket = context.socket( zmq.REQ )        
        reqSocket.connect(arg)
        reqSocket.send_json({'op':'release'})
        ans=reqSocket.recv_json()
        print(" answer: ",ans)
        reqSocket.close()
        reqSocket = context.socket( zmq.REQ )

def serve(repSocket,l):
    while True:
        msg = repSocket.recv_json()
        if msg['op']=='leave':
            repSocket.send_json({'op':'left'})
            break
        if msg['op']=='release':
            print('releasing')
            repSocket.send_json({'op':'released'})


        

def main():
    if len(sys.argv) != 6:
        print("Invalid port")
        exit()
    #Interpretacion de los argumentos pasados por consola
    serverIp = sys.argv[1] # Server's ip ---argv:argumento
    serverPort = sys.argv[2] # Server's port
    myIp = sys.argv[3]
    myPort = sys.argv[4]
    identity = sys.argv[5].encode('ascii')
    
    #Socket por el que se reciben y mandan mensajes al servidor
    context = zmq.Context()
    serverSocket = context.socket(zmq.DEALER)
    serverSocket.identity = identity
    serverSocket.connect("tcp://{}:{}".format(serverIp, serverPort)) #corchetes por que se enviaron los parametros el ip y el port
    serverSocket.send_multipart([bytes('add', 'ascii'),bytes(myIp,'ascii'),bytes(myPort,'ascii')])
    
    #socket por el que se reciben peticiones de otros nodos
    repSocket = context.socket(zmq.REP)
    repSocket.bind("tcp://*:{}".format(myPort))
    print('bind ',myPort)
    #lista de sockets por los que se mandan peticiones a otros nodos
    reqSocket = context.socket(zmq.REQ)


    print("Started node with id {}".format(identity))
    
    poller = zmq.Poller()
    poller.register(sys.stdin, zmq.POLLIN)
    poller.register(serverSocket, zmq.POLLIN)

    fingerTable ={}
    files       ={}
    print ("\n----Menu----")
    print("to leave the system please type 'leave' ")
    l=[]
    t=threading.Thread(target=serve, args=(repSocket,l))
    t.start()
    while True:
        socks = dict(poller.poll())
        if serverSocket in socks:
            op , *msg= serverSocket.recv_multipart()
            print(op,' ',msg)
            op = op.decode()
            if op == 'refused':
                print ('connection refused')
                break
            if op == 'update':
                first = len(fingerTable)==0
                fingerTable={}
                for item in msg:
                    temp=item.split()
                    fingerTable[temp[0].decode()]=(temp[1].decode(),int(temp[2].decode()))
                print('fingerTable updated:',fingerTable)
                if first:askFiles(reqSocket,context,identity,fingerTable)
        if sys.stdin.fileno() in socks:
            command = input()
            command = command.split()
            if command[0]=='leave':
                migrate(reqSocket,context,files,fingerTable)
                serverSocket.send_multipart([bytes('leave', 'ascii')])
                reqSocket = context.socket( zmq.REQ )
                reqSocket.connect("tcp://{}:{}".format('localhost', myPort))
                reqSocket.send_json({'op':'leave'})
                ans=reqSocket.recv_json()
                break
            if command[0]=='store':
                if os.path.exists("store/"+command[1]):
                    print("El archivo Existe")
                else:
                    print("El archivo no existe")
            else:
                print('command "',command[0],'" invalid')

    
if __name__ == '__main__':
    main()
