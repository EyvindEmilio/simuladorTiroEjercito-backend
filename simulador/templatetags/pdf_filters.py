import base64
import cStringIO
import urllib

from django import template
from django.utils.datetime_safe import datetime
from simuladorTiroEjercitoBackend.settings import GET_API_URL

register = template.Library()


@register.filter
def get64(url):
    """
    Method returning base64 image data instead of URL
    :param url:
    """
    if url.startswith("http"):
        image = cStringIO.StringIO(urllib.urlopen(url).read())
        return 'data:image/jpg;base64,' + base64.b64encode(image.read())

    return url


@register.filter
def is_image(list):
    return list[0] == "image" and list[1] is not None and list[1] != ""


@register.filter
def is_datetime(list):
    return list[0] == "datetime"


@register.filter
def get_datetime(list):
    try:
        now = datetime.strptime(list[1], '%Y-%m-%dT%H:%M:%SZ')
    except:
        try:
            now = datetime.strptime(list[1], '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            now = datetime.strptime(list[1], '%Y-%m-%d')
    return now


@register.filter
def get_index_position(list, index):
    return list[index]


@register.filter
def get_label(list):
    return list[1]


@register.filter
def generate_image(base_url, item, list):
    return "%s%s" % (base_url, item[list[0]])


@register.filter
def get_type(list):
    return list[2]


@register.filter
def get_value_from_name(item, list):
    return item[list[0]]


# news
@register.filter
def get_path(url, request):
    return GET_API_URL(request, url)


@register.filter
def index(object_array, key):
    return object_array[key]


@register.filter
def to_datetime(date_text):
    try:
        now = datetime.strptime(date_text, '%Y-%m-%dT%H:%M:%SZ')
    except:
        try:
            now = datetime.strptime(date_text, '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            now = datetime.strptime(date_text, '%Y-%m-%d')
    return now
