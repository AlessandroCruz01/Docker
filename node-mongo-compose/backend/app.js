const express = require('express');
const restful = require('node-restful');

const server = express();
const mongoose = restful.mongoose;
const bodyParser = require('body-parser');
const cors = require('cors');

// Database
mongoose.Promise = global.Promise;
mongoose.connect('mongodb://db/mydb');

//* Middlewares (são executados antes de chegar nas rotas - a palavra middleware é usada para funções que são executadas antes de chegar nas rotas e significa em inglês "entre" ou "no meio de")
server.use(bodyParser.urlencoded({ extended: true }));
server.use(bodyParser.json());
server.use(cors());

//* ODM (Object Data Modeling) - é uma biblioteca que fornece uma solução baseada em esquemas para modelar os dados do aplicativo. Ele inclui recursos de validação de esquema, construção de consultas, ganchos de negócios e muito mais, para ajudar a gerenciar os dados do aplicativo de forma eficiente.
const Client = restful.model('Client', {
    name: { type: String, required: true },
})

//* Rest API - é um estilo de arquitetura de software para sistemas distribuídos, como a web. Ele é baseado em recursos, que são identificados por URLs, e em operações HTTP, como GET, POST, PUT e DELETE, para manipular esses recursos. A API REST é amplamente utilizada para criar serviços web escaláveis e flexíveis.
Client.methods(['get', 'post', 'put', 'delete']);
Client.updateOptions({ new: true, runValidators: true });

//* Routes - é um conjunto de regras que define como as solicitações HTTP devem ser tratadas pelo servidor. As rotas são usadas para mapear URLs para funções específicas que processam as solicitações e retornam respostas. Elas são essenciais para criar uma API RESTful, permitindo que os clientes interajam com os recursos do servidor de maneira organizada e eficiente.
Client.register(server, '/clients');


// Start server
server.listen(3000, () => {
    console.log('Server running on port 3000');
});