import zmq
import sys
from collections import namedtuple

import threading

import pyaudio


def play(list):
    stream = p.open(format = FORMAT,
                            channels = CHANNELS,
                            rate = RATE,
                            input = False,
                            output = True,
                            frames_per_buffer = CHUNK)
    while True:
        if len(list)>-1:
            frames=list.pop(0)
                for frame in frames:
                    stream.write(frame, CHUNK)


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
    p = pyaudio.PyAudio()
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 0.3
    first=True
 
    queue={}
    print ("\n----Menu----")
    print ("- 'bring' {id de usuario}  ......... Invitar a sesion (sin llaves)")
    print ("- 'exit'                   ......... Salir del programa")

    threads=[]
    while True:
        socks = dict(poller.poll())
        if s in socks:
            op , *msg= s.recv_multipart()
            if op.decode()=="connect":
                connected = True
            elif op.decode()=="play":               
                #RECIBIENDO FRAMES
                if msg[0] in queue:
                    queue[msg[0]].append(msg[1:0])
                else: 
                    queue[msg[0]]=[msg[1:]]
                    threads.append( threading.Thread(target=play),args=(queue[msg[0]]))
                    threads[-1].start()
        if sys.stdin.fileno() in socks:
            command = input()
            command = command.split()
            if command[0]=="bring":
                s.send_multipart([bytes(command[0], 'ascii'),bytes(command[1], 'ascii')])
                connected=True
            elif command[0]=="exit":
                s.send_multipart([bytes(command[0], 'ascii'),bytes("NA", 'ascii')])
                break
            else:
                print( ' Operacion no soportada')
        if connected:
            if first:           
                stream = p.open(format = FORMAT,
                            channels = CHANNELS,
                            rate = RATE,
                            input = True,
                            output = False,
                            frames_per_buffer = CHUNK)

                first = False        
            frames = [bytes('send', 'ascii')]
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                frames.append(stream.read(CHUNK))
            #ENVIANDO FRAMES
            s.send_multipart(frames)
                    
    p.terminate()        
    stream.stop_stream()
    stream.close()
    

    
if __name__ == '__main__':
     main()
