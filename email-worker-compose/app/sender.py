import psycopg2
from bottle import route, run, request

DSN = 'dbname=email_sender user=postgres password=password host=db'
SQL = 'INSERT INTO emails (assunto, mensagem) VALUES (%s, %s)'

def register_message(assunto, mensagem):
    conn = psycopg2.connect(DSN)
    cursor = conn.cursor()
    cursor.execute(SQL, (assunto, mensagem))
    conn.commit()
    cursor.close()
    conn.close()

    print(f'Mensagem registrada: {assunto} - {mensagem}')

@route('/', method='POST')
def send():
    assunto = request.forms.get('assunto')
    mensagem = request.forms.get('mensagem')

    register_message(assunto, mensagem)
    return f'Email enviado com assunto: {assunto} e mensagem: {mensagem}'

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True)
