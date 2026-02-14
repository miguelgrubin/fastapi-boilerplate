from src.shared.factory import create_password_service


def test_should_hash():
    service = create_password_service("fake")
    password = "lalala2"

    assert service.hash(password) == password


def test_should_check():
    service = create_password_service("fake")
    password = "lalala2"
    hash = service.hash(password)

    assert service.check(password, hash) is True
