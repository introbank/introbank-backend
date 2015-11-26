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
    getUserTimeline : function(user, cbSuccess, cbFail) {
        var url = "https://api.twitter.com/1.1/statuses/user_timeline.json";
        var authData = Twitter._extractAuthData(user);

        Parse.Cloud.httpRequest({
            url: url,
            followRedirects: true,
            headers: {
                "Authorization": Twitter.getOAuthSignature(url, authData.screenName,
                    authData.authToken, authData.authTokenSecret, authData.consumerKey, authData.consumerSecret)
            },
            params: {
                screen_name: authData.screenName,
                count: 200
            }
        }).then(function (res) {
            cbSuccess(null, res.data);
        }, function (res) {
            cbFail(res.text, "Failed");
        });
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
            "oauth_signature_method": "HMAC-SHA1",
            "screen_name": screenName
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

    saveTwitterContribution: function(user, type, point, tweet, successCb, failCb){
        var TwitterContribution = Parse.Object.extend('TwitterContribution');
        var contrib = new TwitterContribution();
        contrib.set('user', {"__type": "Pointer", "className":user.className, "objectId":user.id});
        contrib.set('point', point);
        contrib.set('type', type);
        contrib.set('targetTwitterId', tweet.user.id_str);
        contrib.set('targetTwitterStatusId', tweet.id_str);
        contrib.save(null, {
            success: function(contrib) {
                successCb(contrib);
            },
            error: function(error) {
                failCb(error);
            }
        })
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
        query.equalTo("user", user).equalTo("group", null).equalTo("artist", null);
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

