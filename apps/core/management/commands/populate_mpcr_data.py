from django.core.management.base import BaseCommand
from apps.core.models import Program, GalleryImage, ImpactStat, Partner, Testimonial


class Command(BaseCommand):
    help = "Populates the database with authentic MPCR programs, impact statistics, partners, and gallery records"

    def handle(self, *args, **options):
        self.stdout.write("Populating MPCR baseline data...")

        # 1. Programs & Activities
        programs_data = [
            {
                "title": "Forest Landscape Restoration (FLR) & Agroforestry",
                "category": "flr",
                "summary": "Restoring degraded agricultural croplands and woodlots across Gatsibo and Rutsiro districts to build climate resilience and sustainable rural livelihoods.",
                "description": (
                    "MPCR actively implements Forest Landscape Restoration (FLR) projects in partnership with "
                    "TerraFund for AFR100 and the World Resources Institute (WRI). In Gatsibo District (Kabarore Sector, "
                    "Nyabikiri Cell), MPCR piloted the restoration of 105 hectares (100 ha cropland with Grevillea robusta "
                    "and fruit trees; 5 ha woodlot into productive Eucalyptus plantation), producing 28,800 seedlings in a "
                    "central nursery. Livelihood incentives including 50 goats and 100 improved cookstoves (ICS) were awarded "
                    "to 150 champion farmers. In Rutsiro District (Western Province), MPCR is executing a multi-year agroforestry "
                    "and land restoration program running from 2026 to 2032."
                ),
                "icon": "tree",
                "image_url": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&w=1200&q=80",
                "target_beneficiaries": "Smallholder farmers, vulnerable rural households, women, youth",
                "location": "Gatsibo District (Eastern Province) & Rutsiro District (Western Province)",
                "is_featured": True,
                "order": 1,
            },
            {
                "title": "Evangelism, Biblical Training & Christian Leadership",
                "category": "evangelism",
                "summary": "Sharing the Gospel of Jesus Christ and strengthening local churches through biblical education, Sunday schools, and correspondence Bible training.",
                "description": (
                    "Rooted in John 3:16, MPCR is committed to making Christ known across Rwanda. The organization mobilizes "
                    "a network of over 25 churches, supports correspondence Bible school courses, and equips pastors and church "
                    "workers with sound theological teaching materials. Through community road shows, Christian film screenings, "
                    "and discipleship initiatives, MPCR nurtures faith, moral integrity, and social harmony."
                ),
                "icon": "book-open",
                "image_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=1200&q=80",
                "target_beneficiaries": "Local church congregations, pastors, youth, children, prisoners",
                "location": "Kigali City, Eastern, Western, and Southern Provinces",
                "is_featured": True,
                "order": 2,
            },
            {
                "title": "Child Protection & Women Economic Empowerment",
                "category": "child_women",
                "summary": "Protecting child rights, fighting gender-based violence, establishing Child Protection Committees (CPCs), and building economic capacity for vulnerable women.",
                "description": (
                    "MPCR stands firm in defending the rights of children and vulnerable women. Through community advocacy and "
                    "close collaboration with local authorities, the organization establishes and trains Child Protection Committees (CPCs). "
                    "Our target is training 25,000 Rwandan youth on child rights and combating violence against women and children, "
                    "while facilitating women's cooperatives with vocational skills and income-generating opportunities."
                ),
                "icon": "shield",
                "image_url": "https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?auto=format&fit=crop&w=1200&q=80",
                "target_beneficiaries": "Vulnerable children, women-headed households, widows, youth",
                "location": "Nyanza, Kamonyi, Gasabo, and Gatsibo Districts",
                "is_featured": True,
                "order": 3,
            },
            {
                "title": "Community Health, Nutrition & HIV Eradication",
                "category": "health",
                "summary": "Promoting holistic health ('Roho nzima itura mu mubiri muzima'), epidemic disease prevention, maternal-child health, and HIV education.",
                "description": (
                    "In line with our founding vision that 'A healthy spirit lives in a healthy body', MPCR delivers health education "
                    "in partnership with MINISANTE and the Global Fund. Field activities include HIV awareness campaigns (such as basic "
                    "HIV prevention education in Muyira Center, Nyanza District), family planning and reproductive health coaching, "
                    "and nutrition enhancement through backyard fruit tree cultivation."
                ),
                "icon": "heart",
                "image_url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1200&q=80",
                "target_beneficiaries": "Rural families, youth, expectant mothers, people living with HIV",
                "location": "Nyanza, Kamonyi, and Nyarugenge Districts",
                "is_featured": True,
                "order": 4,
            },
            {
                "title": "Sustainable Agriculture, Livestock & Cooperatives",
                "category": "agriculture",
                "summary": "Strengthening food security and household incomes through agricultural cooperatives, pineapple farming, livestock distribution, and rural savings (Ibimina).",
                "description": (
                    "MPCR empowers smallholders by grouping vulnerable community members into structured agricultural cooperatives. "
                    "Successes include pineapple farming support in Kirwa Cell (Kayenzi), cattle distribution to 240 cooperative members "
                    "in Kamonyi District in collaboration with local government, goat provision to champion farmers in Gatsibo, and "
                    "fostering community savings and lending associations (Ibimina)."
                ),
                "icon": "users",
                "image_url": "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=1200&q=80",
                "target_beneficiaries": "Cooperative farmers, rural households, vulnerable smallholders",
                "location": "Kayenzi, Kamonyi, Gatsibo, and Rutsiro",
                "is_featured": True,
                "order": 5,
            },
            {
                "title": "Youth Skills, Vocational Training & Higher Education",
                "category": "education",
                "summary": "Empowering youth for self-reliance through vocational trades, carpentry, entrepreneurship, and university scholarships.",
                "description": (
                    "Education is a cornerstone of MPCR's development strategy. With funding from the Embassy of Switzerland, MPCR "
                    "implemented vocational training projects in Gatsibo District to equip youth with marketable trades like carpentry "
                    "and masonry. In higher education, MPCR has sponsored student leaders at Kigali Independent University (ULK) up to "
                    "graduation, and continues mobilizing university students nationwide."
                ),
                "icon": "award",
                "image_url": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1200&q=80",
                "target_beneficiaries": "Unemployed youth, students, emerging community leaders",
                "location": "Gatsibo District & Kigali City",
                "is_featured": True,
                "order": 6,
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
