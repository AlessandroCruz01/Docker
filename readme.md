# Docker

# Conceitos Básicos

## O que é Docker?
Docker é uma plataforma que permite criar, executar e distribuir aplicações em ambientes isolados chamados containers.

Em vez de instalar tudo diretamente no seu sistema operacional (linguagem, dependências, banco, servidor etc.), você empacota a aplicação com tudo que ela precisa para rodar.

Vantagens principais:
- Portabilidade: roda igual no computador do desenvolvedor, no servidor e na nuvem.
- Consistência: evita o problema "na minha máquina funciona".
- Rapidez: inicialização de containers é muito mais rápida que uma máquina virtual.

Exemplo simples:
- Você cria uma API em Node.js.
- Com Docker, essa API roda da mesma forma em qualquer máquina que tenha Docker instalado.

## Porque não uma VM?
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

## O que são Containers?
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

## O que são Imagens em Docker?
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

## Imagem vs Container
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

## Arquitetura
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