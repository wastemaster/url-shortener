import string

from hashids import Hashids
from django.urls import reverse
from django.contrib import messages
from .models import Link

HASH_SALT = 'VyIZlWoq7VQCvJmq54gVHz5mb7GbaXdcT3Qz8dRssMyaYpTZl2ONBBnDA788Ef'
ALPHABET = string.ascii_lowercase

hashids = Hashids(salt=HASH_SALT, alphabet=ALPHABET)


def hash_encode(num):
    """
    Returns hashids.encode(num) with salt.
    """
    return hashids.encode(num)


def get_absolute_short_url(request, alias, remove_schema=True):
    """
    Returns absolute redirect URL, given the `request` object
    and the `alias`.

    Set `remove_schema` to False to prevent schema
    from being removed (default: True).
    """
    if alias:
        full_url = request.build_absolute_uri(
            reverse('url_shortener:alias', args=(alias,)))
    else:
        full_url = request.build_absolute_uri(reverse('url_shortener:index'))
    if remove_schema:
        return full_url[len(request.scheme)+3:]
    return full_url


def generate_link(url, alias):
    new_link = Link(url=url)
    try:
        latest_link = Link.objects.latest('id')
        if Link.objects.filter(alias__exact=alias):
            # handle alias conflict
            new_link.alias = hash_encode(latest_link.id+1)
            original_alias = new_link.alias
        else:
            new_link.alias = alias or hash_encode(latest_link.id+1)
    except Link.DoesNotExist:
        new_link.alias = alias or hash_encode(1)
    new_link.save()
    return new_link
