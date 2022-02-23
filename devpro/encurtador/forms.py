from django.forms import ModelForm

from devpro.encurtador.models import UrlRedirect


class ReduceForm(ModelForm):
    class Meta:
        model = UrlRedirect
        fields = ['destino', 'slug']
