# coding: utf-8

"""
    Agent Protocol

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.6
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from ap_client.models.store_delete_request import StoreDeleteRequest

class TestStoreDeleteRequest(unittest.TestCase):
    """StoreDeleteRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> StoreDeleteRequest:
        """Test StoreDeleteRequest
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `StoreDeleteRequest`
        """
        model = StoreDeleteRequest()
        if include_optional:
            return StoreDeleteRequest(
                namespace = [
                    ''
                    ],
                key = ''
            )
        else:
            return StoreDeleteRequest(
                key = '',
        )
        """

    def testStoreDeleteRequest(self):
        """Test StoreDeleteRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
