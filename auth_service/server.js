let app = require('express')(),
    server = require('http').Server(app),
    bodyParser = require('body-parser')
    express = require('express'),
    cors = require('cors'),
    http = require('http'),
    path = require('path');

let login = require('./Routes/user-auth/login')
let authToken = require('./Routes/user-auth/authtoken')

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
    
app.use(cors())
app.options('*', cors())
app.use('/user', login)
app.use('/authtoken', authToken)


app.use(function(req, res, next) {
    next();
});



// app.use('/images/GymImages', express.static(__dirname+'/Assets/'))

/*first API to check if server is running*/
app.get('*', (req, res) => {
    res.send("working");
})


server.listen(3000, function() {
    console.log('app listening on port: 3000')
})
