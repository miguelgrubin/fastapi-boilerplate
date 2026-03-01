from datetime import datetime

from src.blog.infrastructure.storage.sql_tables import metadata
from src.shared.infrastructure.services.sql_service_sqlalchemy import SqlServiceSqlAlchemy


def test_should_connect_and_disconnect():
    service = SqlServiceSqlAlchemy("sqlite:///:memory:", metadata)
    service.connect()

    assert service._engine is not None

    service.disconnect()

    assert service._engine is None


def test_should_raise_when_session_used_before_connect():
    service = SqlServiceSqlAlchemy("sqlite:///:memory:", metadata)

    try:
        with service.session():
            pass
        assert False, "Should have raised RuntimeError"
    except RuntimeError as e:
        assert "not connected" in str(e)


def test_should_provide_working_session():
    service = SqlServiceSqlAlchemy("sqlite:///:memory:", metadata)
    service.connect()

    # Create tables for the test
    metadata.create_all(service._engine)

    with service.session() as conn:
        result = conn.execute(metadata.tables["users"].select())
        rows = result.fetchall()
        assert rows == []

    service.disconnect()


def test_should_rollback_on_exception():
    service = SqlServiceSqlAlchemy("sqlite:///:memory:", metadata)
    service.connect()

    metadata.create_all(service._engine)

    try:
        with service.session() as conn:
            conn.execute(
                metadata.tables["users"]
                .insert()
                .values(
                    id="1",
                    email="test@test.com",
                    username="test",
                    password_hash="hash",
                    bio=None,
                    image=None,
                    following="[]",
                    followers="[]",
                    created_at=datetime(2024, 1, 1),
                    updated_at=datetime(2024, 1, 1),
                )
            )
            raise ValueError("Simulated error")
    except ValueError:
        pass

    # The insert should have been rolled back
    with service.session() as conn:
        result = conn.execute(metadata.tables["users"].select())
        rows = result.fetchall()
        assert rows == []

    service.disconnect()


def test_should_return_metadata():
    service = SqlServiceSqlAlchemy("sqlite:///:memory:", metadata)
    assert service.get_metadata() is metadata
