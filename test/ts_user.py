# -*- coding: utf-8 -*-
import unittest
import requests

class Test_user(unittest.TestCase):
    # before
    def setUp(self):
        print('Case Before')
        self.headers = {'Content-Type': 'application/json'}
        self.headers['Content-Type'] = 'application/json'
        self.host_url = "http://localhost:3050"
        payload = '{"user": "op", "pwd": "123"}'
        req = requests.post(self.host_url + "/api/user/login", headers=self.headers, data=payload)
        user_list = req.json()
        self.token = user_list["data"]["accessToken"]
        self.headers["Authorization"] = "Bearer " + self.token
        print('Case Before')
        pass

    def test_get_info(self):
        res = requests.get(self.host_url + "/api/user/info", headers=self.headers)
        result = res.json()
        print(result)

if __name__ == "__main__":
    unittest.main()