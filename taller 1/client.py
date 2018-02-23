import zmq
import sys

def main():
    if len(sys.argv) != 4:
        print("Error!!!!")
        exit()
    ip = sys.argv[1] # Server's ip ---argv:argumento
    port = sys.argv[2] # Server's port
    operation = sys.argv[3] # operation to perform

    context = zmq.Context()
    s = context.socket(zmq.REQ)
    s.connect("tcp://{}:{}".format(ip, port)) #corchetes por que se enviaron los parametros el ip y el port

    if operation == "list":
        s.send_json({"op":"list"})  #envieme un mensaje estructural(op), la operacion es lista (op,lista)--send:enviar
        files = s.recv_json() #recv:recibir. es sincrona se queda esperando hasta que este algo.
        print (files)
    elif operation == "download":
        name = input("File to download ")
        s.send_json({"op": "size", "file": name})
        size = int(s.recv())
        if size > -1:
            file=open(name,"ab")
            for i in range(size):
                s.send_json({"op": "download", "file": name,"part":i})
                file.write(s.recv())
            file.close()
        else:
            print("File doesn't exists. :O")
    else:
        print("Error!!! unsupported operation")

    print("Connecting to Server {} at {}".format(ip, port))

if __name__ == '__main__':
     main()

# se ejecuta python client.py 192.168.8.217 4321 list

#Preguntarle al servidor cuantas partes tiene un archivo
