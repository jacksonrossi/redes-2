# Trabalho prático Redes 2 - Tabela Cache

### Descrição do trabalho

Você tem 3 servidores de temperatura em lugares extremos do mundo: ou normalmente muito frios ou normalmente muito quentes. Cada um destes servidores recebem uma resposta e simplemente mandam uma resposta com um número inteiro que mais se aproxima da temperatura medida.
Um cliente não acessa os servidores individualmente, e sim uma cache que mantém os últimos valores recebidos dos 3 servidores. Assim evitamos que o cliente tenha que fazer 3 acessos muito distantes, para fazer 1 acesso mais próximo.
A cache mantém uma tabela cache com os dados, com um prazo de validade para cada entrada de 30 segundos. Implemente o cliente. Implemente também a tabela cache da maneira eficiente que foi apresentada em sala de aula. Quando chega uma requisição e algum valor expirou, deve ser feita nova consulta ao servidor original.
Para os 3 servidores, a dupla pode tanto implementá-los como servidores do trabalho, utilizando número aleatórios dentro de uma faixa razoável para os valores de temperatura ou, alternativamente, obter as informações adequadamente na Web.
Devem ser apresentados logs para múltiplas execuções. Mostre com clareza situações em que uma requisição de usuário encontra/não encontra a cache com informações válidas.


### Como executar

Digite os seguintes comandos em terminais individuais:

```bash
$ python3 servidor_1.py
```
```bash
$ python3 servidor_2.py
```
```bash
$ python3 servidor_3.py
```
```bash
$ python3 cache.py
```
```bash
$ python3 cliente.py
```
Para realizar a consulta da temperatura, na interface do cliente, utilize:
- Consultar a temperatura de todos os servidores
```bash
> consultar
```
- Consultar a temperatura de um servidor específico
```bash
> consultar <i>
```
Por exemplo, consultar o servidor 1
```bash
> consultar 1
```
