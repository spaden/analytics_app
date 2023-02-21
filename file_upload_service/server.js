let app = require('express')(),
    server = require('http').Server(app),
    bodyParser = require('body-parser')
    express = require('express'),
    cors = require('cors'),
    http = require('http'),
    path = require('path');

let fileupload = require('./Routes/fileupload')

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
    
app.use(cors())
app.options('*', cors())
app.use('/fileupload', fileupload)


app.use(function(req, res, next) {
    next();
});



// app.use('/images/GymImages', express.static(__dirname+'/Assets/'))

/*first API to check if server is running*/
app.get('*', (req, res) => {
    res.send("working");
})


server.listen(3004, function() {
    console.log('app listening on port: 3004')
})