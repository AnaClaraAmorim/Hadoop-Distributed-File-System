from distributed import DistributedFileSystem, Node
import random

class Client:
    def __init__(self, dfs, token):
        self.dfs = dfs
        self.token = token

    def put(self, token, filename):
        with open(filename, 'r') as file:
            data = file.read()
        self.dfs.distribute_data(token, filename, data)

    def get(self, token, filename):
        data = self.dfs.retrieve_data(token, filename)
        if data is None:
            print(f'O arquivo {filename} não foi encontrado.')
        else:
            with open(filename, 'w') as file:
                file.write(data)
            print(f'Arquivo {filename} recebido com sucesso.')

    def ls(self):
        keys = Node.get_all_keys()
        print('Arquivos disponíveis:')
        for key in keys:
            print(key)

    def exit(self):
        pass  

def main():
    dfs = DistributedFileSystem()

    port = random.randint(5000, 9999)
    
    dfs.add_node(Node('localhost', port, 'materia_distribuidos'))

    client = Client(dfs, 'materia_distribuidos')

    while True:
        command = input('> ').split()
        if not command:
            continue

        if command[0] == 'put' and len(command) == 3:
            client.put(command[1], command[2])
        elif command[0] == 'get' and len(command) > 2:
            client.get(command[1], command[2])  
        elif command[0] == 'ls':
            client.ls()
        elif command[0] == 'exit':
            break
        else:
            print(f'Comando desconhecido: {command[0]}')

if __name__ == '__main__':
    main()