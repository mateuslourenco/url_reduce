from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from devpro.encurtador.facade import localizar_url_redirect, localizar_url_reduzida, \
    localizar_redirecionamentos_por_data, localizar_redirects
from devpro.encurtador.forms import ReduceForm
from devpro.encurtador.models import UrlRedirect, UrlLog


def redirecionar(request, slug):
    try:
        url_redirect = UrlRedirect.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return redirect(reverse('home'))
    else:
        UrlLog.objects.create(
            origem=request.META.get('HTTP_REFERER'),
            user_agent=request.META.get('HTTP_USER_AGENT'),
            host=request.META.get('HTTP_HOST'),
            ip=request.META.get('REMOTE_ADDR'),
            url_redirect=url_redirect
        )
        return redirect(url_redirect.destino)


def relatorios(request, slug):
    url = localizar_url_redirect(slug)
    url_reduzida = localizar_url_reduzida(request, slug)
    redirecionamentos_por_data = localizar_redirecionamentos_por_data(slug)
    ctx = {
        'reduce': url,
        'url_reduzida': url_reduzida,
        'redirecionamentos_por_data': redirecionamentos_por_data,
        'total_cliques': sum(r.cliques for r in redirecionamentos_por_data)
    }
    return render(request, 'encurtador/relatorio.html', ctx)


def home(request):
    if request.method == 'POST':
        form = ReduceForm(request.POST)
        if form.is_valid():
            reduce = form.save(commit=False)
            reduce.save()
            return HttpResponseRedirect(reverse('home'))
        else:
            ctx = {'form': form}
            return render(request, 'encurtador/home.html', context=ctx)
    else:

        parametro_pagina = request.GET.get('page', '1')
        parametro_limite = '5'

        redirecionamentos = localizar_redirects()
        redirecionamentos_paginator = Paginator(redirecionamentos, parametro_limite)

        try:
            page = redirecionamentos_paginator.page(parametro_pagina)
        except (EmptyPage, PageNotAnInteger):
            page = redirecionamentos_paginator.page(1)

        ctx = {
            'redirecionamentos': page
        }
        return render(request, 'encurtador/home.html', ctx)
