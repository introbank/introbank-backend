
var Account = {
  addMemberRelations : function(groupQuery){
    groupQuery.find({
      success: function(groups) {
        for (var i = 0; i < groups.length; i++) {
          var Group = Parse.Object.extend("Group"); 
          var group = new Group();
          group.id = groups[i].id;
          var membersRelation = group.relation("members");
          var membersQuery = membersRelation.query();
          membersQuery.find({
            success: function(artists) {
              for (var j = 0; j < artists.length; j++) {
                var Artist = Parse.Object.extend("Artist"); 
                var artist = new Artist();
                artist.id = artists[j].id;
                console.log("group:" + group.id);
                console.log("artist:" + artist.id);
                var groupRelation = artist.relation("groups");
                groupRelation.add(group);
                artist.save();
              }
            }
          });
        }
      }
    })
  },
};

module.exports = Account;

