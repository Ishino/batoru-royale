import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TestClient(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://localhost:5000")
        self.assertIn("Batoru", driver.title)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
