import asyncio
import unittest

from coverity_mcp_server.coverity_client import CoverityClient


class DefectSearchTests(unittest.TestCase):
    def test_file_path_uses_coverity_file_filter(self):
        client = CoverityClient(
            "coverity.example.test",
            username="user",
            password="password",
        )
        request = {}

        async def make_request(method, endpoint, params=None, data=None):
            request.update(
                method=method,
                endpoint=endpoint,
                params=params,
                data=data,
            )
            return {"issues": []}

        client._make_request = make_request

        asyncio.run(client.get_defects(file_path="src/authentication"))

        self.assertEqual(request["method"], "POST")
        self.assertEqual(request["endpoint"], "/api/v2/issues/search")
        self.assertEqual(request["params"], {"rowCount": 100})
        self.assertEqual(
            request["data"],
            {
                "filters": [
                    {
                        "columnKey": "file",
                        "matchMode": "subString",
                        "matchers": [
                            {
                                "class": "String",
                                "pattern": "src/authentication",
                            }
                        ],
                    }
                ]
            },
        )
