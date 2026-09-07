import asyncio
import unittest

from coverity_mcp_server.coverity_client import CoverityClient


class DefectSearchTests(unittest.TestCase):
    def test_search_filters_use_coverity_issue_search_schema(self):
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

        asyncio.run(
            client.get_defects(
                filters={"streamId": "Eddynet-CPP_qt6", "status": "New"},
                file_path="zwidget/zwidget/messagedialogbase.cpp",
            )
        )

        self.assertEqual(request["method"], "POST")
        self.assertEqual(request["endpoint"], "/api/v2/issues/search")
        self.assertEqual(request["params"], {"rowCount": 100})
        self.assertEqual(
            request["data"],
            {
                "filters": [
                    {
                        "columnKey": "streams",
                        "matchMode": "oneOrMoreMatch",
                        "matchers": [
                            {
                                "class": "Stream",
                                "name": "Eddynet-CPP_qt6",
                                "type": "nameMatcher",
                            }
                        ],
                    },
                    {
                        "columnKey": "status",
                        "matchMode": "oneOrMoreMatch",
                        "matchers": [{"key": "New", "type": "keyMatcher"}],
                    },
                    {
                        "columnKey": "file",
                        "matchMode": "subString",
                        "matchers": [
                            {
                                "class": "String",
                                "pattern": "zwidget/zwidget/messagedialogbase.cpp",
                            }
                        ],
                    },
                ],
                "snapshotScope": {
                    "show": {
                        "scope": "last()",
                        "includeOutdatedSnapshots": False,
                    }
                },
            },
        )
