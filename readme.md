# Docker

## Conceitos Básicos

### O que é Docker?
Docker é uma plataforma que permite criar, executar e distribuir aplicações em ambientes isolados chamados containers.

Em vez de instalar tudo diretamente no seu sistema operacional (linguagem, dependências, banco, servidor etc.), você empacota a aplicação com tudo que ela precisa para rodar.

Vantagens principais:
- Portabilidade: roda igual no computador do desenvolvedor, no servidor e na nuvem.
- Consistência: evita o problema "na minha máquina funciona".
- Rapidez: inicialização de containers é muito mais rápida que uma máquina virtual.

Exemplo simples:
- Você cria uma API em Node.js.
- Com Docker, essa API roda da mesma forma em qualquer máquina que tenha Docker instalado.

### Porque não uma VM?
VM (Máquina Virtual) e Docker isolam aplicações, mas de formas diferentes.

Diferença central:
- VM virtualiza o hardware e carrega um sistema operacional completo para cada máquina virtual.
- Docker compartilha o kernel do sistema host e isola apenas processos.

Comparação rápida:
- Tamanho:
	- VM: geralmente GBs.
	- Container: geralmente MBs.
- Inicialização:
	- VM: segundos ou minutos.
	- Container: milissegundos ou poucos segundos.
- Uso de recursos:
	- VM: maior consumo de RAM/CPU.
	- Container: mais leve.

Quando usar VM:
- Quando você precisa de isolamento total de sistema operacional.
- Quando precisa rodar SOs diferentes no mesmo host (ex.: Linux e Windows completos).

Quando usar Docker:
- Desenvolvimento de aplicações.
- Microsserviços.
- CI/CD e deploy rápido.

### O que são Containers?
Container é uma instância em execução de uma imagem Docker.

Pense assim:
- Imagem = receita.
- Container = prato pronto feito a partir da receita.

Características:
- Isolado: tem seu próprio processo, rede e sistema de arquivos (em camadas).
- Efêmero por padrão: se você remove o container, os dados internos podem ser perdidos (a menos que use volumes).
- Reproduzível: vários containers podem ser criados da mesma imagem.

Exemplo de comando:
```bash
docker run -d --name meu-nginx -p 8080:80 nginx
```
O que esse comando faz:
- `-d`: executa em segundo plano.
- `--name meu-nginx`: nome do container.
- `-p 8080:80`: porta 8080 do host aponta para a 80 do container.
- `nginx`: imagem usada.

### O que são Imagens em Docker?
Imagem Docker é um pacote imutável com tudo que a aplicação precisa para rodar:
- Código.
- Runtime (ex.: Node, Java, Python).
- Bibliotecas e dependências.
- Configurações básicas.

Imagens são criadas normalmente a partir de um arquivo `Dockerfile`.

Exemplo de `Dockerfile` (Node.js):
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

Depois, você gera a imagem com:
```bash
docker build -t minha-api:1.0 .
```

### Imagem vs Container
Diferença direta:
- Imagem: molde estático, somente leitura.
- Container: execução da imagem, com estado em tempo de execução.

Analogia:
- Imagem = classe.
- Container = objeto instanciado da classe.

Na prática:
- Você pode ter 1 imagem e 10 containers rodando a partir dela.
- Se um container parar, a imagem continua existindo.
- Alterações feitas dentro de um container em execução nao alteram a imagem original automaticamente.

Exemplo:
```bash
docker pull redis
docker run -d --name redis-1 redis
docker run -d --name redis-2 redis
```
Aqui, dois containers (`redis-1` e `redis-2`) usam a mesma imagem (`redis`).

### Arquitetura
Componentes principais da arquitetura Docker:

1. Docker Client
- Interface usada pelo usuario (comando `docker ...`).

2. Docker Daemon (`dockerd`)
- Servico que executa no host e gerencia imagens, containers, redes e volumes.

3. Docker Engine
- Conjunto Client + Daemon + API.

4. Docker Registry
- Repositorio de imagens.
- Exemplo publico: Docker Hub.
- Exemplo privado: registry interno da empresa.

5. Objetos Docker
- Imagens.
- Containers.
- Volumes (persistencia de dados).
- Networks (comunicacao entre containers).

Fluxo basico:
1. Usuario executa `docker run nginx` no Client.
2. Client envia a solicitacao para o Daemon.
3. Se a imagem nao existir localmente, o Daemon baixa do Registry.
4. O Daemon cria e inicia o container.

Exemplo com volume e rede:
```bash
docker network create app-net
docker volume create db-data

docker run -d --name banco --network app-net -v db-data:/var/lib/mysql mysql:8
docker run -d --name api --network app-net -p 3000:3000 minha-api:1.0
```
Nesse caso:
- `app-net` permite comunicacao entre `api` e `banco`.
- `db-data` persiste dados do banco mesmo que o container seja recriado.

## Uso Básico do Docker

### Hello World com Docker
O teste mais comum para verificar se o Docker está funcionando é executar a imagem `hello-world`.

Comando:
```bash
docker run hello-world
```

O que acontece:
- O Docker procura a imagem `hello-world` localmente.
- Se não encontrar, baixa do Docker Hub.
- Cria um container, executa uma mensagem e encerra.

Resultado esperado:
- Você verá um texto confirmando que o Docker instalou e executou corretamente.

### Comando ***Run***
O comando `docker run` cria e inicia um container a partir de uma imagem.

Estrutura básica:
```bash
docker run [opcoes] imagem [comando]
```

Exemplos úteis:
```bash
docker run ubuntu echo "Ola, Docker"
docker run -it ubuntu bash
docker run --name meu-container nginx
```

Principais opções:
- `--name`: define um nome para o container.
- `-it`: modo interativo com terminal.
- `-d`: executa em segundo plano (daemon).
- `-p`: mapeia portas do host para o container.
- `--rm`: remove o container automaticamente ao encerrar.

Exemplo completo:
```bash
docker run -d --name web -p 8080:80 nginx
```
Esse comando inicia o Nginx em background e expõe no navegador em `http://localhost:8080`.

### Comando ***Run*** SEMPRE CRIA UM NOVO CONTAINER
Esse é um ponto muito importante no Docker:

- Sempre que você usa `docker run`, o Docker cria um novo container a partir da imagem.
- Mesmo que a imagem seja a mesma, o container criado terá outro ID (e possivelmente outro nome, se você não definir).

Exemplo:
```bash
docker run --name teste-nginx -d nginx
docker run --name teste-nginx-2 -d nginx
docker ps -a
```
Resultado:
- Você terá dois containers diferentes (`teste-nginx` e `teste-nginx-2`) criados da mesma imagem `nginx`.

Se a ideia for reutilizar um container já existente, não use `run` novamente.

Use estes comandos:
- `docker start <nome-ou-id>`: inicia um container já criado e parado.
- `docker exec -it <nome-ou-id> bash`: entra em um container que já está em execução.

Exemplo de reutilização correta:
```bash
docker run --name app -d nginx
docker stop app
docker start app
docker exec -it app sh
```

Resumo rápido:
- `docker run` = cria + inicia um container novo.
- `docker start` = inicia um container existente.
- `docker exec` = executa comando dentro de um container em execução.

### Dando nomes para Containers
Por padrão, o Docker gera nomes aleatórios (ex.: `happy_turing`).
Para facilitar o dia a dia, é melhor definir nomes explícitos com `--name`.

Exemplo:
```bash
docker run -d --name api-nginx -p 8081:80 nginx
```

Vantagens de nomear containers:
- Fica mais fácil identificar o que cada container faz.
- Simplifica comandos de gerenciamento (`stop`, `start`, `logs`, `exec`).
- Evita trabalhar com IDs longos.

Exemplos de uso com nome:
```bash
docker stop api-nginx
docker start api-nginx
docker logs api-nginx
docker exec -it api-nginx sh
```

Regras importantes:
- O nome deve ser único no Docker local.
- Se tentar reutilizar um nome já existente, o Docker retorna erro.

Exemplo de erro comum:
```bash
docker run --name api-nginx -d nginx
# erro: Conflict. The container name "/api-nginx" is already in use...
```

Como resolver:
1. Remover o container antigo e criar outro com o mesmo nome.
```bash
docker rm -f api-nginx
docker run --name api-nginx -d nginx
```

2. Ou renomear um container existente.
```bash
docker rename api-nginx api-nginx-old
docker run --name api-nginx -d nginx
```

Boa prática de nomenclatura:
- Use nomes descritivos e consistentes, como:
	- `api-prod`
	- `db-mysql`
	- `redis-cache`

### Portas dos Containers
Containers têm portas internas. Para acessar de fora, você precisa mapear com `-p`.

Sintaxe:
```bash
docker run -p PORTA_HOST:PORTA_CONTAINER imagem
```

Exemplo:
```bash
docker run -d --name app-web -p 3000:80 nginx
```

Interpretação:
- `3000` = porta no seu computador.
- `80` = porta dentro do container.

Teste rápido:
- Abra `http://localhost:3000` no navegador.

Dica:
- Para listar mapeamentos de portas: `docker ps`.

### Servidor Web em background
Rodar em background significa deixar o container executando sem travar o terminal.

Comando:
```bash
docker run -d --name site -p 8080:80 nginx
```

Verificando se está rodando:
```bash
docker ps
```

Ver logs do container:
```bash
docker logs site
```

Parar o container:
```bash
docker stop site
```

### Manipulação de Containers em modo Daemon
No dia a dia, você vai iniciar, parar e remover containers em modo daemon (`-d`).

Fluxo comum:
```bash
docker run -d --name minha-api -p 5000:5000 python:3.12-slim sleep infinity
docker ps
docker stop minha-api
docker start minha-api
docker restart minha-api
docker rm -f minha-api
```

Comandos essenciais:
- `docker ps`: lista containers em execução.
- `docker ps -a`: lista todos, inclusive parados.
- `docker stop`: para com segurança.
- `docker start`: inicia um container parado.
- `docker rm`: remove container parado.
- `docker rm -f`: força parada e remoção.

### Nova sintaxe do Docker Client
Nas versões mais novas, o Docker adotou comandos agrupados por tipo de objeto.

Exemplos de equivalência:
- Antigo: `docker ps`
- Novo: `docker container ls`

- Antigo: `docker images`
- Novo: `docker image ls`

- Antigo: `docker rm <id>`
- Novo: `docker container rm <id>`

- Antigo: `docker rmi <imagem>`
- Novo: `docker image rm <imagem>`

Vantagem da nova sintaxe:
- Fica mais organizada e mais fácil de memorizar, porque separa por contexto (`container`, `image`, `network`, `volume`).

Exemplos práticos:
```bash
docker container ls
docker image ls
docker network ls
docker volume ls
```