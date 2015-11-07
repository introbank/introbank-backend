var OAuth = require('cloud/oauth.js');
var sha   = require('cloud/sha1.js');

var Twitter = {
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
            "screen_name": screenName,
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
    
    // Private method
    _parseTwitterActs : function(user) {
        var acts = {
            favouriteCount: user.favourites_count,
            followerCount: user.followers_count,
            id: user.id,
            lang: user.lang,
            profileImageUrl: user.profile_image_url,
            screenName: user.screen_name
        };
        
        return acts;
    },
    
    /**
     * Save the contribution of given user into Contribution class.
     * @param user
     * @param successCb
     * @param failCb
     */
    saveContribution : function(user, successCb, failCb) {
        var acts = Twitter._parseTwitterActs(user);
        
        var Contribution = Parse.Object.extend("Contribution");
        var contrib = new Contribution();
        contrib.set("favourite_count", acts.favouriteCount);
        contrib.set("followers_count", acts.followerCount);
        contrib.set("lang", acts.lang);
        contrib.set("profile_image_url", acts.profileImageUrl);
        contrib.set("screen_name", acts.screenName);
        contrib.save(null,{
            success:function(contrib) {
                successCb(contrib);
            },
            error:function(error) {
                failCb(error);
            }
        });
    },

};

module.exports = Twitter;
