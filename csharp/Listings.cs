using System;

namespace JBSProperties
{
    class Listing : Zillow
    {

      public string Address : base (Address);
      public string CityStateZip : base (CityStateZip);

      Listing listing = new Listing (int addressNumber, string streetAddress, string city, string state, int zipCode)
      {
        Console.WriteLine(addressNumber + " " + streetAddress);
        Console.WriteLine(city + " " + state + ", " + zipCode);
      }
    }
}
