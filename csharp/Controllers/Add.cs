namespace JBSProperties
{
    class Add
    {
      Console.WriteLine ("Please enter the new property's street number");
      int JBSProperties.Listings.addressNumber = Console.ReadLine();

      Console.WriteLine ("Please enter the new property's street name");
      string JBSProperties.Listings.streetAddress = Console.ReadLine();

      Console.WriteLine ("Please enter the new property's city");
      string JBSProperties.Listings.city = Console.ReadLine();

      Console.WriteLine ("Please enter the new property's state");
      string JBSProperties.Listings.state = Console.ReadLine();

      Console.WriteLine ("Please enter the new property's zip code");
      int JBSProperties.Listings.zipCode = Console.ReadLine();

      Console.WriteLine ("Has the new property been rented yet?");
      bool JBSProperties.Listings.rented = Console.ReadLine();
    }
}
