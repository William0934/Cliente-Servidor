import zmq
import sys

def main():
    if len(sys.argv) != 6:
        print("Invalid port")
        exit()

    serverIp = sys.argv[1] # Server's ip ---argv:argumento
    serverPort = sys.argv[2] # Server's port
    myIp = sys.argv[3]
    myPort = sys.argv[4]
    identity = sys.argv[5].encode('ascii')
    
    context = zmq.Context()
    serverSocket = context.socket(zmq.DEALER)
    serverSocket.identity = identity
    serverSocket.connect("tcp://{}:{}".format(serverIp, serverPort)) #corchetes por que se enviaron los parametros el ip y el port
    serverSocket.send_multipart([bytes('add', 'ascii'),bytes(myIp,'ascii'),bytes(myPort,'ascii')])
    
    print("Started node with id {}".format(identity))
    
    poller = zmq.Poller()
    poller.register(sys.stdin, zmq.POLLIN)
    poller.register(serverSocket, zmq.POLLIN)

    fingerTable={}

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
                print('new finger: ',msg)
                fingerTable={}
                for item in msg:
                    temp=item.split()
                    fingerTable[temp[0].decode()]=(temp[1].decode(),int(temp[2].decode()))
                print(fingerTable)


    
if __name__ == '__main__':
    main()
