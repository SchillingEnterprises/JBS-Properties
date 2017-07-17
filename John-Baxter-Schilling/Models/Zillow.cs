namespace John_Baxter_Schilling.Models
{
    public class Zillow : Property
    {
        public string zEstimate { get; }
        public int zpid { get; set; }

        public bool rentZEstimate = true;
        private static readonly string zwsid = "X1-ZWz1fsyqikrsi3_6sext";

        public string ZillowPath => "?zws-id" + zwsid + "&address=" + AddressNumber + StreetName + "&citystatezip=" + City + State + ZipCode + "&rentzestimate=" + rentZEstimate;
    }
}