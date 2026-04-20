from bottle import route, run, request

@route('/', method='POST')
def send():
    assunto = request.forms.get('assunto')
    mensagem = request.forms.get('mensagem')
    return f'Email enviado com assunto: {assunto} e mensagem: {mensagem}'

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True)
