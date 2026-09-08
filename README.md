# Movement for Christ in Rwanda (MPCR) - Official Website

[![Django](https://img.shields.io/badge/Django-6.1-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Proprietary-orange.svg)]()

A modern, responsive, professional informational website for **Movement for Christ in Rwanda (Mouvement Pour Christ au Rwanda - MPCR)**, a registered Christian non-governmental organization (FBO/NGO) headquartered in Nyamirambo, Kigali, Rwanda.

---

## 1. Project Overview

### 1.1 Purpose
The MPCR website establishes the organization's official digital presence, conveys its Christian identity and mission, highlights field activities and environmental initiatives, and provides seamless contact channels for donors, churches, beneficiaries, and government partners.

### 1.2 Guiding Motto & Scripture
- **Scripture:** *"That whoever believes in HIM should not perish but have eternal life"* — **John 3:16** (*Afin que tout homme qui croit en LUI ne périsse pas mais ait la vie éternelle: CHRIST*)
- **Tagline:** *"Roho nzima itura mu mubiri muzima"* (*"A healthy spirit lives in a healthy body"*)
- **Legal Compliance:** Registered under Law No. 06/2012; Legal Personality Certificate of Compliance No. **166/2023** issued by Rwanda Governance Board (RGB).
- **Head Office:** Kigali City, Nyarugenge District, Nyamirambo Sector, Rwanda (P.O. Box 1959, Kigali).

---

## 2. Included Core Pages & Features

1. **Home (`/`)**:
   - Hero banner with organizational foundation, scripture highlights, and direct CTAs.
   - Live Impact statistics bar (105+ ha restored, 28,800+ seedlings produced, 150+ champion farmers, 240+ livestock distributed, 25+ partner churches).
   - About preview & core Christian values (*Gukunda Imana, Impuhwe, Ubunyangamugayo, Gukorera mu mucyo, Ubumwe, Iterambere rirambye*).
   - Featured programs & activities catalog.
   - Beneficiary testimonials from champion farmers (Olivier Ntiyamira, Nyirahishamunda Esperance, Vice Mayor Alice Uwera).
   - Strategic partners showcase (TerraFund for AFR100, WRI, Global Fund, MINISANTE, Embassy of Switzerland, RGB).
   - Call to Action banner with quick contact options.

2. **About Us (`/about/`)**:
   - Historical background (roots in Kinyinya, Gasabo District; compliance under Law No. 06/2012).
   - Official Vision and Mission statements.
   - Core values and biblical foundation.
   - Organizational governance structure (General Assembly, Executive Committee, Audit Council, Executive Secretariat).
   - 10 Specialized functional departments overview.
   - Leadership statement by Eraste NDAYISENGA, Legal Representative.
   - Geographic footprint across Kigali, Eastern, Western, and Southern provinces.

3. **Our Programs / Activities (`/programs/`)**:
   - Dynamic category filtering:
     - *Forest Landscape Restoration (FLR) & Environment* (Gatsibo 105 ha pilot, Rutsiro 2026–2032 project).
     - *Evangelism, Biblical Training & Christian Leadership* (25+ churches, correspondence Bible school).
     - *Child Protection & Women Economic Empowerment* (CPCs, training 25,000 youth on child rights).
     - *Community Health, Nutrition & HIV Eradication* (Muyira HIV education, maternal healthcare).
     - *Sustainable Agriculture & Cooperatives* (Pineapple farming in Kayenzi, livestock distribution, Ibimina).
     - *Youth Skills, Vocational Training & Higher Education* (Swiss Embassy funded vocational school, ULK graduate support).
   - Implementation strategies & priority target groups.
   - Strategic Prospects & Roadmap (2026–2032).

4. **Photo & Project Gallery (`/gallery/`)**:
   - Filterable photo grid categorized by thematic interventions.
   - High-resolution photographs with captions, locations, and dates.
   - Interactive zoomable Lightbox modal for enlarged viewing.
   - Backed by Django `GalleryImage` model with admin uploads.

5. **Contact Us (`/contact/`)**:
   - Complete contact directory:
     - Phone: `(+250) 788 812 075` / `(+250) 788 436 988`
     - Email: `info@mouvementpourchriste.org` / `mchriste1992@gmail.com`
     - Physical: Nyamirambo Sector, Nyarugenge District, Kigali City.
   - Interactive contact inquiry form with CSRF protection, input validation, success alert feedback, and database persistence (`ContactMessage`).
   - Floating WhatsApp button linking directly to `+250788812075` with pre-filled inquiry.
   - Embedded interactive OpenStreetMap centered on Nyamirambo, Kigali.
   - Official social media links (`@mpcr1990`).

6. **Custom Administrator Portal (`/admin/`)**:
   - Branded Django administration console ("MPCR Administration - Movement for Christ in Rwanda").
   - Manage Programs, Gallery Photos, Impact Statistics, Strategic Partners, Testimonials, and Contact Inquiries.
   - Inquiry message management with unread badges and quick action filters.

---

## 3. Project Structure

Adheres strictly to the **Django Project Standard Workflow & Initialization Guide**:

```
mpcr/
├── apps/
│   └── core/
│       ├── management/
│       │   └── commands/
│       │       ├── create_default_admin.py     # Secure admin user creation
│       │       └── populate_mpcr_data.py       # Seeds authentic MPCR baseline data
│       ├── migrations/
│       │   └── 0001_initial.py
│       ├── templates/
│       │   └── core/
│       │       ├── home.html                   # Home page template
│       │       ├── about.html                  # About Us template
│       │       ├── programs.html               # Programs & Activities template
│       │       ├── gallery.html                # Gallery & Lightbox template
│       │       └── contact.html                # Contact page & form template
│       ├── admin.py                            # Custom Admin interface configuration
│       ├── apps.py                             # Core AppConfig (apps.core)
│       ├── forms.py                            # ContactForm with validation
│       ├── models.py                           # Database models
│       ├── tests.py                            # Automated unit tests
│       ├── urls.py                             # App route mappings
│       └── views.py                            # View functions & error handlers
├── config/
│   ├── asgi.py
│   ├── settings.py                             # Central settings & security hardening
│   ├── urls.py                                 # Main URL routing & handler configuration
│   └── wsgi.py
├── static/
│   ├── css/
│   │   └── style.css                           # Master responsive stylesheet
│   ├── js/
│   │   └── main.js                             # Interactive navigation & lightbox JS
│   └── images/
│       └── logo.svg                            # MPCR vector logo
├── media/                                      # Uploaded media assets
├── staticfiles/                                # Output directory for collectstatic
├── templates/
│   ├── base.html                               # Global base template
│   ├── 403.html                                # Custom HTTP 403 Access Denied
│   ├── 404.html                                # Custom HTTP 404 Page Not Found
│   ├── 500.html                                # Custom HTTP 500 Server Error
│   └── includes/
│       ├── navbar.html                         # Top scripture bar + sticky nav
│       ├── footer.html                         # Reusable footer + legal notice
│       ├── messages.html                       # Django flash message alerts
│       └── whatsapp_float.html                 # Floating WhatsApp CTA
├── .env                                        # Local environment secrets (Git ignored)
├── .env.example                                # Safe environment variables template
├── .gitignore                                  # Standard Git ignore rules
├── manage.py                                   # Django management entry point
├── README.md                                   # Documentation
└── requirements.txt                            # Pinned Python dependencies
```

---

## 4. Setup & Local Development

### 4.1 Prerequisites
- Python 3.12+ (tested on Python 3.14)
- Git

### 4.2 Installation

```bash
# 1. Clone repository
git clone <repository-url>
cd mpcr

# 2. Create and activate virtual environment
python -m venv .venv

# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# 3. Install pinned dependencies
pip install -r requirements.txt

# 4. Configure environment variables
# Copy .env.example to .env and adjust if needed:
cp .env.example .env

# 5. Run migrations
python manage.py migrate

# 6. Seed authentic MPCR data and create default superuser
python manage.py populate_mpcr_data
python manage.py create_default_admin

# 7. Collect static files
python manage.py collectstatic --noinput

# 8. Start development server
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser to view the website.  
Access the administration console at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

---

## 5. Automated Testing & Verification

Run the full automated test suite covering models, views, forms, filters, error handling, and admin accessibility:

```bash
python manage.py test apps.core
```

Run Django deployment security checks:

```bash
python manage.py check --deploy
```

---

## 6. Production Deployment Notes (DirectAdmin / Passenger / Nginx)

1. Set `DEBUG=False` in `.env`.
2. Generate a secure, unique `SECRET_KEY` in `.env`.
3. Set `ALLOWED_HOSTS=mouvementpourchriste.org,www.mouvementpourchriste.org,your-domain.com`.
4. Configure database in `.env` (SQLite or PostgreSQL).
5. Run `python manage.py collectstatic --noinput` to collect static assets into `staticfiles/`.
6. Ensure HTTPS is enabled on your hosting server (`SECURE_SSL_REDIRECT=True` and `ENABLE_HSTS=True` in `.env`).
7. Point web server / Passenger to `config/wsgi.py`.
