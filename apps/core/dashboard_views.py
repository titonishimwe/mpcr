from functools import wraps

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .dashboard_forms import (
    GalleryImageForm,
    ImpactStatForm,
    PartnerForm,
    ProgramForm,
    TeamMemberForm,
    TestimonialForm,
)
from .models import (
    ContactMessage,
    GalleryImage,
    ImpactStat,
    Partner,
    Program,
    TeamMember,
    Testimonial,
)


def _staff_required(view):
    """Require a signed-in staff user. Permissions are checked on the server."""

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return view(request, *args, **kwargs)

    return login_required(login_url="dashboard_login")(wrapper)


RESOURCES = {
    "programs": {
        "model": Program,
        "form": ProgramForm,
        "title": "Programs",
        "singular": "program",
        "search": ["title", "summary", "location"],
        "columns": [
            ("title", "Title"),
            ("get_category_display", "Category"),
            ("location", "Location"),
            ("is_featured", "Featured"),
            ("order", "Order"),
        ],
    },
    "gallery": {
        "model": GalleryImage,
        "form": GalleryImageForm,
        "title": "Gallery",
        "singular": "photo",
        "search": ["title", "caption", "location"],
        "columns": [
            ("title", "Title"),
            ("get_category_display", "Category"),
            ("location", "Location"),
            ("is_featured", "Featured"),
            ("order", "Order"),
        ],
    },
    "team": {
        "model": TeamMember,
        "form": TeamMemberForm,
        "title": "Team",
        "singular": "team member",
        "search": ["name", "position", "email", "phone"],
        "columns": [
            ("name", "Name"),
            ("position", "Position"),
            ("phone", "Phone"),
            ("email", "Email"),
            ("is_active", "Active"),
        ],
    },
    "partners": {
        "model": Partner,
        "form": PartnerForm,
        "title": "Partners",
        "singular": "partner",
        "search": ["name", "category"],
        "columns": [
            ("name", "Name"),
            ("category", "Mark"),
            ("website", "Website"),
            ("order", "Order"),
        ],
    },
    "stats": {
        "model": ImpactStat,
        "form": ImpactStatForm,
        "title": "Impact stats",
        "singular": "statistic",
        "search": ["label", "value", "description"],
        "columns": [
            ("value", "Value"),
            ("label", "Label"),
            ("description", "Description"),
            ("order", "Order"),
        ],
    },
    "testimonials": {
        "model": Testimonial,
        "form": TestimonialForm,
        "title": "Testimonials",
        "singular": "testimonial",
        "search": ["author", "role", "quote", "location"],
        "columns": [
            ("author", "Author"),
            ("role", "Role"),
            ("location", "Location"),
            ("order", "Order"),
        ],
    },
}


def resource_config(key):
    config = RESOURCES.get(key)
    if not config:
        raise Http404("Unknown dashboard section")
    return config


def dashboard_context(request, **extra):
    context = {
        "unread_messages": ContactMessage.objects.filter(is_read=False).count(),
        "nav_sections": [
            ("cms", "Website content", "fa-pen-to-square"),
            ("programs", "Programs", "fa-seedling"),
            ("gallery", "Gallery", "fa-images"),
            ("team", "Team", "fa-users"),
            ("partners", "Partners", "fa-handshake"),
            ("stats", "Impact stats", "fa-chart-simple"),
            ("testimonials", "Testimonials", "fa-quote-left"),
            ("messages", "Messages", "fa-envelope"),
        ],
    }
    context.update(extra)
    return context


def dashboard_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("dashboard")

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        if not user.is_staff:
            messages.error(request, "This account cannot manage website content.")
        else:
            login(request, user)
            next_url = request.POST.get("next") or request.GET.get("next")
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect("dashboard")

    return render(
        request,
        "dashboard/login.html",
        {"form": form, "page_title": "Admin sign in - MPCR", "next": request.GET.get("next", "")},
    )


@login_required(login_url="dashboard_login")
@require_POST
def dashboard_logout(request):
    logout(request)
    messages.success(request, "You have signed out.")
    return redirect("dashboard_login")


@_staff_required
def dashboard_home(request):
    context = dashboard_context(
        request,
        page_title="Dashboard - MPCR",
        counts={
            "programs": Program.objects.count(),
            "gallery": GalleryImage.objects.count(),
            "team": TeamMember.objects.filter(is_active=True).count(),
            "partners": Partner.objects.count(),
            "stats": ImpactStat.objects.count(),
            "testimonials": Testimonial.objects.count(),
            "messages": ContactMessage.objects.count(),
        },
        recent_messages=ContactMessage.objects.all()[:5],
    )
    return render(request, "dashboard/home.html", context)


def _row_values(obj, columns):
    values = []
    for attr, _label in columns:
        value = getattr(obj, attr)
        if callable(value):
            value = value()
        values.append(value)
    return values


@_staff_required
def resource_list(request, resource):
    config = resource_config(resource)
    queryset = config["model"].objects.all()
    query = request.GET.get("q", "").strip()
    if query:
        lookup = Q()
        for field in config["search"]:
            lookup |= Q(**{f"{field}__icontains": query})
        queryset = queryset.filter(lookup)

    paginator = Paginator(queryset, 12)
    page = paginator.get_page(request.GET.get("page"))
    rows = [(obj, _row_values(obj, config["columns"])) for obj in page.object_list]

    return render(
        request,
        "dashboard/list.html",
        dashboard_context(
            request,
            page_title=f"{config['title']} - Dashboard",
            resource=resource,
            config=config,
            page_obj=page,
            rows=rows,
            query=query,
        ),
    )


@_staff_required
def resource_create(request, resource):
    config = resource_config(resource)
    form = config["form"](request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{config['singular'].title()} saved.")
        return redirect("dashboard_list", resource=resource)

    return render(
        request,
        "dashboard/form.html",
        dashboard_context(
            request,
            page_title=f"Add {config['singular']} - Dashboard",
            resource=resource,
            config=config,
            form=form,
            is_edit=False,
        ),
    )


@_staff_required
def resource_edit(request, resource, pk):
    config = resource_config(resource)
    obj = get_object_or_404(config["model"], pk=pk)
    form = config["form"](request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{config['singular'].title()} updated.")
        return redirect("dashboard_list", resource=resource)

    return render(
        request,
        "dashboard/form.html",
        dashboard_context(
            request,
            page_title=f"Edit {config['singular']} - Dashboard",
            resource=resource,
            config=config,
            form=form,
            is_edit=True,
            object=obj,
        ),
    )


@_staff_required
@require_POST
def resource_delete(request, resource, pk):
    config = resource_config(resource)
    obj = get_object_or_404(config["model"], pk=pk)
    obj.delete()
    messages.success(request, f"{config['singular'].title()} deleted.")
    return redirect("dashboard_list", resource=resource)


@_staff_required
def message_list(request):
    queryset = ContactMessage.objects.all()
    status = request.GET.get("status", "all")
    if status == "unread":
        queryset = queryset.filter(is_read=False)
    elif status == "read":
        queryset = queryset.filter(is_read=True)

    query = request.GET.get("q", "").strip()
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query)
            | Q(email__icontains=query)
            | Q(subject__icontains=query)
            | Q(message__icontains=query)
        )

    paginator = Paginator(queryset, 12)
    page = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "dashboard/messages.html",
        dashboard_context(
            request,
            page_title="Messages - Dashboard",
            resource="messages",
            page_obj=page,
            query=query,
            status=status,
        ),
    )


@_staff_required
def message_detail(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "toggle":
            message.is_read = not message.is_read
            message.save(update_fields=["is_read"])
            messages.success(request, "Message status updated.")
        elif action == "delete":
            message.delete()
            messages.success(request, "Message deleted.")
            return redirect("dashboard_messages")
        return redirect("dashboard_message", pk=message.pk)

    if not message.is_read:
        message.is_read = True
        message.save(update_fields=["is_read"])

    return render(
        request,
        "dashboard/message_detail.html",
        dashboard_context(
            request,
            page_title=f"{message.subject} - Dashboard",
            resource="messages",
            message_obj=message,
        ),
    )
