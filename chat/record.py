import pyaudio
import wave
 
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 0.3
WAVE_OUTPUT_FILENAME = "file.wav"
 
p = pyaudio.PyAudio()
 
# start Recording

stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True,
                frames_per_buffer = CHUNK)
print ("recording...")
frames = []
 
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print ("finished recording")
 
print (len(frames))

for frame in frames:
	stream.write(frame, CHUNK)

stream.stop_stream()
print (frames)
stream.close()

p.terminate()