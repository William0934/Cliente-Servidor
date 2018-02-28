import zmq
import sys
from collections import namedtuple


queue=[]

def main():
    if len(sys.argv) != 4:
        print("Error!!!!")
        exit()
    ip = sys.argv[1] # Server's ip ---argv:argumento
    port = sys.argv[2] # Server's port
    identity = sys.argv[3].encode('ascii')
    connected = False

    context = zmq.Context()
    s = context.socket(zmq.DEALER)
    s.identity = identity
    s.connect("tcp://{}:{}".format(ip, port)) #corchetes por que se enviaron los parametros el ip y el port
    
    print("Started client with id {}".format(identity))
    
    
    poller = zmq.Poller()
    poller.register(sys.stdin, zmq.POLLIN)
    poller.register(s, zmq.POLLIN)
    print ("\n----Menu----")
    print ("- 'bring' {id de usuario}  ......... Invitar a sesion (sin llaves)")

    while True:
        socks = dict(poller.poll())
        if s in socks:
            op, msg = s.recv_multipart()
            print ("LLEGO: ",op,msg)
            if op.decode()=="connect":
                connected = True
            elif op.decode()=="play":
                print(msg)

        if sys.stdin.fileno() in socks:
            command = input()
            command = command.split()
            if command[0]=="bring":
                s.send_multipart([bytes(command[0], 'ascii'),bytes(command[1], 'ascii') ])
            else:
                print( ' Operacion no soportada')
        if connected:
            s.send_multipart([bytes('send', 'ascii'),bytes("audio", 'ascii') ])

    

    """if resp["flag"]:
        while True:
            operation = input("Digite la operacion a ejecutar: ")
            operation = operation.split()
            if operation[0] == "list":
                s.send_json({"op":"list"})
                ids=s.recv_json()
                print(" Los usuarios disponibles son:")
                for i in ids["IDs"]:    
                    if i!=id:
                        print("   {}".format(i))
            elif operation[0]== "invite":
                s.send_json({"op":"invite","id":operation[1],"who":ids})
                msg=s.recv_json()
                if msg["answer"]=="yes":
                    operation[0] = "connect"
                elif msg["answer"]=="no":
                    print(" El usuario {} ya esta en una sesion".format(operation[1]))
                else:
                    print(" El usuario {} no fue encontrado".format(operation[1]))
            elif operation[0]=="connect":
                s = context.socket(zmq.DEALER)
                s.identity = id
                s.connect("tcp://{}:{}".format(ip, port))
                poller = zmq.Poller()
                poller.register(sys.stdin, zmq.POLLIN)
                poller.register(s, zmq.POLLIN)
                #CREAR HILO DE REPRODUCCION ACA

                while True:
                    socks = dict(poller.poll())
                    if socket in socks:
                        sender, m = socket.recv_multipart()
                        queue.append(m)
            else:
                print(" ERROR: Operacion invalida")

    else:
        print("Error!!! invalid id")"""

if __name__ == '__main__':
     main()
