var oauth = require('cloud/oauth.js');
var sha   = require('cloud/sha1.js');

var consumerKey = "LZXKM3AFHSWWy7c9EVJu90kYZ";
var consumerSecret = "bxR8uOR1FgHLLa0g4gdbNrmu465Qb5Nsd0E14afGExmTKZ7PRV";

var accessor = {
    "consumerSecret": "3699404474-aGC4yBOzlXPCmXinDPzrPZdN3yAJb3V03HLOdls",
    "tokenSecret": "m4AVTdJHknG0qYnkQEgVbMVhQhWfmBLbUuMmmv57R2ckP"
};

var nonce = oauth.nonce(32);
var ts = Math.floor(new Date().getTime() / 1000);
var timestamp = ts.toString();

var params = {
    "oauth_version": "1.0",
    "oauth_consumer_key": consumerKey,
    "oauth_token": consumerSecret,
    "oauth_timestamp": timestamp,
    "oauth_nonce": nonce,
    "oauth_signature_method": "HMAC-SHA1"
};

var url = 'https://api.twitter.com/1.1/statuses/user_timeline.json';

var message = {
    "method": "GET",
    "action": url,
    "parameters": params
};

//lets create signature
oauth.SignatureMethod.sign(message, accessor);
var normPar = oauth.SignatureMethod.normalizeParameters(message.parameters);
console.log("Normalized Parameters: " + normPar);
var baseString = oauth.SignatureMethod.getBaseString(message);
console.log("BaseString: " + baseString);
var sig = oauth.getParameter(message.parameters, "oauth_signature") + "=";
console.log("Non-Encode Signature: " + sig);
var encodedSig = oauth.percentEncode(sig); //finally you got oauth signature
console.log("Encoded Signature: " + encodedSig);


// Use Parse.Cloud.define to define as many cloud functions as you want.
// For example:
Parse.Cloud.define("hello", function(request, response) {
  response.success("Hello world!");
});

Parse.Cloud.define("introbank_test", function(request, response) {
    response.success("This is test");
});

Parse.Cloud.job("userActCollect", function(request, status) {
    console.log("===== userActCollect start =====");
    Parse.Cloud.useMasterKey();
    var query = new Parse.Query(Parse.User);

    query.each(function(user) {
        console.log(user);
    }).then(function() {
        status.success('Success');
    }, function(error) {
        status.error('Something error is occured');
    });

    console.log("Submit Google");
    Parse.Cloud.httpRequest({
        url: "http://google.com",
    }).then(function(res) {
        console.log('======= GOOGLE SUCCESS ======');
    }, function(res) {
        console.error("========== GOOGLE FAIL ========");
    });

    console.log("Submit Twitter");
    Parse.Cloud.httpRequest({
        method: 'GET',
        url: url,
        headers: {
            "Authorization": 'OAuth oauth_consumer_key="'+consumerKey+'", oauth_nonce=' + nonce + ', oauth_signature=' + encodedSig + ', oauth_signature_method="HMAC-SHA1", oauth_timestamp=' + timestamp + ',oauth_token="'+consumerSecret+'", oauth_version="1.0"'
        },
        body: {
            
        }
    }).then(function(res) {
        // In case of request success
        console.log("%%%%%%%%");
        console.log(res.text);
    }, function(res) {
        // In case of request failed
        console.error("^^^^^^^ Request failed ^^^^^^^^^^^");
    });

    console.log(request.params);
    console.log("===== This is cloud code =====");
});
