import socket
import json
import time
from cache import HOST_C, PORT_C, TAM_MSG

def conexao_cache(host, port):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    destino = (host, port)
    cliente.connect(destino)

    time.sleep(1)
    return cliente

def imprime_temperatura(temp):
    print('\n-------------------------------------------------------')
    print('Servidor\t\tTemperatura\t\tCache')
    print('-------------------------------------------------------')
    for s in temp:
        print("{}:\t{:>5}°C\t\t\t{}".format(s.get("nome_servidor"), s.get("temperatura"), s.get("is_cache")))
    print('-------------------------------------------------------')

if __name__ == "__main__":
    pass
    cliente = conexao_cache(HOST_C, PORT_C)

    print('\nDigite CONSULTA para checar as temperaturas')
    print('Para sair use CTRL+X e em seguida Enter')
    print('_____________________________________________\n')
    #print('---------------------------------------------')
    print('> Comando:')

    mensagem = input()

    while mensagem != '\x18':
        if mensagem == 'CONSULTA' or mensagem == 'consulta':
            print("\nChecando temperatura do Servidor...")
            cliente.sendall(b"Get Temp")

            temp = cliente.recv(TAM_MSG)
            temp = json.loads(temp.decode("utf-8"))

            imprime_temperatura(temp)

            print()
            #time.sleep(1)
        else:
            print('Entre com um comando válido')

        print('> Comando:')
        mensagem = input()

    print('Encerrando conexão...\n')
    cliente.close()
