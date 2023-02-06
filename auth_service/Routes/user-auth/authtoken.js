let express = require('express'),
    router = express.Router(),
    crypto = require("crypto"),
    validateAuthToken = require('../../utils/validateAuthToken');


router.get('/', (req, res) => {
    var id = crypto.randomBytes(20).toString('hex')
    id += 'kl22'
    res.set({
        'Content-Type': 'text/plain',
        'auth-token': id
      })
    setTimeout(() => {
        res.send(JSON.stringify({value: id}))
    }, 500)
})

router.get('/validateToken', (req, res) => {
    if (validateAuthToken(req.headers['auth-token'])) {
        res.status(200)
    } else {
        res.status(404)
    }
    res.send()
})


module.exports= router
