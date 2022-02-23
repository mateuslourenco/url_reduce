from django.db.models import Count
from django.db.models.functions import TruncDate
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from devpro.encurtador.forms import ReduceForm
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
    redirecionamentos_por_data = list(
        UrlRedirect.objects.filter(
            slug=slug
        ).annotate(
            data=TruncDate('logs__criado_em')
        ).annotate(
            cliques=Count('data')
        ).order_by('data')
    )
    ctx = {
        'reduce': url_redirect,
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
        return render(request, 'encurtador/home.html')
