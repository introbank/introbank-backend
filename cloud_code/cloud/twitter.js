var OAuth = require('cloud/oauth.js');
var sha   = require('cloud/sha1.js');
var TokenSetting = require('cloud/token_setting.js');

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

    /**
     * @param user 
     * @param cbSuccess
     * @param cbFail
     */
    getLike : function(user, cbSuccess, cbFail) {
        var url = "https://api.twitter.com/1.1/favorites/list.json";
        var offsetData = user.get("twitterApiOffset");
        var authData = Twitter._extractAuthData(user);
        var params = {"screen_name": authData.screenName, "count":50};

        if (offsetData && offsetData.get("favoritesListSinceId")){
            params["since_id"] = offsetData.get("favoritesListSinceId");
            console.log("set sence_id=" + params["since_id"]);
        }


        Twitter.httpUserOAuthedRequest(url, authData, params, cbSuccess, cbFail);
    },
    
    /**
     * @param user 
     * @param cbSuccess
     * @param cbFail
     */
    getUserTimeline : function(user, cbSuccess, cbFail) {
        var url = "https://api.twitter.com/1.1/statuses/user_timeline.json";
        var offsetData = user.get("twitterApiOffset");
        var authData = Twitter._extractAuthData(user);
        var params = {"screen_name": authData.screenName, "count":50};

        if (offsetData && offsetData.get("userTimelineSinceId")){
            params["since_id"] = offsetData.get("userTimelineSinceId");
            console.log("set sence_id=" + params["since_id"]);
        }

        Twitter.httpUserOAuthedRequest(url, authData, params, cbSuccess, cbFail);
    },

    /**
     * @param twitterIds 
     * @param cbSuccess
     * @param cbFail
     */
    getTwitterUsersLookup : function(twitterIds, cbSuccess, cbFail) {
        var url = "https://api.twitter.com/1.1/users/lookup.json";
        var user_id = twitterIds.join(",");
        console.log("user_id=" + user_id);
        var params = {"user_id": user_id};

        Twitter.httpAppOAuthedRequest(url, params, cbSuccess, cbFail);
    },

    saveTwitterApiOffset : function(user, data, successCb, failCb){
        console.log("saveTwitterApiOffset start");
        var TwitterApiOffset = Parse.Object.extend("TwitterApiOffset");
        var query = new Parse.Query(TwitterApiOffset);
        query.equalTo("user", user);
        query.find({
            success: function(results) {
                console.log("saveTwitterApiOffset::user=" + user.id);
                // not  target records
                var twitterApiOffset = new TwitterApiOffset();
                if (results.length == []){
                    console.log("twitterApiOffset create");
                    twitterApiOffset.set("user", user);
                }
                else{
                    console.log("twitterApiOffset update");
                    twitterApiOffset = results.pop();
                }
                for (var key in data) {
                    var value = data[key];
                    console.log("saveTwitterApiOffset::" + key + "=" + value);
                    twitterApiOffset.set(key, value);
                }
                twitterApiOffset.save(null, {
                    success: function(response) {
                        console.log("update user twitterApiOffset");
                        user.set("twitterApiOffset", twitterApiOffset);
                        user.save(null, {
                            success: function(res){successCb(null, res);},
                            error: function(error){failCb(error)}
                        });
                    },
                    error: function(res, error) {
                        failCb(error);
                    }
                });
            },
            error: function(error){
                failCb(error);
            }
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
    getOAuthSignature : function(url, params, authToken, authTokenSecret,
                                     consumerKey, consumerSecret) {
        var nonce = OAuth.nonce(32);
        var ts = Math.floor(new Date().getTime() / 1000);
        var timestamp = ts.toString();

        var accessor = {
            "consumerSecret": consumerSecret,
            "tokenSecret": authTokenSecret
        };

        var oauthPramas = {
            "oauth_version": "1.0",
            "oauth_consumer_key": consumerKey,
            "oauth_token": authToken,
            "oauth_timestamp": timestamp,
            "oauth_nonce": nonce,
            "oauth_signature_method": "HMAC-SHA1"
        };
        
        for (var attrname in params) {
            if (params.hasOwnProperty(attrname)) {
                oauthPramas[attrname] = params[attrname];
            }
        }

        var message = {
            "method": "GET",
            "action": url,
            "parameters": oauthPramas
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
        var col = target.className.toLowerCase();
        query.equalTo("targetTwitterId", target.get("twitterId")).equalTo(col, null);
        query.find({
            success: function(twitterContrib) {
                if (twitterContrib.length == 0){
                    console.log("twitterContrib has no recode.");
                }
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
     *
     */
    updateTargetAccountInfo : function(target, twitterUserInfo, successCb, failCb) {
        console.log("updateTargetAccountInfo start:: objectId=" + target.id);
        // error handling
        if (target.get("twitterId") != twitterUserInfo.id_str){
            console.log("error. target=" + target.get("twitterId") + ", twitterId=" + twitterUserInfo.id_str);
            failCb("targetId error");
        }
        else{
        target.set("name", twitterUserInfo.name);
        target.set("info", twitterUserInfo.description);
        var imageUrl = twitterUserInfo.profile_image_url_https.replace("_normal","");
        target.set("imageUrl", imageUrl);
        target.set("twitterUsername", twitterUserInfo.screen_name);
        target.save(null, {
                    success:function(result) {
                        successCb(result);
                    },
                    error:function(error) {
                        console.log(error.message)
                        failCb(error);
                    }
                });
        }
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
                console.log("delete recodes for user::" + user.get("username"));
                deletes = [];
                // 1 hour
                var targetTimestamp = Date.now() - 3600000;
                for(var i = 0; i < twitterContrib.length; i++){
                    var update = Date.parse(twitterContrib[i].get("updatedAt"));
                    if(update < targetTimestamp){
                        deletes.push(twitterContrib[i]);
                    }
                }
                console.log("delete recodes::" + deletes.length);
                Parse.Object.destroyAll(deletes, {
                    success:function(res) {
                        successCb(null, res);
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

    httpUserOAuthedRequest : function(url, authData, params, cbSuccess, cbFail) {
        console.log("url=" + url);
        Parse.Cloud.httpRequest({
            url: url,
            followRedirects: true,
            headers: {
                "Authorization": Twitter.getOAuthSignature(url, params,
                    authData.authToken, authData.authTokenSecret, authData.consumerKey, authData.consumerSecret)
            },
            params: params
        }).then(function (res) {
            // In case of request success, save his contribution
            // into Contribution class in Parse DB.
            cbSuccess(null, res.data);
        }, function (res) {
            // In case of request failed
            cbFail(res.text, "Failed");
        });
    },

    httpAppOAuthedRequest : function(url, params, cbSuccess, cbFail) {
        console.log("url=" + url);
        var token = TokenSetting.DATA_SYNC;
        Parse.Cloud.httpRequest({
            url: url,
            followRedirects: true,
            headers: {
                "Authorization": Twitter.getOAuthSignature(url, params,
                    token.ACCESS_TOKEN_KEY, token.ACCESS_TOKEN_SECRET, token.CONSUMER_KEY, token.CONSUMER_SECRET)
            },
            params: params
        }).then(function (res) {
            // In case of request success, save his contribution
            // into Contribution class in Parse DB.
            cbSuccess(null, res.data);
        }, function (res) {
            // In case of request failed
            cbFail(res.text, "Failed");
        });
    },

    migragteTwitterContirbution : function() {
        var contribList = [];
        var TwitterContribution = Parse.Object.extend("TwitterContribution");
        var query = new Parse.Query(TwitterContribution);
        query.limit(1000);
        query.equalTo("type", "retweet");
        query.equalTo("point", null);
        query.find({
            success: function(twitterContrib) {
                console.log("twitterContrib.length= " + twitterContrib.length);
                for (var i = 0; i < twitterContrib.length; i++) {
                    var contrib = twitterContrib[i];
                    contrib.set("point", 2);
                    contribList.push(contrib);
                }
                console.log("contribList.length= " + contribList.length);
                Parse.Object.saveAll(contribList, {
                    success:function(results) {
                        console.log(results);
                    },
                    error:function(error) {
                        console.log(error.message)
                        failCb(error);
                    }
                });

                },
            error: function(error){
                console.log(error.message)
                failCb(error);
            }
        });
   },
};


module.exports = Twitter;

