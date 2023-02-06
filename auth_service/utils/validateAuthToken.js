function validateAuthToken(token) {
    console.log(token)
    if (token.charAt(token.length - 1) == '2') {
        return true
    } else {
        return false
    }
}
module.exports = validateAuthToken
