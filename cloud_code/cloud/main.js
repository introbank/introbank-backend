var OAuth = require('cloud/oauth.js');
var sha   = require('cloud/sha1.js');
var Twitter = require('cloud/twitter.js');

var url = 'https://api.twitter.com/1.1/users/show.json';

// Use Parse.Cloud.define to define as many cloud functions as you want.
// For example:
Parse.Cloud.define("hello", function(request, response) {
  response.success("Hello  world!");
});

Parse.Cloud.define("introbank_test", function(request, response) {
    response.success("This is test");
});

/**
 *  Collect user contribution from Twitter regularly.
 *  Obtain authentication information from User class and
 *  lookup their contributions such as favourites through Twitter API.
 */
Parse.Cloud.job("userActCollect", function(request, status) {
    console.log("===== userActCollect start =====");

    // In order to lookup authentication information.
    Parse.Cloud.useMasterKey();

    var query = new Parse.Query(Parse.User);
    query.each(function(user) {
        if (user.get("authData") != undefined && user.get("authData").twitter != undefined) {
            var authToken = user.get("authData").twitter.auth_token;
            var authTokenSecret = user.get("authData").twitter.auth_token_secret;
            var screenName = user.get("authData").twitter.screen_name;
            var consumerKey = user.get("authData").twitter.consumer_key;
            var consumerSecret = user.get("authData").twitter.consumer_secret;

            // Access Twitter API to obtain basic info for this user.
            Parse.Cloud.httpRequest({
                url: url,
                followRedirects: true,
                headers: {
                    "Authorization": Twitter.getOAuthSignature(url, screenName,
                        authToken, authTokenSecret, consumerKey, consumerSecret)
                },
                params: {
                    screen_name: screenName
                }
            }).then(function (res) {
                // In case of request success, save his contribution
                // into Contribution class in Parse DB.
                Twitter.saveContribution(res.data, function(contrib) {
                    status.success("Success");
                }, function(error) {
                    status.fail("Failed");
                });
            }, function (res) {
                // In case of request failed
                console.log(res.text);
                status.fail("Failed");
            });
        }
    }).then(function() {
        // Query submit succeeded
        console.log("Query success");
    }, function(error) {
        // In case of query access error.
        console.log("Query failed");
        status.fail("Failed");
    });
});
