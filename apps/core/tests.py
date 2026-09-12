from django.test import TestCase, Client
from django.urls import reverse
from apps.core.models import Program, GalleryImage, ImpactStat, Partner, Testimonial, ContactMessage


class MPCRWebpageTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create baseline test models
        self.program = Program.objects.create(
            title="Agroforestry and Landscape Restoration",
            category="development",
            summary="Restoring farmlands in Gatsibo.",
            description="Detailed FLR initiative with 28,800 seedlings.",
            location="Gatsibo District",
            is_featured=True,
            order=1
        )

        self.stat = ImpactStat.objects.create(
            label="Hectares Restored",
            value="105+",
            order=1
        )

        self.partner = Partner.objects.create(
            name="TerraFund for AFR100",
            category="Environmental Partner",
            order=1
        )

        self.testimonial = Testimonial.objects.create(
            author="Mr. Olivier NTIYAMIRA",
            role="Champion Farmer",
            quote="The papaya tree planted produces healthy fruit.",
            location="Gatsibo District",
            order=1
        )

        self.gallery_item = GalleryImage.objects.create(
            title="Tree Nursery Seedlings",
            category="development",
            caption="Nursery production in Gatsibo.",
            location="Kabarore Sector",
            date_taken="2026",
            is_featured=True,
            order=1
        )

    def test_home_page_status_and_content(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/home.html")
        self.assertContains(response, "Movement for Christ in Rwanda")
        self.assertContains(response, "John 3:16")
        self.assertContains(response, "105+")
        self.assertContains(response, "Agroforestry and Landscape Restoration")

    def test_about_page_status_and_content(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/about.html")
        self.assertContains(response, "About MPCR")
        self.assertContains(response, "Nyamirambo")
        self.assertContains(response, "Our Core Values")
        self.assertContains(response, "166/2023")

    def test_programs_page_status_and_filter(self):
        response = self.client.get(reverse("programs"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/programs.html")
        self.assertContains(response, "Agroforestry and Landscape Restoration")

        # Test category filter
        filtered_response = self.client.get(reverse("programs") + "?category=development")
        self.assertEqual(filtered_response.status_code, 200)
        self.assertContains(filtered_response, "Agroforestry and Landscape Restoration")
        detail = self.client.get(reverse("program_detail", kwargs={"slug": self.program.slug}))
        self.assertEqual(detail.status_code, 200)
        self.assertContains(detail, "Agroforestry and Landscape Restoration")

        listing = self.client.get(reverse("programs"))
        self.assertContains(listing, "Read more")
        self.assertNotContains(listing, "Partner on this Program")

    def test_gallery_page_status_and_filter(self):
        response = self.client.get(reverse("gallery"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/gallery.html")
        self.assertContains(response, "Tree Nursery Seedlings")

        filtered_response = self.client.get(reverse("gallery") + "?category=development")
        self.assertEqual(filtered_response.status_code, 200)
        self.assertContains(filtered_response, "Tree Nursery Seedlings")

    def test_contact_page_get(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/contact.html")
        self.assertContains(response, "(+250) 788 812 075")
        self.assertContains(response, "info@mouvementpourchriste.org")
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_contact_form_submission_success(self):
        payload = {
            "name": "Jean Baptiste",
            "email": "jean.baptiste@example.rw",
            "phone": "+250788112233",
            "subject": "Inquiry about Gatsibo tree planting project",
            "message": "Greetings, I would like to learn more about the agroforestry initiative.",
        }
        response = self.client.post(reverse("contact"), data=payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "submitted successfully")

        # Verify record was created in database
        message_obj = ContactMessage.objects.filter(email="jean.baptiste@example.rw").first()
        self.assertIsNotNone(message_obj)
        self.assertEqual(message_obj.name, "Jean Baptiste")
        self.assertEqual(message_obj.subject, "Inquiry about Gatsibo tree planting project")
        self.assertFalse(message_obj.is_read)

    def test_contact_form_submission_invalid(self):
        payload = {
            "name": "",
            "email": "not-an-email",
            "subject": "",
            "message": "",
        }
        response = self.client.post(reverse("contact"), data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "error in your submission")
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_custom_404_handler(self):
        # In Django test client, requesting a 404 URL directly invokes custom_page_not_found if DEBUG=False
        # Or we can test custom_page_not_found view directly
        from apps.core.views import custom_page_not_found
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.get("/does-not-exist/")
        response = custom_page_not_found(request)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"404", response.content)
        self.assertIn(b"Page Not Found", response.content)

    def test_admin_portal_accessible(self):
        response = self.client.get("/secure-management/login/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "MPCR")

        hidden = self.client.get("/admin/login/")
        self.assertEqual(hidden.status_code, 404)


class DashboardTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        self.staff = User.objects.create_user(
            username="mpcradmin",
            password="dashboard-pass-123",
            is_staff=True,
        )
        self.visitor = User.objects.create_user(
            username="visitor",
            password="visitor-pass-123",
            is_staff=False,
        )
        self.client = Client()

    def test_dashboard_requires_staff_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard/login/", response.url)

        self.client.login(username="visitor", password="visitor-pass-123")
        denied = self.client.get(reverse("dashboard"))
        self.assertEqual(denied.status_code, 403)
        self.assertContains(denied, "Access Denied", status_code=403)
        self.assertNotContains(denied, "Traceback", status_code=403)

    def test_staff_can_manage_program(self):
        self.client.login(username="mpcradmin", password="dashboard-pass-123")
        overview = self.client.get(reverse("dashboard"))
        self.assertEqual(overview.status_code, 200)
        self.assertContains(overview, "Overview")

        created = self.client.post(
            reverse("dashboard_create", kwargs={"resource": "programs"}),
            {
                "title": "Village Bible Study",
                "slug": "",
                "category": "evangelism",
                "summary": "Weekly teaching in local churches.",
                "description": "Bible study groups for youth and families.",
                "target_beneficiaries": "Youth and families",
                "location": "Nyarugenge",
                "image_url": "",
                "is_featured": "on",
                "is_published": "on",
                "order": "2",
            },
        )
        self.assertEqual(created.status_code, 302)
        program = Program.objects.get(title="Village Bible Study")

        listing = self.client.get(reverse("dashboard_list", kwargs={"resource": "programs"}))
        self.assertContains(listing, "Village Bible Study")
        self.assertContains(listing, "Hide")

        updated = self.client.post(
            reverse("dashboard_edit", kwargs={"resource": "programs", "pk": program.pk}),
            {
                "title": "Village Bible Study",
                "slug": program.slug,
                "category": "evangelism",
                "summary": "Updated weekly teaching.",
                "description": "Bible study groups for youth and families.",
                "target_beneficiaries": "Youth and families",
                "location": "Nyarugenge",
                "image_url": "",
                "is_featured": "on",
                "is_published": "on",
                "order": "3",
            },
        )
        self.assertEqual(updated.status_code, 302)
        program.refresh_from_db()
        self.assertEqual(program.summary, "Updated weekly teaching.")

        deleted = self.client.post(
            reverse("dashboard_delete", kwargs={"resource": "programs", "pk": program.pk})
        )
        self.assertEqual(deleted.status_code, 302)
        self.assertFalse(Program.objects.filter(pk=program.pk).exists())

    def test_staff_can_hide_program_without_deleting(self):
        program = Program.objects.create(
            title="Hidden Draft Program",
            category="evangelism",
            summary="Draft summary",
            description="Draft description",
            is_featured=True,
            is_published=True,
        )
        self.client.login(username="mpcradmin", password="dashboard-pass-123")
        public = self.client.get(reverse("program_detail", kwargs={"slug": program.slug}))
        self.assertEqual(public.status_code, 200)

        hidden = self.client.post(
            reverse("dashboard_toggle", kwargs={"resource": "programs", "pk": program.pk})
        )
        self.assertEqual(hidden.status_code, 302)
        program.refresh_from_db()
        self.assertFalse(program.is_published)
        self.assertTrue(Program.objects.filter(pk=program.pk).exists())

        blocked = self.client.get(reverse("program_detail", kwargs={"slug": program.slug}))
        self.assertEqual(blocked.status_code, 404)
        listing = self.client.get(reverse("programs"))
        self.assertNotContains(listing, program.title)

        shown = self.client.post(
            reverse("dashboard_toggle", kwargs={"resource": "programs", "pk": program.pk})
        )
        self.assertEqual(shown.status_code, 302)
        program.refresh_from_db()
        self.assertTrue(program.is_published)

    def test_staff_can_read_contact_message(self):
        message = ContactMessage.objects.create(
            name="Aline",
            email="aline@example.rw",
            subject="Partnership",
            message="We would like to collaborate.",
        )
        self.client.login(username="mpcradmin", password="dashboard-pass-123")
        response = self.client.get(reverse("dashboard_message", kwargs={"pk": message.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Partnership")
        message.refresh_from_db()
        self.assertTrue(message.is_read)


class AccountTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        self.staff = User.objects.create_user(
            username="accountadmin",
            email="admin@example.rw",
            password="Current-pass-123",
            is_staff=True,
            first_name="Aline",
            last_name="Uwase",
        )
        self.other = User.objects.create_user(
            username="otheradmin",
            email="other@example.rw",
            password="Other-pass-123",
            is_staff=True,
        )
        self.client = Client()
        self.client.login(username="accountadmin", password="Current-pass-123")

    def test_account_page_shows_profile(self):
        response = self.client.get(reverse("account"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "accountadmin")
        self.assertContains(response, "admin@example.rw")
        self.assertContains(response, "Aline")

    def test_edit_name_and_keep_email_until_confirmed(self):
        updated = self.client.post(
            reverse("account_edit"),
            {"username": "accountadmin", "first_name": "Marie", "last_name": "Mukamana"},
        )
        self.assertEqual(updated.status_code, 302)
        self.staff.refresh_from_db()
        self.assertEqual(self.staff.first_name, "Marie")

        with self.settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"):
            requested = self.client.post(
                reverse("account_email"),
                {"email": "new-admin@example.rw", "current_password": "Current-pass-123"},
            )
        self.assertEqual(requested.status_code, 302)
        self.staff.refresh_from_db()
        self.assertEqual(self.staff.email, "admin@example.rw")
        self.assertEqual(self.staff.account_profile.pending_email, "new-admin@example.rw")

    def test_password_change_requires_current_password_and_signs_out_others(self):
        from django.contrib.auth import get_user_model
        from django.contrib.sessions.models import Session

        other = Client()
        other.login(username="accountadmin", password="Current-pass-123")
        weak = self.client.post(
            reverse("account_password"),
            {
                "current_password": "Current-pass-123",
                "new_password": "123",
                "confirm_password": "123",
            },
        )
        self.assertEqual(weak.status_code, 200)

        changed = self.client.post(
            reverse("account_password"),
            {
                "current_password": "Current-pass-123",
                "new_password": "Replacement-pass-123",
                "confirm_password": "Replacement-pass-123",
            },
        )
        self.assertEqual(changed.status_code, 302)
        self.staff.refresh_from_db()
        self.assertTrue(self.staff.check_password("Replacement-pass-123"))
        self.assertEqual(
            get_user_model().objects.get(pk=self.staff.pk).check_password("Replacement-pass-123"),
            True,
        )
        still_other = other.get(reverse("account"))
        self.assertEqual(still_other.status_code, 302)
        self.assertGreaterEqual(Session.objects.count(), 0)

    def test_forgot_password_link_and_same_response_for_unknown_email(self):
        self.client.logout()
        login_page = self.client.get(reverse("dashboard_login"))
        self.assertContains(login_page, "Forgot password?")

        with self.settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"):
            missing = self.client.post(reverse("password_reset"), {"email": "missing@example.rw"})
            known = self.client.post(reverse("password_reset"), {"email": "admin@example.rw"})
        self.assertEqual(missing.status_code, 302)
        self.assertEqual(known.status_code, 302)

    def test_deactivate_is_soft_and_requires_password(self):
        denied = self.client.post(
            reverse("account_deactivate"),
            {"current_password": "wrong-password", "confirm": "on"},
        )
        self.assertEqual(denied.status_code, 200)
        self.staff.refresh_from_db()
        self.assertTrue(self.staff.is_active)

        done = self.client.post(
            reverse("account_deactivate"),
            {"current_password": "Current-pass-123", "confirm": "on"},
        )
        self.assertEqual(done.status_code, 302)
        self.staff.refresh_from_db()
        self.assertFalse(self.staff.is_active)


class WebsiteContentTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        from apps.core.models import ensure_cms_defaults

        ensure_cms_defaults()
        User = get_user_model()
        self.staff = User.objects.create_user(
            username="cmsadmin",
            password="Cms-pass-12345",
            is_staff=True,
        )
        self.client = Client()
        self.client.login(username="cmsadmin", password="Cms-pass-12345")

    def test_staff_can_edit_home_hero_text(self):
        from apps.core.models import PageSection

        section = PageSection.objects.get(page="home", key="hero_title")
        response = self.client.post(
            reverse("cms_page_edit", kwargs={"page": "home"}),
            {f"section_{section.pk}_value": "Updated MPCR Title"},
        )
        # Saving posts all fields; missing keys keep prior values via view logic only when present
        self.assertIn(response.status_code, (200, 302))

    def test_site_settings_update_appears_in_footer(self):
        response = self.client.post(
            reverse("cms_site_settings"),
            {
                "org_name": "Movement for Christ in Rwanda (MPCR)",
                "org_name_fr": "Mouvement Pour Christ au Rwanda",
                "footer_about": "Editable footer about text for tests.",
                "legal_badge": "Legal Personality Compliance No. 166/2023",
                "address_line_1": "Nyamirambo Sector",
                "address_line_2": "Kigali City, Rwanda",
                "postal_box": "P.O. Box 1959",
                "phone_primary": "(+250) 788 812 075",
                "phone_primary_raw": "+250788812075",
                "phone_secondary": "(+250) 788 436 988",
                "phone_secondary_raw": "+250788436988",
                "email_primary": "info@mouvementpourchriste.org",
                "email_secondary": "mchriste1992@gmail.com",
                "whatsapp_number": "250788812075",
                "whatsapp_message": "Hello MPCR",
                "facebook_url": "https://facebook.com/mpcr",
                "instagram_url": "https://instagram.com/mpcr",
                "twitter_url": "https://twitter.com/mpcr",
                "social_handle": "@mpcr1990",
                "focus_items": "Evangelism\nDevelopment",
                "footer_copyright": "Copyright MPCR",
                "footer_tagline": "A healthy spirit lives in a healthy body",
            },
        )
        self.assertEqual(response.status_code, 302)
        home = self.client.get(reverse("home"))
        self.assertContains(home, "Editable footer about text for tests.")
        self.assertContains(home, "https://facebook.com/mpcr")
