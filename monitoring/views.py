# -*- coding: UTF-8 -*-

from datetime import timedelta
from django.views import generic
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.utils.timezone import now

from . import models
from . import forms

import logging
logger = logging.getLogger(__name__)

# Prihlasovani
class LoginView(generic.FormView):
    form_class = forms.PrihlaseniForm
    template_name = 'monitoring/login.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        logger.error("valid")
        username = form.cleaned_data['username']
        heslo = form.cleaned_data['password']
        user = authenticate(username=username, password=heslo)
        if user is not None:
            if user.is_active:
                login(self.request, user)
        return HttpResponseRedirect(reverse_lazy('monitoring:index',))


# Dashboard
class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'monitoring/index.html'


# Výpis bran a jejich informací
class GatewayListView(LoginRequiredMixin, generic.ListView):
    model = models.Gateway
    context_object_name = 'gateways'
    template_name = 'monitoring/gateway/list.html'


# Posledních 10 zpráv ze všech bran
class GatewayZpravyListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'monitoring/gateway/zpravy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'zpravy': models.Zprava.objects.all().order_by('-created')[:10]})
        return context

# Přidání brány
class GatewayCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Gateway
    form_class = forms.GatewayForm
    template_name = 'monitoring/gateway/form.html'

    def get_success_url(self):
        return reverse_lazy('monitoring:gateway-list')

# Editace brány
class GatewayEditView(LoginRequiredMixin, generic.UpdateView):
    model = models.Gateway
    form_class = forms.GatewayForm
    template_name = 'monitoring/gateway/form.html'

    def get_success_url(self):
        return reverse_lazy('monitoring:gateway-list')


# Výpis zařízení a jejich informací
class ZarizeniListView(LoginRequiredMixin, generic.ListView):
    model = models.Zarizeni
    context_object_name = 'vsechna_zarizeni'
    template_name = 'monitoring/zarizeni/list.html'


# Posledních 10 dat ze všech zařízení
class ZarizeniZpravyListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'monitoring/zarizeni/zpravy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'zpravy': models.Zprava.objects.all().order_by('-created')[:10]})
        return context

# Přidání zařízení
class ZarizeniCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Zarizeni
    form_class = forms.GatewayForm
    template_name = 'monitoring/zarizeni/form.html'

    def get_success_url(self):
        return reverse_lazy('monitoring:zarizeni-list')

# Editace zařízení
class ZarizeniEditView(LoginRequiredMixin, generic.UpdateView):
    model = models.Zarizeni
    form_class = forms.ZarizeniForm
    template_name = 'monitoring/zarizeni/form.html'

    def get_success_url(self):
        return reverse_lazy('monitoring:zarizeni-list')
    