"""
Core views.py file for redirectable project

Returns:
    _type_: _description_
"""

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

import core.models as models
import core.forms as forms

####################################################################
# Unauthenticated Views
####################################################################

class HomeView(TemplateView):
    """
    View to display the home page

    Args:
        TemplateView (_type_): _description_
    """
    template_name = 'index.html'


####################################################################
# Authenticated Views
####################################################################

class DashboardView(TemplateView):
    """
    View to display the dashboard

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        """_summary_

        Returns:
            _type_: _description_
        """
        context = super().get_context_data(**kwargs)
        redirects = models.Redirects.objects.filter(user=self.request.user)

        context['redirects'] = redirects
        context['form'] = forms.RedirectsForm(initial={'http_https': 'https'})
        context['sslsetupform'] = forms.SSLSetupForm()
        context['sslcertuploadform'] = forms.SSLCertUploadForm()
        return context

    def post(self, request, *args, **kwargs):
        """_summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        form = forms.RedirectsForm(request.POST)

        if form.is_valid():
            print('valid form')
            r = models.Redirects()
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
    """
    View to delete a redirect

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    if kwargs['r']:

        redirect_to_delete = get_object_or_404(models.Redirects, id=kwargs['r'])
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
    """
    View to redirect a user to the correct URL

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    url = request.build_absolute_uri('/').strip("/")
    redirect_obj = get_object_or_404(models.Redirects, url_from=url)
    print('From URL: ', url)
    print('To URL: ', redirect_obj.url_to)

    response = HttpResponse("", status=302)
    response['Location'] = str(redirect_obj.http_https) + '://' + str(redirect_obj.url_to)
    return response