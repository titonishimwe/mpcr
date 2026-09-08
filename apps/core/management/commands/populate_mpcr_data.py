from django.core.management.base import BaseCommand
from apps.core.models import Program, GalleryImage, ImpactStat, Partner, Testimonial


class Command(BaseCommand):
    help = "Populates the database with authentic MPCR programs, impact statistics, partners, and gallery records"

    def handle(self, *args, **options):
        self.stdout.write("Populating MPCR baseline data...")

        # 1. Programs & Activities
        programs_data = [
            {
                "title": "Strengthening Climate Change Adaptation Capacity for Poor and Vulnerable Households in Gatsibo District",
                "category": "flr",
                "summary": "Building the capacity of poor and vulnerable households in Gatsibo District to adapt to climate change and protect their livelihoods.",
                "description": (
                    "The project strengthens climate change adaptation among poor and vulnerable households in Gatsibo District. "
                    "Households are supported to protect land, food, and income against climate shocks. "
                    "Field work links restoration, livelihood support, and practical household resilience. "
                    "The intervention is implemented with local communities in Gatsibo District."
                ),
                "icon": "tree",
                "image_url": "",
                "target_beneficiaries": "Poor and vulnerable households",
                "location": "Gatsibo District",
                "is_featured": True,
                "order": 1,
            },
            {
                "title": "Single Stream Funding (SSF/VIH) for HIV/AIDS in Nyanza District",
                "category": "health",
                "summary": "HIV/AIDS response in Nyanza District, financed by the Global Fund through Single Stream Funding (SSF/VIH).",
                "description": (
                    "Single Stream Funding (SSF/VIH) supports HIV/AIDS services in Nyanza District. "
                    "The project is financed by the Global Fund. "
                    "Activities strengthen community access to HIV/AIDS prevention and care. "
                    "The work is implemented with local partners in Nyanza District."
                ),
                "icon": "heart",
                "image_url": "",
                "target_beneficiaries": "Communities affected by HIV/AIDS",
                "location": "Nyanza District",
                "is_featured": True,
                "order": 2,
            },
            {
                "title": "Professional Training in Carpentry, Gatsibo District",
                "category": "education",
                "summary": "Professional carpentry training in Gatsibo District under project 7F-01352.11.01, financed by the Embassy of Switzerland.",
                "description": (
                    "Project 7F-01352.11.01 provides professional training, specifically in carpentry, in Gatsibo District. "
                    "The project is financed by the Embassy of Switzerland. "
                    "Youth gain practical trade skills for employment and self-reliance. "
                    "Training is delivered with local communities in Gatsibo District."
                ),
                "icon": "award",
                "image_url": "",
                "target_beneficiaries": "Youth in vocational training",
                "location": "Gatsibo District",
                "is_featured": True,
                "order": 3,
            },
            {
                "title": "Scaling Up Access to HIV/AIDS Prevention Services in Rwanda",
                "category": "health",
                "summary": "Scaling up access to HIV/AIDS prevention services in Rwanda, financed by the Global Fund (R6 / VIII/R6).",
                "description": (
                    "The project scales up access to HIV/AIDS prevention services in Rwanda. "
                    "It is financed by the Global Fund under grant R6 / VIII/R6. "
                    "Community outreach reaches youth and households with prevention education. "
                    "The focus is prevention and wider access to HIV/AIDS services."
                ),
                "icon": "heart",
                "image_url": "",
                "target_beneficiaries": "Youth and communities at risk of HIV",
                "location": "Rwanda",
                "is_featured": True,
                "order": 4,
            },
            {
                "title": "Adopting Agroforestry for Land Restoration, Sustainable Livelihoods and Community Well-being in Rutsiro District",
                "category": "flr",
                "summary": "Agroforestry for land restoration, sustainable livelihoods, and community well-being in Rutsiro District, Western Province. Financed by Vumbuzi Impact Africa Foundation (VIA) in partnership with TerraFund and the World Resources Institute (WRI).",
                "description": (
                    "The project adopts agroforestry for land restoration, sustainable livelihoods, and community well-being in Rutsiro District, Western Province. "
                    "It is financed by Vumbuzi Impact Africa Foundation (VIA). "
                    "Implementation is in partnership with TerraFund and the World Resources Institute (WRI). "
                    "Communities restore degraded land while strengthening household livelihoods."
                ),
                "icon": "tree",
                "image_url": "",
                "target_beneficiaries": "Farming communities and rural households",
                "location": "Rutsiro District, Western Province",
                "is_featured": True,
                "order": 5,
            },
        ]

        for p in programs_data:
            Program.objects.update_or_create(title=p["title"], defaults=p)
        self.stdout.write(self.style.SUCCESS(f"Loaded {len(programs_data)} programs."))

        # 2. Impact Statistics
        stats_data = [
            {"value": "105+", "label": "Hectares Restored", "description": "100 ha cropland & 5 ha woodlot under active restoration in Gatsibo", "icon": "map", "order": 1},
            {"value": "28,800+", "label": "Seedlings Produced", "description": "High-quality agroforestry, woodlot & fruit trees nursery production", "icon": "sprout", "order": 2},
            {"value": "150+", "label": "Champion Farmers", "description": "Awarded goats and clean energy improved cookstoves (ICS)", "icon": "award", "order": 3},
            {"value": "240+", "label": "Livestock Distributed", "description": "Cows & goats provided to cooperative households for self-reliance", "icon": "heart", "order": 4},
            {"value": "25+", "label": "Partner Churches", "description": "Mobilized in evangelism, discipleship, and community transformation", "icon": "home", "order": 5},
            {"value": "10+", "label": "Districts Reached", "description": "Operations in Kigali, Eastern, Western, and Southern Provinces", "icon": "compass", "order": 6},
        ]
        for s in stats_data:
            ImpactStat.objects.update_or_create(label=s["label"], defaults=s)
        self.stdout.write(self.style.SUCCESS(f"Loaded {len(stats_data)} impact statistics."))

        # 3. Testimonials
        testimonials_data = [
            {
                "author": "Mr. Olivier NTIYAMIRA",
                "role": "Champion Farmer & Mobilizer",
                "location": "Nyabikiri Cell, Gatsibo District",
                "quote": "The papaya tree I was given and planted has started producing fruit. My children now have fruit to eat, and I am convinced that this will help them enjoy better health. We are grateful for the support you have provided, which helps our families become self-sufficient.",
                "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80",
                "order": 1,
            },
            {
                "author": "Madame NYIRAHISHAMUNDA Esperance",
                "role": "Champion Farmer & Cooperative Member",
                "location": "Kabarore Sector, Gatsibo District",
                "quote": "The trees that were provided to us have greatly benefited our farm. They create a favorable microclimate and crops grown alongside them are healthier, sign of better yield ahead. These trees also give us confidence that in the future we will have a sustainable source of firewood, timber, and fruits.",
                "image_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=400&q=80",
                "order": 2,
            },
            {
                "author": "Alice UWERA",
                "role": "Vice Mayor in charge of Socio-Economic Affairs",
                "location": "Kamonyi District",
                "quote": "Partnerships like the one with MPCR have brought tangible life changes to our community, enabling over 240 cooperative members to receive livestock and build sustainable household livelihoods in line with national development targets.",
                "image_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80",
                "order": 3,
            },
        ]
        for t in testimonials_data:
            Testimonial.objects.update_or_create(author=t["author"], defaults=t)
        self.stdout.write(self.style.SUCCESS(f"Loaded {len(testimonials_data)} testimonials."))

        # 4. Strategic Partners
        partners_data = [
            {"name": "TerraFund for AFR100", "category": "Forestry & Climate Partner", "website": "https://www.wri.org/initiatives/terrafund", "order": 1},
            {"name": "World Resources Institute (WRI)", "category": "Global Technical Partner", "website": "https://www.wri.org", "order": 2},
            {"name": "The Global Fund", "category": "International Health & HIV Partner", "website": "https://www.theglobalfund.org", "order": 3},
            {"name": "MINISANTE (Ministry of Health Rwanda)", "category": "Government Institutional Partner", "website": "https://www.moh.gov.rw", "order": 4},
            {"name": "Embassy of Switzerland in Rwanda", "category": "International Development Partner", "website": "https://www.eda.admin.ch/kigali", "order": 5},
            {"name": "Rwanda Governance Board (RGB)", "category": "Regulatory & Oversight Authority", "website": "https://www.rgb.rw", "order": 6},
            {"name": "African Forest Forum (AFF)", "category": "Pan-African Forestry Body", "website": "https://africanforestforum.org", "order": 7},
            {"name": "Rwanda NGO Forum (RGOF)", "category": "Civil Society Coalition", "website": "https://www.rwandangoforum.org", "order": 8},
            {"name": "International Movement for Christ (IMC)", "category": "Global Christian Fellowship", "website": "https://mouvementpourchriste.org", "order": 9},
            {"name": "EMMAUS Center", "category": "Theological & Bible Education", "website": "https://mouvementpourchriste.org", "order": 10},
        ]
        for p in partners_data:
            Partner.objects.update_or_create(name=p["name"], defaults=p)
        self.stdout.write(self.style.SUCCESS(f"Loaded {len(partners_data)} partners."))

        # 5. Gallery Photos
        gallery_data = [
            {
                "title": "Central Tree Nursery Operation",
                "category": "flr",
                "caption": "Project nursery beds producing Grevillea, Eucalyptus, Avocado, Tree Tomatoes, and Papaya seedlings for 105 ha landscape restoration.",
                "image_url": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?auto=format&fit=crop&w=800&q=80",
                "location": "Kabarore Sector, Gatsibo District",
                "date_taken": "October 2023 - 2026",
                "order": 1,
            },
            {
                "title": "Grevillea Agroforestry in Cropland",
                "category": "flr",
                "caption": "Successful integration of Grevillea robusta in agricultural cropland at 5m spacing, improving microclimate and soil moisture retention.",
                "image_url": "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=800&q=80",
                "location": "Nyabikiri Cell, Gatsibo District",
                "date_taken": "June 2026",
                "order": 2,
            },
            {
                "title": "Restored Eucalyptus Woodlot Plantation",
                "category": "flr",
                "caption": "Rehabilitated woodlot plot restored with healthy Eucalyptus trees planted at 2.5m x 2m spacing for sustainable timber and carbon capture.",
                "image_url": "https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80",
                "location": "Nyabikiri Cell, Gatsibo District",
                "date_taken": "June 2026",
                "order": 3,
            },
            {
                "title": "Champion Farmers with Papaya Harvest",
                "category": "flr",
                "caption": "Beneficiary champion farmers holding ripe, homegrown papayas produced from project nursery fruit tree seedlings.",
                "image_url": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?auto=format&fit=crop&w=800&q=80",
                "location": "Nyabikiri Cell, Gatsibo District",
                "date_taken": "2024 - 2026",
                "order": 4,
            },
            {
                "title": "On-Site Seedling Distribution to Community",
                "category": "community",
                "caption": "Community gathering in Kabarore Sector receiving seedlings, tools, and technical coaching for home plot planting.",
                "image_url": "https://images.unsplash.com/photo-1593113598332-cd288d649433?auto=format&fit=crop&w=800&q=80",
                "location": "Kabarore Sector, Gatsibo District",
                "date_taken": "Tree Planting Season",
                "order": 5,
            },
            {
                "title": "Livestock & Goat Incentive Award Scheme",
                "category": "community",
                "caption": "Small ruminants (goats) and improved cookstoves delivered to 150 champion farmers who achieved top seedling survival rates.",
                "image_url": "https://images.unsplash.com/photo-1524024973431-2ad916746881?auto=format&fit=crop&w=800&q=80",
                "location": "Gatsibo & Kamonyi Districts",
                "date_taken": "June 2026",
                "order": 6,
            },
            {
                "title": "Higher Education Sponsorship ULK Graduation",
                "category": "education",
                "caption": "Celebration of MPCR sponsored students Gildas Niyonzima and John Bosco Nkusi graduating from Kigali Independent University (ULK).",
                "image_url": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=800&q=80",
                "location": "ULK Kigali Campus",
                "date_taken": "Graduation Ceremony",
                "order": 7,
            },
            {
                "title": "Youth HIV/AIDS Awareness & Health Training",
                "category": "health",
                "caption": "Community health facilitator Celine Mukeshimana conducting basic education on epidemic diseases and HIV prevention for youth.",
                "image_url": "https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?auto=format&fit=crop&w=800&q=80",
                "location": "Muyira Center, Nyanza District",
                "date_taken": "Field Outreach",
                "order": 8,
            },
            {
                "title": "Donor Monitoring Visit by Prof. Jean Nduwamungu",
                "category": "leadership",
                "caption": "Donor representative Prof. Jean Nduwamungu inspecting restored agroforestry farmlands and consulting with local champion farmers.",
                "image_url": "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=800&q=80",
                "location": "Nyabikiri Cell, Gatsibo District",
                "date_taken": "22-23 June 2026",
                "order": 9,
            },
        ]
        for g in gallery_data:
            GalleryImage.objects.update_or_create(title=g["title"], defaults=g)
        self.stdout.write(self.style.SUCCESS(f"Loaded {len(gallery_data)} gallery photos."))

        self.stdout.write(self.style.SUCCESS("MPCR data successfully seeded!"))
