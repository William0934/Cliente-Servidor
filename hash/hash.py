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

def equal(a,b):    
    if b==None or len(a) != len(b):
        return False
    else:
        for i in range(len(a)):
            if a[i] != b[i]:
                return False 
    return True


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
        print(ident," ",op," ",args)
        ident=ident.decode()
        
        if op.decode()=="add":            
            if not validKey(nodes,ident):
                socket.send_multipart([bytes(ident,'ascii') ,bytes("refused", 'ascii')])
            else:
                print('loading')
                nodes[ident]=(args[0].decode(),args[1].decode())
                print(ident," ",nodes[ident])
                for key in nodes:
                    if key in fingers:
                        temp=fingers[key]
                    else: temp=None
                    fingers[key]=getFingerTable(nodes,key)
                    if not equal(fingers[key],temp):
                        msg=[bytes(key,'ascii'),bytes("update", 'ascii')]
                        temp=[]
                        for finger in fingers[key]:
                            temp.append(bytes(str(finger)+" "+str(nodes[str(finger)][0])+" "+str(nodes[str(finger)][1]),'ascii'))
                        msg+=temp
                        print("msg: ",msg)
                        socket.send_multipart(msg)
                print('finishing')
                    
                

if __name__ == '__main__':
    main()
