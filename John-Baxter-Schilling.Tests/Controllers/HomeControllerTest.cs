using System.Web.Mvc;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using John_Baxter_Schilling;
using John_Baxter_Schilling.Controllers;

namespace John_Baxter_Schilling.Tests.Controllers
{
    [TestClass]
    public class HomeControllerTest
    {
        [TestMethod]
        public void Index()
        {
            // Arrange
            HomeController controller = new HomeController();

            // Act
            ViewResult result = controller.Index() as ViewResult;

            // Assert
            Assert.IsNotNull(result);
            Assert.AreEqual("Home Page", result.ViewBag.Title);
        }
    }
}
