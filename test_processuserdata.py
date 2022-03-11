import unittest
from processuserdata import ProcessUserData, StateStatsCounter, binary_search_right_most, binary_search_state_for_index
from app import parse_users_list
import json


# I'm still working on learning proper Unit Testing practices
class TestProcessUserData(unittest.TestCase):

    def setUp(self):
        with open ('test_data_files/small_json.json', 'r') as f:
            self.users_data = parse_users_list(json.load(f))
        with open ('test_data_files/medium_json.json', 'r') as f:
            self.users_data_medium = parse_users_list(json.load(f))


    def test_get_gender_distribution(self):
        gender = ProcessUserData(self.users_data).get_gender_distribution()
        self.assertAlmostEqual(gender["female"], 100.0)
        self.assertAlmostEqual(gender["male"], 0)

    def test_get_name_distribution_AM_versus_NZ(self):
        last_name_distribution = ProcessUserData(self.users_data).get_name_distribution_AM_versus_NZ('last_name')
        first_name_distribution = ProcessUserData(self.users_data).get_name_distribution_AM_versus_NZ('first_name')

        self.assertDictEqual(last_name_distribution, {"A_to_M": 100.0, "N_to_Z": 0})
        self.assertDictEqual(first_name_distribution, {"A_to_M": 0, "N_to_Z": 100.0})

        last_name_distribution_medium = ProcessUserData(self.users_data_medium).get_name_distribution_AM_versus_NZ('last_name')
        first_name_distribution_medium = ProcessUserData(self.users_data_medium).get_name_distribution_AM_versus_NZ('first_name')

        self.assertDictEqual(last_name_distribution_medium, {"A_to_M": 65.0, "N_to_Z": 35.0})
        self.assertDictEqual(first_name_distribution_medium, {"A_to_M": 70.0, "N_to_Z": 30.0})

    def test_binary_search_right_most(self):
        count_lower_small = binary_search_right_most(self.users_data, 'last_name', 'N')
        self.assertEqual(count_lower_small, 1)
        count_lower_small = binary_search_right_most(self.users_data, 'first_name', 'N')
        self.assertEqual(count_lower_small, 0)

        data_sorted = sorted(
            self.users_data_medium, key=lambda i: str(i['first_name'])
        )  
        count_lower_medium = binary_search_right_most(data_sorted, 'first_name', 'N')
        self.assertEqual(count_lower_medium, 14)

        data_sorted = sorted(
            self.users_data_medium, key=lambda i: str(i['last_name'])
        )  
        count_lower_medium = binary_search_right_most(data_sorted, 'last_name', 'N')
        self.assertEqual(count_lower_medium, 13)

    def test_get_percentage_of_people_ten_most_populous_states(self):
        top_ten = ProcessUserData(self.users_data).get_percentage_of_people_ten_most_populous_states()
        self.assertEqual(top_ten["California"], 100.0)
        top_ten = ProcessUserData(self.users_data_medium).get_percentage_of_people_ten_most_populous_states()
        self.assertEqual(top_ten['Florida'], 15.0)


    






if __name__ == '__main__':
    unittest.main()