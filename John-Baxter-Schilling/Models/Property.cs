namespace John_Baxter_Schilling.Models
{
    public class Property
    {
        public int AddressNumber { get; set; }
        public string StreetName { get; set; }
        public string City { get; set; }
        public string State { get; set; }
        public int ZipCode { get; set; }
        public bool RentStatus { get; set; }

        public string OfficialAddress
        {
            get
            {
                return AddressNumber + " " + StreetName + "|" + City + " " + State + " " + ZipCode;
            }
        }
    }
}