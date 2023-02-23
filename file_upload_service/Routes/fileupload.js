let express = require("express"),
  router = express.Router(),
  multer = require("multer"),
  axios = require('axios');

const { MongoClient } = require("mongodb");

let upload = multer({
  storage: multer.diskStorage({
    destination: function (req, file, cb) {
      cb(null, "./userfiles");
    },
    filename: function (req, file, cb) {
      cb(null, file.originalname);
    }
  })
})

async function insertData(username, analyticsdata) {
  var url = "mongodb://localhost:27017/"

  const client = new MongoClient(url)
  
  try {
    const result = await client.db('analytics_app')
                            .collection('user_data')
                            .updateOne(
                              { 'username': username },
                              { $set: { 'userdata': analyticsdata } },
                              { upsert: true })
    
 } catch(err) {
   console.log(err)
 }
}


router.post("/", upload.single('myFile'),   async (req, res, next) => {
    
   const username =  req.body.username

   const files = req.file

   if (!files) {
        const error = new Error('Please choose files')
        error.httpStatusCode = 400
        return next(error)
   }

   axios.post('http://127.0.0.1:8004/getallsentiments', {
        'filename': 'D:/projects/github/analytics_app/file_upload_service/userfiles/' + files.filename
    })
   .then(re => {
      insertData(username, re.data)
      res.send({dt: re.data})
   })
   .catch(err => console.log(err))
  
})

module.exports = router;
