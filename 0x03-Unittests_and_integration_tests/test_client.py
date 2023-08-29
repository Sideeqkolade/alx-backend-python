#!/usr/bin/env python3
"""
This module tests client.py
"""
import unittest
import requests
from unittest.mock import PropertyMock, patch, Mock
from typing import Dict
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class


class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google", {"key": "value"}),
        ("abc", {"key": "value"})
    ])
    def test_org(self, org_name: str, output: Dict) -> None:
        """Test the GithubOrgClient.org method"""
        expected_url = f"{GithubOrgClient.ORG_URL.format(org=org_name)}"
        with patch('client.get_json', return_value=output) as mock_get_json:
            client = GithubOrgClient(org_name)
            result = client.org
            mock_get_json.assert_called_once_with(expected_url)
            self.assertEqual(result, output)

    @parameterized.expand([
        ("google", ("https://api.github.com/orgs/adobe/repos")),
        ("abc", ("https://api.github.com/orgs/abc/repos")),
        ('Netflix', ("https://api.github.com/orgs/Netflix/repos"))
    ])
    def test_public_repos_url(self, org_name: str, output: str) -> None:
        """Test the GithubOrgClient.public-repos_url method"""
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = output
            client = GithubOrgClient(org_name)
            result = client._public_repos_url
            self.assertEqual(result, output)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test the GithubOrgClient public_repos method"""
        payload = {
            "repos_url": "https://api.github.com/orgs/google/repos",
            "repos": [
                {
                    "id": 7697149,
                    "node_id": "MDEwOlJlcG9zaXRvcnk3Njk3MTQ5",
                    "name": "episodes.dart",
                    "full_name": "google/episodes.dart",
                    "private": False,
                    "owner": {
                            "login": "google",
                            "id": 1342004,
                            },
                    "forks": 22,
                    "open_issues": 0,
                    "watchers": 12,
                    "default_branch": "master",
                },
                {
                    "id": 7776515,
                    "node_id": "MDEwOlJlcG9zaXRvcnk3Nzc2NTE1",
                    "name": "cpp-netlib",
                    "full_name": "google/cpp-netlib",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                        },
                    "forks": 59,
                    "open_issues": 0,
                    "watchers": 292,
                    "default_branch": "master",
                },
            ]
        }
        # print(anm(payload, (("repos"), )))
        mock_get_json.return_value = payload["repos"]
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as pmock:
            pmock.return_value = payload["repos_url"]
            # public_repo = GithubOrgClient("google").public_repos()
            # print(public_repo)
            self.assertEqual(GithubOrgClient("google").public_repos(),
                             ["episodes.dart", "cpp-netlib"], )
            pmock.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, license, key, ret):
        """Tests the has_license static method"""
        repo_to_check = GithubOrgClient.has_license(license, key)
        self.assertEqual(repo_to_check, ret)


@parameterized_class(('payload', 'output'), [
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache_repos': TEST_PAYLOAD[0][3]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class"""
    def setUp(self) -> None:
        self.patcher = patch('requests.get')
        self.mock_get = self.patcher.start()

    def tearDown(self) -> None:
        self.patcher.stop()
