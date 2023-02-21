let express = require("express"),
  router = express.Router(),
  multer = require("multer"),
  axios = require('axios');

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


router.post("/", upload.single('myFile'),   async (req, res, next) => {
    
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
    res.send(re.data)
   })
   .catch(err => console.log(err))
   
})

module.exports = router;
