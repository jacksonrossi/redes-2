import socket
import time
from random import randrange

HOST = "localhost"
PORT = 9003
TAM_MSG = 1024  #em bytes
NAME = "Ghadames, LIBIA"

def verifica_temperatura():
    print('Verificando temperatura do Servidor 3 ..')
    time.sleep(2)
    return randrange(20) + 50

if __name__ == "__main__":
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    origem = (HOST, PORT)
    tcp.bind(origem)
    tcp.listen(1)
    print('\nServidor Iniciado no IP', HOST, 'na porta', PORT)
    conexao, cache = tcp.accept()
    print('\nConexão realizada por:', cache)

    while True:
        msg = conexao.recv(TAM_MSG)
        temperatura = verifica_temperatura()
        conexao.sendall(str(temperatura).encode("utf-8"))
