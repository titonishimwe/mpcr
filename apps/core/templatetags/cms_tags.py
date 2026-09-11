from django import template
from django.templatetags.static import static
from django.utils.html import escape
from django.utils.safestring import mark_safe
import re

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


@register.filter
def md_inline(value):
    """Escape text, then turn **bold** markers into <strong>."""
    text = escape(value or "")
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return mark_safe(text)


@register.filter
def md_rich(value):
    """Escape text, support **bold**, and convert newlines to paragraphs/breaks."""
    text = escape(value or "").strip()
    if not text:
        return ""
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    blocks = [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]
    html_parts = [f"<p>{block.replace(chr(10), '<br>')}</p>" for block in blocks]
    return mark_safe("".join(html_parts))
