#
# TRABALHO REDES II
# JACKSON ROSSI BORGUEZANI - GRR20176573
# BRUNO EDUARDO FARIAS - GRR20186715
#
import socket
import time
from random import randrange
import logging

HOST = "localhost"
PORT = 9003 #porta de conexão
TAM_MSG = 1024  #em bytes
NAME = "Ghadames, LIBIA"

#gera a temperatura aleatoriamente
def verifica_temperatura():
    t = randrange(20) + 50
    #print('Verificando temperatura do Servidor (3) {} ... {}ºC'.format(NAME, t))
    logging.info('Verificando temperatura do Servidor (3) {} ... {}ºC'.format(NAME, t))
    time.sleep(2)
    return t

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler()
        ]
    )

    #abre socket de conexão, define origem, coloca em modo passivo (listen)
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    origem = (HOST, PORT)
    tcp.bind(origem)
    tcp.listen()
    #print('\nServidor Iniciado no IP', HOST, 'na porta', PORT)
    logging.info('\n\n')
    logging.info('Servidor 3 - Iniciado no IP {} na porta {}'.format(HOST, PORT))

    while True:
        #aceita nova conexão
        conexao, cache = tcp.accept()
        #print('\nConexão realizada por:', cache)
        logging.info('Servidor 3 - Conexão realizada por: {}'.format(cache))

        while True:
            #recebe as mensagens de solicitação
            msg = conexao.recv(TAM_MSG)
            if not msg:
                break
            temperatura = verifica_temperatura()
            #envia a temperatura como resposta
            conexao.sendall(str(temperatura).encode("utf-8"))

        #finaliza conexão cache
        #print('Finalizando conexão cache', cache)
        logging.info('Servidor 3 - Finalizando conexão cache {}'.format(cache))
        conexao.close()
