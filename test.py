import pyaudio
import socket
import threading
from pydub import AudioSegment
from pydub.utils import make_chunks
import pydub

pydub.AudioSegment.export_options = {'format': 'opus', 'codec': 'libopus'}


CHUNK = 256
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 48000

def recorder(stream):
    data = stream.read(CHUNK, exception_on_overflow=False)
    return bytes(data)

def speaker(stream,data):
    stream.write(data)

def receive(client_socket):
    length = CHUNK*4
    buf = bytearray()
    while True:
        buf += client_socket.recv(length - len(buf))
        if len(buf) >= length:
            break
    return bytes(buf)

def send(client_socket, data):
    client_socket.sendall(data)
    
def encode_opus(audio_data):
    audio = AudioSegment(audio_data, sample_width=2, frame_rate=RATE, channels=CHANNELS)
    chunks = make_chunks(audio, CHUNK)
    opus_chunks = []
    for chunk in chunks:
        opus_chunk = chunk.export(format='opus')
        opus_chunks.append(opus_chunk.read())  # 변경된 부분
    opus_data = b''.join(opus_chunks)
    return opus_data

def decode_opus(opus_data):
    opus_audio = AudioSegment(opus_data, frame_rate=RATE, channels=CHANNELS, sample_width=2)
    pcm_audio = opus_audio.export(format='s16le')
    return pcm_audio.read()

def close_connection(client_socket, mic_stream, speaker_stream):
    client_socket.close()
    mic_stream.stop_stream()
    mic_stream.close()
    speaker_stream.stop_stream()
    speaker_stream.close()
    sound_obj.terminate()

sound_obj = pyaudio.PyAudio()
mic_stream = sound_obj.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
speaker_stream = sound_obj.open(format=FORMAT,channels=CHANNELS,rate=RATE,output=True,frames_per_buffer=CHUNK)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 10002))    

def writer(sock, mic_stream):
    while True:
        data = recorder(mic_stream)
        opus_data = encode_opus(data)
        send(client_socket, opus_data)
        if not is_running:
            break

def reader(sock, speaker_stream):
    while True:
        opus_data = receive(client_socket)
        if opus_data == b'':
            break
        pcm_data = decode_opus(opus_data)
        speaker(speaker_stream, pcm_data)
        if not is_running:
            break

is_running = True
writer_thread = threading.Thread(target=writer, args=(client_socket,mic_stream))
reader_thread = threading.Thread(target=reader, args=(client_socket,speaker_stream))

writer_thread.start()
reader_thread.start()

while is_running:
    user_input = input("'exit' 입력시 연결종료 : ")
    if user_input == "exit":
        is_running = False
        close_connection(client_socket, mic_stream, speaker_stream)
        
writer_thread.join()
reader_thread.join()
