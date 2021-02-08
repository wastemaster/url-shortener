from django.shortcuts import get_object_or_404
from django.http import (HttpResponsePermanentRedirect)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .misc import (get_absolute_short_url,
                   generate_link)
from .forms import URLShortenerForm
from .models import Link


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
