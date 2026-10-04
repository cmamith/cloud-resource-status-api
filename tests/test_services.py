from app.services import get_instance_status


def test_get_existing_instance():
    instance = get_instance_status("i-001")

    assert instance is not None
    assert instance.instance_id == "i-001"
    assert instance.state == "running"


def test_get_missing_instance():
    instance = get_instance_status("i-999")

    assert instance is None