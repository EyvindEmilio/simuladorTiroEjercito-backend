from django import template
import urllib, cStringIO, base64

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
