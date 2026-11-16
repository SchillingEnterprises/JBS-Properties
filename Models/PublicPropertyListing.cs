namespace John_Baxter_Schilling.Models
{
    /// <summary>
    /// The complete allowlist of fields approved for anonymous property display.
    /// Add a field only after reviewing its public-disclosure implications.
    /// </summary>
    public class PublicPropertyListing
    {
        public string Address { get; set; }
        public string Status { get; set; }
    }
}
