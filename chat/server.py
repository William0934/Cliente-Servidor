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
        ident, op , *dest= socket.recv_multipart()
        if op.decode()=="bring":
            i=whereIs(sessions,ident)
            d=whereIs(sessions,op[1])
            if d == -1:
                if i!= -1:
                    sessions[i].append(op)
                else:
                    sessions.append([ident,dest[0]])
                socket.send_multipart([dest[0] ,bytes("connect", 'ascii'), bytes("NA", 'ascii')])
        elif op.decode()=="send":
            i=whereIs(sessions,ident)
            dest.insert(0,"id")
            dest.insert(1,bytes("play", 'ascii'))
            for id in sessions[i]:
                dest[0]=id
                if id!=ident:
                    socket.send_multipart(dest)
        elif op.decode()=="exit":
            i=whereIs(sessions,ident)
            sessions[i].remove(ident)

if __name__ == '__main__':
    main()
