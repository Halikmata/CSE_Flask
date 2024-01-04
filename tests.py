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

    def test_get_church_by_id(self):
        response = self.app.get("/church/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("test edit" in response.data.decode())
        
    def test_add_church(self):
        data = [{
                    "conference_id": 10,
                    "details": "This is a fourth test post in unit test adding two churches again.",
                },{
                    "conference_id": 20,
                    "details": "This is to be deleted.",
                }]
        response = self.app.post('/church', json=data)
        self.assertEqual(response.status_code, 201)
        
    # def test_add_church(self):
    #     data = {
    #                 "conference_id": 18,
    #                 "details": "This is a third test post in unit test adding only one church.",
    #             }
    #     response = self.app.post('/church', json=data)
    #     self.assertEqual(response.status_code, 201)


if __name__ == "__main__":
    unittest.main()
