import pytest
from django.urls import reverse


@pytest.fixture
def resp(client):
    return client.get(reverse('relatorios', kwargs={'slug': 'slug'}))


def test_status_code(resp):
    assert resp.status_code == 200
