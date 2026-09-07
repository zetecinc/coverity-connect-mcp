import asyncio
import unittest

from coverity_mcp_server.coverity_client import CoverityClient


class DefectSearchTests(unittest.TestCase):
    def test_search_filters_use_coverity_v3_issue_search_schema(self):
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
                filters={
                    "projectId": "10002",
                    "streamId": "Eddynet-CPP_qt6",
                    "status": "New",
                },
                file_path="zwidget/zwidget/messagedialogbase.cpp",
            )
        )

        self.assertEqual(request["method"], "POST")
        self.assertEqual(request["endpoint"], "/api/v3/issues/search")
        self.assertEqual(
            request["params"],
            {
                "includeColumnLabels": "false",
                "offset": 0,
                "queryType": "bySnapshot",
                "rowCount": 100,
                "sortColumn": "firstDetected",
                "sortOrder": "desc",
                "locale": "en_US",
            },
        )
        self.assertEqual(
            request["data"],
            {
                "filters": [
                    {
                        "columnKey": "project",
                        "matchMode": "oneOrMoreMatch",
                        "matchers": [{"type": "idMatcher", "id": "10002"}],
                    },
                    {
                        "columnKey": "streams",
                        "matchMode": "oneOrMoreMatch",
                        "matchers": [
                            {
                                "class": "Stream",
                                "type": "nameMatcher",
                                "name": "Eddynet-CPP_qt6",
                            }
                        ],
                    },
                    {
                        "columnKey": "status",
                        "matchMode": "oneOrMoreMatch",
                        "matchers": [{"type": "keyMatcher", "key": "New"}],
                    },
                    {
                        "columnKey": "displayFile",
                        "matchMode": "oneOrMoreMatch",
                        "matchers": [
                            {
                                "type": "keyMatcher",
                                "key": "*zwidget/zwidget/messagedialogbase.cpp*",
                            }
                        ],
                    },
                ],
                "columns": [
                    "cid",
                    "displayType",
                    "displayImpact",
                    "status",
                    "firstDetected",
                    "classification",
                    "severity",
                    "action",
                    "displayCategory",
                    "displayFunction",
                    "displayFile",
                ],
                "snapshotScope": {
                    "show": {
                        "scope": "last()",
                        "includeOutdatedSnapshots": False,
                    },
                    "compareTo": {
                        "scope": "",
                        "includeOutdatedSnapshots": False,
                    },
                },
            },
        )

    def test_search_normalizes_v3_rows(self):
        client = CoverityClient(
            "coverity.example.test",
            username="user",
            password="key",
        )

        async def make_request(method, endpoint, params=None, data=None):
            return {
                "offset": 0,
                "totalRows": 1,
                "rows": [[
                    {"key": "cid", "value": "206296"},
                    {"key": "status", "value": "New"},
                    {
                        "key": "displayFile",
                        "value": "/zwidget/zwidget/messagedialogbase.cpp",
                    },
                ]],
            }

        client._make_request = make_request

        defects = asyncio.run(client.get_defects(file_path="messagedialogbase.cpp"))

        self.assertEqual(
            defects,
            [{
                "cid": "206296",
                "status": "New",
                "displayFile": "/zwidget/zwidget/messagedialogbase.cpp",
            }],
        )
