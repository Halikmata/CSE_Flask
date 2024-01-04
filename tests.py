import unittest
import warnings
from api import app


class MyAppTests(unittest.TestCase):
    
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_get_church(self):
        response = self.app.get("/church")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("test post" in response.data.decode())

    def test_getactors_by_id(self):
        response = self.app.get("/church/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("test edit" in response.data.decode())


if __name__ == "__main__":
    unittest.main()
