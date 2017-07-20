using System;
using System.Xml;
using System.Xml.Serialization;
using System.ComponentModel;


namespace John_Baxter_Schilling.Models
{
    public class Zillow : Property
    {

        /// <remarks/>
        [Serializable()]
        [DesignerCategory("code")]
        [XmlType(AnonymousType = true)]
        [XmlRoot(Namespace = "", IsNullable = false)]
        public partial class links
        {

            private string homedetailsField;

            private string graphsanddataField;

            private string mapthishomeField;

            private string comparablesField;

            /// <remarks/>
            public string homedetails
            {
                get => homedetailsField;
                set => homedetailsField = value;
            }

            /// <remarks/>
            public string graphsanddata
            {
                get => graphsanddataField;
                set => graphsanddataField = value;
            }

            /// <remarks/>
            public string mapthishome
            {
                get => mapthishomeField;
                set => mapthishomeField = value;
            }

            /// <remarks/>
            public string comparables
            {
                get => comparablesField;
                set => comparablesField = value;
            }
        }

        /// <remarks/>
        [Serializable()]
        [DesignerCategory("code")]
        [XmlType(AnonymousType = true)]
        [XmlRoot(Namespace = "", IsNullable = false)]
        public partial class address
        {

            private string streetField;

            private ushort zipcodeField;

            private string cityField;

            private string stateField;

            private decimal latitudeField;

            private decimal longitudeField;

            /// <remarks/>
            public string street
            {
                get => streetField;
                set => streetField = value;
            }

            /// <remarks/>
            public ushort zipcode
            {
                get => zipcodeField;
                set => zipcodeField = value;
            }

            /// <remarks/>
            public string city
            {
                get => cityField;
                set => cityField = value;
            }

            /// <remarks/>
            public string state
            {
                get => stateField;
                set => stateField = value;
            }

            /// <remarks/>
            public decimal latitude
            {
                get => latitudeField;
                set => latitudeField = value;
            }

            /// <remarks/>
            public decimal longitude
            {
                get => longitudeField;
                set => longitudeField = value;
            }
        }

        /// <remarks/>
        [Serializable()]
        [DesignerCategory("code")]
        [XmlType(AnonymousType = true)]
        [XmlRoot(Namespace = "", IsNullable = false)]
        public partial class zestimate
        {

            private zestimateAmount amountField;

            private string lastupdatedField;

            private zestimateOneWeekChange oneWeekChangeField;

            private zestimateValueChange valueChangeField;

            private zestimateValuationRange valuationRangeField;

            private byte percentileField;

            /// <remarks/>
            public zestimateAmount amount
            {
                get => amountField;
                set => amountField = value;
            }

            /// <remarks/>
            [XmlElement("last-updated")]
            public string lastupdated
            {
                get => lastupdatedField;
                set => lastupdatedField = value;
            }

            /// <remarks/>
            public zestimateOneWeekChange oneWeekChange
            {
                get => oneWeekChangeField;
                set => oneWeekChangeField = value;
            }

            /// <remarks/>
            public zestimateValueChange valueChange
            {
                get => valueChangeField;
                set => valueChangeField = value;
            }

            /// <remarks/>
            public zestimateValuationRange valuationRange
            {
                get => valuationRangeField;
                set => valuationRangeField = value;
            }

            /// <remarks/>
            public byte percentile
            {
                get => percentileField;
                set => percentileField = value;
            }
        }

        /// <remarks/>
        [Serializable()]
        [DesignerCategory("code")]
        [XmlType(AnonymousType = true)]
        public partial class zestimateAmount
        {

            private string currencyField;

            private ushort valueField;

            /// <remarks/>
            [XmlAttribute()]
            public string currency
            {
                get => currencyField;
                set => currencyField = value;
            }

            /// <remarks/>
            [XmlText()]
            public ushort Value
            {
                get => valueField;
                set => valueField = value;
            }
        }

        /// <remarks/>
        [Serializable()]
        [DesignerCategory("code")]
        [XmlType(AnonymousType = true)]
        public partial class zestimateOneWeekChange
        {

            private bool deprecatedField;

            /// <remarks/>
            [XmlAttribute()]
            public bool deprecated
            {
                get => deprecatedField;
                set => deprecatedField = value;
            }
        }

        /// <remarks/>
        [Serializable()]
        [DesignerCategory("code")]
        [XmlType(AnonymousType = true)]
        public partial class zestimateValueChange
        {

            private byte durationField;

            private string currencyField;

            private short valueField;

            /// <remarks/>
            [XmlAttribute()]
            public byte duration
            {
                get => durationField;
                set => durationField = value;
            }

            /// <remarks/>
            [XmlAttribute()]
            public string currency
            {
                get => currencyField;
                set => currencyField = value;
            }

            /// <remarks/>
            [XmlText()]
            public short Value
            {
                get => valueField;
                set => valueField = value;
            }
        }

        /// <remarks/>
        [Serializable()]
        [DesignerCategory("code")]
        [XmlType(AnonymousType = true)]
        public partial class zestimateValuationRange
        {

            private zestimateValuationRangeLow lowField;

            private zestimateValuationRangeHigh highField;

            /// <remarks/>
            public zestimateValuationRangeLow low
            {
                get => lowField;
                set => lowField = value;
            }

            /// <remarks/>
            public zestimateValuationRangeHigh high
            {
                get => highField;
                set => highField = value;
            }
        }

        /// <remarks/>
        [Serializable()]
        [DesignerCategory("code")]
        [XmlType(AnonymousType = true)]
        public partial class zestimateValuationRangeLow
        {

            private string currencyField;

            private ushort valueField;

            /// <remarks/>
            [XmlAttribute()]
            public string currency
            {
                get => currencyField;
                set => currencyField = value;
            }

            /// <remarks/>
            [XmlText()]
            public ushort Value
            {
                get => valueField;
                set => valueField = value;
            }
        }

        /// <remarks/>
        [Serializable()]
        [DesignerCategory("code")]
        [XmlType(AnonymousType = true)]
        public partial class zestimateValuationRangeHigh
        {

            private string currencyField;

            private ushort valueField;

            /// <remarks/>
            [XmlAttribute()]
            public string currency
            {
                get => currencyField;
                set => currencyField = value;
            }

            /// <remarks/>
            [XmlText()]
            public ushort Value
            {
                get => valueField;
                set => valueField = value;
            }
        }

        /// <remarks/>
        [Serializable()]
        [DesignerCategory("code")]
        [XmlType(AnonymousType = true)]
        [XmlRoot(Namespace = "", IsNullable = false)]
        public partial class rentzestimate
        {

            private rentzestimateAmount amountField;

            private string lastupdatedField;

            private rentzestimateOneWeekChange oneWeekChangeField;

            private rentzestimateValueChange valueChangeField;

            private rentzestimateValuationRange valuationRangeField;

            /// <remarks/>
            public rentzestimateAmount amount
            {
                get => amountField;
                set => amountField = value;
            }

            /// <remarks/>
            [XmlElement("last-updated")]
            public string lastupdated
            {
                get => lastupdatedField;
                set => lastupdatedField = value;
            }

            /// <remarks/>
            public rentzestimateOneWeekChange oneWeekChange
            {
                get => oneWeekChangeField;
                set => oneWeekChangeField = value;
            }

            /// <remarks/>
            public rentzestimateValueChange valueChange
            {
                get => valueChangeField;
                set => valueChangeField = value;
            }

            /// <remarks/>
            public rentzestimateValuationRange valuationRange
            {
                get => valuationRangeField;
                set => valuationRangeField = value;
            }
        }

        /// <remarks/>
        [Serializable()]
        [DesignerCategory("code")]
        [XmlType(AnonymousType = true)]
        public partial class rentzestimateAmount
        {

            private string currencyField;

            private ushort valueField;

            /// <remarks/>
            [XmlAttribute()]
            public string currency
            {
                get => currencyField;
                set => currencyField = value;
            }

            /// <remarks/>
            [XmlText()]
            public ushort Value
            {
                get => valueField;
                set => valueField = value;
            }
        }

        /// <remarks/>
        [Serializable()]
        [DesignerCategory("code")]
        [XmlType(AnonymousType = true)]
        public partial class rentzestimateOneWeekChange
        {

            private bool deprecatedField;

            /// <remarks/>
            [XmlAttribute()]
            public bool deprecated
            {
                get => deprecatedField;
                set => deprecatedField = value;
            }
        }

        /// <remarks/>
        [Serializable()]
        [DesignerCategory("code")]
        [XmlType(AnonymousType = true)]
        public partial class rentzestimateValueChange
        {

            private byte durationField;

            private string currencyField;

            private byte valueField;

            /// <remarks/>
            [XmlAttribute()]
            public byte duration
            {
                get => durationField;
                set => durationField = value;
            }

            /// <remarks/>
            [XmlAttribute()]
            public string currency
            {
                get => currencyField;
                set => currencyField = value;
            }

            /// <remarks/>
            [XmlText()]
            public byte Value
            {
                get => valueField;
                set => valueField = value;
            }
        }

        /// <remarks/>
        [Serializable()]
        [DesignerCategory("code")]
        [XmlType(AnonymousType = true)]
        public partial class rentzestimateValuationRange
        {

            private rentzestimateValuationRangeLow lowField;

            private rentzestimateValuationRangeHigh highField;

            /// <remarks/>
            public rentzestimateValuationRangeLow low
            {
                get => lowField;
                set => lowField = value;
            }

            /// <remarks/>
            public rentzestimateValuationRangeHigh high
            {
                get => highField;
                set => highField = value;
            }
        }

        /// <remarks/>
        [Serializable()]
        [DesignerCategory("code")]
        [XmlType(AnonymousType = true)]
        public partial class rentzestimateValuationRangeLow
        {

            private string currencyField;

            private ushort valueField;

            /// <remarks/>
            [XmlAttribute()]
            public string currency
            {
                get => currencyField;
                set => currencyField = value;
            }

            /// <remarks/>
            [XmlText()]
            public ushort Value
            {
                get => valueField;
                set => valueField = value;
            }
        }

        /// <remarks/>
        [Serializable()]
        [DesignerCategory("code")]
        [XmlType(AnonymousType = true)]
        public partial class rentzestimateValuationRangeHigh
        {

            private string currencyField;

            private ushort valueField;

            /// <remarks/>
            [XmlAttribute()]
            public string currency
            {
                get => currencyField;
                set => currencyField = value;
            }

            /// <remarks/>
            [XmlText()]
            public ushort Value
            {
                get => valueField;
                set => valueField = value;
            }
        }

        /// <remarks/>
        [Serializable()]
        [DesignerCategory("code")]
        [XmlType(AnonymousType = true)]
        [XmlRoot(Namespace = "", IsNullable = false)]
        public partial class localRealEstate
        {

            private localRealEstateRegion regionField;

            /// <remarks/>
            public localRealEstateRegion region
            {
                get => regionField;
                set => regionField = value;
            }
        }

        /// <remarks/>
        [Serializable()]
        [DesignerCategory("code")]
        [XmlType(AnonymousType = true)]
        public partial class localRealEstateRegion
        {

            private string zindexValueField;

            private localRealEstateRegionLinks linksField;

            private string nameField;

            private uint idField;

            private string typeField;

            /// <remarks/>
            public string zindexValue
            {
                get => zindexValueField;
                set => zindexValueField = value;
            }

            /// <remarks/>
            public localRealEstateRegionLinks links
            {
                get => linksField;
                set => linksField = value;
            }

            /// <remarks/>
            [XmlAttribute()]
            public string name
            {
                get => nameField;
                set => nameField = value;
            }

            /// <remarks/>
            [XmlAttribute()]
            public uint id
            {
                get => idField;
                set => idField = value;
            }

            /// <remarks/>
            [XmlAttribute()]
            public string type
            {
                get => typeField;
                set => typeField = value;
            }
        }

        /// <remarks/>
        [Serializable()]
        [DesignerCategory("code")]
        [XmlType(AnonymousType = true)]
        public partial class localRealEstateRegionLinks
        {

            private string overviewField;

            private string forSaleByOwnerField;

            private string forSaleField;

            /// <remarks/>
            public string overview
            {
                get => overviewField;
                set => overviewField = value;
            }

            /// <remarks/>
            public string forSaleByOwner
            {
                get => forSaleByOwnerField;
                set => forSaleByOwnerField = value;
            }

            /// <remarks/>
            public string forSale
            {
                get => forSaleField;
                set => forSaleField = value;
            }
        }

        /// <remarks/>
        [Serializable()]
        [DesignerCategory("code")]
        [XmlType(AnonymousType = true)]
        [XmlRoot(Namespace = "", IsNullable = false)]
        public partial class regions
        {

            private uint zipcodeidField;

            private ushort cityidField;

            private ushort countyidField;

            private byte stateidField;

            /// <remarks/>
            [XmlElement("zipcode-id")]
            public uint Zipcodeid
            {
                get => zipcodeidField;
                set => zipcodeidField = value;
            }

            /// <remarks/>
            [XmlElement("city-id")]
            public ushort Cityid
            {
                get => cityidField;
                set => cityidField = value;
            }

            /// <remarks/>
            [XmlElement("county-id")]
            public ushort Countyid
            {
                get => countyidField;
                set => countyidField = value;
            }

            /// <remarks/>
            [XmlElement("state-id")]
            public byte Stateid
            {
                get => stateidField;
                set => stateidField = value;
            }
        }


        public string zEstimate { get; }
        public int zpid { get; set; }

        public bool rentZEstimate = true;
        private static readonly string zwsid = "X1-ZWz1fsyqikrsi3_6sext";

        public string ZillowPath => "?zws-id" + zwsid + "&address=" + AddressNumber + StreetName + "&citystatezip=" + City + State + ZipCode + "&rentzestimate=" + rentZEstimate;
    }
}
