#
# TRABALHO REDES II
# JACKSON ROSSI BORGUEZANI - GRR20176573
# BRUNO EDUARDO FARIAS - GRR20186715
#
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
    #print('\n> Iniciando Tabela Cache')
    logging.info('\n> Iniciando Tabela Cache')
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

    #print(':: Obteve a temperatura {} do servidor {}'.format(temp, server.get("nome_servidor")))
    logging.info(':: Obteve a temperatura {} ºC do servidor {}'.format(temp, server.get("nome_servidor")))

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
    #print("update: s {}, temp {}", TABELA_CACHE[server_u.get("id")].get("id"), TABELA_CACHE[server_u.get("id")].get("temperatura"))

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

    #print('\nCache Iniciada no IP', HOST_C, 'na porta', PORT_C)
    logging.info('Cache iniciada no IP {} na porta {}'.format(HOST_C, PORT_C))
    conexao, cli = tcp.accept() #aceita conexões

    while True:
        #recebe conexões
        msg = conexao.recv(TAM_MSG)
        if not msg:
            break
        else:
            logging.info('\n\n\nRecebeu conexão...')
            dados = []
            #print("\n> Checando temperatura do Servidor... Hora atual: {}\n".format(datetime.now().time()))
            logging.info('Checando temperatura do Servidor...')
            for server in TABELA_CACHE:
                #em_cache = True
                #se está em cache e com timestamp válido (dentro dos 30s)
                if dados_validos(server):
                    #print('{} : Dados em cache válidos\n::   {}ºC Horário: {}'.format(server.get("nome_servidor"), server.get("temperatura"), server.get("timestamp")))
                    logging.info('{} : Dados em cache válidos\n::   {}ºC Timestamp do dado na cache: {}'.format(server.get("nome_servidor"), server.get("temperatura"), server.get("timestamp")))
                    is_cache = True
                else:
                    if server.get("inicializado"):
                        #print('{} : Dados em cache expirados (última atualização: {})\n:: Solicitando temperatura do servidor'.format(server.get("nome_servidor"), server.get("timestamp")))
                        logging.info('{} : Dados em cache expirados (última atualização: {})\n:: Solicitando temperatura do servidor'.format(server.get("nome_servidor"), server.get("timestamp")))
                    else:
                        #print('{} : Dados em cache expirados \n:: Solicitando temperatura do servidor'.format(server.get("nome_servidor")))
                        logging.info('{} : Dados em cache expirados \n:: Solicitando temperatura do servidor'.format(server.get("nome_servidor")))

                    #solicita temperatura e atualiza cache
                    server_up = solicita_temp(server)
                    atualiza_cache(server_up)
                    server = server_up
                    is_cache = False

                #json para ser enviado ao cliente
                dados.append({
                    "nome_servidor": server.get("nome_servidor"),
                    "temperatura": server.get("temperatura"),
                    "is_cache": is_cache
                })

        #envia resposta pro cliente
        conexao.sendall(str(json.dumps(dados)).encode("utf-8"))
        #print()
        logging.info('')
        time.sleep(1)


    #print('> Encerrando conexão com servidores ...\n')
    logging.info('> Encerrando conexão com servidores ...\n')
    servidores[0].close()
    servidores[1].close()
    servidores[2].close()
