from django.db import models


class UrlRedirect(models.Model):
    destino = models.URLField(max_length=512)
    slug = models.SlugField(max_length=128, unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'url redirect para {self.destino}'
