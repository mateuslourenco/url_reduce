import pytest
from django.urls import reverse
from model_bakery import baker

from devpro.django_assertions import assert_contains
from devpro.encurtador.models import UrlRedirect


@pytest.fixture
def redirects(db):
    return baker.make(UrlRedirect, 2)


@pytest.fixture
def resp(client, redirects):
    return client.get(reverse('home'))


def test_status_code(resp):
    assert resp.status_code == 200


def test_listar_redirects(resp, redirects):
    for redirect in redirects:
        assert_contains(resp, redirect.slug)


def test_pagina_anterior_presente(resp):
    assert_contains(resp, 'Anterior')


def test_proxima_pagina_presente(resp):
    assert_contains(resp, 'Próxima')


@pytest.fixture
def resp_post(client, db):
    return client.post(reverse('home'), data={'destino': 'teste.teste', 'slug': 'teste'})


def test_status_code_post(resp_post):
    assert resp_post.status_code == 302
    assert resp_post.url == reverse('home')


def test_redirect_existe_no_db(resp_post):
    assert UrlRedirect.objects.exists()


@pytest.fixture
def redirect_criado(db):
    return baker.make(UrlRedirect)


@pytest.fixture
def resp_post_com_redirect_ja_existente(client, redirect_criado):
    return client.post(reverse('home'), data={'destino': redirect_criado.destino, 'slug': redirect_criado.slug})


def test_redirect_ja_existente(resp_post_com_redirect_ja_existente):
    assert_contains(resp_post_com_redirect_ja_existente, 'Url redirect com este Slug já existe.')
