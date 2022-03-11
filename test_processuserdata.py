import unittest
from processuserdata import ProcessUserData, StateStatsCounter
from app import parse_users_list
import json

class TestProcessUserData(unittest.TestCase):

    def setUp(self):
        with open ('test_data_files/small_json.json', 'r') as f:
            self.users_data = parse_users_list(json.load(f))

    def test_parse_users_list(self):
        with open ('test_data_files/small_json.json', 'r') as f2:
            data = parse_users_list(json.load(f2))

        self.assertEqual(type(data), list)

        self.assertEquals(data[0]['first_name'], 'Susan')
        self.assertEquals(data[0]['last_name'], 'Long')
        self.assertEquals(data[0]['gender'], 'female')
        self.assertEquals(data[0]['state'], 'California')
        self.assertEquals(data[0]['age'], 30)


    def test_get_gender_distribution(self):
        gender = ProcessUserData(self.users_data).get_gender_distribution()
        self.assertAlmostEqual(gender["female"], 100.0)
        self.assertAlmostEqual(gender["male"], 0)

    def test_get_name_distribution_AM_versus_NZ(self):
        last_name_distribution = ProcessUserData(self.users_data).get_name_distribution_AM_versus_NZ('last_name')
        first_name_distribution = ProcessUserData(self.users_data).get_name_distribution_AM_versus_NZ('first_name')

        self.assertDictEqual(last_name_distribution, {"A_to_M": 100.0, "N_to_Z": 0})






if __name__ == '__main__':
    unittest.main()