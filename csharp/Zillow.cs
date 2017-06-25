namespace JohnBaxterSchillingProperties
{
    class Zillow : Listings
    {
      public string zEstimate;
      public string getSearchResults;
      public string zws-id;
      public int zpid;
      public bool rentZEstimate;

      public string Address : base (addressNumber, streetAddress);
      public string CityStateZip : base (city, state, zipcode);
      rentZEstimate = true;

      // Connect to Zillow
      Zillow zillow = new Zillow
      {
          string GetSearchResultsURL = getSearchResults + "?zws-id" + zwid + "&address=" + Address + "&citystatezip=" + CityStateZip + "&rentzestimate=" + rentZEstimate;

          string ZEstimateURL = zEstimate + "?zws-id=" + zws-id + "&zpid=" + zpid + "&rentzestimate=" + rentZEstimate;
      }

      var client = new WebClient();
      var content = client.DownloadData(GetSearchResultsURL);
    }
}
