namespace John_Baxter_Schilling.Models
{
    public class Property
    {
        public int AddressNumber { get; set; }
        public string StreetName { get; set; }
        public string City { get; set; }
        public int ZipCode { get; set; }
        public bool RentStatus { get; set; }

        public enum State
        {
            KY = 0,
            IN = 1,
            AA = 2,
            AE = 3,
            AK = 4,
            AL = 5,
            AP = 6,
            AR = 7,
            AS = 8,
            AZ = 9,
            CA = 10,
            CO = 11,
            CT = 12,
            DC = 13,
            DE = 14,
            FL = 15,
            FM = 16,
            GA = 17,
            GU = 18,
            HI = 19,
            IA = 20,
            ID = 21,
            IL = 22,
            KS = 23,
            LA = 24,
            MA = 25,
            MD = 26,
            ME = 27,
            MH =28,
            MI = 29,
            MN = 30,
            MO = 31,
            MP = 32,
            MS = 33,
            MT = 34,
            NC = 35,
            ND = 36,
            NE = 37,
            NH = 38,
            NJ = 39,
            NM = 40,
            NV = 41,
            NY = 42,
            OH = 43,
            OK = 44,
            OR = 45,
            PA = 46,
            PR = 47,
            PW = 48,
            RI = 49,
            SC = 50,
            SD = 51,
            TN = 52,
            TX = 53,
            UT = 54,
            VA = 55,
            VI = 56,
            VT = 57,
            WA = 58,
            WI = 59,
            WV = 60,
            WY = 61
        }

        public string OfficialAddress
        {
            get
            {
                return AddressNumber + " " + StreetName + "|" + City + " " + State + " " + ZipCode;
            }
        }
    }
}
