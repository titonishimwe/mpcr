from django import template
from django.templatetags.static import static
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def cms_media(url):
    if not url:
        return ""
    if url.startswith(("http://", "https://", "/")):
        return url
    return static(url)


@register.filter
def cms_br(value):
    return mark_safe("<br>".join(escape(part) for part in (value or "").splitlines()))
