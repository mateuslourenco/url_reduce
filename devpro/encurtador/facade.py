from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.db.models.functions import TruncDate

from devpro.encurtador.models import UrlRedirect


def localizar_url_redirect(slug: str) -> UrlRedirect:
    return UrlRedirect.objects.get(slug=slug)


def localizar_redirecionamentos_por_data(slug):
    return list(
        UrlRedirect.objects.filter(
            slug=slug
        ).annotate(
            data=TruncDate('logs__criado_em')
        ).annotate(
            cliques=Count('data')
        ).order_by('data')
    )


def localizar_url_reduzida(request, slug):
    return request.build_absolute_uri(f'/{slug}')


def localizar_redirects():
    return UrlRedirect.objects.all()


def paginizacao(request):
    parametro_pagina = request.GET.get('page', '1')
    parametro_limite = '5'

    redirecionamentos = localizar_redirects()
    redirecionamentos_paginator = Paginator(redirecionamentos, parametro_limite)

    try:
        page = redirecionamentos_paginator.page(parametro_pagina)
    except (EmptyPage, PageNotAnInteger):
        page = redirecionamentos_paginator.page(1)
    return page
