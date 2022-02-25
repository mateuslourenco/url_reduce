import pytest
from django.urls import reverse
from model_bakery import baker

from devpro.encurtador.models import UrlRedirect, UrlLog


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


def test_log_criado(resp):
    assert UrlLog.objects.exists()


@pytest.fixture
def resp_slug_invalido(client, db):
    return client.get(reverse('redirecionar', kwargs={'slug': 'invalido'}))


def test_status_code_slug_invalido(resp_slug_invalido):
    assert resp_slug_invalido.status_code == 302
    assert resp_slug_invalido.url == reverse('home')
