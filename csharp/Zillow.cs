namespace JohnBaxterSchillingProperties
{
    class Zillow
    {
      public string zestimate;
      public string zws-id;
      public int zpid;
      public bool rentzestimate;

      // Connect to Zillow
      Zillow zillow = new Zillow
      {
          return zestimate + "?zws-id=" + zws-id + "&zpid=" + zpid + "&rentzestimate=" + rentzestimate;
      }
    }
}
