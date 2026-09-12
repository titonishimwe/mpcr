import logging

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import (
    GalleryImage,
    HeroSlide,
    Partner,
    Program,
    TeamMember,
    ensure_cms_defaults,
    get_page_sections,
)
from .forms import ContactForm

logger = logging.getLogger("mpcr")


def paginate(request, queryset, per_page):
    page = Paginator(queryset, per_page).get_page(request.GET.get("page"))
    params = request.GET.copy()
    params.pop("page", None)
    return page, params.urlencode()


def home(request):
    ensure_cms_defaults()
    featured_programs = Program.objects.filter(is_published=True, is_featured=True)[:6]
    preview_gallery = GalleryImage.objects.filter(is_published=True, is_featured=True)[:6]
    team_members = TeamMember.objects.filter(is_active=True)
    partners = Partner.objects.filter(is_published=True)
    hero_slides = list(HeroSlide.objects.filter(is_active=True))
    if not hero_slides:
        ensure_cms_defaults()
        hero_slides = list(HeroSlide.objects.filter(is_active=True))

    context = {
        "page_title": "Home - Movement for Christ in Rwanda (MPCR)",
        "featured_programs": featured_programs,
        "preview_gallery": preview_gallery,
        "team_members": team_members,
        "partners": partners,
        "cms": get_page_sections("home"),
        "hero_slides": hero_slides,
    }
    return render(request, "core/home.html", context)


def about(request):
    context = {
        "page_title": "About Us - Movement for Christ in Rwanda",
        "cms": get_page_sections("about"),
    }
    return render(request, "core/about.html", context)


def programs(request):
    selected_category = request.GET.get("category", "all")
    programs_list = Program.objects.filter(is_published=True)
    if selected_category and selected_category != "all":
        programs_list = programs_list.filter(category=selected_category)

    categories = Program.CATEGORY_CHOICES
    programs_page, pagination_query = paginate(request, programs_list, 6)

    context = {
        "page_title": "Our Programs & Activities - MPCR",
        "programs": programs_page,
        "page_obj": programs_page,
        "pagination_query": pagination_query,
        "categories": categories,
        "selected_category": selected_category,
        "cms": get_page_sections("programs"),
    }
    return render(request, "core/programs.html", context)


def program_detail(request, slug):
    program = get_object_or_404(Program, slug=slug, is_published=True)
    related = (
        Program.objects.filter(is_published=True, category=program.category)
        .exclude(pk=program.pk)[:3]
    )
    context = {
        "page_title": f"{program.title} - MPCR",
        "program": program,
        "related_programs": related,
        "cms": get_page_sections("programs"),
    }
    return render(request, "core/program_detail.html", context)


def gallery(request):
    selected_category = request.GET.get("category", "all")
    photos_list = GalleryImage.objects.filter(is_published=True)
    if selected_category and selected_category != "all":
        photos_list = photos_list.filter(category=selected_category)

    categories = GalleryImage.CATEGORY_CHOICES
    photos_page, pagination_query = paginate(request, photos_list, 9)

    context = {
        "page_title": "Activity & Project Gallery - MPCR",
        "photos": photos_page,
        "page_obj": photos_page,
        "pagination_query": pagination_query,
        "categories": categories,
        "selected_category": selected_category,
        "cms": get_page_sections("gallery"),
    }
    return render(request, "core/gallery.html", context)


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save()
            messages.success(
                request,
                f"Thank you, {contact_msg.name}! Your message has been submitted successfully. An MPCR coordinator will get back to you shortly."
            )
            return redirect(reverse("contact"))
        else:
            messages.error(
                request,
                "There was an error in your submission. Please correct the indicated fields."
            )
    else:
        form = ContactForm()

    context = {
        "page_title": "Contact Us - Movement for Christ in Rwanda",
        "form": form,
        "cms": get_page_sections("contact"),
    }
    return render(request, "core/contact.html", context)


def custom_page_not_found(request, exception=None):
    return render(request, "404.html", {"page_title": "Page Not Found"}, status=404)


def custom_server_error(request):
    logger.error("Server error while handling %s", request.path)
    return render(request, "500.html", {"page_title": "Server Error"}, status=500)


def custom_permission_denied(request, exception=None):
    return render(request, "403.html", {"page_title": "Access Denied"}, status=403)


def csrf_failure(request, reason=""):
    """Friendly page when a form was submitted with an expired/stale CSRF token."""
    logger.warning("CSRF failure on %s: %s", request.path, reason)
    return render(
        request,
        "403_csrf.html",
        {
            "page_title": "Session expired",
            "reason": reason,
            "retry_url": request.path,
        },
        status=403,
    )
