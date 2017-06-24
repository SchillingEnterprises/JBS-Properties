var  Zillow  = require ('node-zillow'),
      mapsapi = require ('google-maps-api' )( 'AIzaSyDdNpQIIQNziuF5szq1DfRNKAUdNY3yNp4');

mapsapi().then( function( maps ) {

  //use the google.maps object as you please
});

var zillow = new Zillow({{zws-id}})
var parameters = {
  zpid: {{zpid}}
};

zillow.get('GetZestimate', parameters)
  .then(function(results) {
    return results;
    // results here is an object { message: {}, request: {}, response: {}}
  })
