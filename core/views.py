from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from urllib.request import urlopen
from core.models import *


class HomeView(TemplateView):
    template_name = 'index.html'

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

def redirect_url(request):

    url = request.build_absolute_uri('/').strip("/")
    redirect_obj = get_object_or_404(Redirects, url_from=url)
    print('From URL: ', url)
    print('To URL: ', redirect_obj.url_to)

    response = HttpResponse("", status=302)
    response['Location'] = str(redirect_obj.http_https) + '://' + str(redirect_obj.url_to)
    return response
