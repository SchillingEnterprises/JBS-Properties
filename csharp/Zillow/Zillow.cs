namespace Zillow
{
    class Declarations : Key
    {
      public string zEstimate;
      public string getSearchResults;
      private string zwsid;

      private readonly bool rentZEstimate = true;
      private readonly int zpid = Zillow.Key.zpid;
      private readonly string address = JBSProperties.Listings.addressNumber + JBSProperties.Listings.streetAddress;
      private readonly string cityStateZip = JBSProperties.Listings.city + JBSProperties.Listings.state +
      JBSProperties.Listings.zipCode;
    }

    class GetSearchResults
    {
      string GetSearchResultsURL = getSearchResults + "?zws-id" + zws-id + "&address=" + address + "&citystatezip=" + cityStateZip + "&rentzestimate=" + rentZEstimate;
      return (GetSearchResultsURL);
    }

    class ZEstimate
    {
      string ZEstimateURL = zEstimate + "?zws-id=" + zws-id + "&zpid=" + zpid + "&rentzestimate=" + rentZEstimate;
      return (ZEstimateURL);
    }

      public static XmlDocument MakeRequest (string requestUrl)
      {
          try
          {
              HttpWebRequest request = WebRequest.Create (requestUrl) as HttpWebRequest;
              HttpWebResponse response = request.GetResponse () as HttpWebResponse;

              XmlDocument xmlDoc = new XmlDocument ();
              xmlDoc.Load (response.GetResponseStream ());
              return (xmlDoc);

          }
          catch (Exception e)
          {
              Console.WriteLine (e.Message);

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
