var OAuth = require('cloud/oauth.js');
var sha   = require('cloud/sha1.js');
var IntroApp = require('cloud/intro_app.js');

var Twitter = {

    _extractAuthData : function(user) {
        if (user.get("authData") != undefined
            && user.get("authData").twitter != undefined) {
            return {
                screenName: user.get('authData').twitter.screen_name,
                authToken: user.get('authData').twitter.auth_token,
                authTokenSecret: user.get('authData').twitter.auth_token_secret,
                consumerKey: user.get('authData').twitter.consumer_key,
                consumerSecret: user.get('authData').twitter.consumer_secret
            }
        }
    },

    getLike : function(user, cbSuccess, cbFail) {
        var url = "https://api.twitter.com/1.1/favorites/list.json";
        var authData = Twitter._extractAuthData(user);

        Parse.Cloud.httpRequest({
            url: url,
            followRedirects: true,
            headers: {
                "Authorization": Twitter.getOAuthSignature(url, authData.screenName,
                    authData.authToken, authData.authTokenSecret, authData.consumerKey, authData.consumerSecret)
            },
            params: {
                screen_name: authData.screenName
            }
        }).then(function (res) {
            // In case of request success, save his contribution
            // into Contribution class in Parse DB.
            cbSuccess(null, res.data);
        }, function (res) {
            // In case of request failed
            cbFail(res.text, "Failed");
        });
    },
    
    /**
     * @param statusId 
     * @param cbSuccess
     * @param cbFail
     */
    getRetweeters : function(statusId, cbSuccess, cbFail) {
        console.log("+++++++++++++++++++++");
        var url = "https://api.twitter.com/1.1/statuses/retweeters/ids.json";

        Parse.Cloud.httpRequest({
            url: url,
            followRedirects: true,
            headers: {
                "Authorization": Twitter.getIntroAppSignature(url)
            },
            params: {
                id : statusId
            }
        }).then(function (res) {
            // In case of request success, save his contribution
            cbSuccess(null, res.data);
        }, function (res) {
            // In case of request failed
            cbFail(res.text);
        });
    },

    /**
     * Create OAuth 2.0 signature for Twitter API v1.1
     * @param url
     * @param consumerSecret
     * @returns {string}
     */
    getIntroAppSignature : function(url) {
        var nonce = OAuth.nonce(32);
        var timestamp = OAuth.timestamp();
        var accessor = {
            "consumerSecret": IntroApp.CONSUMER_SECRET,
            "tokenSecret": IntroApp.ACCESS_TOKEN_SECRET
        };

        var consumerKey = IntroApp.CONSUMER_KEY;
        var authToken = IntroApp.ACCESS_TOKEN_KEY;

        var params = {
            "oauth_version": "1.0",
            "oauth_consumer_key": consumerKey,
            "oauth_token": authToken,
            "oauth_timestamp": timestamp,
            "oauth_nonce": nonce,
            "oauth_signature_method": "HMAC-SHA1"
        };

        var message = {
            "method": "GET",
            "action": url,
            "parameters": params
        };

        OAuth.SignatureMethod.sign(message, accessor);
        var normPar = OAuth.SignatureMethod.normalizeParameters(message.parameters);
        var baseString = OAuth.SignatureMethod.getBaseString(message);
        var sig = OAuth.getParameter(message.parameters, "oauth_signature") + "=";
        var encodedSig = OAuth.percentEncode(sig);

        return 'OAuth oauth_consumer_key="'+consumerKey+'", oauth_nonce=' + nonce + ', oauth_signature=' + encodedSig + ', oauth_signature_method="HMAC-SHA1", oauth_timestamp=' + timestamp + ',oauth_token="'+authToken+'", oauth_version="1.0"';

    },

    /**
     * Create OAuth 2.0 signature for Twitter API v1.1
     * @param url
     * @param screenName
     * @param authToken
     * @param authTokenSecret
     * @param consumerKey
     * @param consumerSecret
     * @returns {string}
     */
    getOAuthSignature : function(url, screenName, authToken, authTokenSecret,
                                     consumerKey, consumerSecret) {
        var nonce = OAuth.nonce(32);
        var ts = Math.floor(new Date().getTime() / 1000);
        var timestamp = ts.toString();

        var accessor = {
            "consumerSecret": consumerSecret,
            "tokenSecret": authTokenSecret
        };

        var params = {
            "oauth_version": "1.0",
            "oauth_consumer_key": consumerKey,
            "oauth_token": authToken,
            "oauth_timestamp": timestamp,
            "oauth_nonce": nonce,
            "oauth_signature_method": "HMAC-SHA1"
        };

        if(screenName != null){
            params["screen_name"] = screenName;
        }

        var message = {
            "method": "GET",
            "action": url,
            "parameters": params
        };

        OAuth.SignatureMethod.sign(message, accessor);
        var normPar = OAuth.SignatureMethod.normalizeParameters(message.parameters);
        var baseString = OAuth.SignatureMethod.getBaseString(message);
        var sig = OAuth.getParameter(message.parameters, "oauth_signature") + "=";
        var encodedSig = OAuth.percentEncode(sig);

        return 'OAuth oauth_consumer_key="'+consumerKey+'", oauth_nonce=' + nonce + ', oauth_signature=' + encodedSig + ', oauth_signature_method="HMAC-SHA1", oauth_timestamp=' + timestamp + ',oauth_token="'+authToken+'", oauth_version="1.0"';
    },

    /**
     * save TwitterContribution tweet, users 
     * @param type
     * @param target
     * @param successCb
     * @param failCb
     */

    saveTwitterLikeContribution: function(user, like, successCb, failCb) {
        var TwitterContribution = Parse.Object.extend('TwitterContribution');
        var contrib = new TwitterContribution();
        contrib.set('user', {"__type": "Pointer", "className":user.className, "objectId":user.id});
        contrib.set('point', 10);
        contrib.set('type', 'like');
        contrib.set('targetTwitterId', like.user.id_str);
        contrib.set('targetTwitterStatusId', like.id_str);
        contrib.save(null, {
            success: function(contrib) {
                successCb(contrib);
            },
            error: function(error) {
                failCb(error);
            }
        })
    },
    
    saveTwitterRetweetContribution: function(tweet, retweeters, successCb, failCb){
        var userQuery = new Parse.Query(Parse.User);
        for (var i = 0; i < retweeters.length; i++){
            console.log(retweeters.id_str);
            tmp = new Parse.Query(Parse.User); 
            userQuery = Parse.Query.or(userQuery, tmp.equalTo("twitterId", retweeters.id_str));
        }

        userQuery.find({
                success: function(user){
                    var TwitterContribution = Parse.Object.extend('TwitterContribution');
                    var contrib = new TwitterContribution();
                    contrib.set('point', 20);
                    contrib.set('type', 'retweet');
                    contrib.set('tweet', 'tweet');
                    contrib.ddUnique('user', user);
                    if(user.length > 0){
                        Parse.Object.saveAll(contrib, {
                            success:function(contrib) {
                                successCb(contrib);
                            },
                            error:function(error) {
                                console.log(error.message);
                                failCb(error);
                            }
                        });                             
                    }
                },
                error: function(error){
                    console.log(error.message);
                }
        });
    },

    /**
     * Update the TwitterContribution by join Perfomer/Group on TwitterId
     * @param type
     * @param target
     * @param successCb
     * @param failCb
     */
    updateTwitterContribution : function(target, successCb, failCb) {
        var TwitterContribution = Parse.Object.extend("TwitterContribution");
        var query = new Parse.Query(TwitterContribution);
        query.equalTo("targetTwitterId", target.get("twitterId"));
        query.find({
            success: function(twitterContrib) {
                if (twitterContrib.length == 0){
                    console.log("twitterContrib has no recode.");
                }
                var col = target.className.toLowerCase();
                var data = {};
                data[col] = {"__type": "Pointer", "className":target.className, "objectId":target.id};
                for (var i = 0; i < twitterContrib.length; i++) {
                    twitterContrib[i].set(data);
                }
                Parse.Object.saveAll(twitterContrib, {
                    success:function(tiwtterContrib) {
                        successCb(tiwtterContrib);
                    },
                    error:function(error) {
                        console.log(error.message)
                        failCb(error);
                    }
                });},
            error: function(error){
                failCb(error);
            }
        });
    },

    /**
     * Delete TwitterContribution UseLess Recodes 
     * @param type
     * @param target
     * @param successCb
     * @param failCb
     */
    cleanTwitterContribution : function(user, successCb, failCb) {
        var TwitterContribution = Parse.Object.extend("TwitterContribution");
        var query = new Parse.Query(TwitterContribution);
        // not introbank target records
        query.equalTo("user", user).equalTo("group", null).equalTo("performer", null);
        query.find({
            success: function(twitterContrib) {
                // delete
                Parse.Object.destroyAll(twitterContrib, {
                    success:function(tiwtterContrib) {
                        successCb(tiwtterContrib);
                    },
                    error:function(error) {
                        console.log(error.message)
                        failCb(error);
                    }
                });
            },
            error: function(error){
                failCb(error);
            }
        });
    },
};


module.exports = Twitter;

