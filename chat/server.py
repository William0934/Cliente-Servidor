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
        elif op.decode()=="exit":
            i=whereIs(sessions,ident)
            sessions[i].remove(ident)
        print(sessions)

if __name__ == '__main__':
    main()
