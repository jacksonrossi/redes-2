import socket
import time
from random import randrange
from datetime import datetime, timedelta
from servidor_1 import HOST as HOST_1, PORT as PORT_1, NAME as NAME_1
from servidor_2 import HOST as HOST_2, PORT as PORT_2, NAME as NAME_2
from servidor_3 import HOST as HOST_3, PORT as PORT_3, NAME as NAME_3

TAM_MSG = 1024    #em bytes
TABELA_CACHE = []
DURACAO = 30    #em segundos
N_SERVER = [NAME_1, NAME_2, NAME_3]

def conexao_servidor(host, port):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    destino = (host, port)
    cliente.connect(destino)

    time.sleep(1)
    return cliente

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

def inicia_cache(servidores):
    print('\n****Iniciando Tabela Cache***\n')
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

def dados_validos(server):
    tempo_atual = datetime.now()
    tempo_cache = server.get("timestamp")
    if server.get("inicializado") and tempo_atual <= tempo_cache + timedelta(seconds=DURACAO):
        return True
    else:
        return False

def solicita_temp(server):
    conexao = server.get("conexao")

    conexao.sendall(b"Solicita temperatura")
    temp = conexao.recv(TAM_MSG)

    temp = temp.decode("utf-8")

    return{
        "id": server.get("id"),
        "nome_servidor": server.get("nome_servidor"),
        "temperatura": temp,
        "timestamp": datetime.now(),
        "inicializado": True,
        "conexao": server.get("conexao")

    }

def atualiza_cache(server, server_u):
    
    #for s in TABELA_CACHE: 
    #    if s.get("id") == server_u.get("id"):
    #        TABELA_CACHE.insert(server.get("id"), server_u)
    TABELA_CACHE[server.get("id")] = server_u

def imprime_temperatura():
    for s in TABELA_CACHE:
        print("Servidor {} está com temperatura em {}°".format(s.get("nome_servidor"), s.get("temperatura")))


if __name__ == "__main__":
    servidores = []

    print("Conectando com servidor {} ..".format(N_SERVER[0]))
    servidores.append(conexao_servidor(HOST_1, PORT_1))

    print("Conectando com servidor {} ..".format(N_SERVER[1]))
    servidores.append(conexao_servidor(HOST_2, PORT_2))

    print("Conectando com servidor {} ..".format(N_SERVER[2]))
    servidores.append(conexao_servidor(HOST_3, PORT_3))

    TABELA_CACHE = inicia_cache(servidores)

    while True:
        temp_servidores = []
        print("> Checando temperatura do Servidor")
        for server in TABELA_CACHE:
            em_cache = True
            if dados_validos(server):
                print('{} : Dados em cache válidos'.format(server.get("nome_servidor")))
            else:
                print('{} : Dados em cache expirados ... Solicitando temperatura do servidor'.format(server.get("nome_servidor")))
                server_up = solicita_temp(server)
                atualiza_cache(server, server_up)

        
        imprime_temperatura()

        print()
        time.sleep(3)

