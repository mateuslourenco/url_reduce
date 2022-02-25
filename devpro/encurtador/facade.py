from django.db.models import Count
from django.db.models.functions import TruncDate

from devpro.encurtador.models import UrlRedirect


def localizar_url_redirect(slug):
    return UrlRedirect.objects.get(slug=slug)


def localizar_redirecionamentos(slug):
    return list(
        UrlRedirect.objects.filter(
            slug=slug
        ).annotate(
            data=TruncDate('logs__criado_em')
        ).annotate(
            cliques=Count('data')
        ).order_by('data')
    )
