# Hadoop-Distributed-File-System

A implementação deste Sistema de Arquivos Distribuído (DFS) consiste em três arquivos Python: distributed.py, client.py e test.py. Segue abaixo a descrição de como preparar o ambiente, instalar e executar o sistema:

Pré-requisitos:

Certifique-se de que o Python 3.6 ou superior esteja instalado no seu sistema. Você pode verificar isso através do comando no terminal:

python --version

Execução:

Inicie o DFS, abrindo um terminal e navegando até o diretório onde você colocou os arquivos. Depois, execute o script client.py com o seguinte comando:

python client.py

Depois de inicializar o client.py, você verá um prompt de comando (>), onde pode inserir os seguintes comandos:

put [token] [filename]: Carrega o conteúdo do arquivo especificado para o sistema.
get [token] [filename]: Recupera o arquivo especificado do sistema.
ls: Lista todos os arquivos disponíveis no sistema.
exit: Fecha o sistema DFS.

Teste:

Você pode testar a implementação executando o script test.py com o seguinte comando:

python test.py

O script test.py executa testes unitários para verificar se o armazenamento e a recuperação de dados estão funcionando corretamente.
