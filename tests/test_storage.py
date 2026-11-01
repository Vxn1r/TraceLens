from tracelens.models import Observation
from tracelens.storage.sqlite_store import SQLiteStore


def test_observation_round_trip_in_sqlite():
    with SQLiteStore(":memory:") as store:
        observation = Observation(
            target="example.com",
            category="DNS A",
            value="192.0.2.10",
            source="System-configured DNS resolver",
            method="DNS query: A",
        )
        assert store.add_many([observation]) == 1
        assert store.count("example.com") == 1
        saved = store.list_observations("example.com")

    assert len(saved) == 1
    assert saved[0].value == "192.0.2.10"
    assert saved[0].category == "DNS A"
    assert saved[0].id is not None


def test_empty_insert_is_safe():
    with SQLiteStore(":memory:") as store:
        assert store.add_many([]) == 0
        assert store.count() == 0
