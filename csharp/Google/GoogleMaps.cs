namespace GoogleMaps
{
    class Declarations : Key
    {
      private readonly string key = GoogleMaps.Key.zpid;
      string GoogleMapsURL = @"https://maps.googleapis.com/maps/api/streetview?size=400x400&location=" + JBSProperties.Listings.Latitude + ", " + JBSProperties.Listings.Longitude + "&key=" + key;
    }

    class Operations
    {
      WebRequest request = WebRequest.Create(GoogleMapsURL);
      WebResponse response = request.GetResponse();
      Stream data = response.GetResponseStream();
      StreamReader reader = new StreamReader(data);

      // json-formatted string from maps api
      string responseFromServer = reader.ReadToEnd();
      response.Close();
    }
}
