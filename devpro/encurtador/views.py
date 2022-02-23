from django.shortcuts import redirect, render

from devpro.encurtador.models import UrlRedirect


def redirecionar(request, slug):
    url_redirect = UrlRedirect.objects.get(slug=slug)
    return redirect(url_redirect.destino)


def relatorios(request, slug):
    url_redirect = UrlRedirect.objects.get(slug=slug)
    url_reduzida = request.build_absolute_uri(f'/{slug}')
    ctx = {
        'reduce': url_redirect,
        'url_reduzida': url_reduzida,
    }
    return render(request, 'encurtador/relatorio.html', ctx)
