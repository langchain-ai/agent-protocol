# coding: utf-8

"""
    Agent Protocol

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.6
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from ap_client.api.agents_api import AgentsApi


class TestAgentsApi(unittest.TestCase):
    """AgentsApi unit test stubs"""

    def setUp(self) -> None:
        self.api = AgentsApi()

    def tearDown(self) -> None:
        pass

    def test_get_agent(self) -> None:
        """Test case for get_agent

        Get Agent
        """
        pass

    def test_get_agent_schemas(self) -> None:
        """Test case for get_agent_schemas

        Get Agent Schemas
        """
        pass

    def test_search_agents(self) -> None:
        """Test case for search_agents

        Search Agents
        """
        pass


if __name__ == '__main__':
    unittest.main()
