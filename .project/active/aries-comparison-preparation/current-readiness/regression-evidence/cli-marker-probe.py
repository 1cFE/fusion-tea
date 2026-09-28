"""Pytest boundary probe; intentional errors distinguish markers from guards."""
import pytest
@pytest.fixture
def wrong_signature():
    assert False, 'wrong signature must remain an error'
@pytest.fixture
def known_signature():
    return 1
@pytest.mark.xfail(strict=True)
def test_static_marker_hides_guard(wrong_signature):
    assert False

def test_dynamic_marker_preserves_guard(wrong_signature, request):
    request.node.add_marker(pytest.mark.xfail(strict=True))
    assert False

def test_dynamic_marker_known_legacy_failure(known_signature, request):
    request.node.add_marker(pytest.mark.xfail(strict=True))
    assert known_signature == 0

def test_dynamic_marker_rejects_unexpected_success(request):
    request.node.add_marker(pytest.mark.xfail(strict=True))
    assert True
