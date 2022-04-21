#----------------------------------------------------------------------------------------------
#               Arquivo: cliente.py
#----------------------------------------------------------------------------------------------
#               Autores: Bruno Eduardo Farias GRR20186715
#                        Jackson Rossi Borguezani GRR20176573
#         Atualizado em: [21/04/2022, 00h45]
#----------------------------------------------------------------------------------------------
#           Implementa o Cliente
#----------------------------------------------------------------------------------------------

import socket
import json
import time
from cache import HOST_C, PORT_C, TAM_MSG, N_SERVER

#cria a conexão com a cache
def conexao_cache(host, port):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    destino = (host, port)
    cliente.connect(destino)

    time.sleep(1)
    return cliente

#imprime para o cliente na tela a temperatura
def imprime_temperatura(temp):
    print('\n\t-----------------------------------------------------')
    print('\tServidor\t\tTemperatura\t\tCache')
    print('\t-----------------------------------------------------')
    for s in temp:
        print("\t{}:\t{:>5}°C\t\t\t{}".format(s.get("nome_servidor"), s.get("temperatura"), s.get("is_cache")))
    print('\t-----------------------------------------------------')
#envia solicitação, recebe e imprime
def envia_recebe_imprime(cmd):

    #cliente.sendall(b"consultar")
    cliente.send(str(cmd).encode())

    #recebe as temperaturas
    temp = cliente.recv(TAM_MSG)
    temp = json.loads(temp.decode("utf-8"))

    #imprime a temperatura
    imprime_temperatura(temp)
    print()


if __name__ == "__main__":
    pass
    cliente = conexao_cache(HOST_C, PORT_C)

    print('\n============================================================================')
    print('Para checar as temperaturas digite:\n')
    print('\tconsultar \t= Consulta a temperatura dos 3 servidores')
    print('\tconsultar <i> \t= Consulta a temperatura do servidor i = {1, 2 ou 3}')
    print('\tctrl+x e Enter \t= Sair')
    print('\nServidores Disponíveis:\n(1) {} \n(2) {} \n(3) {}'.format(N_SERVER[0], N_SERVER[1], N_SERVER[2]))
    print('============================================================================\n')
    #print('---------------------------------------------')
    print('> Comando:')

    mensagem = input()

    #trata mensagens do usuário até chegar CTRL+X e ENTER
    while mensagem != '\x18':
        if mensagem == 'CONSULTAR' or mensagem == 'consultar':
            print("\nChecando temperatura dos Servidores...")
            #envia solicitação de temperaturas pra cache, recebe e imprime
            envia_recebe_imprime(mensagem)

        elif mensagem == 'CONSULTAR 1' or mensagem == 'consultar 1':
            print("\nChecando temperatura do Servidor (1)...")
            #envia solicitação de temperaturas pra cache, recebe e imprime
            envia_recebe_imprime(mensagem)

        elif mensagem == 'CONSULTAR 2' or mensagem == 'consultar 2':
            print("\nChecando temperatura do Servidor (2)...")
            #envia solicitação de temperaturas pra cache, recebe e imprime
            envia_recebe_imprime(mensagem)

        elif mensagem == 'CONSULTAR 3' or mensagem == 'consultar 3':
            print("\nChecando temperatura do Servidor (3)...")
            #envia solicitação de temperaturas pra cache, recebe e imprime
            envia_recebe_imprime(mensagem)

        else:
            print('\nEntre com um comando válido\n')
            print('\tconsultar \t= Consulta a temperatura dos 3 servidores')
            print('\tconsultar <i> \t= Consulta a temperatura do servidor i = {1, 2 ou 3}')
            print('\tctrl+x e Enter \t= Sair\n')

        print('> Comando:')
        mensagem = input()

    print('Encerrando conexão...\n')
    cliente.close()
