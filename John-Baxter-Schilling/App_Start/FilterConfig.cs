using System.Web;
using System.Web.Mvc;

namespace John_Baxter_Schilling
{
    public class FilterConfig
    {
        public static void RegisterGlobalFilters(GlobalFilterCollection filters)
        {
            filters.Add(new HandleErrorAttribute());
        }
    }
}
