import socket
import threading


class Node(threading.Thread):
    instances = []

    @classmethod
    def get_all_keys(cls):
        keys = set()
        for instance in cls.instances:
            keys.update(instance.data.keys())
        return keys

    def __init__(self, host, port, token):
        super().__init__()
        self.host = host
        self.port = port
        self.token = token  
        self.data = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.__class__.instances.append(self)

    def store_data(self, key, value):
        self.data[key] = value

    def retrieve_data(self, key):
        return self.data.get(key, None)

    def run(self):
        self.server.listen(5)
        print(f'Node listening on {self.host}:{self.port}')
        while True:
            if self.server.fileno() == -1:
                break
            client, addr = self.server.accept()
            data = client.recv(1024).decode()
            received_token, key, value = data.split(':', 2)
            if received_token != self.token:
                client.send('Invalid token'.encode())
                client.close()
                continue  # interrompe a execução atual do loop
            if value == '':
                # Se o valor for vazio, então está tentando recuperar dados.
                result = self.retrieve_data(key)
                if result:
                    client.send(result.encode())
                else:
                    client.send('Key not found'.encode())
            else:
                # Caso contrário, está armazenando dados.
                self.store_data(key, value)
                client.send(f'Stored {key}:{value} on {self.host}:{self.port}'.encode())
            client.close()

class DistributedFileSystem:
    def __init__(self):
        self.nodes = []
        self.data = {}  # Armazena os dados aqui para redistribuição

    def add_node(self, node):
        node.start()  # Inicia o servidor Node em uma nova thread.
        self.nodes.append((node.host, node.port))
        self.redistribute_data(node.token)  # Redistribui os dados sempre que um novo nó é adicionado.

    def distribute_data(self, token, key, value):
        self.data[key] = value  # Armazena os dados aqui para redistribuição
        self.redistribute_data(token)  # Redistribui os dados sempre que novos dados são inseridos

    def redistribute_data(self, token):
        for key, value in self.data.items():
            host, port = self.nodes[hash(key) % len(self.nodes)]
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.send(f'{token}:{key}:{value}'.encode())
                response = s.recv(1024).decode()
                print(response)

    def retrieve_data(self, token, key):
        # Recupera os dados do primeiro nó que os possui.
        for host, port in self.nodes:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.send(f'{token}:{key}:'.encode())  # Envia uma chave com valor vazio para recuperar dados.
                data = s.recv(1024).decode()
                if data != 'Key not found':
                    return data