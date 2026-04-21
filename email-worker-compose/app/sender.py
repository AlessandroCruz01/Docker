import psycopg2
import redis
import json
import os
from bottle import Bottle, request

class Sender(Bottle):
    def __init__(self):
        super().__init__()
        self.route('/', method='POST', callback=self.send)
        redis_host = os.getenv('REDIS_HOST', 'queue')
        self.fila = redis.Redis(host=redis_host, port=6379, db=0)

        db_host = os.getenv('DB_HOST', 'db')
        db_user = os.getenv('DB_USER', 'postgres')
        db_name = os.getenv('DB_NAME', 'email_sender')
        db_password = os.getenv('DB_PASSWORD', 'password')
        DSN = f'dbname={db_name} user={db_user} password={db_password} host={db_host}'
        self.conn = psycopg2.connect(DSN)

    def register_message(self, assunto, mensagem):
        SQL = 'INSERT INTO emails (assunto, mensagem) VALUES (%s, %s)'
        cursor = self.conn.cursor()
        cursor.execute(SQL, (assunto, mensagem))
        self.conn.commit()
        cursor.close()
        self.conn.close()

        mensagem = { 'mensagem': mensagem, 'assunto': assunto }
        self.fila.rpush('sender', json.dumps(mensagem))

        print(f'Mensagem registrada: {assunto} - {mensagem}')

    def send(self):
        assunto = request.forms.get('assunto')
        mensagem = request.forms.get('mensagem')

        self.register_message(assunto, mensagem)
        return f'Email enviado com assunto: {assunto} e mensagem: {mensagem}'

if __name__ == '__main__':
    sender = Sender()
    sender.run(host='0.0.0.0', port=8080, debug=True)
