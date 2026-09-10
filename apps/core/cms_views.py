from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .cms_defaults import PAGES
from .cms_forms import HeroSlideForm, SiteSettingsForm
from .dashboard_views import _staff_required, dashboard_context
from .models import HeroSlide, PageSection, SiteSettings, ensure_cms_defaults


@_staff_required
def cms_home(request):
    ensure_cms_defaults()
    pages = []
    for key, label in PAGES.items():
        pages.append(
            {
                "key": key,
                "label": label,
                "count": PageSection.objects.filter(page=key).count(),
            }
        )
    return render(
        request,
        "dashboard/cms_home.html",
        dashboard_context(
            request,
            page_title="Website content - Dashboard",
            resource="cms",
            pages=pages,
            hero_count=HeroSlide.objects.count(),
        ),
    )


@_staff_required
def cms_site_settings(request):
    ensure_cms_defaults()
    settings_obj = SiteSettings.load()
    form = SiteSettingsForm(request.POST or None, instance=settings_obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Site settings saved. Footer, contact details, and social links are updated.")
        return redirect("cms_site_settings")

    return render(
        request,
        "dashboard/cms_site.html",
        dashboard_context(
            request,
            page_title="Site settings - Dashboard",
            resource="cms",
            form=form,
        ),
    )


@_staff_required
def cms_page_edit(request, page):
    if page not in PAGES:
        messages.error(request, "Unknown page.")
        return redirect("cms_home")

    ensure_cms_defaults()
    sections = list(PageSection.objects.filter(page=page))
    if request.method == "POST":
        for section in sections:
            prefix = f"section_{section.pk}"
            if section.field_type == PageSection.FIELD_IMAGE:
                uploaded = request.FILES.get(f"{prefix}_image")
                if uploaded:
                    section.image = uploaded
                section.image_url = request.POST.get(f"{prefix}_image_url", section.image_url).strip()
                if request.POST.get(f"{prefix}_clear_image") == "on":
                    section.image = None
            else:
                section.value = request.POST.get(f"{prefix}_value", section.value)
            section.save()
        messages.success(request, f"{PAGES[page]} page content saved.")
        return redirect("cms_page_edit", page=page)

    return render(
        request,
        "dashboard/cms_page.html",
        dashboard_context(
            request,
            page_title=f"Edit {PAGES[page]} - Dashboard",
            resource="cms",
            page_key=page,
            page_label=PAGES[page],
            sections=sections,
        ),
    )


@_staff_required
def cms_hero_list(request):
    ensure_cms_defaults()
    slides = HeroSlide.objects.all()
    return render(
        request,
        "dashboard/cms_hero_list.html",
        dashboard_context(
            request,
            page_title="Hero slides - Dashboard",
            resource="cms",
            slides=slides,
        ),
    )


@_staff_required
def cms_hero_create(request):
    form = HeroSlideForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Hero slide added.")
        return redirect("cms_hero_list")
    return render(
        request,
        "dashboard/cms_hero_form.html",
        dashboard_context(
            request,
            page_title="Add hero slide - Dashboard",
            resource="cms",
            form=form,
            is_edit=False,
        ),
    )


@_staff_required
def cms_hero_edit(request, pk):
    slide = get_object_or_404(HeroSlide, pk=pk)
    form = HeroSlideForm(request.POST or None, request.FILES or None, instance=slide)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Hero slide updated.")
        return redirect("cms_hero_list")
    return render(
        request,
        "dashboard/cms_hero_form.html",
        dashboard_context(
            request,
            page_title="Edit hero slide - Dashboard",
            resource="cms",
            form=form,
            is_edit=True,
            object=slide,
        ),
    )


@_staff_required
@require_POST
def cms_hero_delete(request, pk):
    slide = get_object_or_404(HeroSlide, pk=pk)
    slide.delete()
    messages.success(request, "Hero slide deleted.")
    return redirect("cms_hero_list")
