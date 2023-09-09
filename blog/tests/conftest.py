import os

import pytest

os.environ.setdefault(
    "EDMERALD_SETTINGS_MODULE", "blog.configs.testing.settings.TestingAppSettings"
)


@pytest.fixture(scope="module")
def anyio_backend():
    return ("asyncio", {"debug": True})
