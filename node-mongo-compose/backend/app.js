const express = require('express');
const restful = require('node-restful');

const server = express();
const mongoose = restful.mongoose;

// Database
mongoose.Promise = global.Promise;
mongoose.connect('mongodb://db/mydb');

// Test
server.get('/', (req, res) => {
    res.send('Hello World!');
})

// Start server
server.listen(3000, () => {
    console.log('Server running on port 3000');
});