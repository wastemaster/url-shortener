from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import (HttpResponseRedirect,
                         HttpResponsePermanentRedirect)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .misc import (hash_encode,
                   get_absolute_short_url,
                   generate_link)
from .forms import URLShortenerForm
from .models import Link


def index(request):
    if request.method == 'POST':
        form = URLShortenerForm(request.POST)
        if form.is_valid():
            original_alias = form.cleaned_data['alias']
            alias = original_alias.lower()
            url = form.cleaned_data['url']
            new_link = generate_link(url, alias)
            return HttpResponseRedirect(reverse('url_shortener:preview',
                args=(new_link.alias,)))
    else:
        form = URLShortenerForm()
    return render(request, 'url_shortener/index.html', {
        'form': form,
        'absolute_index_url': get_absolute_short_url(request, ''),
    })


def preview(request, alias):
    link = get_object_or_404(Link, alias__iexact=alias)
    return render(request, 'url_shortener/preview.html', {
        'alias': alias,
        'absolute_short_url': get_absolute_short_url(request, alias, remove_schema=False),
        'url': link.url,
    })


def redirect(request, alias, extra=''):
    link = get_object_or_404(Link, alias__iexact=alias)
    link.clicks_count += 1
    link.save()
    return HttpResponsePermanentRedirect(link.url + extra)


@csrf_exempt
def api(request):
    data = {}
    if request.method == 'POST':
        form = URLShortenerForm(request.POST)
        if form.is_valid():
            original_alias = form.cleaned_data['alias']
            alias = original_alias.lower()
            url = form.cleaned_data['url']
            new_link = generate_link(url, alias)
            data['url'] = url
            data['alias'] = new_link.alias
            data['link'] = get_absolute_short_url(request, new_link.alias,
                remove_schema=False)
    return JsonResponse(data)
