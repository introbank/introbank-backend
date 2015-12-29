var OAuth = require('cloud/oauth.js');
var sha   = require('cloud/sha1.js');
var Twitter = require('cloud/twitter.js');
var Account = require('cloud/account.js');
var StringHash = require('cloud/string-hash.js');

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
    query.include("twitterApiOffset");
    query.each(function(user) {
        Twitter.getLike(user, function(error, likes) {
            for (var i = 0; i < likes.length; i++) {
                var like = likes[i];
                Twitter.saveTwitterContribution(user, "like", 10, like, function(result) {
                    console.log("Success saving twitter contribution");
                           
                },
                function(error) {
                    console.log("Failed saving twitter contribution::" + error);
                });
            }
            if (likes.length > 0){
            Twitter.saveTwitterApiOffset(user, {favoritesListSinceId: likes[0].id_str}, 
                    function(result){ 
                        console.log("Success saving api offset");
                    },
                    function(error){
                        console.log("Failed saving twitter api offset.code=" + error.code + ", message=" + error.message);
                    }); 
            }
            else{
                console.log("no new like data and offset is not changed");
            }
        }, function(error, result) {

        });
    }).then(function() {

    }, function(error) {
        console.log("Query submission failed");
        status.error("Query failed");
    });
});

Parse.Cloud.job('updateTwitterContribution', function(request, status) {
    console.log("Started update twitter contribution");

    Parse.Cloud.useMasterKey();
    var Group = Parse.Object.extend("Group");
    var Artist = Parse.Object.extend("Artist");

    var types = ["group", "artist"];
    // ここはParse.Promise.whenを使う予定： https://parse.com/docs/jp/js/guide
    for (var i = 0; i < types.length; i++){

        var query = null;
        if (types[i] == "group"){
          query = new Parse.Query(Group);
        }
        else if (types[i] == "artist"){
          query = new Parse.Query(Artist);
        }

        query.each(function(target) {
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
    console.log("Started collecting twitter retweet");
    Parse.Cloud.useMasterKey();

    var query = new Parse.Query(Parse.User);
    query.include("twitterApiOffset");
    query.each(function(user) {
        Twitter.getUserTimeline(user, function(error, tweets) {
            for (var i = 0; i < tweets.length; i++) {
                var tweet = tweets[i];
                if(tweet.retweeted == true){
                    var retweet = tweet.retweeted_status;
                    Twitter.saveTwitterContribution(user, "retweet", 20, retweet, function(result) {
                            console.log("Success saving twitter contribution");
                        }
                        , function(error) {
                            console.log("Failed saving twitter contribution::" + error);
                        }
                        );
                }
            }
            if (tweets.length > 0){
            Twitter.saveTwitterApiOffset(user, {userTimelineSinceId: tweets[0].id_str}, 
                    function(result){ 
                        console.log("Success saving api offset");
                    },
                    function(error){
                        console.log("Failed saving twitter api offset.code=" + error.code + ", message=" + error.message);
                    }); 
            }
            else{
                console.log("no new tweet data and offset is not changed");
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

Parse.Cloud.define("syncTwitterUserData", function(request, response) {
    console.log("Started sync account's twitter user data");
    Parse.Cloud.useMasterKey();
    var params = request["params"]["request"];
    console.log(params.farmNum);
    var farmNum = params["farmNum"];
    var type = params["type"];
    var now = new Date();
    var farm = now.getHours() % farmNum;

    console.log("farm=" + farm);
    console.log("type=" + type);

    var Account = Parse.Object.extend(type);

    var query = new Parse.Query(Account);
    query.limit(1000);
    query.ascending("name");
    query.find(function(accounts) {
        var twitterIds= [];
        var updateAccounts = [];
        for(var i = 0; i < accounts.length; i++){
            var account = accounts[i];
            var objectId = account.id;
            var hash = StringHash.calc(objectId)  % farmNum;
            if (hash == farm){
                //console.log("twitterId=" + account.get("twitterId") + ", name=" + account.get("name"));
                twitterIds.push(account.get("twitterId"));
                updateAccounts.push(account);
            }
        }
        Twitter.getTwitterUsersLookup(twitterIds, function(error, userslookup) {
            for (var i = 0; i < userslookup.length; i++) {
                Twitter.updateTargetAccountInfo(updateAccounts[i], userslookup[i], 
                function(){
                    //console.log("update account data success");
                },
                function(){
                    console.log("update" + type  + "data failed");
                }
                );
            }
        }, function(error, result) {
        });
    })
});


Parse.Cloud.job('syncArtistTwitterUserData', function(request, status) {
  Parse.Cloud.run('syncTwitterUserData', {request:request["params"]});
});

Parse.Cloud.job('syncGroupTwitterUserData', function(request, status) {
  Parse.Cloud.run('syncTwitterUserData', {request:request["params"]});
});


Parse.Cloud.define("syncNewAccountData", function(request, response) {
    console.log("Started sync account's twitter user data");
    Parse.Cloud.useMasterKey();
    var params = request["params"]["request"];
    var limit = params["limit"];
    var type = params["type"];
    console.log("limit=" + limit);
    console.log("type=" + type);

    var Account = Parse.Object.extend(type);
    var query = new Parse.Query(Account);
    query.limit(limit);
    query.descending("createdAt");
    query.find(function(accounts) {
        var twitterIds = [];
        for(var i = 0; i < accounts.length; i++){
            twitterIds.push(accounts[i].get("twitterId"));
        }      
        Twitter.getTwitterUsersLookup(twitterIds, function(error, userslookup) {
            for (var i = 0; i < userslookup.length; i++) {
                Twitter.updateTargetAccountInfo(accounts[i], userslookup[i], 
                function(){
                },
                function(){
                    console.log("update" + type  + "data failed");
                }
                );
            }
        }, function(error, result) {
        });
    })
});

Parse.Cloud.job('syncNewArtistData', function(request, status) {
  Parse.Cloud.run('syncNewAccountData', {request:request["params"]});
});

Parse.Cloud.job('syncNewGroupData', function(request, status) {
  Parse.Cloud.run('syncNewAccountData', {request:request["params"]});
});


Parse.Cloud.job('addMembersRelation', function(request, status) {
  console.log("Started add relation from group to artist");
  Parse.Cloud.useMasterKey();
  var params = request["params"];
  var limit = params["limit"];
  console.log("limit=" + limit);
  var query = new Parse.Query("Group");
  query.limit(limit);
  query.descending("createdAt");
  Account.addMemberRelations(query);
});


