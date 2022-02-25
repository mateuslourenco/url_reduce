from django.db.models import Count
from django.db.models.functions import TruncDate

from devpro.encurtador.models import UrlRedirect


def localizar_url_redirect(slug: str) -> UrlRedirect:
    return UrlRedirect.objects.get(slug=slug).order_by('-id')


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
