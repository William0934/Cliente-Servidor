import zmq
import sys




def main():
    if len(sys.argv) != 4:
        print("Error!!!!")
        exit()
    ip = sys.argv[1] # Server's ip ---argv:argumento
    port = sys.argv[2] # Server's port
    id = sys.argv[3] # ID

    context = zmq.Context()
    s = context.socket(zmq.REQ)
    s.connect("tcp://{}:{}".format(ip, port)) #corchetes por que se enviaron los parametros el ip y el port
    s.send_json({"op":"register","id":id})
    resp = s.recv_json()
    if resp["flag"]:
        while True:
            print ("\n----Menu----")
            print ("- 'list'                    ......... Listar usuarios conectados")
            print ("- 'invite' {id de usuario}  ......... Invitar a sesion (sin llaves)")
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
                s.send_json({"op":"invite","id":operation[1]})
                msg=s.recv_json()
                if msg["answer"]=="yes":
                    operation[0] = "connect"
                elif msg["answer"]=="no":
                else:

    else:
        print("Error!!! invalid id")

if __name__ == '__main__':
     main()

# se ejecuta python client.py 192.168.8.217 4321 list

#Preguntarle al servidor cuantas partes tiene un archivo
