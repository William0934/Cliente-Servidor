import zmq
from math import pow
import sys

numberOfBytes=5

def validKey(dict,key):
    keys = list(dict.keys())
    max=pow(2,numberOfBytes)
    if key in keys or int(key)>max:
        return False
    return True

def next(value,list):
    if int(list[-1])<value:
        return list[0]
    else:
        for id in list:
            if value<=int(id):
                return id

def getFingerTable(nodes,id):
    table=[]
    keys = list(nodes.keys())
    temp=[]
    for k in keys:
        temp.append(int(k))
    keys=sorted(temp)
    max=pow(2,numberOfBytes)
    for i in range(numberOfBytes):
        table.append(str(int(next(pow(2,i)+int(id),keys)%max)))
    table=sorted(table)
    
    d={}
    temp = [int(d.setdefault(x,x)) for x in table if x not in d ]
    i=int(id)
    if i in temp:
        temp.remove(i)
    temp.sort()

    return temp

def main():
    if len(sys.argv) != 2:
        print("Invalid port")
        exit()

    context = zmq.Context()
    socket = context.socket(zmq.ROUTER)

    port= sys.argv[1]
    socket.bind("tcp://*:{}".format(port))
    print("Started server")

    nodes={} #asocia key con tupla de ip y puerto
    fingers={} #asocia key con fingerTable

    while True:
        ident, op , *args = socket.recv_multipart()
        ident=ident.decode()
        
        if op.decode()=="add":            
            if not validKey(nodes,ident):
                socket.send_multipart([bytes(ident,'ascii') ,bytes("refused", 'ascii')])
            else:
                nodes[ident]=(args[0].decode(),args[1].decode())
                fingers[ident]=getFingerTable(nodes,ident)
                msg=[bytes(ident,'ascii'),bytes("acepted", 'ascii')]
                temp=[]
                for finger in fingers[ident]:
                    temp.append(bytes(str(finger),'ascii'))
                msg+=temp
                print(msg)
                socket.send_multipart(msg)
                
                

if __name__ == '__main__':
    main()
