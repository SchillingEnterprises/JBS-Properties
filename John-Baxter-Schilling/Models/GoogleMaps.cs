namespace John_Baxter_Schilling.Models
{
    public class GoogleMaps : Property
    {
        public static double Latitude { get; }
        public static double Longitude { get; }
        private static readonly string key = "AIzaSyDdNpQIIQNziuF5szq1DfRNKAUdNY3yNp4";
        public byte[] GoogleMap { get; }
        public string GoogleMapsURL = "https://maps.googleapis.com/maps/api/streetview?size=400x400&location=" + Latitude + ", " + Longitude + "&key=" + key;
    }
}