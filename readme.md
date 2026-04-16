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

### Mapear diretórios para containers
Mapear diretórios permite compartilhar arquivos entre sua máquina e o container.

Isso é muito útil para:
- Desenvolvimento local (editar código no host e refletir no container).
- Persistir dados fora do ciclo de vida do container.
- Compartilhar arquivos de configuração.

Existem 2 formas mais comuns:

1. Bind mount (pasta local -> pasta no container)
- Usa um caminho real da sua máquina.

Exemplo no Windows:
```bash
docker run -d --name site-html -p 8082:80 -v C:/Users/aless/Desktop/Docker/site:/usr/share/nginx/html nginx
```

Nesse exemplo:
- `C:/Users/aless/Desktop/Docker/site` = pasta no host.
- `/usr/share/nginx/html` = pasta dentro do container.
- Tudo que você editar na pasta local aparece no Nginx.

2. Volume nomeado (gerenciado pelo Docker)
- Ideal para dados de banco e persistência de longo prazo.

Exemplo:
```bash
docker volume create dados-mysql
docker run -d --name mysql-db -e MYSQL_ROOT_PASSWORD=123456 -v dados-mysql:/var/lib/mysql mysql:8
```

Nesse caso:
- O Docker gerencia onde os dados ficam no host.
- Mesmo removendo o container, os dados continuam no volume.

Comandos úteis para inspeção:
```bash
docker inspect site-html
docker volume ls
docker volume inspect dados-mysql
```

Resumo rápido:
- Bind mount: melhor para código e arquivos do projeto.
- Volume nomeado: melhor para dados persistentes (ex.: banco de dados).

### Manipulação de Container e modo daemon

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

## Dockerfile e Build de Imagens
### O que é um Dockerfile?
`Dockerfile` é um arquivo de texto com instruções para montar uma imagem Docker personalizada.

Pense nele como uma receita com passos sequenciais:
- Escolher imagem base.
- Copiar arquivos.
- Instalar dependências.
- Definir comando de inicialização.

Exemplo simples (Node.js):
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

### Principais instruções
- `FROM`: define a imagem base.
- `WORKDIR`: define diretório de trabalho dentro da imagem.
- `COPY`: copia arquivos do host para a imagem.
- `RUN`: executa comandos durante o build.
- `EXPOSE`: documenta a porta usada pela aplicação.
- `CMD`: comando padrão executado quando o container inicia.

### Build da imagem
Para gerar uma imagem a partir do `Dockerfile`:

```bash
docker build -t minha-api:1.0 .
```

Detalhes:
- `-t`: aplica nome e tag à imagem.
- `.`: contexto de build (pasta atual).

### Executando a imagem criada
Depois do build:

```bash
docker run -d --name minha-api-container -p 3000:3000 minha-api:1.0
```

### Boas práticas iniciais
- Use imagens base leves, como `alpine`, quando fizer sentido.
- Copie primeiro arquivos de dependências (`package.json`, `requirements.txt`) para aproveitar cache.
- Evite colocar segredos no `Dockerfile`.
- Use `.dockerignore` para não enviar arquivos desnecessários no contexto de build.

## Deixando de ser apenas um usuário

### Diferença entre Container e Imagem
Você já viu essa diferença antes, mas aqui vale fixar com foco em uso profissional:

- Imagem: template imutável, versionável e distribuível.
- Container: processo em execução criado a partir de uma imagem.

O que isso muda na prática:
- Você versiona e compartilha imagem.
- Você inicia, para e remove container.
- Problema de runtime normalmente e investigado no container.
- Problema de empacotamento normalmente e corrigido na imagem (Dockerfile).

Resumo mental:
- Imagem = artefato de entrega.
- Container = instancia de execucao.

### Entendendo melhor as imagens
Uma imagem Docker e formada por camadas (layers). Cada instrucao relevante do Dockerfile cria uma camada.

Exemplo:
- `FROM node:20-alpine` cria a base.
- `COPY package*.json ./` cria nova camada.
- `RUN npm install` cria outra camada.

Vantagens das camadas:
- Reuso de cache no build (mais velocidade).
- Download incremental (menos dados).
- Versionamento mais eficiente.

Comando util para inspecionar historico da imagem:
```bash
docker history minha-api:1.0
```

Comando para ver detalhes tecnicos:
```bash
docker image inspect minha-api:1.0
```

### Comandos básicos de gerenciamento de imagem
Comandos mais usados no dia a dia:

```bash
docker image ls
docker pull nginx:latest
docker image rm nginx:latest
docker image prune
docker tag minha-api:1.0 minha-api:latest
```

O que cada um faz:
- `docker image ls`: lista imagens locais.
- `docker image pull`: baixa imagem de um registry.
- `docker image rm`: remove imagem local.
- `docker image prune`: remove imagens dangling (sem tag em uso).
- `docker image tag`: cria nova tag para a mesma imagem.
- `docker image inspect`: pega informações sobre aquela imagem.
- `docker image build`: gera uma imagem.
- `docker image push`: publicar em um registry local ou em um registry do docker hub.

Boas praticas:
- Prefira tags explicitas em ambiente de producao (ex.: `1.0.3`) em vez de apenas `latest`.
- Limpe imagens nao usadas periodicamente para economizar disco.

### Docker Hub x Docker Registry
Os dois armazenam imagens, mas com objetivos diferentes.

Docker Hub:
- Servico publico oficial mais comum.
- Bom para estudo, projetos abertos e distribuicao simples.

Docker Registry (generico/privado):
- Solucao para hospedar imagens internamente (empresa).
- Controle de acesso, politicas de seguranca e compliance.

Exemplos:
- Publico: `docker.io/library/nginx`
- Privado: `registry.minhaempresa.com/minha-api:1.0`

Regra pratica:
- Projeto pessoal/open-source: Docker Hub.
- Projeto corporativo: registry privado.

### Meu Primeiro build
Vamos criar um primeiro build completo de forma guiada.

Passo 1: criar um `Dockerfile` simples
```dockerfile
FROM nginx:alpine
COPY . /usr/share/nginx/html
```

Passo 2: gerar imagem
```bash
docker build -t meu-site:1.0 .
```

Passo 3: executar container
```bash
docker run -d --name meu-site-container -p 8085:80 meu-site:1.0
```

Passo 4: validar
- Abra `http://localhost:8085`.
- Verifique logs com `docker logs meu-site-container`.

### Uso das instruções de preparação
Instrucoes de preparacao definem base e ambiente inicial da imagem.

Principais:
- `FROM`: define a base.
- `WORKDIR`: define pasta de trabalho.
- `ENV`: define variaveis de ambiente.
- `ARG`: define argumentos de build.

Exemplo:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ARG APP_VERSION=1.0.0
```

Quando usar:
- Sempre no inicio do Dockerfile.
- Para padronizar ambiente antes de copiar codigo ou instalar dependencias.

### Uso das instruções de povoamento
Instrucoes de povoamento colocam arquivos e dependencias dentro da imagem.

Principais:
- `COPY`: copia arquivos do host.
- `ADD`: copia arquivos e permite recursos extras (como URL/tar), mas use com criterio.
- `RUN`: executa comandos de instalacao/configuracao no build.

Exemplo (Node.js):
```dockerfile
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
```

Dica importante de performance:
- Copie primeiro os arquivos de dependencias.
- Execute instalacao.
- Copie o restante do codigo depois.

Isso melhora o cache quando voce altera apenas codigo-fonte.

### Uso das instruções de execução do Container
Essas instrucoes definem como o container se comporta em runtime.

Principais:
- `EXPOSE`: documenta porta da aplicacao.
- `CMD`: comando padrao ao iniciar container.
- `ENTRYPOINT`: comando principal fixo do container.

Exemplo:
```dockerfile
EXPOSE 3000
CMD ["npm", "start"]
```

Diferenca rapida:
- `CMD` pode ser sobrescrito facilmente no `docker run`.
- `ENTRYPOINT` normalmente define o executavel principal da imagem.

Exemplo com sobrescrita de CMD:
```bash
docker run --rm minha-api:1.0 npm test
```

### Enviar imagens para o Docker Hub
Fluxo basico para publicar sua imagem:

1. Fazer login:
```bash
docker login
```

2. Criar tag no formato `usuario/repositorio:tag`:
```bash
docker tag minha-api:1.0 seuusuario/minha-api:1.0
```

3. Enviar para o Hub:
```bash
docker push seuusuario/minha-api:1.0
```

4. Testar pull em outro ambiente:
```bash
docker pull seuusuario/minha-api:1.0
```

Boas praticas de publicacao:
- Use tags semanticas (`1.0.0`, `1.1.0`, `2.0.0`).
- Mantenha um `README` do repositorio no Docker Hub com instrucoes de uso.
- Evite enviar imagem com segredos embutidos.

## Redes

### Visão Geral e Tipos de Redes
Rede Docker define como containers se comunicam entre si e com o mundo externo.

Em termos simples:
- Sem rede: container isolado de qualquer comunicacao.
- Bridge: rede padrao para comunicacao entre containers no mesmo host.
- Host: container compartilha a rede do sistema host.

Comando para listar redes existentes:
```bash
docker network ls
```

Redes padrao normalmente criadas pelo Docker:
- `bridge`: rede default para containers.
- `host`: usa pilha de rede do host.
- `none`: sem interface de rede util para trafego externo.

Comando para inspecionar detalhes de uma rede:
```bash
docker network inspect bridge
```

### Rede Tipo None (Sem Rede)
No modo `none`, o container nao recebe conectividade externa.

Caracteristicas:
- Sem acesso a internet.
- Sem comunicacao com outros containers.
- Util para execucoes isoladas e cenarios de seguranca.

Exemplo:
```bash
docker run --rm --network none alpine ip addr
```

O que observar:
- Geralmente apenas a interface `lo` (loopback) aparece.

Cenario comum:
- Processamento de arquivos locais sem necessidade de rede.

### Rede Tipo Bridge
`bridge` e o tipo mais usado no dia a dia para desenvolvimento local.

Como funciona:
- Cada container recebe um IP interno.
- Containers na mesma rede podem se comunicar.
- Com rede customizada, containers resolvem nomes por DNS interno.

Exemplo rapido com rede bridge customizada:
```bash
docker network create app-net

docker run -d --name api --network app-net nginx
docker run -it --rm --name client --network app-net alpine sh
```

Dentro do `client`, voce pode testar:
```bash
ping api
```

Vantagens da bridge customizada:
- Isolamento entre grupos de containers.
- Descoberta de servicos por nome (`api`, `db`, `redis`).
- Melhor organizacao para ambientes com varios projetos.

Conectar um container em uma rede existente:
```bash
docker network connect app-net meu-container
```

Desconectar:
```bash
docker network disconnect app-net meu-container
```

### Rede Tipo Host
No modo `host`, o container usa diretamente a interface de rede do host.

Implicacoes:
- Nao ha NAT de porta como no `-p` da bridge.
- Menos isolamento de rede.
- Pode ter ganho de performance em alguns cenarios.

Exemplo:
```bash
docker run --rm --network host nginx
```

Importante:
- Em Linux, o comportamento e direto e previsivel.
- Em Docker Desktop (Windows/macOS), o suporte ao modo host pode variar conforme versao e configuracao.

Quando considerar `host`:
- Aplicacoes com requisitos de baixa latencia.
- Ferramentas de monitoramento que precisam enxergar a rede do host.

Resumo pratico:
- `none`: maximo isolamento.
- `bridge`: equilibrio entre isolamento e comunicacao.
- `host`: maximo acesso a rede do host, com menos isolamento.

### Boas Práticas com Redes Docker
- Prefira redes `bridge` customizadas em vez da `bridge` padrao para projetos reais.
- Evite expor portas desnecessarias com `-p`.
- Mantenha containers do mesmo contexto na mesma rede (ex.: `frontend`, `api`, `db`).
- Use nomes de containers servico-orientados (`api`, `postgres`, `redis`) para facilitar DNS interno.
- Inspecione redes regularmente para diagnostico: `docker network inspect <nome-da-rede>`.

### Exemplo Completo: API + Banco na Mesma Rede
```bash
docker network create projeto-net

docker run -d \
	--name postgres \
	--network projeto-net \
	-e POSTGRES_PASSWORD=123456 \
	postgres:16

docker run -d \
	--name api \
	--network projeto-net \
	-p 3000:3000 \
	minha-api:1.0
```

Nesse cenario:
- A API pode acessar o banco usando `postgres` como host.
- Apenas a API expoe porta para fora.
- O banco permanece acessivel somente dentro da rede interna.

## Coordenando Múltiplos Containers

### Introdução
Gerenciar um único container é simples. O desafio real aparece quando sua aplicação é composta por múltiplos serviços: API, banco de dados, cache, fila de mensagens, etc.

Problemas comuns sem orquestração:
- Subir e parar cada container manualmente é trabalhoso e propenso a erros.
- Garantir a ordem de inicialização (banco antes da API, por exemplo) é difícil.
- Recriar o ambiente em outra máquina exige repetir todos os comandos.

A solução para esse problema é o **Docker Compose**.

Docker Compose permite descrever toda a infraestrutura de um projeto em um único arquivo `compose.yaml` (ou `docker-compose.yml`) e gerenciar tudo com comandos simples.

### Gerenciamento de Micro-Service
Em arquiteturas de microsserviços, cada serviço é uma aplicação independente com sua própria responsabilidade:
- Serviço de autenticação.
- Serviço de pagamentos.
- Serviço de notificações.
- Etc.

Cada um deles pode rodar em seu próprio container, com sua própria imagem, porta e configuração.

Desafios do gerenciamento:
- Como garantir que todos sobem juntos?
- Como fazer um serviço encontrar o outro pela rede?
- Como compartilhar variáveis de ambiente de forma organizada?

Docker Compose resolve esses problemas ao definir todos os serviços, redes e volumes em um único arquivo declarativo.

### Docker Compose

#### O que é Docker Compose?
Docker Compose é uma ferramenta para definir e executar aplicações com múltiplos containers.

Com um único arquivo `compose.yaml`, você descreve:
- Quais serviços existem.
- Como cada um deve ser construído ou qual imagem usar.
- Quais portas expor.
- Quais volumes e redes usar.
- Variáveis de ambiente.
- Dependências entre serviços.

#### Estrutura básica do compose.yaml
```yaml
services:
  nome-do-servico:
    image: imagem:tag
    ports:
      - "PORTA_HOST:PORTA_CONTAINER"
    environment:
      - VARIAVEL=valor
    volumes:
      - nome-volume:/caminho/no/container
    depends_on:
      - outro-servico

volumes:
  nome-volume:
```

#### Exemplo completo: API + PostgreSQL + Redis
```yaml
services:
  api:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://user:senha@postgres:5432/appdb
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:16
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=senha
      - POSTGRES_DB=appdb
    volumes:
      - dados-postgres:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  dados-postgres:
```

Nesse exemplo:
- `api` depende de `postgres` e `redis` (sobe depois deles).
- `postgres` persiste dados em um volume nomeado.
- Todos os serviços se comunicam pelo nome do serviço (`postgres`, `redis`) como hostname, pois o Compose cria automaticamente uma rede interna.

#### Comandos principais do Docker Compose
```bash
# Subir todos os serviços em background
docker compose up -d

# Ver status dos serviços
docker compose ps

# Ver logs de todos os serviços
docker compose logs

# Ver logs de um serviço específico
docker compose logs api

# Parar e remover containers
docker compose down

# Parar e remover containers + volumes
docker compose down -v

# Reconstruir imagens antes de subir
docker compose up -d --build

# Reiniciar um serviço específico
docker compose restart api

# Executar comando dentro de um serviço em execução
docker compose exec api sh
```

#### depends_on e ordem de inicialização
A opção `depends_on` garante que um serviço só inicia após os serviços listados estarem no estado `started`.

Atenção importante:
- `depends_on` não garante que o serviço dependente está *pronto* para receber conexões, apenas que o container iniciou.
- Para aguardar o serviço estar realmente disponível, use `healthcheck` combinado com `condition: service_healthy`.

Exemplo com healthcheck:
```yaml
services:
  api:
    build: .
    depends_on:
      postgres:
        condition: service_healthy

  postgres:
    image: postgres:16
    environment:
      - POSTGRES_PASSWORD=senha
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
```

#### Variáveis de ambiente com arquivo .env
Em vez de declarar variáveis diretamente no `compose.yaml`, você pode usar um arquivo `.env` na mesma pasta.

Arquivo `.env`:
```
POSTGRES_USER=user
POSTGRES_PASSWORD=minhasenha
POSTGRES_DB=appdb
```

`compose.yaml` referenciando o `.env`:
```yaml
services:
  postgres:
    image: postgres:16
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
```

Boas práticas:
- Adicione `.env` ao `.gitignore` para não vazar senhas no repositório.
- Mantenha um `.env.example` com os nomes das variáveis (sem os valores reais) para documentação.

#### Boas Práticas com Docker Compose
- Prefira `compose.yaml` como nome do arquivo (padrão mais recente).
- Sempre defina volumes nomeados para dados persistentes (bancos de dados, uploads).
- Use redes customizadas se precisar isolar grupos de serviços.
- Utilize `healthcheck` para serviços críticos como bancos de dados.
- Não coloque segredos diretamente no `compose.yaml`; use variáveis de ambiente ou secrets.
- Mantenha o `compose.yaml` versionado junto ao código do projeto.

## Projeto de Cadastro Simples

### Estrutura Inicial
Vamos construir um projeto simples de cadastro de usuários utilizando Docker Compose. O objetivo é aplicar na prática os conceitos vistos até aqui: Dockerfile, volumes, redes e orquestração com Compose.

Tecnologias usadas:
- **Backend**: Node.js com Express.
- **Banco de dados**: PostgreSQL.
- **Frontend**: HTML estático servido pelo Nginx.

Estrutura de pastas do projeto:
```
cadastro/
├── backend/
│   ├── Dockerfile
│   ├── package.json
│   └── index.js
├── frontend/
│   └── index.html
└── compose.yaml
```

Arquivo `backend/index.js` — API simples de cadastro:
```js
const express = require('express');
const { Pool } = require('pg');

const app = express();
app.use(express.json());

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

app.get('/usuarios', async (req, res) => {
  const result = await pool.query('SELECT * FROM usuarios ORDER BY id');
  res.json(result.rows);
});

app.post('/usuarios', async (req, res) => {
  const { nome, email } = req.body;
  const result = await pool.query(
    'INSERT INTO usuarios (nome, email) VALUES ($1, $2) RETURNING *',
    [nome, email]
  );
  res.status(201).json(result.rows[0]);
});

app.listen(3000, () => console.log('API rodando na porta 3000'));
```

Arquivo `backend/package.json`:
```json
{
  "name": "cadastro-api",
  "version": "1.0.0",
  "main": "index.js",
  "dependencies": {
    "express": "^4.18.2",
    "pg": "^8.11.3"
  }
}
```

Arquivo `backend/Dockerfile`:
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["node", "index.js"]
```

Arquivo `frontend/index.html` — formulário de cadastro:
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Cadastro</title>
</head>
<body>
  <h1>Cadastro de Usuários</h1>
  <form id="form">
    <input type="text" id="nome" placeholder="Nome" required>
    <input type="email" id="email" placeholder="Email" required>
    <button type="submit">Cadastrar</button>
  </form>
  <ul id="lista"></ul>

  <script>
    const API = 'http://localhost:3000';

    async function carregarUsuarios() {
      const res = await fetch(`${API}/usuarios`);
      const usuarios = await res.json();
      document.getElementById('lista').innerHTML =
        usuarios.map(u => `<li>${u.nome} — ${u.email}</li>`).join('');
    }

    document.getElementById('form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const nome = document.getElementById('nome').value;
      const email = document.getElementById('email').value;
      await fetch(`${API}/usuarios`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome, email }),
      });
      e.target.reset();
      carregarUsuarios();
    });

    carregarUsuarios();
  </script>
</body>
</html>
```

### Configurando ambiente com Docker Compose
Com a estrutura criada, o próximo passo é orquestrar todos os serviços com o `compose.yaml`.

Arquivo `compose.yaml`:
```yaml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: cadastro
      POSTGRES_PASSWORD: senha123
      POSTGRES_DB: cadastrodb
    volumes:
      - dados-postgres:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U cadastro"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgres://cadastro:senha123@postgres:5432/cadastrodb
    depends_on:
      postgres:
        condition: service_healthy

  frontend:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./frontend:/usr/share/nginx/html:ro

volumes:
  dados-postgres:
```

O que cada parte faz:
- `postgres`: banco de dados com volume persistente e healthcheck.
- `backend`: API Node.js que só sobe após o banco estar pronto.
- `frontend`: Nginx servindo o HTML estático via bind mount.

Inicializando o banco de dados:
Antes de usar a API, é necessário criar a tabela `usuarios`. Uma forma simples é executar o comando após os containers estarem de pé:

```bash
docker compose up -d

docker compose exec postgres psql -U cadastro -d cadastrodb -c \
  "CREATE TABLE IF NOT EXISTS usuarios (id SERIAL PRIMARY KEY, nome TEXT NOT NULL, email TEXT NOT NULL);"
```

Verificando se tudo subiu corretamente:
```bash
docker compose ps
docker compose logs backend
```

### Finalizando Cadastro
Com tudo configurado, o projeto está pronto para uso.

Testando pelo navegador:
- Acesse `http://localhost:8080` para ver o formulário.
- Preencha nome e email e clique em **Cadastrar**.
- A lista de usuários é atualizada automaticamente.

Testando a API diretamente:
```bash
# Cadastrar usuário
curl -X POST http://localhost:3000/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nome": "João", "email": "joao@email.com"}'

# Listar usuários
curl http://localhost:3000/usuarios
```

Encerrando o ambiente:
```bash
# Parar sem remover dados
docker compose down

# Parar e remover volume (apaga dados do banco)
docker compose down -v
```

Reconstruindo após mudança no código:
```bash
docker compose up -d --build
```

Resumo do que foi aplicado neste projeto:
- `Dockerfile` para empacotar a API Node.js.
- `compose.yaml` para orquestrar backend, banco e frontend.
- Volume nomeado para persistir dados do PostgreSQL.
- Bind mount para servir o frontend sem rebuild.
- `healthcheck` e `depends_on` para garantir ordem de inicialização.
- Rede interna automática do Compose para comunicação entre serviços.