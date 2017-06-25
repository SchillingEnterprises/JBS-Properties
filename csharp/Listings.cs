using System;

namespace JohnBaxterSchillingProperties
{
    class Listing
    {
      public int addressNumber;
      public string streetAddress;
      public string city;
      public string state;
      public int zipcode;

      Listing listing = new Listing (int addressNumber, string streetAddress, string city, string state, int zipcode)
      {
        Console.WriteLine(addressNumber + " " + streetAddress);
        Console.WriteLine(city + " " + state + ", " + zipcode);
        Console.WriteLine(Zillow.url);
      }
    }
}
