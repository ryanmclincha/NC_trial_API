from app import parse_users_list
import unittest
import json


class TestApp(unittest.TestCase):

    def test_parse_users_list(self):
        with open ('test_data_files/small_json.json', 'r') as f:
            data = parse_users_list(json.load(f))

        self.assertEqual(type(data), list)

        self.assertEquals(data[0]['first_name'], 'Susan')
        self.assertEquals(data[0]['last_name'], 'Long')
        self.assertEquals(data[0]['gender'], 'female')
        self.assertEquals(data[0]['state'], 'California')
        self.assertEquals(data[0]['age'], 30)


if __name__ == '__main__':
    unittest.main()