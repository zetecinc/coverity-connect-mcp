import asyncio
import os
import unittest
from unittest.mock import patch

from click.testing import CliRunner

from coverity_mcp_server.coverity_client import CoverityClient
from coverity_mcp_server.coverity_client_production import (
    CoverityClient as ProductionCoverityClient,
)
from coverity_mcp_server import main, main_production


class FakeResponse:
    status = 200

    async def json(self):
        return {}


class FakeRequest:
    async def __aenter__(self):
        return FakeResponse()

    async def __aexit__(self, exc_type, exc_value, traceback):
        return False


class FakeSession:
    def __init__(self):
        self.request_kwargs = None

    def request(self, _method, _url, **kwargs):
        self.request_kwargs = kwargs
        return FakeRequest()


class DirectConnectionTests(unittest.TestCase):
    def test_cli_preserves_environment_configuration_without_options(self):
        environment = {
            "COVERITY_HOST": "coverity.example.test",
            "COVERITY_PORT": "8443",
            "COVERITY_SSL": "true",
            "COVAUTHUSER": "user",
            "COVAUTHKEY": "key",
        }

        with (
            patch.dict(os.environ, environment, clear=False),
            patch.object(main, "run_server") as run_server,
        ):
            result = CliRunner().invoke(main.cli)

            self.assertEqual(result.exit_code, 0, result.output)
            run_server.assert_called_once_with()
            self.assertEqual(os.environ["COVERITY_HOST"], "coverity.example.test")
            self.assertEqual(os.environ["COVERITY_PORT"], "8443")
            self.assertEqual(os.environ["COVERITY_SSL"], "true")

    def test_cli_options_override_environment_configuration(self):
        environment = {
            "COVERITY_HOST": "coverity.example.test",
            "COVERITY_PORT": "8443",
            "COVERITY_SSL": "true",
        }

        with (
            patch.dict(os.environ, environment, clear=False),
            patch.object(main, "run_server"),
        ):
            result = CliRunner().invoke(
                main.cli,
                ["--host", "other.example.test", "--port", "8080", "--no-ssl"],
            )

            self.assertEqual(result.exit_code, 0, result.output)
            self.assertEqual(os.environ["COVERITY_HOST"], "other.example.test")
            self.assertEqual(os.environ["COVERITY_PORT"], "8080")
            self.assertEqual(os.environ["COVERITY_SSL"], "False")

    def test_initializers_honor_configured_port_and_ssl(self):
        environment = {
            "COVERITY_HOST": "sq-buildsrv02.zetec.com",
            "COVERITY_PORT": "8080",
            "COVERITY_SSL": "false",
            "COVAUTHUSER": "user",
            "COVAUTHKEY": "key",
        }

        for module in (main, main_production):
            with self.subTest(module=module.__name__):
                with (
                    patch.dict(os.environ, environment, clear=False),
                    patch.object(module, "CoverityClient") as client_class,
                ):
                    module.coverity_client = None
                    module.initialize_client()

                self.assertEqual(client_class.call_args.kwargs["port"], 8080)
                self.assertFalse(client_class.call_args.kwargs["use_ssl"])
                module.coverity_client = None

    def test_requests_ignore_proxy_environment_variables(self):
        for client_class in (CoverityClient, ProductionCoverityClient):
            with self.subTest(client_class=client_class.__module__):
                client = client_class(
                    "coverity.example.test",
                    username="user",
                    password="key",
                )
                session = FakeSession()

                async def get_session():
                    return session

                client._get_session = get_session
                with patch.dict(
                    os.environ,
                    {
                        "HTTP_PROXY": "http://proxy.example.test:3128",
                        "HTTPS_PROXY": "http://proxy.example.test:3128",
                        "PROXY_HOST": "proxy.example.test",
                        "PROXY_PORT": "3128",
                    },
                ):
                    asyncio.run(client._make_request("GET", "/api/v2/projects"))

                self.assertNotIn("proxy", session.request_kwargs)

    def test_sessions_do_not_trust_proxy_environment_variables(self):
        for client_class in (CoverityClient, ProductionCoverityClient):
            with self.subTest(client_class=client_class.__module__):
                client = client_class(
                    "coverity.example.test",
                    username="user",
                    password="key",
                )
                with patch(
                    f"{client_class.__module__}.aiohttp.ClientSession"
                ) as session_class:
                    asyncio.run(client._get_session())

                self.assertFalse(session_class.call_args.kwargs["trust_env"])
