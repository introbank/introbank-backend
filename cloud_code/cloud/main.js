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
                Twitter.saveTwitterLikeContribution(user, likes[i], function(result) {
                    console.log("Success saving twitter contribution");
                }, function(error) {
                    console.log("Failed saving twitter contribution::" + error);
                });
            }
        }, function(error, result) {

        });
    }).then(function() {
        console.log("Query submit success");
    }, function(error) {
        console.log("Query submission failed");
        status.error("Query failed");
    });
});

Parse.Cloud.job('updateTwitterContribution', function(request, status) {
    console.log("Started update twitter contribution");

    Parse.Cloud.useMasterKey();
    var Group = Parse.Object.extend("Group");
    var Performer = Parse.Object.extend("Performer");

    var types = ["group", "performer"];
    // ここはParse.Promise.whenを使う予定： https://parse.com/docs/jp/js/guide
    for (var i = 0; i < types.length; i++){

        var query = null;
        if (types[i] == "group"){
          query = new Parse.Query(Group);
        }
        else if (types[i] == "performer"){
          query = new Parse.Query(Performer);
        }

        query.each(function(target) {
            console.log("Update twitter contribution. target.id=" + target.id);
            console.log("Update twitter contribution. target.twitterId=" + target.get("twitterId"));

            Twitter.updateTwitterContribution(target,
                function(responce){
                    console.log("Success update twitter contribution");
                },
                function(error){
                    console.log("Fail update twitter contribution");
                }
                );
        }).then(function() {
            //status.success("Success update twitter contribution");
        }, function(error) {
            console.log("Query submission failed");
            //status.error("Query failed");
        });
    }
});

Parse.Cloud.job('cleanTwitterContribution', function(request, status) {
    console.log("Started clean twitter contribution");
    Parse.Cloud.useMasterKey();
    var query = new Parse.Query(Parse.User);
    query.each(function(user) {
        console.log("Clean twitter contribution. user.id=" + user.id);
        Twitter.cleanTwitterContribution(user,
            function(responce){
                console.log("Success clean twitter contribution");
            },
            function(error){
                console.log("Fail clean twitter contribution");
            }
            );
    }).then(function() {
        //status.success("Success update twitter contribution");
    }, function(error) {
        console.log("Query submission failed");
        //status.error("Query failed");
    });
});

Parse.Cloud.job('collectTwitterRetweet', function(request, status) {
    console.log("Started collect twitter retweet contribution");
    Parse.Cloud.useMasterKey();
    var Tweet = Parse.Object.extend("Tweet");
    var query = new Parse.Query(Tweet);

    query.equalTo("isReflected", false).equalTo("retweetCount", null);
    query.each(function(tweet) {
        console.log("collect retweet. tweet.id=" + tweet.id);
        Twitter.getRetweeters(tweet.get("twitterStatusId")
            , function(error, retweeters){
                console.log("*********")
                Twitter.saveTwitterRetweetContribution(tweet, retweeters, function(){}, function(){});
            }
            , function(error) {
                console.log(error);
            }
        );
    }
        , function(error){
            console.log(error);
        }
    );
});
