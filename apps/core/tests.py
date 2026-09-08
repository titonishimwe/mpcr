from django.test import TestCase, Client
from django.urls import reverse
from apps.core.models import Program, GalleryImage, ImpactStat, Partner, Testimonial, ContactMessage


class MPCRWebpageTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create baseline test models
        self.program = Program.objects.create(
            title="Agroforestry and Landscape Restoration",
            category="flr",
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
            category="flr",
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
        self.assertContains(response, "Eraste NDAYISENGA")
        self.assertContains(response, "166/2023")

    def test_programs_page_status_and_filter(self):
        response = self.client.get(reverse("programs"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/programs.html")
        self.assertContains(response, "Agroforestry and Landscape Restoration")

        # Test category filter
        filtered_response = self.client.get(reverse("programs") + "?category=flr")
        self.assertEqual(filtered_response.status_code, 200)
        self.assertContains(filtered_response, "Agroforestry and Landscape Restoration")

    def test_gallery_page_status_and_filter(self):
        response = self.client.get(reverse("gallery"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/gallery.html")
        self.assertContains(response, "Tree Nursery Seedlings")

        filtered_response = self.client.get(reverse("gallery") + "?category=flr")
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
        response = self.client.get("/admin/login/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "MPCR")
