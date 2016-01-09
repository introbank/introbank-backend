
var Account = {
  addMemberRelations : function(group){
    //console.log("addMemberRelations start. group=" + group.id);
    var membersQuery = group.relation("members").query();
    membersQuery.find({
      success: function(artists) {
        var artistList = [];
        for(i = 0; i < artists.length ; i++){
          //console.log("addMemberRelations start. artist=" + artists[i].id);
          var groupRelation = artists[i].relation("groups");
          groupRelation.add(group);
          artistList.push(artists[i]);
        }
        Parse.Object.saveAll(artistList, {
          success: function(results) {
          // All the objects were saved.
          console.log("saveAll group::" + group.id + " success.");
          },
          error: function(results, error) {
          console.log("saveAll group::" + group.id + " faild.");
          console.log(error);
          // An error occurred while saving one of the objects.
          }, 
        });
      },
      error: function(artists, error) {
        console.log(error);
      }
    }
    );

  },
};

module.exports = Account;

