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
    ans = serverSocket.recv_multipart()
    print(ans)
    print("Started node with id {}".format(identity))
    
    
if __name__ == '__main__':
    main()
