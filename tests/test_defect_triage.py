import unittest

from coverity_mcp_server.coverity_client import CoverityClient


class SoapObject:
    pass


class FakeFactory:
    def create(self, _name):
        return SoapObject()


class FakeService:
    def __init__(self):
        self.update_arguments = None

    def getStreamDefects(self, merged_defect_ids, filter_spec):
        self.merged_defect_ids = merged_defect_ids
        self.filter_spec = filter_spec
        defect = SoapObject()
        defect.cid = 12345
        defect.id = SoapObject()
        return [defect]

    def updateStreamDefects(self, defect_ids, defect_state):
        self.update_arguments = (defect_ids, defect_state)


class FakeSoapClient:
    def __init__(self):
        self.factory = FakeFactory()
        self.service = FakeService()


class MarkDefectIntentionalTests(unittest.TestCase):
    def test_updates_only_the_requested_stream_defect(self):
        client = CoverityClient(
            "coverity.example.test",
            username="user",
            password="key",
        )
        soap_client = FakeSoapClient()
        client._create_defect_service_client = lambda: soap_client

        result = client._mark_defect_intentional_sync(12345, "main")

        self.assertEqual(
            soap_client.service.merged_defect_ids[0].cid,
            12345,
        )
        self.assertEqual(
            soap_client.service.filter_spec.streamIdList[0].name,
            "main",
        )
        defect_ids, defect_state = soap_client.service.update_arguments
        self.assertEqual(len(defect_ids), 1)
        classification = defect_state.defectStateAttributeValues[0]
        self.assertEqual(
            classification.attributeDefinitionId.name,
            "Classification",
        )
        self.assertEqual(classification.attributeValueId.name, "Intentional")
        self.assertEqual(
            result,
            {
                "cid": 12345,
                "stream_name": "main",
                "classification": "Intentional",
                "updated": True,
            },
        )

    def test_rejects_invalid_cid(self):
        client = CoverityClient(
            "coverity.example.test",
            username="user",
            password="key",
        )

        with self.assertRaises(ValueError):
            import asyncio

            asyncio.run(client.mark_defect_intentional(0, "main"))

    def test_marks_false_positive_in_the_requested_stream(self):
        client = CoverityClient(
            "coverity.example.test",
            username="user",
            password="key",
        )
        soap_client = FakeSoapClient()
        client._create_defect_service_client = lambda: soap_client

        result = client._mark_defect_false_positive_sync(12345, "main")

        defect_ids, defect_state = soap_client.service.update_arguments
        self.assertEqual(len(defect_ids), 1)
        classification = defect_state.defectStateAttributeValues[0]
        self.assertEqual(
            classification.attributeValueId.name,
            "False Positive",
        )
        self.assertEqual(
            result,
            {
                "cid": 12345,
                "stream_name": "main",
                "classification": "False Positive",
                "updated": True,
            },
        )
