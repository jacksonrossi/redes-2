#----------------------------------------------------------------------------------------------
#               Arquivo: servidor_2.py
#----------------------------------------------------------------------------------------------
#               Autores: Bruno Eduardo Farias GRR20186715
#                        Jackson Rossi Borguezani GRR20176573
#         Atualizado em: [21/04/2022, 00h45]
#----------------------------------------------------------------------------------------------
#           Implementa o Servidor TCP (2)
#----------------------------------------------------------------------------------------------

import socket
import time
from random import randrange
import logging

HOST = "localhost"
PORT = 9002 #porta de conexão
TAM_MSG = 1024  #em bytes
NAME = "Snag,    CANADA"

#gera a temperatura aleatoriamente
def verifica_temperatura():
    t = randrange(20) - 30
    logging.info('Verificando temperatura do Servidor (2) {} ... {}ºC'.format(NAME, t))
    time.sleep(1)
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
    logging.info('\n\n')
    logging.info('Servidor 2 - Iniciado no IP {} na porta {}'.format(HOST, PORT))

    while True:
        #aceita nova conexão
        conexao, cache = tcp.accept()
        logging.info('Servidor 2 - Conexão realizada por: {}'.format(cache))

        while True:
            #recebe as mensagens de solicitação
            msg = conexao.recv(TAM_MSG)
            if not msg:
                break
            temperatura = verifica_temperatura()
            #envia a temperatura como resposta
            conexao.sendall(str(temperatura).encode("utf-8"))

        #finaliza conexão cache
        print()
        logging.info('Servidor 2 - Finalizando conexão cache {}'.format(cache))
        conexao.close()
        #break
