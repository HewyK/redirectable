from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from urllib.request import urlopen
from django.contrib import messages

from core.models import *
from core.forms import *

####################################################################
# Unauthenticated Views
####################################################################

class HomeView(TemplateView):
    template_name = 'index.html'


####################################################################
# Authenticated Views
####################################################################

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        redirects = Redirects.objects.filter(user=self.request.user)

        context['redirects'] = redirects
        context['form'] = RedirectsForm(initial={'http_https': 'https'})
        return context

    def post(self, request, *args, **kwargs):

        form = RedirectsForm(request.POST)

        if form.is_valid():
            print('valid form')
            r = Redirects()
            r.user = self.request.user
            r.url_from = form.cleaned_data['url_from']
            r.url_to = form.cleaned_data['url_to']
            r.http_https = form.cleaned_data['http_https']
            r.save()
            messages.add_message(self.request, messages.INFO, 'Added Successfully')
        else:
            print('invalid form')
            messages.add_message(self.request, messages.ERROR, 'Error Adding Redirect')

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/'))


def DeleteRedirectView(request, **kwargs):

    if kwargs['r']:

        redirect_to_delete = get_object_or_404(Redirects, id=kwargs['r'])
        print('Deleting Redirect: ', redirect_to_delete)

        redirect_to_delete.delete()
        messages.add_message(request, messages.INFO, 'Deleted Successfully')

    else:
        messages.add_message(request, messages.ERROR, 'Error Deleting redirect')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

####################################################################
# Redirect Views
####################################################################

def redirect_url(request):

    url = request.build_absolute_uri('/').strip("/")
    redirect_obj = get_object_or_404(Redirects, url_from=url)
    print('From URL: ', url)
    print('To URL: ', redirect_obj.url_to)

    response = HttpResponse("", status=302)
    response['Location'] = str(redirect_obj.http_https) + '://' + str(redirect_obj.url_to)
    return response

