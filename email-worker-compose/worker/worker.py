import redis
import json
import os
from time import sleep
from random import randint

if __name__ == "__main__":
    redis_host = os.getenv('REDIS_HOST', 'queue')
    r = redis.Redis(host=redis_host, port=6379, db=0)
    print("Worker iniciado, aguardando mensagens...")
    while True:
        mensagem = json.loads(r.blpop('sender')[1])
        # Simula o envio do email....
        print(f"Enviando email para {mensagem['assunto']}...")
        sleep(randint(15, 45))
        print(f"Email para {mensagem['assunto']} enviado com sucesso!")