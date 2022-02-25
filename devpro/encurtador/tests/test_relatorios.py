import pytest
from django.urls import reverse
from model_bakery import baker

from devpro.django_assertions import assert_contains
from devpro.encurtador.models import UrlRedirect


@pytest.fixture
def url_redirect(db):
    redirecionador = baker.make(UrlRedirect)
    return redirecionador


@pytest.fixture
def resp(client, url_redirect):
    return client.get(reverse('relatorios', kwargs={'slug': url_redirect.slug}))


def test_status_code(resp):
    assert resp.status_code == 200


def test_url_original_presente(resp, url_redirect):
    assert_contains(resp, url_redirect.destino)


def test_url_reduzida_presente(resp, url_redirect):
    assert_contains(resp, f'/{url_redirect.slug}')


@pytest.fixture
def resp_slug_invalido(client, url_redirect):
    return client.get(reverse('relatorios', kwargs={'slug': url_redirect.slug + '1'}))


def test_url_relatorio_invalido(resp_slug_invalido):
    assert resp_slug_invalido.status_code == 302
    assert resp_slug_invalido.url == reverse('home')
