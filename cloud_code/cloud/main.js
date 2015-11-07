var OAuth = require('cloud/oauth.js');
var sha   = require('cloud/sha1.js');
var Twitter = require('cloud/twitter.js');

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
});

Parse.Cloud.job('collectTwitterLike', function(request, status) {
    console.log("Started collecting twitter likes");

    Parse.Cloud.useMasterKey();

    var query = new Parse.Query(Parse.User);
    query.each(function(user) {
        Twitter.getLike(user, function(error, likes) {
            for (var i = 0; i < likes.length; i++) {
                Twitter.saveTwitterContribution(likes[i], function(result) {
                    //status.success("Success saving twitter contribution");
                    console.log("Success saving twitter contribution");
                }, function(error) {
                    status.error("Failed saving twitter contribution");
                });
            }
        }, function(error, result) {

        });
    }).then(function() {
        console.log("Query submit success");
    }, function(error) {
        console.log("Query submission failed");
        status.error("Query failed");
    })

});

Parse.Cloud.job('updateTwitterContribution', function(request, status) {
    console.log("Started updating twitter contribution class");

    Parse.Cloud.useMasterKey();
    var targets = [{type:"group", query:new Parse.Query(Parse.Group)}, {type:"performer", query: new Parse.Query(Parse.Performer)}]
    for (var i = 0; i < targets.lenght; i++){
        targets[i].query.each(function(result) {
            Twitter.updateTwitterContribution(targets[i].type, result.objectId, result.twitterId,
                    function(result) {
                        console.log("Success update twitter contribution. twitterId=" + result.twitterId);
                    }, function(error) {
                    status.error("Failed saving twitter contribution");
                })}
            ).then(function() {
            status.success("Success saving twitter contribution");
            console.log("Query submit success");
            }, function(error) {
                console.log("Query submission failed");
                status.error("Query failed");
            })
    }
});
