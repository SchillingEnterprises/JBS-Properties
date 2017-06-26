namespace JohnBaxterSchillingProperties
{
    class Zillow : Listings
    {
      public string zEstimate;
      public string getSearchResults;
      public string zws-id;
      public int zpid = Zillow/key.zpid;
      public bool rentZEstimate = true;

      public string Address : base (addressNumber, streetAddress);
      public string CityStateZip : base (city, state, zipcode);


      // Connect to Zillow
      Zillow zillow = new Zillow
      {
          string GetSearchResultsURL = getSearchResults + "?zws-id" + zwid + "&address=" + Address + "&citystatezip=" + CityStateZip + "&rentzestimate=" + rentZEstimate;

          return (GetSearchResultsURL);


          string ZEstimateURL = zEstimate + "?zws-id=" + zws-id + "&zpid=" + zpid + "&rentzestimate=" + rentZEstimate;

          return (ZEstimateURL);
      }

      public static XmlDocument MakeRequest(string requestUrl)
      {
          try
          {
              HttpWebRequest request = WebRequest.Create(requestUrl) as HttpWebRequest;
              HttpWebResponse response = request.GetResponse() as HttpWebResponse;

              XmlDocument xmlDoc = new XmlDocument();
              xmlDoc.Load(response.GetResponseStream());
              return (xmlDoc);

          }
          catch (Exception e)
          {
              Console.WriteLine(e.Message);

              Console.Read();
              return null;
          }
      }

      static public void ProcessResponse(XmlDocument locationsResponse)
      {
      }

      //Create namespace manager
      XmlNamespaceManager nsmgr = new XmlNamespaceManager(locationsResponse.NameTable);
      nsmgr.AddNamespace("rest","http://schemas.microsoft.com/search/local/ws/rest/v1");

      var client = new WebClient();
      var content = client.DownloadData(GetSearchResultsURL);
    }
}
