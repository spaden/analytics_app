let express = require('express'),
    router = express.Router();


router.post('/', (req, res) => {
    var data = req.body
    console.log(data.username)
    console.log(data.userpass)
    
    res.type('text/plain')
    res.status(200)
    res.send('Success')
})


module.exports = router;
