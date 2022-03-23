from asynctest import TestCase as AsyncTestCase
from asynctest import mock as async_mock

from ..cache import ProfileCache


class TestProfileCache(AsyncTestCase):
    async def setUp(self):
        pass

    async def test_get_not_in_cache(self):
        cache = ProfileCache(1)

        assert cache.get("1") is None

    async def test_put_get_in_cache(self):
        cache = ProfileCache(1)

        profile = async_mock.MagicMock()
        await cache.put("1", profile)

        assert cache.get("1") is profile

    async def test_remove(self):
        cache = ProfileCache(1)

        profile = async_mock.MagicMock()
        await cache.put("1", profile)

        assert cache.get("1") is profile

        cache.remove("1")

        assert cache.get("1") is None

    async def test_has_true(self):
        cache = ProfileCache(1)

        profile = async_mock.MagicMock()

        assert cache.has("1") is False
        await cache.put("1", profile)
        assert cache.has("1") is True

    async def test_cleanup(self):
        cache = ProfileCache(1)

        profile1 = async_mock.MagicMock()
        profile2 = async_mock.MagicMock()

        await cache.put("1", profile1)

        assert len(cache.profiles) == 1

        await cache.put("2", profile2)

        assert len(cache.profiles) == 1
        assert cache.get("1") == None

    async def test_cleanup_lru(self):
        cache = ProfileCache(3)

        profile1 = async_mock.MagicMock()
        profile2 = async_mock.MagicMock()
        profile3 = async_mock.MagicMock()
        profile4 = async_mock.MagicMock()

        await cache.put("1", profile1)
        await cache.put("2", profile2)
        await cache.put("3", profile3)

        assert len(cache.profiles) == 3

        cache.get("1")

        await cache.put("4", profile4)

        assert len(cache.profiles) == 3
        assert cache.get("1") == profile1
        assert cache.get("2") == None
        assert cache.get("3") == profile3
        assert cache.get("4") == profile4
