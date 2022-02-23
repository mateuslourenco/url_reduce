import pytest
from django.urls import reverse
from model_bakery import baker

from devpro.encurtador.models import UrlRedirect


@pytest.fixture
def url_redirect(db):
    redirecionador = baker.make(UrlRedirect)
    return redirecionador


@pytest.fixture
def resp(client, url_redirect):
    return client.get(reverse('redirecionar', kwargs={'slug': url_redirect.slug}))


def test_redirect(resp, url_redirect):
    assert resp.status_code == 302
    assert resp.url == url_redirect.destino
