from .models import SiteSettings, ensure_cms_defaults


def site_content(request):
    try:
        site = SiteSettings.objects.filter(pk=1).first()
        if site is None:
            ensure_cms_defaults()
            site = SiteSettings.load()
    except Exception:
        site = None
    return {"site": site}
