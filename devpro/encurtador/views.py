from django.shortcuts import redirect, render

from devpro.encurtador.models import UrlRedirect, UrlLog


def redirecionar(request, slug):
    url_redirect = UrlRedirect.objects.get(slug=slug)
    UrlLog.objects.create(
        origem=request.META.get('HTTP_REFERER'),
        user_agent=request.META.get('HTTP_USER_AGENT'),
        host=request.META.get('HTTP_HOST'),
        ip=request.META.get('REMOTE_ADDR'),
        url_redirect=url_redirect
    )
    return redirect(url_redirect.destino)


def relatorios(request, slug):
    url_redirect = UrlRedirect.objects.get(slug=slug)
    url_reduzida = request.build_absolute_uri(f'/{slug}')
    ctx = {
        'reduce': url_redirect,
        'url_reduzida': url_reduzida,
    }
    return render(request, 'encurtador/relatorio.html', ctx)
