from django.db import models
from django.urls import reverse


class UrlRedirect(models.Model):
    destino = models.URLField(max_length=512)
    slug = models.SlugField(max_length=128, unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'url redirect para {self.destino}'

    class Meta:
        ordering = ('-id',)

    def localizar_url_reduzida(self):
        return reverse('redirecionar', kwargs={'slug': self.slug})

    def localizar_relatorio(self):
        return reverse('relatorios', kwargs={'slug': self.slug})


class UrlLog(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    origem = models.URLField(max_length=512, null=True, blank=True)
    user_agent = models.CharField(max_length=512, null=True, blank=True)
    host = models.CharField(max_length=512, null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    url_redirect = models.ForeignKey(UrlRedirect, on_delete=models.DO_NOTHING, related_name='logs')
