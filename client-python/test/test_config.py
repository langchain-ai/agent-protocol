# coding: utf-8

"""
    Agent Protocol

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.6
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from ap_client.models.config import Config

class TestConfig(unittest.TestCase):
    """Config unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Config:
        """Test Config
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Config`
        """
        model = Config()
        if include_optional:
            return Config(
                tags = [
                    ''
                    ],
                recursion_limit = 56,
                configurable = ap_client.models.configurable.Configurable()
            )
        else:
            return Config(
        )
        """

    def testConfig(self):
        """Test Config"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
