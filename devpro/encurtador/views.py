from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from devpro.encurtador.facade import localizar_url_redirect, localizar_url_reduzida, \
    localizar_redirecionamentos_por_data, paginizacao
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
    try:
        url = localizar_url_redirect(slug)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('home'))
    else:
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
            ctx = {
                'form': form,
                'redirecionamentos': paginizacao(request)
            }
            return render(request, 'encurtador/home.html', context=ctx)
    else:
        ctx = {
            'redirecionamentos': paginizacao(request)
        }
        return render(request, 'encurtador/home.html', ctx)
