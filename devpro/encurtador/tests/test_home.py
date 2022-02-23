import pytest
from django.urls import reverse

from devpro.django_assertions import assert_contains
from devpro.encurtador.models import UrlRedirect


@pytest.fixture
def resp(client):
    return client.get(reverse('home'))


def test_status_code(resp):
    assert resp.status_code == 200


@pytest.fixture
def resp_post(client, db):
    return client.post(reverse('home'), data={'destino': 'teste.teste', 'slug': 'teste'})


def test_redirect_existe_no_db(resp_post):
    assert UrlRedirect.objects.exists()


@pytest.fixture
def redirect_criado(db):
    return UrlRedirect.objects.create(destino='teste.teste', slug='teste')


@pytest.fixture
def resp_post_com_redirect_ja_existente(client, redirect_criado):
    return client.post(reverse('home'), data={'destino': redirect_criado.destino, 'slug': redirect_criado.slug})


def test_redirect_ja_existente(resp_post_com_redirect_ja_existente):
    assert_contains(resp_post_com_redirect_ja_existente, 'Url redirect com este Slug já existe.')
