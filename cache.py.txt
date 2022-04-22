#----------------------------------------------------------------------------------------------
#               Arquivo: cache.py
#----------------------------------------------------------------------------------------------
#               Autores: Bruno Eduardo Farias GRR20186715
#                        Jackson Rossi Borguezani GRR20176573
#         Atualizado em: [21/04/2022, 00h45]
#----------------------------------------------------------------------------------------------
#         Implementa a Tabela Cache das Temperaturas e sua Comunicação Cliente-Servidor
#----------------------------------------------------------------------------------------------

import socket
import time
import json
import logging
from random import randrange
from datetime import datetime, timedelta
from servidor_1 import HOST as HOST_1, PORT as PORT_1, NAME as NAME_1
from servidor_2 import HOST as HOST_2, PORT as PORT_2, NAME as NAME_2
from servidor_3 import HOST as HOST_3, PORT as PORT_3, NAME as NAME_3

TAM_MSG = 1024    #em bytes
TABELA_CACHE = []
DURACAO = 30    #em segundos
N_SERVER = [NAME_1, NAME_2, NAME_3]
HOST_C = "localhost"
PORT_C = 9000

#realiza as conexões com os servidores
def conexao_servidor(host, port):
    cache = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    destino = (host, port)
    cache.connect(destino)

    time.sleep(1)
    return cache

#inicializa dados na cache
def insere_dados(ide, nome, temperatura, timestamp, conexao):
    server = {
        "id": ide,
        "nome_servidor": nome,
        "temperatura": temperatura,
        "timestamp": timestamp,
        "inicializado": False,
        "conexao": conexao
    }
    return server

#inicializa cache
def inicia_cache(servidores):
    logging.info('')
    logging.info('Iniciando Tabela Cache')
    cache = []
    for i in range (0, 3):
        server = insere_dados(
            i,
            N_SERVER[i],
            0,
            datetime.now(),
            servidores[i]
        )
        cache.append(server)
    return cache

#verifica se os dados foram inicializados e se o tempo está válido (dentro dos 30 segundos)
def dados_validos(server):
    tempo_atual = datetime.now()
    tempo_cache = server.get("timestamp")
    if server.get("inicializado") and tempo_atual <= tempo_cache + timedelta(seconds=DURACAO):
        return True
    else:
        return False

#solicita a temperatura do servidor (quando não encontrado ou não está válido na cache)
def solicita_temp(server):
    conexao = server.get("conexao")
    conexao.sendall(b"Solicita temperatura")
    temp = conexao.recv(TAM_MSG)
    temp = temp.decode("utf-8")
    logging.info('Obteve a temperatura {} ºC do servidor {}\n'.format(temp, server.get("nome_servidor")))

    return{
        "id": server.get("id"),
        "nome_servidor": server.get("nome_servidor"),
        "temperatura": temp,
        "timestamp": datetime.now(),
        "inicializado": True,
        "conexao": server.get("conexao")
    }

#atualiza a cache com as novas temperaturas
def atualiza_cache(server_u):
    TABELA_CACHE[server_u.get("id")] = server_u

def consulta(server, dados):
    if dados_validos(server):
        logging.info('{} : Dados em cache válidos'.format(server.get("nome_servidor")))
        logging.info('{}ºC Timestamp do dado na cache: {}\n'.format(server.get("temperatura"), server.get("timestamp")))
        is_cache = True
    else:
        if server.get("inicializado"):
            logging.info('{} : Dados em cache EXPIRADOS (última atualização: {})'.format(server.get("nome_servidor"), server.get("timestamp")))
            logging.info('Solicitando temperatura dos servidores')
        else:
            logging.info('{} : Dados em cache EXPIRADOS (NÃO INICIALIZADOS)'.format(server.get("nome_servidor")))
            logging.info('Solicitando temperatura dos servidores')
        #solicita temperatura e atualiza cache
        #for serv in TABELA_CACHE:
        server_up = solicita_temp(serv)
        atualiza_cache(server_up)
        server = server_up
        is_cache = False
        #server = TABELA_CACHE[server.get("id")]

    #json para ser enviado ao cliente
    dados.append({
        "nome_servidor": server.get("nome_servidor"),
        "temperatura": server.get("temperatura"),
        "is_cache": is_cache
    })
    return dados

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler()
        ]
    )

    servidores = []

    #print("Conectando com servidor {} ..".format(N_SERVER[0]))
    logging.info("Conectando com servidor {} ..".format(N_SERVER[0]))
    servidores.append(conexao_servidor(HOST_1, PORT_1))

    #print("Conectando com servidor {} ..".format(N_SERVER[1]))
    logging.info("Conectando com servidor {} ..".format(N_SERVER[1]))
    servidores.append(conexao_servidor(HOST_2, PORT_2))

    #print("Conectando com servidor {} ..".format(N_SERVER[2]))
    logging.info("Conectando com servidor {} ..".format(N_SERVER[2]))
    servidores.append(conexao_servidor(HOST_3, PORT_3))

    TABELA_CACHE = inicia_cache(servidores)

    #abre socket no modo passivo
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind((HOST_C, PORT_C))
    tcp.listen()

    logging.info('Cache iniciada no IP {} na porta {}'.format(HOST_C, PORT_C))
    conexao, cli = tcp.accept() #aceita conexões
    logging.info('Conexão com Cliente realizada por {}'.format(cli))

    while True:
        #recebe conexões
        dados = []
        msg = conexao.recv(TAM_MSG)
        cmd = msg.decode()
        print()
        if not msg:
            break
        elif cmd == "consultar" or cmd == "CONSULTAR":
            logging.info('Recebeu solicitação...')
            logging.info('Checando temperatura dos Servidores...')
            #realiza a consulta dos três servidores
            for server in TABELA_CACHE:
                dados = consulta(server, dados)
        elif cmd == "consultar 1" or cmd == "CONSULTAR 1":
            logging.info('Recebeu solicitação...')
            logging.info('Checando temperatura do Servidor (1)...')
            server = TABELA_CACHE[0]
            dados = consulta(server, dados)
        elif cmd == "consultar 2" or cmd == "CONSULTAR 2":
            logging.info('Recebeu solicitação...')
            logging.info('Checando temperatura do Servidor (2)...')
            server = TABELA_CACHE[1]
            dados = consulta(server, dados)
        elif cmd == "consultar 3" or cmd == "CONSULTAR 3":
            logging.info('Recebeu solicitação...')
            logging.info('Checando temperatura do Servidor (3)...')
            server = TABELA_CACHE[2]
            dados = consulta(server, dados)

        #envia resposta pro cliente
        conexao.sendall(str(json.dumps(dados)).encode("utf-8"))
        #print()
        logging.info('')
        time.sleep(1)

    logging.info('Encerrando conexão com servidores ...\n')
    servidores[0].close()
    servidores[1].close()
    servidores[2].close()
