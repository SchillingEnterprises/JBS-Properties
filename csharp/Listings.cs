using System;

namespace JBSProperties
{
  class public static void Main(){
    class Listing : Zillow, GoogleMaps
    {

      public string Address : base (Address);
      public string CityStateZip : base (CityStateZip);
      public double Latitude : base (Latitude);
      public double Longitude : base (Longitude);

      Listing listing = new Listing (int addressNumber, string streetAddress, string city, string state, int zipCode)
      {
        Console.WriteLine (addressNumber + " " + streetAddress);
        Console.WriteLine (city + " " + state + ", " + zipCode);
      }
    }
  }
}
