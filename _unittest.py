import base64
import json
import time
import unittest
import os
import requests

import src.config as cfg


class TestTemplateSanic(unittest.TestCase):
    def setUp(self):
        print('setUp...')

    def tearDown(self):
        print('\ntearDown... \n')

    # @unittest.skip(u"强制跳过示例")
    def test_server_200(self):
        pass


if __name__ == '__main__':
    unittest.main()
