from django import template
from django.templatetags.static import static

register = template.Library()


@register.filter
def cms_media(url):
    if not url:
        return ""
    if url.startswith(("http://", "https://", "/")):
        return url
    return static(url)


@register.filter
def linebreaksbr_safe(value):
    return (value or "").replace("\n", "<br>")
