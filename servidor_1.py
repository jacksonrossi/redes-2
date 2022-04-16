import socket
import time
from random import randrange

HOST = "localhost"
PORT = 9001
TAM_MSG = 1024  #em bytes
NAME = "Dallol, ETIOPIA"

def verifica_temperatura():
    t = randrange(10) + 40
    print('Verificando temperatura do Servidor (2) {} ... {}ºC'.format(NAME, t))
    time.sleep(2)
    return t

if __name__ == "__main__":
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    origem = (HOST, PORT)
    tcp.bind(origem)
    tcp.listen()
    print('\nServidor Iniciado no IP', HOST, 'na porta', PORT)

    while True:
        conexao, cache = tcp.accept()
        print('\nConexão realizada por:', cache)

        while True:
            msg = conexao.recv(TAM_MSG)
            if not msg:
                break
            temperatura = verifica_temperatura()
            conexao.sendall(str(temperatura).encode("utf-8"))
        print('Finalizando conexão cache', cache)
        conexao.close()
