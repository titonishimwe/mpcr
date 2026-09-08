from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import Program, GalleryImage, ImpactStat, Partner, TeamMember
from .forms import ContactForm


def home(request):
    featured_programs = Program.objects.filter(is_featured=True)[:6]
    preview_gallery = GalleryImage.objects.filter(is_featured=True)[:6]
    team_members = TeamMember.objects.filter(is_active=True)

    context = {
        "page_title": "Home - Movement for Christ in Rwanda (MPCR)",
        "featured_programs": featured_programs,
        "preview_gallery": preview_gallery,
        "team_members": team_members,
    }
    return render(request, "core/home.html", context)


def about(request):
    partners = Partner.objects.all()
    stats = ImpactStat.objects.all()[:4]

    context = {
        "page_title": "About Us - Movement for Christ in Rwanda",
        "partners": partners,
        "stats": stats,
    }
    return render(request, "core/about.html", context)


def programs(request):
    selected_category = request.GET.get("category", "all")
    if selected_category and selected_category != "all":
        programs_list = Program.objects.filter(category=selected_category)
    else:
        programs_list = Program.objects.all()

    categories = Program.CATEGORY_CHOICES

    context = {
        "page_title": "Our Programs & Activities - MPCR",
        "programs": programs_list,
        "categories": categories,
        "selected_category": selected_category,
    }
    return render(request, "core/programs.html", context)


def gallery(request):
    selected_category = request.GET.get("category", "all")
    if selected_category and selected_category != "all":
        photos_list = GalleryImage.objects.filter(category=selected_category)
    else:
        photos_list = GalleryImage.objects.all()

    categories = GalleryImage.CATEGORY_CHOICES

    context = {
        "page_title": "Activity & Project Gallery - MPCR",
        "photos": photos_list,
        "categories": categories,
        "selected_category": selected_category,
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
    }
    return render(request, "core/contact.html", context)


def custom_page_not_found(request, exception=None):
    return render(request, "404.html", {"page_title": "Page Not Found - MPCR"}, status=404)


def custom_server_error(request):
    return render(request, "500.html", {"page_title": "Server Error - MPCR"}, status=500)


def custom_permission_denied(request, exception=None):
    return render(request, "403.html", {"page_title": "Access Denied - MPCR"}, status=403)
