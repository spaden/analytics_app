let express = require('express'),
    router = express.Router();
const { MongoClient } = require("mongodb");


async function insertUser(data, db) {
    try {
        const result = await db.collection('users_auth').insertOne({
            username: data.username,
            userpass: data.userpass
        })
        if (!result.insertedId) {
            return false
        }
    } catch(err) {
        return false
    }
    
    return true
}   

router.post('/checkuser', async (req, res) => {
    var data = req.body
    var url = "mongodb://localhost:27017/"

    const client = new MongoClient(url)
    let userAuth = false
    let newUser = false

    try {

        const cursor = await client.db('analytics_app')
                            .collection('users_auth')
                            .find({username: data.username, userpass: data.userpass})
        const resp = await cursor.toArray()

        if (resp.length == 1) {
            userAuth = true
        } else {
            const insertStatus = await insertUser(data, client.db('analytics_app'))
            if (insertStatus) {
                userAuth = true
                newUser = true
            }
        }
    } catch {

    }
    
    res.type('text/plain')
    
    if (userAuth) {
        res.status(200)
    } else {
        res.status(500)
    }
    let userRes = [{}]
    if (!newUser) {
        try {
            const cursor = await client.db('analytics_app')
                                        .collection('user_data')
                                        .find({username: data.username}).project({ userdata: 1, _id: 0})
            const resp = await cursor.toArray()

            userRes = resp

        } catch {

        }
    }
    res.send(userRes)
})


module.exports = router;
