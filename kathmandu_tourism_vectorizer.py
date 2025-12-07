"""
Kathmandu Tourism Data Vectorizer
=================================
This script creates vector embeddings for tourism data about Kathmandu, Nepal.
Designed for fast retrieval in an iOS tourism app.

Usage:
    1. Add your tourism data to the TOURISM_DATA list
    2. Run this script to generate embeddings
    3. Export to your preferred vector database format
"""

import json
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict
from enum import Enum

# ============================================================================
# CONFIGURATION
# ============================================================================

# Choose your embedding provider
EMBEDDING_PROVIDER = "sentence_transformers"  # Options: "openai", "sentence_transformers", "cohere"
EMBEDDING_MODEL = "text-embedding-3-small"  # For OpenAI
VECTOR_DIMENSION = 1536  # Depends on your embedding model

# Vector database options
VECTOR_DB = "pinecone"  # Options: "pinecone", "qdrant", "chroma", "weaviate", "faiss"


# ============================================================================
# DATA MODELS
# ============================================================================

class PlaceCategory(Enum):
    TEMPLE = "temple"
    HERITAGE_SITE = "heritage_site"
    MUSEUM = "museum"
    RESTAURANT = "restaurant"
    HOTEL = "hotel"
    MARKET = "market"
    VIEWPOINT = "viewpoint"
    TREKKING = "trekking"
    ADVENTURE = "adventure"
    CULTURAL = "cultural"
    NATURE = "nature"
    SHOPPING = "shopping"
    NIGHTLIFE = "nightlife"
    SPA_WELLNESS = "spa_wellness"
    TRANSPORT = "transport"


@dataclass
class Location:
    latitude: float
    longitude: float
    address: str
    area: str  # e.g., "Thamel", "Durbar Square", "Boudha"
    ward: Optional[int] = None


@dataclass
class OpeningHours:
    monday: str
    tuesday: str
    wednesday: str
    thursday: str
    friday: str
    saturday: str
    sunday: str
    notes: Optional[str] = None  # e.g., "Closed on public holidays"


@dataclass
class PriceInfo:
    currency: str  # "NPR" or "USD"
    nepali_citizen: Optional[float] = None
    saarc_citizen: Optional[float] = None
    foreign_tourist: Optional[float] = None
    price_range: Optional[str] = None  # For restaurants: "$", "$$", "$$$"
    notes: Optional[str] = None


@dataclass
class TourismPlace:
    id: str
    name: str
    name_nepali: Optional[str]
    category: PlaceCategory
    subcategories: List[str]
    description: str
    short_description: str
    location: Location
    opening_hours: Optional[OpeningHours]
    price_info: Optional[PriceInfo]
    
    # Rich content
    highlights: List[str]
    tips: List[str]
    best_time_to_visit: Optional[str]
    time_needed: Optional[str]  # e.g., "2-3 hours"
    
    # Media
    images: List[str]  # URLs or asset names
    
    # Connectivity
    nearby_places: List[str]  # IDs of nearby places
    related_places: List[str]  # IDs of related places
    
    # Metadata
    tags: List[str]
    languages_spoken: List[str]
    accessibility: Optional[str]
    phone: Optional[str]
    website: Optional[str]
    email: Optional[str]
    
    # Ratings
    google_rating: Optional[float] = None
    tripadvisor_rating: Optional[float] = None
    
    # For search optimization
    keywords: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []


# ============================================================================
# SAMPLE TOURISM DATA - KATHMANDU
# ============================================================================

TOURISM_DATA: List[TourismPlace] = [
    TourismPlace(
        id="ktm_pashupatinath",
        name="Pashupatinath Temple",
        name_nepali="पशुपतिनाथ मन्दिर",
        category=PlaceCategory.TEMPLE,
        subcategories=["hindu_temple", "unesco_world_heritage", "pilgrimage"],
        description="""Pashupatinath Temple is one of the most sacred Hindu temples dedicated to Lord Shiva, 
        located on the banks of the Bagmati River. This UNESCO World Heritage Site is the oldest Hindu temple 
        in Kathmandu, dating back to 400 AD. The temple complex spans 264 hectares and includes 518 temples 
        and monuments. The main pagoda-style temple has a gilded roof and silver doors, accessible only to Hindus. 
        Cremation ghats along the river are an important feature where Hindu funeral rites are performed. 
        The temple is especially significant during Maha Shivaratri when hundreds of thousands of devotees 
        gather from Nepal and India.""",
        short_description="Sacred Hindu temple dedicated to Lord Shiva, UNESCO World Heritage Site on the Bagmati River.",
        location=Location(
            latitude=27.7107,
            longitude=85.3487,
            address="Pashupatinath, Kathmandu",
            area="Gaushala",
            ward=7
        ),
        opening_hours=OpeningHours(
            monday="4:00 AM - 9:00 PM",
            tuesday="4:00 AM - 9:00 PM",
            wednesday="4:00 AM - 9:00 PM",
            thursday="4:00 AM - 9:00 PM",
            friday="4:00 AM - 9:00 PM",
            saturday="4:00 AM - 9:00 PM",
            sunday="4:00 AM - 9:00 PM",
            notes="Evening aarti at 7:00 PM"
        ),
        price_info=PriceInfo(
            currency="NPR",
            nepali_citizen=0,
            saarc_citizen=500,
            foreign_tourist=1000,
            notes="Main temple interior only accessible to Hindus"
        ),
        highlights=[
            "UNESCO World Heritage Site",
            "Ancient Hindu temple from 400 AD",
            "Evening aarti ceremony",
            "Cremation ghats on Bagmati River",
            "Sadhus (holy men) in the complex",
            "Beautiful pagoda architecture"
        ],
        tips=[
            "Arrive early morning to avoid crowds",
            "Dress modestly - cover shoulders and knees",
            "Photography restrictions inside main temple",
            "Best to visit during Maha Shivaratri festival",
            "Hire a local guide for cultural context",
            "Be respectful at cremation ghats"
        ],
        best_time_to_visit="Early morning (5-7 AM) or evening for aarti",
        time_needed="2-3 hours",
        images=["pashupatinath_main.jpg", "pashupatinath_ghat.jpg", "pashupatinath_sadhus.jpg"],
        nearby_places=["ktm_boudhanath", "ktm_guhyeshwari"],
        related_places=["ktm_swayambhunath", "ktm_changu_narayan"],
        tags=["temple", "hindu", "unesco", "spiritual", "pilgrimage", "shiva", "cremation", "sacred"],
        languages_spoken=["Nepali", "Hindi", "English"],
        accessibility="Partially accessible - some stairs and uneven surfaces",
        phone="+977-1-4470837",
        website="https://www.pashupatinath.org.np",
        email="info@pashupatinath.org.np",
        google_rating=4.7,
        tripadvisor_rating=4.5,
        keywords=["shiva temple", "hindu temple", "cremation", "bagmati river", "pilgrimage", "shivaratri"]
    ),
    
    TourismPlace(
        id="ktm_boudhanath",
        name="Boudhanath Stupa",
        name_nepali="बौद्धनाथ स्तूप",
        category=PlaceCategory.HERITAGE_SITE,
        subcategories=["buddhist_stupa", "unesco_world_heritage", "tibetan_culture"],
        description="""Boudhanath Stupa is one of the largest spherical stupas in Nepal and a UNESCO World Heritage Site. 
        This ancient stupa is the center of Tibetan Buddhism in Nepal and a major pilgrimage site. 
        The massive mandala-style stupa features the all-seeing eyes of Buddha painted on four sides of the tower. 
        The surrounding area is home to over 50 Tibetan monasteries and is a thriving center of Tibetan culture. 
        Devotees walk clockwise around the stupa, spinning prayer wheels and chanting mantras. 
        The stupa was damaged in the 2015 earthquake but has been beautifully restored.""",
        short_description="Massive Buddhist stupa and UNESCO site, center of Tibetan Buddhism in Nepal.",
        location=Location(
            latitude=27.7215,
            longitude=85.3620,
            address="Boudha, Kathmandu",
            area="Boudha",
            ward=6
        ),
        opening_hours=OpeningHours(
            monday="6:00 AM - 9:00 PM",
            tuesday="6:00 AM - 9:00 PM",
            wednesday="6:00 AM - 9:00 PM",
            thursday="6:00 AM - 9:00 PM",
            friday="6:00 AM - 9:00 PM",
            saturday="6:00 AM - 9:00 PM",
            sunday="6:00 AM - 9:00 PM",
            notes="Best visited at dawn or dusk"
        ),
        price_info=PriceInfo(
            currency="NPR",
            nepali_citizen=0,
            saarc_citizen=100,
            foreign_tourist=400
        ),
        highlights=[
            "One of the largest stupas in the world",
            "UNESCO World Heritage Site",
            "Center of Tibetan Buddhism",
            "Beautiful rooftop restaurants with stupa views",
            "Prayer wheel circumambulation",
            "Tibetan monasteries nearby"
        ],
        tips=[
            "Visit at dawn or dusk for best atmosphere",
            "Walk clockwise around the stupa",
            "Try rooftop cafes for great views",
            "Visit surrounding monasteries",
            "Best during Losar (Tibetan New Year)",
            "Many shops sell authentic Tibetan handicrafts"
        ],
        best_time_to_visit="Early morning or sunset",
        time_needed="2-3 hours",
        images=["boudhanath_main.jpg", "boudhanath_prayer_wheels.jpg", "boudhanath_monks.jpg"],
        nearby_places=["ktm_pashupatinath", "ktm_kopan_monastery"],
        related_places=["ktm_swayambhunath", "ktm_namo_buddha"],
        tags=["stupa", "buddhist", "unesco", "tibetan", "spiritual", "monastery", "meditation"],
        languages_spoken=["Nepali", "Tibetan", "English"],
        accessibility="Wheelchair accessible around main stupa",
        phone=None,
        website=None,
        email=None,
        google_rating=4.7,
        tripadvisor_rating=4.5,
        keywords=["buddhist stupa", "tibetan", "prayer wheels", "monastery", "meditation", "losar"]
    ),
    
    TourismPlace(
        id="ktm_swayambhunath",
        name="Swayambhunath (Monkey Temple)",
        name_nepali="स्वयम्भूनाथ",
        category=PlaceCategory.HERITAGE_SITE,
        subcategories=["buddhist_stupa", "unesco_world_heritage", "viewpoint"],
        description="""Swayambhunath, also known as the Monkey Temple due to the holy monkeys living there, 
        is an ancient religious complex atop a hill in the Kathmandu Valley. The site has both Buddhist 
        and Hindu shrines and is one of the oldest religious sites in Nepal, believed to be over 2,000 years old. 
        The iconic white dome stupa with Buddha's watchful eyes is visible from all over Kathmandu. 
        Visitors must climb 365 steps to reach the top, where they are rewarded with panoramic valley views. 
        The complex includes temples, shrines, a monastery, and a museum.""",
        short_description="Ancient hilltop stupa with panoramic valley views, known for resident monkeys.",
        location=Location(
            latitude=27.7149,
            longitude=85.2903,
            address="Swayambhunath, Kathmandu",
            area="Swayambhu",
            ward=15
        ),
        opening_hours=OpeningHours(
            monday="5:00 AM - 9:00 PM",
            tuesday="5:00 AM - 9:00 PM",
            wednesday="5:00 AM - 9:00 PM",
            thursday="5:00 AM - 9:00 PM",
            friday="5:00 AM - 9:00 PM",
            saturday="5:00 AM - 9:00 PM",
            sunday="5:00 AM - 9:00 PM"
        ),
        price_info=PriceInfo(
            currency="NPR",
            nepali_citizen=0,
            saarc_citizen=100,
            foreign_tourist=200
        ),
        highlights=[
            "Panoramic views of Kathmandu Valley",
            "365 steps to the top",
            "Friendly resident monkeys",
            "Ancient Buddhist and Hindu shrines",
            "Beautiful sunset views",
            "UNESCO World Heritage Site"
        ],
        tips=[
            "Visit at sunrise for best views and fewer crowds",
            "Watch your belongings - monkeys can be mischievous",
            "Wear comfortable shoes for climbing steps",
            "Alternative vehicle road to top available",
            "Bring water for the climb",
            "Don't feed the monkeys"
        ],
        best_time_to_visit="Sunrise or sunset",
        time_needed="1.5-2 hours",
        images=["swayambhunath_main.jpg", "swayambhunath_view.jpg", "swayambhunath_monkeys.jpg"],
        nearby_places=["ktm_durbar_square", "ktm_garden_of_dreams"],
        related_places=["ktm_boudhanath", "ktm_pashupatinath"],
        tags=["stupa", "buddhist", "hindu", "unesco", "viewpoint", "monkeys", "sunset", "stairs"],
        languages_spoken=["Nepali", "English"],
        accessibility="Difficult - 365 steep steps (vehicle road alternative available)",
        phone=None,
        website=None,
        email=None,
        google_rating=4.6,
        tripadvisor_rating=4.5,
        keywords=["monkey temple", "stupa", "hilltop", "panoramic view", "sunrise", "sunset", "ancient"]
    ),
    
    TourismPlace(
        id="ktm_durbar_square",
        name="Kathmandu Durbar Square",
        name_nepali="काठमाडौं दरबार स्क्वायर",
        category=PlaceCategory.HERITAGE_SITE,
        subcategories=["unesco_world_heritage", "palace", "architecture"],
        description="""Kathmandu Durbar Square is a historic plaza in front of the old royal palace of the 
        Kathmandu Kingdom. This UNESCO World Heritage Site showcases spectacular Newar architecture with 
        numerous temples, palaces, courtyards, and statues dating from the 12th to 18th centuries. 
        Key attractions include the Hanuman Dhoka Palace, the home of the living goddess Kumari, 
        the impressive Taleju Temple, and the nine-story Basantapur Tower. Though some structures were 
        damaged in the 2015 earthquake, restoration work continues and the square remains a vibrant 
        center of cultural and religious life.""",
        short_description="Historic palace square with stunning Newar architecture and living goddess Kumari.",
        location=Location(
            latitude=27.7045,
            longitude=85.3068,
            address="Durbar Square, Kathmandu",
            area="Basantapur",
            ward=12
        ),
        opening_hours=OpeningHours(
            monday="7:00 AM - 7:00 PM",
            tuesday="7:00 AM - 7:00 PM",
            wednesday="7:00 AM - 7:00 PM",
            thursday="7:00 AM - 7:00 PM",
            friday="7:00 AM - 7:00 PM",
            saturday="7:00 AM - 7:00 PM",
            sunday="7:00 AM - 7:00 PM",
            notes="Kumari appears at her window around 9 AM and 4 PM"
        ),
        price_info=PriceInfo(
            currency="NPR",
            nepali_citizen=0,
            saarc_citizen=150,
            foreign_tourist=1000,
            notes="Multi-day pass available for foreigners"
        ),
        highlights=[
            "Hanuman Dhoka Palace complex",
            "Living Goddess Kumari's residence",
            "Taleju Temple",
            "Basantapur Tower views",
            "Intricate wood carvings",
            "Active local market atmosphere"
        ],
        tips=[
            "Hire a licensed guide for historical context",
            "Visit early morning to see Kumari",
            "Explore surrounding narrow streets",
            "Combine with Patan and Bhaktapur Durbar Squares",
            "Photography allowed in most areas",
            "Watch for ongoing restoration work"
        ],
        best_time_to_visit="Morning for Kumari sighting",
        time_needed="2-3 hours",
        images=["durbar_square_main.jpg", "durbar_square_kumari.jpg", "durbar_square_palace.jpg"],
        nearby_places=["ktm_thamel", "ktm_asan_bazaar", "ktm_freak_street"],
        related_places=["ktm_patan_durbar", "ktm_bhaktapur_durbar"],
        tags=["palace", "unesco", "architecture", "kumari", "newar", "history", "temple", "cultural"],
        languages_spoken=["Nepali", "English"],
        accessibility="Partially accessible - some uneven surfaces",
        phone=None,
        website=None,
        email=None,
        google_rating=4.5,
        tripadvisor_rating=4.0,
        keywords=["durbar square", "palace", "kumari", "living goddess", "newar", "hanuman dhoka", "heritage"]
    ),
    
    TourismPlace(
        id="ktm_thamel",
        name="Thamel",
        name_nepali="ठमेल",
        category=PlaceCategory.MARKET,
        subcategories=["tourist_hub", "shopping", "nightlife", "dining"],
        description="""Thamel is Kathmandu's main tourist district, a vibrant maze of narrow streets packed 
        with hotels, restaurants, shops, and travel agencies. Known as the gateway to the Himalayas, 
        this is where most trekkers and tourists base themselves. The area offers everything from budget 
        hostels to boutique hotels, authentic Nepali cuisine to international restaurants, and countless 
        shops selling trekking gear, handicrafts, singing bowls, and souvenirs. The nightlife scene includes 
        rooftop bars, live music venues, and clubs. Despite its touristy nature, Thamel retains charm with 
        its mix of old buildings and colorful prayer flags.""",
        short_description="Vibrant tourist hub with shops, restaurants, hotels, and lively nightlife.",
        location=Location(
            latitude=27.7153,
            longitude=85.3123,
            address="Thamel, Kathmandu",
            area="Thamel",
            ward=26
        ),
        opening_hours=OpeningHours(
            monday="Most shops 9 AM - 9 PM",
            tuesday="Most shops 9 AM - 9 PM",
            wednesday="Most shops 9 AM - 9 PM",
            thursday="Most shops 9 AM - 9 PM",
            friday="Most shops 9 AM - 9 PM",
            saturday="Most shops 9 AM - 9 PM",
            sunday="Most shops 9 AM - 9 PM",
            notes="Restaurants and bars open later"
        ),
        price_info=PriceInfo(
            currency="NPR",
            price_range="$-$$$",
            notes="Bargaining expected in shops"
        ),
        highlights=[
            "Trekking gear shops",
            "Handicraft and souvenir stores",
            "Diverse international cuisine",
            "Rooftop restaurants and bars",
            "Live music venues",
            "Travel and tour agencies"
        ],
        tips=[
            "Bargain in shops - start at 50% of asking price",
            "Verify trekking gear authenticity",
            "Book tours through reputable agencies",
            "Try rooftop restaurants for great views",
            "Explore side streets for unique finds",
            "Be cautious of touts and scams"
        ],
        best_time_to_visit="Evening for atmosphere and nightlife",
        time_needed="Half day to explore",
        images=["thamel_street.jpg", "thamel_shops.jpg", "thamel_night.jpg"],
        nearby_places=["ktm_durbar_square", "ktm_garden_of_dreams", "ktm_kaiser_mahal"],
        related_places=["ktm_asan_bazaar", "ktm_patan"],
        tags=["shopping", "nightlife", "restaurants", "tourist", "trekking", "accommodation", "bars"],
        languages_spoken=["Nepali", "English", "Hindi"],
        accessibility="Narrow streets, some accessible areas",
        phone=None,
        website=None,
        email=None,
        google_rating=4.3,
        tripadvisor_rating=4.0,
        keywords=["tourist area", "shopping", "restaurants", "nightlife", "trekking gear", "hotels", "backpacker"]
    ),
    
    TourismPlace(
        id="ktm_garden_of_dreams",
        name="Garden of Dreams",
        name_nepali="सपनाको बगैंचा",
        category=PlaceCategory.NATURE,
        subcategories=["garden", "heritage", "relaxation"],
        description="""The Garden of Dreams is a neo-classical historical garden in Kaiser Mahal, 
        offering a peaceful escape from the chaos of nearby Thamel. Built in the early 1920s by 
        Field Marshal Kaiser Shumsher Rana, this garden features European-inspired architecture 
        with pavilions, pergolas, ponds, and ornamental fountains. Recently restored with Austrian 
        assistance, the garden includes a cafe and occasionally hosts cultural events. The beautifully 
        manicured lawns, shaded pathways, and quiet corners make it perfect for relaxation, 
        reading, or escaping Kathmandu's heat and noise.""",
        short_description="Peaceful neo-classical garden, a serene escape from bustling Thamel.",
        location=Location(
            latitude=27.7141,
            longitude=85.3161,
            address="Tridevi Marg, Thamel, Kathmandu",
            area="Thamel",
            ward=26
        ),
        opening_hours=OpeningHours(
            monday="9:00 AM - 10:00 PM",
            tuesday="9:00 AM - 10:00 PM",
            wednesday="9:00 AM - 10:00 PM",
            thursday="9:00 AM - 10:00 PM",
            friday="9:00 AM - 10:00 PM",
            saturday="9:00 AM - 10:00 PM",
            sunday="9:00 AM - 10:00 PM"
        ),
        price_info=PriceInfo(
            currency="NPR",
            nepali_citizen=100,
            saarc_citizen=200,
            foreign_tourist=400
        ),
        highlights=[
            "Beautiful neo-classical architecture",
            "Peaceful escape from city chaos",
            "Lovely cafe inside the garden",
            "Well-maintained lawns and fountains",
            "Cultural events and concerts",
            "Perfect for photography"
        ],
        tips=[
            "Great spot for afternoon relaxation",
            "Enjoy coffee at the garden cafe",
            "Visit after exploring busy Thamel",
            "Check for evening events",
            "Good spot for reading",
            "Romantic evening atmosphere"
        ],
        best_time_to_visit="Late afternoon for pleasant weather",
        time_needed="1-2 hours",
        images=["garden_dreams_main.jpg", "garden_dreams_fountain.jpg", "garden_dreams_pavilion.jpg"],
        nearby_places=["ktm_thamel", "ktm_durbar_square", "ktm_kaiser_mahal"],
        related_places=["ktm_nagarkot", "ktm_godavari"],
        tags=["garden", "peaceful", "relaxation", "cafe", "photography", "romantic", "heritage"],
        languages_spoken=["Nepali", "English"],
        accessibility="Wheelchair accessible",
        phone="+977-1-4425340",
        website="https://www.gardenofdreams.org.np",
        email="info@gardenofdreams.org.np",
        google_rating=4.5,
        tripadvisor_rating=4.5,
        keywords=["garden", "peaceful", "relaxation", "cafe", "heritage", "european", "romantic"]
    ),
    
    TourismPlace(
        id="ktm_patan_durbar",
        name="Patan Durbar Square",
        name_nepali="ललितपुर दरबार स्क्वायर",
        category=PlaceCategory.HERITAGE_SITE,
        subcategories=["unesco_world_heritage", "palace", "architecture", "newar"],
        description="""Patan Durbar Square, located in Lalitpur, is one of the three Durbar Squares in the Kathmandu Valley 
        and a UNESCO World Heritage Site. This ancient square showcases exquisite Newar architecture with intricately carved 
        wooden windows, temples, and palaces dating back to the 16th century. The square is home to the Krishna Mandir, 
        a stone temple built in the Shikhara style, and the Golden Temple (Hiranya Varna Mahavihar), a Buddhist monastery 
        covered in gold. The Patan Museum, housed in the former royal palace, displays traditional Nepali art and artifacts.""",
        short_description="UNESCO World Heritage Site showcasing exquisite Newar architecture and ancient temples.",
        location=Location(
            latitude=27.6736,
            longitude=85.3244,
            address="Patan Durbar Square, Lalitpur",
            area="Patan",
            ward=22
        ),
        opening_hours=OpeningHours(
            monday="7:00 AM - 7:00 PM",
            tuesday="7:00 AM - 7:00 PM",
            wednesday="7:00 AM - 7:00 PM",
            thursday="7:00 AM - 7:00 PM",
            friday="7:00 AM - 7:00 PM",
            saturday="7:00 AM - 7:00 PM",
            sunday="7:00 AM - 7:00 PM"
        ),
        price_info=PriceInfo(
            currency="NPR",
            nepali_citizen=0,
            saarc_citizen=150,
            foreign_tourist=1000,
            notes="Multi-day pass available"
        ),
        highlights=[
            "UNESCO World Heritage Site",
            "Krishna Mandir (stone temple)",
            "Golden Temple (Hiranya Varna Mahavihar)",
            "Patan Museum",
            "Intricate wood carvings",
            "Traditional Newar architecture"
        ],
        tips=[
            "Visit Patan Museum for cultural context",
            "Best visited in morning light",
            "Hire a local guide for history",
            "Combine with Bhaktapur Durbar Square",
            "Photography allowed",
            "Explore surrounding narrow streets"
        ],
        best_time_to_visit="Morning for best lighting",
        time_needed="2-3 hours",
        images=["patan_durbar_main.jpg", "patan_krishna_temple.jpg", "patan_golden_temple.jpg"],
        nearby_places=["ktm_bhaktapur_durbar", "ktm_kopan_monastery"],
        related_places=["ktm_durbar_square", "ktm_bhaktapur_durbar"],
        tags=["unesco", "architecture", "newar", "temple", "palace", "museum", "heritage", "cultural"],
        languages_spoken=["Nepali", "English"],
        accessibility="Partially accessible - some uneven surfaces",
        phone=None,
        website=None,
        email=None,
        google_rating=4.6,
        tripadvisor_rating=4.5,
        keywords=["patan", "durbar square", "lalitpur", "krishna mandir", "golden temple", "newar", "unesco"]
    ),
    
    TourismPlace(
        id="ktm_bhaktapur_durbar",
        name="Bhaktapur Durbar Square",
        name_nepali="भक्तपुर दरबार स्क्वायर",
        category=PlaceCategory.HERITAGE_SITE,
        subcategories=["unesco_world_heritage", "palace", "architecture", "medieval"],
        description="""Bhaktapur Durbar Square is the most well-preserved of the three Durbar Squares in the Kathmandu Valley. 
        This UNESCO World Heritage Site transports visitors back to medieval Nepal with its cobblestone streets, ancient temples, 
        and traditional Newar architecture. The square features the 55-Window Palace, Nyatapola Temple (Nepal's tallest temple), 
        and the Golden Gate. The city is famous for its pottery square where artisans create traditional clay pots. 
        Bhaktapur is also known as the 'City of Devotees' and offers a glimpse into authentic Nepali culture.""",
        short_description="Best-preserved medieval city in Nepal, UNESCO World Heritage Site with ancient temples.",
        location=Location(
            latitude=27.6710,
            longitude=85.4298,
            address="Bhaktapur Durbar Square, Bhaktapur",
            area="Bhaktapur",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="7:00 AM - 7:00 PM",
            tuesday="7:00 AM - 7:00 PM",
            wednesday="7:00 AM - 7:00 PM",
            thursday="7:00 AM - 7:00 PM",
            friday="7:00 AM - 7:00 PM",
            saturday="7:00 AM - 7:00 PM",
            sunday="7:00 AM - 7:00 PM"
        ),
        price_info=PriceInfo(
            currency="NPR",
            nepali_citizen=0,
            saarc_citizen=500,
            foreign_tourist=1500,
            notes="Multi-day pass available"
        ),
        highlights=[
            "Nyatapola Temple (tallest in Nepal)",
            "55-Window Palace",
            "Golden Gate",
            "Pottery Square",
            "Medieval architecture",
            "UNESCO World Heritage Site"
        ],
        tips=[
            "Visit Pottery Square to see artisans at work",
            "Try Juju Dhau (King Curd) - local specialty",
            "Best visited early morning or late afternoon",
            "Allow 3-4 hours to explore fully",
            "Wear comfortable walking shoes",
            "Hire a guide for historical context"
        ],
        best_time_to_visit="Early morning or late afternoon",
        time_needed="3-4 hours",
        images=["bhaktapur_durbar_main.jpg", "bhaktapur_nyatapola.jpg", "bhaktapur_pottery.jpg"],
        nearby_places=["ktm_changu_narayan", "ktm_nagarkot"],
        related_places=["ktm_durbar_square", "ktm_patan_durbar"],
        tags=["unesco", "medieval", "architecture", "pottery", "newar", "heritage", "cultural", "temple"],
        languages_spoken=["Nepali", "English"],
        accessibility="Cobblestone streets - challenging for wheelchairs",
        phone=None,
        website=None,
        email=None,
        google_rating=4.7,
        tripadvisor_rating=4.5,
        keywords=["bhaktapur", "durbar square", "nyatapola", "pottery", "medieval", "unesco", "juju dhau"]
    ),
    
    TourismPlace(
        id="ktm_nagarkot",
        name="Nagarkot",
        name_nepali="नगरकोट",
        category=PlaceCategory.VIEWPOINT,
        subcategories=["viewpoint", "sunrise", "himalayas", "mountain_view"],
        description="""Nagarkot is a popular hill station located 32 km east of Kathmandu, famous for its spectacular sunrise 
        and sunset views of the Himalayas. At an elevation of 2,195 meters, it offers panoramic vistas of eight of the world's 
        highest peaks including Mount Everest, Langtang, Ganesh Himal, and more. The village is surrounded by pine forests and 
        offers numerous hiking trails. Many visitors stay overnight to catch the breathtaking sunrise over the snow-capped mountains. 
        Nagarkot is also a great base for trekking and nature walks.""",
        short_description="Hill station with spectacular sunrise views of the Himalayas including Mount Everest.",
        location=Location(
            latitude=27.7153,
            longitude=85.5208,
            address="Nagarkot, Bhaktapur District",
            area="Nagarkot",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="24 hours",
            tuesday="24 hours",
            wednesday="24 hours",
            thursday="24 hours",
            friday="24 hours",
            saturday="24 hours",
            sunday="24 hours"
        ),
        price_info=PriceInfo(
            currency="NPR",
            nepali_citizen=0,
            saarc_citizen=0,
            foreign_tourist=0,
            notes="Free entry, accommodation charges apply"
        ),
        highlights=[
            "Sunrise views of Mount Everest",
            "Panoramic Himalayan vistas",
            "Eight highest peaks visible",
            "Hiking and trekking trails",
            "Peaceful mountain atmosphere",
            "Stargazing opportunities"
        ],
        tips=[
            "Stay overnight for sunrise experience",
            "Best views in October-April (clear season)",
            "Wake up early (5:30 AM) for sunrise",
            "Bring warm clothing - it gets cold",
            "Book accommodation in advance during peak season",
            "Try local mountain cuisine"
        ],
        best_time_to_visit="October to April for clearest views",
        time_needed="1-2 days (overnight recommended)",
        images=["nagarkot_sunrise.jpg", "nagarkot_himalayas.jpg", "nagarkot_viewpoint.jpg"],
        nearby_places=["ktm_bhaktapur_durbar", "ktm_changu_narayan"],
        related_places=["ktm_swayambhunath", "pokhara_sarangkot"],
        tags=["viewpoint", "sunrise", "himalayas", "everest", "mountain", "hiking", "nature", "scenic"],
        languages_spoken=["Nepali", "English"],
        accessibility="Some viewpoints accessible, hiking trails vary",
        phone=None,
        website=None,
        email=None,
        google_rating=4.5,
        tripadvisor_rating=4.5,
        keywords=["nagarkot", "sunrise", "everest", "himalayas", "mountain view", "viewpoint", "hiking"]
    ),
    
    TourismPlace(
        id="ktm_changu_narayan",
        name="Changu Narayan Temple",
        name_nepali="चाँगुनारायण मन्दिर",
        category=PlaceCategory.TEMPLE,
        subcategories=["hindu_temple", "unesco_world_heritage", "ancient", "architecture"],
        description="""Changu Narayan is an ancient Hindu temple dedicated to Lord Vishnu, located on a hilltop in Bhaktapur district. 
        Dating back to the 4th century, it is considered the oldest temple in Nepal and a UNESCO World Heritage Site. The temple 
        features exquisite stone, wood, and metal carvings depicting various incarnations of Vishnu. The two-story pagoda-style 
        structure is surrounded by ancient stone sculptures and inscriptions. The temple offers beautiful views of the Kathmandu 
        Valley and is less crowded than other heritage sites.""",
        short_description="Oldest temple in Nepal (4th century), UNESCO World Heritage Site dedicated to Lord Vishnu.",
        location=Location(
            latitude=27.7153,
            longitude=85.4298,
            address="Changu Narayan, Bhaktapur",
            area="Changu",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="6:00 AM - 6:00 PM",
            tuesday="6:00 AM - 6:00 PM",
            wednesday="6:00 AM - 6:00 PM",
            thursday="6:00 AM - 6:00 PM",
            friday="6:00 AM - 6:00 PM",
            saturday="6:00 AM - 6:00 PM",
            sunday="6:00 AM - 6:00 PM"
        ),
        price_info=PriceInfo(
            currency="NPR",
            nepali_citizen=0,
            saarc_citizen=100,
            foreign_tourist=300
        ),
        highlights=[
            "Oldest temple in Nepal (4th century)",
            "UNESCO World Heritage Site",
            "Exquisite stone and wood carvings",
            "Ancient inscriptions",
            "Beautiful valley views",
            "Less crowded than other sites"
        ],
        tips=[
            "Combine visit with Bhaktapur Durbar Square",
            "Hire a guide to understand the carvings",
            "Best visited in morning",
            "Photography allowed",
            "Wear comfortable shoes for climb",
            "Respect the sacred space"
        ],
        best_time_to_visit="Morning for best lighting",
        time_needed="1-2 hours",
        images=["changu_narayan_main.jpg", "changu_carvings.jpg", "changu_view.jpg"],
        nearby_places=["ktm_bhaktapur_durbar", "ktm_nagarkot"],
        related_places=["ktm_pashupatinath", "ktm_swayambhunath"],
        tags=["temple", "ancient", "unesco", "hindu", "vishnu", "architecture", "heritage", "spiritual"],
        languages_spoken=["Nepali", "English"],
        accessibility="Requires climbing steps",
        phone=None,
        website=None,
        email=None,
        google_rating=4.6,
        tripadvisor_rating=4.5,
        keywords=["changu narayan", "oldest temple", "vishnu", "unesco", "ancient", "bhaktapur"]
    ),
    
    TourismPlace(
        id="ktm_kopan_monastery",
        name="Kopan Monastery",
        name_nepali="कोपन मठ",
        category=PlaceCategory.CULTURAL,
        subcategories=["buddhist_monastery", "meditation", "tibetan", "spiritual"],
        description="""Kopan Monastery is a Tibetan Buddhist monastery located on a hilltop north of Boudhanath. Founded in 1969, 
        it is one of the most important centers for Tibetan Buddhism in Nepal. The monastery offers meditation courses, Buddhist 
        philosophy classes, and retreats for both beginners and advanced practitioners. The peaceful grounds feature beautiful 
        gardens, prayer wheels, and stunning views of the Kathmandu Valley. Kopan is particularly famous for its month-long 
        meditation courses that attract students from around the world.""",
        short_description="Tibetan Buddhist monastery offering meditation courses and spiritual retreats.",
        location=Location(
            latitude=27.7333,
            longitude=85.3667,
            address="Kopan, Kathmandu",
            area="Kopan",
            ward=6
        ),
        opening_hours=OpeningHours(
            monday="9:00 AM - 5:00 PM",
            tuesday="9:00 AM - 5:00 PM",
            wednesday="9:00 AM - 5:00 PM",
            thursday="9:00 AM - 5:00 PM",
            friday="9:00 AM - 5:00 PM",
            saturday="9:00 AM - 5:00 PM",
            sunday="9:00 AM - 5:00 PM",
            notes="Meditation courses have different schedules"
        ),
        price_info=PriceInfo(
            currency="NPR",
            nepali_citizen=0,
            saarc_citizen=0,
            foreign_tourist=0,
            notes="Donations welcome, courses have fees"
        ),
        highlights=[
            "Tibetan Buddhist meditation center",
            "Month-long meditation courses",
            "Beautiful hilltop location",
            "Peaceful gardens and grounds",
            "Buddhist philosophy classes",
            "Stunning valley views"
        ],
        tips=[
            "Book meditation courses in advance",
            "Respect the monastery rules",
            "Dress modestly",
            "No photography inside main halls",
            "Combine visit with Boudhanath",
            "Attend morning prayers if possible"
        ],
        best_time_to_visit="Morning for prayers, any time for grounds",
        time_needed="1-2 hours (or longer for courses)",
        images=["kopan_monastery_main.jpg", "kopan_gardens.jpg", "kopan_meditation.jpg"],
        nearby_places=["ktm_boudhanath", "ktm_pashupatinath"],
        related_places=["ktm_boudhanath", "ktm_swayambhunath"],
        tags=["monastery", "buddhist", "tibetan", "meditation", "spiritual", "retreat", "peaceful"],
        languages_spoken=["Nepali", "Tibetan", "English"],
        accessibility="Some areas accessible, meditation halls may have steps",
        phone="+977-1-4811966",
        website="https://kopanmonastery.com",
        email="info@kopanmonastery.com",
        google_rating=4.7,
        tripadvisor_rating=4.5,
        keywords=["kopan", "monastery", "meditation", "tibetan", "buddhist", "retreat", "spiritual"]
    ),
    
    TourismPlace(
        id="pokhara_phewa_lake",
        name="Phewa Lake",
        name_nepali="फेवा ताल",
        category=PlaceCategory.NATURE,
        subcategories=["lake", "boating", "viewpoint", "nature"],
        description="""Phewa Lake, also known as Fewa Lake, is the second largest lake in Nepal and the centerpiece of Pokhara's 
        natural beauty. The lake offers stunning reflections of the Annapurna mountain range, including the famous Machhapuchhre 
        (Fishtail) peak. Visitors can enjoy boating, kayaking, and paddle boating on the lake. The lakeside area is lined with 
        restaurants, cafes, and hotels. The Tal Barahi Temple, located on an island in the middle of the lake, is a popular 
        destination accessible only by boat. The lake is especially beautiful at sunrise and sunset.""",
        short_description="Beautiful lake in Pokhara with stunning mountain reflections and boating activities.",
        location=Location(
            latitude=28.2096,
            longitude=83.9856,
            address="Lakeside, Pokhara",
            area="Lakeside",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="6:00 AM - 7:00 PM",
            tuesday="6:00 AM - 7:00 PM",
            wednesday="6:00 AM - 7:00 PM",
            thursday="6:00 AM - 7:00 PM",
            friday="6:00 AM - 7:00 PM",
            saturday="6:00 AM - 7:00 PM",
            sunday="6:00 AM - 7:00 PM"
        ),
        price_info=PriceInfo(
            currency="NPR",
            nepali_citizen=0,
            saarc_citizen=0,
            foreign_tourist=0,
            notes="Boating charges apply (500-1000 NPR)"
        ),
        highlights=[
            "Stunning Annapurna mountain reflections",
            "Boating and kayaking",
            "Tal Barahi Temple on island",
            "Beautiful sunrise and sunset",
            "Lakeside restaurants and cafes",
            "Peaceful atmosphere"
        ],
        tips=[
            "Visit at sunrise for best mountain views",
            "Take a boat to Tal Barahi Temple",
            "Enjoy lakeside dining",
            "Try kayaking or paddle boating",
            "Best weather October-April",
            "Watch sunset from lakeside"
        ],
        best_time_to_visit="Early morning or evening",
        time_needed="2-3 hours",
        images=["phewa_lake_main.jpg", "phewa_boating.jpg", "phewa_sunset.jpg"],
        nearby_places=["pokhara_sarangkot", "pokhara_world_peace_pagoda"],
        related_places=["pokhara_begnas_lake", "pokhara_rara_lake"],
        tags=["lake", "boating", "nature", "mountains", "annapurna", "scenic", "peaceful", "temple"],
        languages_spoken=["Nepali", "English"],
        accessibility="Lakeside accessible, boating requires mobility",
        phone=None,
        website=None,
        email=None,
        google_rating=4.6,
        tripadvisor_rating=4.5,
        keywords=["phewa lake", "pokhara", "boating", "annapurna", "mountain view", "lakeside", "fewa"]
    ),
    
    TourismPlace(
        id="pokhara_sarangkot",
        name="Sarangkot",
        name_nepali="साराङकोट",
        category=PlaceCategory.VIEWPOINT,
        subcategories=["viewpoint", "sunrise", "himalayas", "paragliding"],
        description="""Sarangkot is a popular hilltop viewpoint located 5 km northwest of Pokhara, offering spectacular panoramic 
        views of the Annapurna mountain range, Dhaulagiri, and Machhapuchhre (Fishtail) peak. At an elevation of 1,600 meters, 
        it's one of the best places in Nepal to watch sunrise over the Himalayas. The viewpoint is also famous for paragliding, 
        with many operators offering tandem flights that launch from Sarangkot and land near Phewa Lake. The area has several 
        hotels and restaurants catering to sunrise watchers.""",
        short_description="Best sunrise viewpoint in Pokhara with stunning Himalayan vistas and paragliding opportunities.",
        location=Location(
            latitude=28.2500,
            longitude=83.8500,
            address="Sarangkot, Pokhara",
            area="Sarangkot",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="24 hours",
            tuesday="24 hours",
            wednesday="24 hours",
            thursday="24 hours",
            friday="24 hours",
            saturday="24 hours",
            sunday="24 hours"
        ),
        price_info=PriceInfo(
            currency="NPR",
            nepali_citizen=0,
            saarc_citizen=0,
            foreign_tourist=0,
            notes="Free entry, paragliding costs 8000-12000 NPR"
        ),
        highlights=[
            "Spectacular sunrise views",
            "Annapurna mountain range",
            "Paragliding launch site",
            "Dhaulagiri and Machhapuchhre views",
            "Photography paradise",
            "Peaceful mountain atmosphere"
        ],
        tips=[
            "Wake up early (5:30 AM) for sunrise",
            "Best views October-April",
            "Try paragliding for unique experience",
            "Bring warm clothing - it's cold at dawn",
            "Book accommodation in advance",
            "Check weather forecast before visiting"
        ],
        best_time_to_visit="October to April for clearest views",
        time_needed="2-3 hours (or overnight)",
        images=["sarangkot_sunrise.jpg", "sarangkot_paragliding.jpg", "sarangkot_mountains.jpg"],
        nearby_places=["pokhara_phewa_lake", "pokhara_world_peace_pagoda"],
        related_places=["ktm_nagarkot", "pokhara_dhampus"],
        tags=["viewpoint", "sunrise", "himalayas", "annapurna", "paragliding", "mountain", "scenic"],
        languages_spoken=["Nepali", "English"],
        accessibility="Viewpoint accessible, paragliding requires mobility",
        phone=None,
        website=None,
        email=None,
        google_rating=4.7,
        tripadvisor_rating=4.5,
        keywords=["sarangkot", "sunrise", "annapurna", "paragliding", "viewpoint", "pokhara", "himalayas"]
    ),
    
    TourismPlace(
        id="pokhara_world_peace_pagoda",
        name="World Peace Pagoda",
        name_nepali="विश्व शान्ति स्तूप",
        category=PlaceCategory.TEMPLE,
        subcategories=["buddhist_stupa", "viewpoint", "hiking", "peaceful"],
        description="""The World Peace Pagoda, also known as Shanti Stupa, is a Buddhist stupa located on a hilltop overlooking 
        Pokhara and Phewa Lake. Built by Japanese Buddhists in 1973, it's one of 80 peace pagodas around the world. The white 
        dome-shaped structure offers panoramic views of the Annapurna range, Pokhara city, and Phewa Lake. Visitors can reach it 
        by hiking from the lakeside (about 1 hour) or by taking a boat across the lake and then hiking. The pagoda is a symbol 
        of peace and provides a serene atmosphere for meditation and reflection.""",
        short_description="Buddhist peace pagoda with stunning views of Pokhara, Phewa Lake, and Annapurna mountains.",
        location=Location(
            latitude=28.2000,
            longitude=83.9500,
            address="Ananda Hill, Pokhara",
            area="Lakeside",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="6:00 AM - 6:00 PM",
            tuesday="6:00 AM - 6:00 PM",
            wednesday="6:00 AM - 6:00 PM",
            thursday="6:00 AM - 6:00 PM",
            friday="6:00 AM - 6:00 PM",
            saturday="6:00 AM - 6:00 PM",
            sunday="6:00 AM - 6:00 PM"
        ),
        price_info=PriceInfo(
            currency="NPR",
            nepali_citizen=0,
            saarc_citizen=0,
            foreign_tourist=0
        ),
        highlights=[
            "Panoramic views of Pokhara",
            "Stunning Phewa Lake vista",
            "Annapurna mountain views",
            "Peaceful meditation spot",
            "Beautiful hiking trail",
            "Symbol of world peace"
        ],
        tips=[
            "Hike from lakeside for best experience",
            "Take boat across lake then hike",
            "Best visited early morning or evening",
            "Bring water for the hike",
            "Wear comfortable hiking shoes",
            "Respect the peaceful atmosphere"
        ],
        best_time_to_visit="Early morning or sunset",
        time_needed="2-3 hours (including hike)",
        images=["peace_pagoda_main.jpg", "peace_pagoda_view.jpg", "peace_pagoda_hike.jpg"],
        nearby_places=["pokhara_phewa_lake", "pokhara_sarangkot"],
        related_places=["ktm_boudhanath", "ktm_swayambhunath"],
        tags=["stupa", "buddhist", "peace", "viewpoint", "hiking", "meditation", "scenic", "peaceful"],
        languages_spoken=["Nepali", "English"],
        accessibility="Requires hiking - challenging for wheelchairs",
        phone=None,
        website=None,
        email=None,
        google_rating=4.6,
        tripadvisor_rating=4.5,
        keywords=["world peace pagoda", "shanti stupa", "pokhara", "hiking", "viewpoint", "buddhist", "peace"]
    ),
    
    TourismPlace(
        id="chitwan_national_park",
        name="Chitwan National Park",
        name_nepali="चितवन राष्ट्रिय निकुञ्ज",
        category=PlaceCategory.NATURE,
        subcategories=["national_park", "wildlife", "jungle_safari", "unesco"],
        description="""Chitwan National Park is Nepal's first national park and a UNESCO World Heritage Site, covering 932 square 
        kilometers of subtropical lowlands. The park is famous for its population of one-horned rhinoceros, Bengal tigers, elephants, 
        and over 500 species of birds. Visitors can experience jungle safaris on elephant back, jeep safaris, canoe rides, and 
        guided nature walks. The park also has a crocodile breeding center and elephant breeding center. Tharu cultural programs 
        showcase the local indigenous culture. The best time to visit is October to March when wildlife is most active.""",
        short_description="UNESCO World Heritage Site with one-horned rhinos, tigers, and diverse wildlife in jungle setting.",
        location=Location(
            latitude=27.5000,
            longitude=84.3333,
            address="Chitwan District",
            area="Sauraha",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="6:00 AM - 6:00 PM",
            tuesday="6:00 AM - 6:00 PM",
            wednesday="6:00 AM - 6:00 PM",
            thursday="6:00 AM - 6:00 PM",
            friday="6:00 AM - 6:00 PM",
            saturday="6:00 AM - 6:00 PM",
            sunday="6:00 AM - 6:00 PM"
        ),
        price_info=PriceInfo(
            currency="NPR",
            nepali_citizen=100,
            saarc_citizen=1500,
            foreign_tourist=2000,
            notes="Additional charges for safaris and activities"
        ),
        highlights=[
            "One-horned rhinoceros",
            "Bengal tigers",
            "Elephant safaris",
            "Jungle walks",
            "Bird watching (500+ species)",
            "Tharu cultural programs"
        ],
        tips=[
            "Best visited October-March",
            "Book safaris in advance",
            "Bring binoculars for bird watching",
            "Wear neutral-colored clothing",
            "Follow guide's instructions for safety",
            "Stay at least 2-3 days"
        ],
        best_time_to_visit="October to March (dry season)",
        time_needed="2-3 days recommended",
        images=["chitwan_rhino.jpg", "chitwan_elephant_safari.jpg", "chitwan_jungle.jpg"],
        nearby_places=["chitwan_tharu_village"],
        related_places=["pokhara_phewa_lake"],
        tags=["national park", "wildlife", "safari", "rhino", "tiger", "jungle", "unesco", "nature"],
        languages_spoken=["Nepali", "English", "Tharu"],
        accessibility="Limited - safaris require mobility",
        phone="+977-56-580123",
        website="https://chitwannationalpark.gov.np",
        email=None,
        google_rating=4.7,
        tripadvisor_rating=4.5,
        keywords=["chitwan", "national park", "rhino", "tiger", "safari", "wildlife", "jungle", "unesco"]
    ),
    
    TourismPlace(
        id="lumbini_buddha_birthplace",
        name="Lumbini - Buddha's Birthplace",
        name_nepali="लुम्बिनी",
        category=PlaceCategory.HERITAGE_SITE,
        subcategories=["unesco_world_heritage", "buddhist", "pilgrimage", "sacred"],
        description="""Lumbini is the birthplace of Siddhartha Gautama, who later became Buddha. This UNESCO World Heritage Site 
        is one of the most important Buddhist pilgrimage sites in the world. The sacred garden contains the Mayadevi Temple, marking 
        the exact spot where Buddha was born, and the Ashoka Pillar erected by Emperor Ashoka in 249 BC. The area features numerous 
        monasteries built by Buddhist countries from around the world, each showcasing unique architectural styles. The Lumbini 
        Museum and International Research Institute provide insights into Buddhism and the site's history.""",
        short_description="Sacred birthplace of Buddha, UNESCO World Heritage Site and major Buddhist pilgrimage destination.",
        location=Location(
            latitude=27.4833,
            longitude=83.2833,
            address="Lumbini, Rupandehi District",
            area="Lumbini",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="6:00 AM - 6:00 PM",
            tuesday="6:00 AM - 6:00 PM",
            wednesday="6:00 AM - 6:00 PM",
            thursday="6:00 AM - 6:00 PM",
            friday="6:00 AM - 6:00 PM",
            saturday="6:00 AM - 6:00 PM",
            sunday="6:00 AM - 6:00 PM"
        ),
        price_info=PriceInfo(
            currency="NPR",
            nepali_citizen=0,
            saarc_citizen=200,
            foreign_tourist=500
        ),
        highlights=[
            "Birthplace of Buddha",
            "Mayadevi Temple",
            "Ashoka Pillar (249 BC)",
            "International monasteries",
            "UNESCO World Heritage Site",
            "Sacred garden"
        ],
        tips=[
            "Visit early morning for peaceful atmosphere",
            "Explore international monasteries",
            "Visit Lumbini Museum",
            "Respect the sacred space",
            "Allow full day to explore",
            "Best visited during Buddha Jayanti"
        ],
        best_time_to_visit="Year-round, Buddha Jayanti (May) is special",
        time_needed="Full day",
        images=["lumbini_temple.jpg", "lumbini_pillar.jpg", "lumbini_monasteries.jpg"],
        nearby_places=[],
        related_places=["ktm_boudhanath", "ktm_swayambhunath"],
        tags=["buddhist", "pilgrimage", "unesco", "sacred", "buddha", "temple", "heritage", "spiritual"],
        languages_spoken=["Nepali", "English"],
        accessibility="Main areas accessible, some monasteries may have steps",
        phone="+977-71-580141",
        website="https://lumbini.gov.np",
        email=None,
        google_rating=4.6,
        tripadvisor_rating=4.5,
        keywords=["lumbini", "buddha", "birthplace", "pilgrimage", "unesco", "mayadevi", "buddhist", "sacred"]
    ),
    
    # ============================================================================
    # DANG DISTRICT - Tharu Culture & Terai Region
    # ============================================================================
    
    TourismPlace(
        id="dang_dharapani",
        name="Dharapani (World's Tallest Trishul)",
        name_nepali="धरापानी",
        category=PlaceCategory.HERITAGE_SITE,
        subcategories=["religious", "monument", "tharu_culture"],
        description="""Dharapani is home to the world's tallest Trishul (trident), a massive 108-foot tall religious monument 
        dedicated to Lord Shiva. Located in the heart of Dang Valley, this impressive structure stands as a symbol of Hindu 
        devotion and Tharu cultural heritage. The Trishul is surrounded by a temple complex and is a significant pilgrimage site 
        for devotees. The area offers beautiful views of the surrounding Terai plains and is especially vibrant during religious 
        festivals like Maha Shivaratri.""",
        short_description="World's tallest Trishul (108 feet) dedicated to Lord Shiva, symbol of Tharu culture.",
        location=Location(
            latitude=28.0500,
            longitude=82.4833,
            address="Dharapani, Dang District",
            area="Dharapani",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="6:00 AM - 8:00 PM",
            tuesday="6:00 AM - 8:00 PM",
            wednesday="6:00 AM - 8:00 PM",
            thursday="6:00 AM - 8:00 PM",
            friday="6:00 AM - 8:00 PM",
            saturday="6:00 AM - 8:00 PM",
            sunday="6:00 AM - 8:00 PM"
        ),
        price_info=PriceInfo(
            currency="NPR",
            nepali_citizen=0,
            saarc_citizen=0,
            foreign_tourist=0
        ),
        highlights=[
            "World's tallest Trishul (108 feet)",
            "Lord Shiva temple complex",
            "Tharu cultural significance",
            "Beautiful Terai valley views",
            "Religious pilgrimage site",
            "Festival celebrations"
        ],
        tips=[
            "Visit during Maha Shivaratri for special celebrations",
            "Best visited in morning or evening",
            "Respect the religious site",
            "Combine with Tharu Cultural Museum visit",
            "Photography allowed",
            "Try local Tharu food nearby"
        ],
        best_time_to_visit="Year-round, especially during festivals",
        time_needed="1-2 hours",
        images=["dharapani_trishul.jpg", "dharapani_temple.jpg", "dharapani_festival.jpg"],
        nearby_places=["dang_tharu_museum", "dang_jakhera_lake"],
        related_places=["dang_bageshwori_temple"],
        tags=["temple", "trishul", "shiva", "tharu", "religious", "monument", "heritage", "cultural"],
        languages_spoken=["Nepali", "Tharu", "Hindi", "English"],
        accessibility="Main area accessible",
        phone=None,
        website=None,
        email=None,
        google_rating=4.4,
        tripadvisor_rating=4.3,
        keywords=["dharapani", "trishul", "shiva", "world tallest", "tharu", "dang", "religious", "monument"]
    ),
    
    TourismPlace(
        id="dang_jakhera_lake",
        name="Jakhera Lake",
        name_nepali="जखेरा ताल",
        category=PlaceCategory.NATURE,
        subcategories=["lake", "nature", "bird_watching", "peaceful"],
        description="""Jakhera Lake is a serene natural lake located in Dang district, surrounded by lush greenery and traditional 
        Tharu villages. The lake is a haven for bird watchers, with numerous migratory and local bird species. The peaceful 
        atmosphere makes it perfect for relaxation and nature walks. Local Tharu communities often use the lake for fishing and 
        traditional activities. The area around the lake offers opportunities for boating and picnicking.""",
        short_description="Serene natural lake perfect for bird watching, boating, and peaceful nature walks.",
        location=Location(
            latitude=28.0833,
            longitude=82.5000,
            address="Jakhera, Dang District",
            area="Jakhera",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="6:00 AM - 6:00 PM",
            tuesday="6:00 AM - 6:00 PM",
            wednesday="6:00 AM - 6:00 PM",
            thursday="6:00 AM - 6:00 PM",
            friday="6:00 AM - 6:00 PM",
            saturday="6:00 AM - 6:00 PM",
            sunday="6:00 AM - 6:00 PM"
        ),
        price_info=PriceInfo(
            currency="NPR",
            nepali_citizen=0,
            saarc_citizen=0,
            foreign_tourist=0,
            notes="Boating charges may apply"
        ),
        highlights=[
            "Bird watching paradise",
            "Peaceful natural setting",
            "Boating opportunities",
            "Traditional Tharu fishing",
            "Nature walks",
            "Picnic spot"
        ],
        tips=[
            "Bring binoculars for bird watching",
            "Best visited early morning or evening",
            "Respect the natural environment",
            "Try local Tharu snacks nearby",
            "Wear comfortable walking shoes",
            "Check for migratory bird seasons"
        ],
        best_time_to_visit="Early morning or evening, October-March for birds",
        time_needed="2-3 hours",
        images=["jakhera_lake_main.jpg", "jakhera_birds.jpg", "jakhera_boating.jpg"],
        nearby_places=["dang_dharapani", "dang_tharu_museum"],
        related_places=["pokhara_phewa_lake"],
        tags=["lake", "nature", "bird watching", "peaceful", "boating", "tharu", "wildlife", "scenic"],
        languages_spoken=["Nepali", "Tharu", "English"],
        accessibility="Lakeside accessible, boating requires mobility",
        phone=None,
        website=None,
        email=None,
        google_rating=4.3,
        tripadvisor_rating=4.2,
        keywords=["jakhera lake", "dang", "bird watching", "nature", "lake", "tharu", "peaceful", "boating"]
    ),
    
    TourismPlace(
        id="dang_tharu_museum",
        name="Tharu Cultural Museum",
        name_nepali="थारू सांस्कृतिक संग्रहालय",
        category=PlaceCategory.MUSEUM,
        subcategories=["cultural", "museum", "tharu", "heritage"],
        description="""The Tharu Cultural Museum showcases the rich heritage, traditions, and lifestyle of the Tharu people, 
        one of Nepal's indigenous communities. The museum displays traditional Tharu artifacts, clothing, musical instruments, 
        agricultural tools, and household items. Visitors can learn about Tharu festivals, rituals, dance forms, and traditional 
        architecture. The museum also organizes cultural programs and demonstrations of Tharu traditions. It's an excellent place 
        to understand the unique Tharu way of life in the Terai region.""",
        short_description="Museum showcasing Tharu culture, traditions, artifacts, and way of life in Terai region.",
        location=Location(
            latitude=28.0667,
            longitude=82.4833,
            address="Dang District",
            area="Dang",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="9:00 AM - 5:00 PM",
            tuesday="9:00 AM - 5:00 PM",
            wednesday="9:00 AM - 5:00 PM",
            thursday="9:00 AM - 5:00 PM",
            friday="9:00 AM - 5:00 PM",
            saturday="9:00 AM - 5:00 PM",
            sunday="Closed"
        ),
        price_info=PriceInfo(
            currency="NPR",
            nepali_citizen=50,
            saarc_citizen=100,
            foreign_tourist=200
        ),
        highlights=[
            "Tharu artifacts and tools",
            "Traditional clothing display",
            "Cultural demonstrations",
            "Tharu dance performances",
            "Traditional architecture models",
            "Festival and ritual exhibits"
        ],
        tips=[
            "Hire a guide for better understanding",
            "Attend cultural programs if available",
            "Ask about Tharu homestay opportunities",
            "Respect the cultural artifacts",
            "Photography may have restrictions",
            "Combine with Tharu village visit"
        ],
        best_time_to_visit="Morning or afternoon",
        time_needed="1-2 hours",
        images=["tharu_museum_main.jpg", "tharu_artifacts.jpg", "tharu_dance.jpg"],
        nearby_places=["dang_dharapani", "dang_jakhera_lake"],
        related_places=["chitwan_national_park"],
        tags=["museum", "tharu", "cultural", "heritage", "indigenous", "traditions", "artifacts", "education"],
        languages_spoken=["Nepali", "Tharu", "English"],
        accessibility="Museum accessible",
        phone=None,
        website=None,
        email=None,
        google_rating=4.2,
        tripadvisor_rating=4.1,
        keywords=["tharu museum", "tharu culture", "dang", "cultural museum", "tharu heritage", "indigenous", "terai"]
    ),
    
    TourismPlace(
        id="dang_chamera_gupha",
        name="Chamera Gupha (Bat Cave)",
        name_nepali="चमेरा गुफा",
        category=PlaceCategory.NATURE,
        subcategories=["cave", "nature", "adventure", "wildlife"],
        description="""Chamera Gupha, also known as the Bat Cave, is a natural limestone cave located in Dang district. 
        The cave is home to thousands of bats and offers an adventurous exploration experience. The cave features interesting 
        rock formations, stalactites, and stalagmites. Visitors can explore the cave with proper lighting and guidance. 
        The surrounding area is rich in biodiversity and offers opportunities for nature walks. The cave is especially interesting 
        for adventure enthusiasts and nature lovers.""",
        short_description="Natural limestone cave home to thousands of bats, perfect for adventure and exploration.",
        location=Location(
            latitude=28.1000,
            longitude=82.4500,
            address="Chamera, Dang District",
            area="Chamera",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="8:00 AM - 5:00 PM",
            tuesday="8:00 AM - 5:00 PM",
            wednesday="8:00 AM - 5:00 PM",
            thursday="8:00 AM - 5:00 PM",
            friday="8:00 AM - 5:00 PM",
            saturday="8:00 AM - 5:00 PM",
            sunday="8:00 AM - 5:00 PM"
        ),
        price_info=PriceInfo(
            currency="NPR",
            nepali_citizen=50,
            saarc_citizen=100,
            foreign_tourist=200
        ),
        highlights=[
            "Thousands of bats",
            "Limestone formations",
            "Stalactites and stalagmites",
            "Adventure exploration",
            "Rich biodiversity",
            "Nature trails"
        ],
        tips=[
            "Bring flashlight or headlamp",
            "Wear sturdy shoes",
            "Hire a local guide",
            "Be careful of slippery surfaces",
            "Respect the bat habitat",
            "Best visited in dry season"
        ],
        best_time_to_visit="October to April (dry season)",
        time_needed="2-3 hours",
        images=["chamera_cave_main.jpg", "chamera_bats.jpg", "chamera_formations.jpg"],
        nearby_places=["dang_purandhara_waterfall"],
        related_places=["dang_jakhera_lake"],
        tags=["cave", "bats", "adventure", "nature", "exploration", "wildlife", "limestone", "hidden_gem"],
        languages_spoken=["Nepali", "Tharu", "English"],
        accessibility="Challenging - requires climbing and crawling",
        phone=None,
        website=None,
        email=None,
        google_rating=4.1,
        tripadvisor_rating=4.0,
        keywords=["chamera gupha", "bat cave", "dang", "cave", "adventure", "bats", "exploration", "hidden gem"]
    ),
    
    TourismPlace(
        id="dang_purandhara_waterfall",
        name="Purandhara Waterfall",
        name_nepali="पुरन्धरा झरना",
        category=PlaceCategory.NATURE,
        subcategories=["waterfall", "nature", "hiking", "scenic"],
        description="""Purandhara Waterfall is a beautiful natural waterfall located in the hills of Dang district. The waterfall 
        cascades down from a height, creating a picturesque setting surrounded by lush green forests. The area around the 
        waterfall is perfect for picnics, nature walks, and photography. The sound of falling water and the cool mist create a 
        refreshing atmosphere. Visitors can enjoy the natural beauty and take a refreshing dip in the pool at the base of the 
        waterfall during the dry season.""",
        short_description="Beautiful waterfall surrounded by lush forests, perfect for nature walks and picnics.",
        location=Location(
            latitude=28.1167,
            longitude=82.4333,
            address="Purandhara, Dang District",
            area="Purandhara",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="6:00 AM - 6:00 PM",
            tuesday="6:00 AM - 6:00 PM",
            wednesday="6:00 AM - 6:00 PM",
            thursday="6:00 AM - 6:00 PM",
            friday="6:00 AM - 6:00 PM",
            saturday="6:00 AM - 6:00 PM",
            sunday="6:00 AM - 6:00 PM"
        ),
        price_info=PriceInfo(
            currency="NPR",
            nepali_citizen=0,
            saarc_citizen=0,
            foreign_tourist=0
        ),
        highlights=[
            "Beautiful waterfall",
            "Lush forest surroundings",
            "Picnic spot",
            "Nature photography",
            "Refreshing pool",
            "Peaceful atmosphere"
        ],
        tips=[
            "Best visited after monsoon (Oct-Apr)",
            "Wear comfortable hiking shoes",
            "Bring water and snacks",
            "Be careful on slippery rocks",
            "Great for photography",
            "Combine with Chamera Cave visit"
        ],
        best_time_to_visit="October to April (post-monsoon)",
        time_needed="2-3 hours",
        images=["purandhara_waterfall_main.jpg", "purandhara_nature.jpg", "purandhara_pool.jpg"],
        nearby_places=["dang_chamera_gupha"],
        related_places=["dang_jakhera_lake"],
        tags=["waterfall", "nature", "hiking", "scenic", "picnic", "photography", "peaceful", "hidden_gem"],
        languages_spoken=["Nepali", "Tharu", "English"],
        accessibility="Requires hiking - challenging for wheelchairs",
        phone=None,
        website=None,
        email=None,
        google_rating=4.2,
        tripadvisor_rating=4.1,
        keywords=["purandhara waterfall", "dang", "waterfall", "nature", "hiking", "scenic", "hidden gem"]
    ),
    
    TourismPlace(
        id="dang_bageshwori_temple",
        name="Bageshwori Temple",
        name_nepali="बागेश्वरी मन्दिर",
        category=PlaceCategory.TEMPLE,
        subcategories=["hindu_temple", "religious", "tharu_culture"],
        description="""Bageshwori Temple is an important Hindu temple dedicated to Goddess Bageshwori (a form of Goddess Durga) 
        located in Dang district. The temple holds significant religious importance for the local Tharu and Hindu communities. 
        The temple architecture reflects traditional Terai style and is surrounded by a peaceful compound. The temple is 
        especially vibrant during festivals like Dashain and Navratri when devotees gather for prayers and celebrations. 
        The area around the temple offers insights into local religious practices and Tharu cultural traditions.""",
        short_description="Important Hindu temple dedicated to Goddess Bageshwori, significant for Tharu community.",
        location=Location(
            latitude=28.0500,
            longitude=82.4667,
            address="Dang District",
            area="Dang",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="5:00 AM - 8:00 PM",
            tuesday="5:00 AM - 8:00 PM",
            wednesday="5:00 AM - 8:00 PM",
            thursday="5:00 AM - 8:00 PM",
            friday="5:00 AM - 8:00 PM",
            saturday="5:00 AM - 8:00 PM",
            sunday="5:00 AM - 8:00 PM"
        ),
        price_info=PriceInfo(
            currency="NPR",
            nepali_citizen=0,
            saarc_citizen=0,
            foreign_tourist=0
        ),
        highlights=[
            "Goddess Bageshwori temple",
            "Traditional Terai architecture",
            "Festival celebrations",
            "Tharu cultural significance",
            "Peaceful temple compound",
            "Religious pilgrimage site"
        ],
        tips=[
            "Visit during Dashain or Navratri for festivals",
            "Respect the religious site",
            "Dress modestly",
            "Photography may have restrictions",
            "Try prasad (temple offering) if available",
            "Combine with Dharapani visit"
        ],
        best_time_to_visit="Morning or evening, especially during festivals",
        time_needed="30 minutes - 1 hour",
        images=["bageshwori_temple_main.jpg", "bageshwori_festival.jpg"],
        nearby_places=["dang_dharapani", "dang_tharu_museum"],
        related_places=["ktm_pashupatinath"],
        tags=["temple", "hindu", "bageshwori", "tharu", "religious", "goddess", "festival", "cultural"],
        languages_spoken=["Nepali", "Tharu", "Hindi", "English"],
        accessibility="Temple accessible",
        phone=None,
        website=None,
        email=None,
        google_rating=4.3,
        tripadvisor_rating=4.2,
        keywords=["bageshwori temple", "dang", "temple", "goddess", "tharu", "hindu", "religious"]
    ),
    
    TourismPlace(
        id="dang_tharu_homestay",
        name="Tharu Homestay Experience",
        name_nepali="थारू होमस्टे",
        category=PlaceCategory.CULTURAL,
        subcategories=["homestay", "cultural", "tharu", "authentic"],
        description="""Tharu homestays in Dang offer an authentic cultural immersion experience. Visitors can stay with local 
        Tharu families, participate in daily activities like farming, cooking traditional meals, and learning Tharu customs. 
        The homestays provide traditional Tharu-style accommodation with mud houses, thatched roofs, and open courtyards. 
        Guests can enjoy traditional Tharu cuisine, watch cultural dance performances, and learn about Tharu way of life. 
        This is an excellent way to support local communities while experiencing authentic Terai culture.""",
        short_description="Authentic homestay experience with Tharu families, offering cultural immersion and traditional lifestyle.",
        location=Location(
            latitude=28.0667,
            longitude=82.4833,
            address="Various Tharu Villages, Dang District",
            area="Dang",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="24 hours",
            tuesday="24 hours",
            wednesday="24 hours",
            thursday="24 hours",
            friday="24 hours",
            saturday="24 hours",
            sunday="24 hours"
        ),
        price_info=PriceInfo(
            currency="NPR",
            price_range="$$",
            notes="Typically 1000-2000 NPR per night including meals"
        ),
        highlights=[
            "Authentic Tharu culture",
            "Traditional mud houses",
            "Tharu cuisine experience",
            "Cultural dance performances",
            "Farming activities",
            "Community interaction"
        ],
        tips=[
            "Book in advance",
            "Respect local customs",
            "Participate in daily activities",
            "Try traditional Tharu food",
            "Learn basic Tharu greetings",
            "Bring gifts for host family"
        ],
        best_time_to_visit="Year-round, October-March for pleasant weather",
        time_needed="1-3 days recommended",
        images=["tharu_homestay_main.jpg", "tharu_homestay_food.jpg", "tharu_homestay_dance.jpg"],
        nearby_places=["dang_tharu_museum", "dang_dharapani"],
        related_places=["chitwan_national_park"],
        tags=["homestay", "tharu", "cultural", "authentic", "community", "traditional", "immersion", "hidden_gem"],
        languages_spoken=["Nepali", "Tharu", "English"],
        accessibility="Varies by homestay",
        phone=None,
        website=None,
        email=None,
        google_rating=4.5,
        tripadvisor_rating=4.4,
        keywords=["tharu homestay", "dang", "homestay", "tharu culture", "authentic", "cultural immersion", "terai"]
    ),
    
    # ============================================================================
    # ADDITIONAL DANG DISTRICT PLACES
    # ============================================================================
    
    TourismPlace(
        id="dang_barhakune_daha",
        name="Barhakune Daha",
        name_nepali="बारहकुने दह",
        category=PlaceCategory.NATURE,
        subcategories=["lake", "religious", "nature", "tharu"],
        description="""Barhakune Daha is a famous 'twelve-cornered' lake dedicated to Lord Vishnu, located in Dang District. 
        This unique geometric lake is considered sacred and is an important religious site for Hindus. The lake's distinctive 
        twelve-cornered shape makes it architecturally and spiritually significant. Surrounded by natural beauty, it's a peaceful 
        spot for meditation and religious ceremonies. The area is especially vibrant during festivals when devotees gather to 
        perform rituals and prayers.""",
        short_description="Sacred twelve-cornered lake dedicated to Lord Vishnu, important religious site in Dang.",
        location=Location(
            latitude=28.0667,
            longitude=82.4833,
            address="Dang District",
            area="Dang",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="6:00 AM - 6:00 PM",
            tuesday="6:00 AM - 6:00 PM",
            wednesday="6:00 AM - 6:00 PM",
            thursday="6:00 AM - 6:00 PM",
            friday="6:00 AM - 6:00 PM",
            saturday="6:00 AM - 6:00 PM",
            sunday="6:00 AM - 6:00 PM"
        ),
        price_info=PriceInfo(currency="NPR", nepali_citizen=0, saarc_citizen=0, foreign_tourist=0),
        highlights=["Twelve-cornered geometric design", "Sacred to Lord Vishnu", "Religious ceremonies", "Natural beauty"],
        tips=["Visit during festivals for cultural experience", "Respect religious customs", "Photography allowed"],
        best_time_to_visit="Year-round, especially during festivals",
        time_needed="1 hour",
        images=[],
        nearby_places=[],
        related_places=["dang_dharapani"],
        tags=["lake", "vishnu", "religious", "sacred", "tharu", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Accessible",
        phone=None,
        website=None,
        email=None,
        google_rating=4.2,
        tripadvisor_rating=4.0,
        keywords=["barhakune daha", "twelve cornered lake", "vishnu", "dang", "lake", "religious"]
    ),
    
    TourismPlace(
        id="dang_chamera_gupha",
        name="Chamera Gupha (Bat Cave)",
        name_nepali="चमेरा गुफा",
        category=PlaceCategory.ADVENTURE,
        subcategories=["cave", "adventure", "prehistoric", "nature"],
        description="""Chamera Gupha, also known as the Bat Cave, is a prehistoric cave system in Dang District, ideal for 
        adventure seekers and nature enthusiasts. This ancient cave system features impressive stalactites and stalagmites, 
        and is home to various bat species. The cave offers a unique underground exploration experience with its winding passages 
        and natural formations. It's an excellent destination for those interested in geology, archaeology, and adventure activities. 
        The cave requires some physical fitness to explore fully.""",
        short_description="Prehistoric cave system with bat colonies, perfect for adventure and exploration.",
        location=Location(
            latitude=28.0833,
            longitude=82.5000,
            address="Dang District",
            area="Dang",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="8:00 AM - 5:00 PM",
            tuesday="8:00 AM - 5:00 PM",
            wednesday="8:00 AM - 5:00 PM",
            thursday="8:00 AM - 5:00 PM",
            friday="8:00 AM - 5:00 PM",
            saturday="8:00 AM - 5:00 PM",
            sunday="8:00 AM - 5:00 PM"
        ),
        price_info=PriceInfo(currency="NPR", nepali_citizen=50, saarc_citizen=100, foreign_tourist=200),
        highlights=["Prehistoric cave system", "Bat colonies", "Stalactites and stalagmites", "Adventure exploration"],
        tips=["Bring flashlight", "Wear appropriate footwear", "Physical fitness required", "Guide recommended"],
        best_time_to_visit="Dry season (October to May)",
        time_needed="2-3 hours",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["cave", "bat", "adventure", "prehistoric", "exploration", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Requires physical fitness, uneven terrain",
        phone=None,
        website=None,
        email=None,
        google_rating=4.3,
        tripadvisor_rating=4.1,
        keywords=["chamera gupha", "bat cave", "cave", "adventure", "dang", "prehistoric"]
    ),
    
    TourismPlace(
        id="dang_purandhara_waterfall",
        name="Purandhara Waterfall",
        name_nepali="पुरन्धरा झरना",
        category=PlaceCategory.NATURE,
        subcategories=["waterfall", "nature", "jungle", "scenic"],
        description="""Purandhara Waterfall is a beautiful natural waterfall located in the dense jungle of Babai in Dang District. 
        This scenic waterfall cascades through lush green forests, creating a serene and picturesque setting. The area surrounding 
        the waterfall is rich in biodiversity, making it perfect for nature lovers and photographers. The journey to the waterfall 
        involves a trek through beautiful jungle paths, adding to the adventure. It's an ideal spot for picnics, nature walks, 
        and enjoying the peaceful sounds of flowing water.""",
        short_description="Beautiful natural waterfall in dense jungle, perfect for nature lovers and photography.",
        location=Location(
            latitude=28.1000,
            longitude=82.5167,
            address="Babai, Dang District",
            area="Babai",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="6:00 AM - 6:00 PM",
            tuesday="6:00 AM - 6:00 PM",
            wednesday="6:00 AM - 6:00 PM",
            thursday="6:00 AM - 6:00 PM",
            friday="6:00 AM - 6:00 PM",
            saturday="6:00 AM - 6:00 PM",
            sunday="6:00 AM - 6:00 PM"
        ),
        price_info=PriceInfo(currency="NPR", nepali_citizen=0, saarc_citizen=0, foreign_tourist=0),
        highlights=["Natural waterfall", "Dense jungle setting", "Rich biodiversity", "Scenic beauty"],
        tips=["Wear comfortable trekking shoes", "Bring water and snacks", "Best during monsoon season", "Photography recommended"],
        best_time_to_visit="Monsoon season (June-September) for full flow",
        time_needed="2-3 hours including trek",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["waterfall", "nature", "jungle", "scenic", "trekking", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Requires trekking, moderate difficulty",
        phone=None,
        website=None,
        email=None,
        google_rating=4.4,
        tripadvisor_rating=4.2,
        keywords=["purandhara waterfall", "waterfall", "babai", "jungle", "nature", "dang"]
    ),
    
    TourismPlace(
        id="dang_ambikeshwori_temple",
        name="Ambikeshwori Temple",
        name_nepali="अम्बिकेश्वरी मन्दिर",
        category=PlaceCategory.TEMPLE,
        subcategories=["temple", "shakti_peeth", "religious", "hindu"],
        description="""Ambikeshwori Temple is one of the most significant Shakti Peeths in the Dang region, dedicated to Goddess 
        Ambika (a form of Durga). This important Hindu temple attracts devotees from across Nepal and India, especially during 
        Navratri and other major festivals. The temple complex features traditional architecture and is surrounded by peaceful 
        natural settings. It's a powerful spiritual destination where devotees come to seek blessings and perform religious rituals. 
        The temple holds great religious significance in the Shakti tradition of Hinduism.""",
        short_description="Significant Shakti Peeth temple dedicated to Goddess Ambika, important pilgrimage site.",
        location=Location(
            latitude=28.0667,
            longitude=82.4833,
            address="Dang District",
            area="Dang",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="5:00 AM - 8:00 PM",
            tuesday="5:00 AM - 8:00 PM",
            wednesday="5:00 AM - 8:00 PM",
            thursday="5:00 AM - 8:00 PM",
            friday="5:00 AM - 8:00 PM",
            saturday="5:00 AM - 8:00 PM",
            sunday="5:00 AM - 8:00 PM"
        ),
        price_info=PriceInfo(currency="NPR", nepali_citizen=0, saarc_citizen=0, foreign_tourist=0),
        highlights=["Shakti Peeth significance", "Goddess Ambika temple", "Major pilgrimage site", "Traditional architecture"],
        tips=["Visit during Navratri for special ceremonies", "Respect temple customs", "Remove shoes before entering"],
        best_time_to_visit="During Navratri and major festivals",
        time_needed="1-2 hours",
        images=[],
        nearby_places=[],
        related_places=["dang_bageshwori_temple"],
        tags=["temple", "shakti peeth", "ambika", "durga", "religious", "pilgrimage", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi", "Sanskrit"],
        accessibility="Temple accessible",
        phone=None,
        website=None,
        email=None,
        google_rating=4.5,
        tripadvisor_rating=4.3,
        keywords=["ambikeshwori temple", "shakti peeth", "ambika", "temple", "dang", "pilgrimage"]
    ),
    
    TourismPlace(
        id="dang_goraksha_ratna_nath",
        name="Goraksha Ratna Nath Temple",
        name_nepali="गोरक्ष रत्न नाथ मन्दिर",
        category=PlaceCategory.TEMPLE,
        subcategories=["temple", "historic", "religious", "nath"],
        description="""Goraksha Ratna Nath Temple is a historic temple located in Chaughera, Dang District, with deep religious 
        significance. This ancient temple is associated with the Nath tradition of Hinduism and is dedicated to Lord Shiva in his 
        form as Gorakhnath. The temple features traditional architecture and is surrounded by a peaceful environment. It attracts 
        devotees and spiritual seekers interested in the Nath yogic tradition. The temple area offers a serene atmosphere for 
        meditation and religious contemplation.""",
        short_description="Historic temple in Chaughera with deep religious significance in the Nath tradition.",
        location=Location(
            latitude=28.0500,
            longitude=82.4500,
            address="Chaughera, Dang District",
            area="Chaughera",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="6:00 AM - 7:00 PM",
            tuesday="6:00 AM - 7:00 PM",
            wednesday="6:00 AM - 7:00 PM",
            thursday="6:00 AM - 7:00 PM",
            friday="6:00 AM - 7:00 PM",
            saturday="6:00 AM - 7:00 PM",
            sunday="6:00 AM - 7:00 PM"
        ),
        price_info=PriceInfo(currency="NPR", nepali_citizen=0, saarc_citizen=0, foreign_tourist=0),
        highlights=["Historic significance", "Nath tradition", "Gorakhnath temple", "Peaceful atmosphere"],
        tips=["Respect religious customs", "Quiet meditation possible", "Combine with nearby temples"],
        best_time_to_visit="Year-round, especially during festivals",
        time_needed="1 hour",
        images=[],
        nearby_places=[],
        related_places=["dang_ambikeshwori_temple"],
        tags=["temple", "gorakhnath", "nath", "historic", "religious", "chaughera", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Temple accessible",
        phone=None,
        website=None,
        email=None,
        google_rating=4.3,
        tripadvisor_rating=4.1,
        keywords=["goraksha ratna nath", "gorakhnath", "nath temple", "chaughera", "dang", "temple"]
    ),
    
    TourismPlace(
        id="dang_chhillikot",
        name="Chhillikot",
        name_nepali="छिल्लिकोट",
        category=PlaceCategory.VIEWPOINT,
        subcategories=["viewpoint", "hilltop", "ruins", "scenic"],
        description="""Chhillikot is a hilltop viewpoint offering panoramic views of the Dang valley and ancient ruins. This scenic 
        location provides breathtaking vistas of the surrounding Terai plains and distant hills. The area features historic ruins 
        that add to its archaeological significance. It's an excellent spot for photography, especially during sunrise and sunset. 
        The trek to Chhillikot offers beautiful natural scenery and is popular among nature enthusiasts and history buffs.""",
        short_description="Hilltop viewpoint with panoramic valley views and ancient ruins.",
        location=Location(
            latitude=28.1000,
            longitude=82.5000,
            address="Dang District",
            area="Dang",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="6:00 AM - 6:00 PM",
            tuesday="6:00 AM - 6:00 PM",
            wednesday="6:00 AM - 6:00 PM",
            thursday="6:00 AM - 6:00 PM",
            friday="6:00 AM - 6:00 PM",
            saturday="6:00 AM - 6:00 PM",
            sunday="6:00 AM - 6:00 PM"
        ),
        price_info=PriceInfo(currency="NPR", nepali_citizen=0, saarc_citizen=0, foreign_tourist=0),
        highlights=["Panoramic valley views", "Ancient ruins", "Sunrise/sunset views", "Photography spot"],
        tips=["Best visited at sunrise or sunset", "Bring camera", "Wear comfortable shoes for trek"],
        best_time_to_visit="Early morning or evening for best views",
        time_needed="2-3 hours including trek",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["viewpoint", "hilltop", "ruins", "scenic", "panoramic", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Requires trekking, moderate difficulty",
        phone=None,
        website=None,
        email=None,
        google_rating=4.4,
        tripadvisor_rating=4.2,
        keywords=["chhillikot", "viewpoint", "hilltop", "ruins", "dang valley", "panoramic"]
    ),
    
    TourismPlace(
        id="dang_sawarikot",
        name="Sawarikot",
        name_nepali="सावरिकोट",
        category=PlaceCategory.HERITAGE_SITE,
        subcategories=["fort", "historic", "trekking", "ruins"],
        description="""Sawarikot is an ancient fort area offering trekking opportunities and historical exploration. This historic 
        site features ruins of an old fortification that provides insights into the region's past. The area is perfect for trekking 
        enthusiasts and history lovers who want to explore ancient architecture and enjoy scenic natural surroundings. The trek to 
        Sawarikot offers beautiful views and a sense of adventure, making it a popular destination for those interested in both 
        history and outdoor activities.""",
        short_description="Ancient fort ruins perfect for trekking and historical exploration.",
        location=Location(
            latitude=28.0833,
            longitude=82.4833,
            address="Dang District",
            area="Dang",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="6:00 AM - 6:00 PM",
            tuesday="6:00 AM - 6:00 PM",
            wednesday="6:00 AM - 6:00 PM",
            thursday="6:00 AM - 6:00 PM",
            friday="6:00 AM - 6:00 PM",
            saturday="6:00 AM - 6:00 PM",
            sunday="6:00 AM - 6:00 PM"
        ),
        price_info=PriceInfo(currency="NPR", nepali_citizen=0, saarc_citizen=0, foreign_tourist=0),
        highlights=["Ancient fort ruins", "Trekking opportunities", "Historical significance", "Scenic views"],
        tips=["Bring water and snacks", "Wear trekking shoes", "Guide recommended for history"],
        best_time_to_visit="Dry season (October to May)",
        time_needed="3-4 hours",
        images=[],
        nearby_places=[],
        related_places=["dang_chhillikot"],
        tags=["fort", "ruins", "historic", "trekking", "ancient", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Requires trekking, moderate to difficult",
        phone=None,
        website=None,
        email=None,
        google_rating=4.2,
        tripadvisor_rating=4.0,
        keywords=["sawarikot", "fort", "ruins", "trekking", "historic", "dang"]
    ),
    
    TourismPlace(
        id="dang_rapti_peace_park",
        name="Rapti Peace Park",
        name_nepali="राप्ती शान्ति पार्क",
        category=PlaceCategory.NATURE,
        subcategories=["park", "recreational", "river", "nature"],
        description="""Rapti Peace Park is a popular local recreational park located near the Rapti river in Dang District. This 
        peaceful park offers a relaxing environment for families, picnics, and outdoor activities. The park features beautiful 
        natural settings with river views, making it an ideal spot for relaxation and recreation. It's a favorite destination for 
        locals and visitors looking to enjoy nature, take leisurely walks, or simply unwind by the river. The park provides a 
        serene escape from daily life.""",
        short_description="Popular recreational park near Rapti river, perfect for picnics and relaxation.",
        location=Location(
            latitude=28.0667,
            longitude=82.4667,
            address="Near Rapti River, Dang District",
            area="Dang",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="6:00 AM - 7:00 PM",
            tuesday="6:00 AM - 7:00 PM",
            wednesday="6:00 AM - 7:00 PM",
            thursday="6:00 AM - 7:00 PM",
            friday="6:00 AM - 7:00 PM",
            saturday="6:00 AM - 7:00 PM",
            sunday="6:00 AM - 7:00 PM"
        ),
        price_info=PriceInfo(currency="NPR", nepali_citizen=0, saarc_citizen=0, foreign_tourist=0),
        highlights=["Riverside location", "Recreational activities", "Picnic spots", "Natural beauty"],
        tips=["Great for family outings", "Bring picnic supplies", "Evening walks recommended"],
        best_time_to_visit="Year-round, especially evenings",
        time_needed="1-2 hours",
        images=[],
        nearby_places=[],
        related_places=["dang_jakhera_lake"],
        tags=["park", "recreational", "rapti river", "picnic", "nature", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Park accessible",
        phone=None,
        website=None,
        email=None,
        google_rating=4.3,
        tripadvisor_rating=4.1,
        keywords=["rapti peace park", "park", "rapti river", "recreational", "picnic", "dang"]
    ),
    
    TourismPlace(
        id="dang_koilabas",
        name="Koilabas",
        name_nepali="कोइलाबास",
        category=PlaceCategory.HERITAGE_SITE,
        subcategories=["historic", "border_town", "architecture", "cultural"],
        description="""Koilabas is a historic trade town with unique architecture located on the Indian border in Dang District. 
        This border town has a rich history as a trading hub and features distinctive architectural styles that reflect its 
        commercial past. The town offers a glimpse into traditional border trade culture and features interesting buildings and 
        structures. It's an interesting destination for those interested in history, architecture, and border culture. The town 
        maintains its traditional character while serving as an important border crossing point.""",
        short_description="Historic border trade town with unique architecture and commercial heritage.",
        location=Location(
            latitude=28.0167,
            longitude=82.3833,
            address="Koilabas, Dang District (India Border)",
            area="Koilabas",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="24 hours",
            tuesday="24 hours",
            wednesday="24 hours",
            thursday="24 hours",
            friday="24 hours",
            saturday="24 hours",
            sunday="24 hours"
        ),
        price_info=PriceInfo(currency="NPR", price_range="$", notes="Border crossing fees may apply"),
        highlights=["Historic trade town", "Unique architecture", "Border culture", "Commercial heritage"],
        tips=["Border crossing documentation required", "Explore traditional architecture", "Try local border cuisine"],
        best_time_to_visit="Year-round",
        time_needed="2-3 hours",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["border town", "historic", "trade", "architecture", "cultural", "koilabas", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi", "English"],
        accessibility="Town accessible",
        phone=None,
        website=None,
        email=None,
        google_rating=4.1,
        tripadvisor_rating=3.9,
        keywords=["koilabas", "border town", "trade", "historic", "architecture", "dang"]
    ),
    
    TourismPlace(
        id="dang_banglachuli",
        name="Banglachuli",
        name_nepali="बाङ्लाचुली",
        category=PlaceCategory.VIEWPOINT,
        subcategories=["hill_station", "viewpoint", "scenic", "cool_weather"],
        description="""Banglachuli is a scenic hill station area offering cool weather and beautiful views in Dang District. This 
        elevated location provides relief from the heat of the Terai plains and offers pleasant weather throughout the year. The 
        area features beautiful natural scenery, making it perfect for relaxation and enjoying nature. It's an ideal destination 
        for those seeking cooler temperatures and scenic vistas. The hill station atmosphere makes it a popular retreat for 
        locals and visitors.""",
        short_description="Scenic hill station with cool weather and beautiful views, perfect retreat.",
        location=Location(
            latitude=28.1167,
            longitude=82.5167,
            address="Banglachuli, Dang District",
            area="Banglachuli",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="24 hours",
            tuesday="24 hours",
            wednesday="24 hours",
            thursday="24 hours",
            friday="24 hours",
            saturday="24 hours",
            sunday="24 hours"
        ),
        price_info=PriceInfo(currency="NPR", nepali_citizen=0, saarc_citizen=0, foreign_tourist=0),
        highlights=["Cool weather", "Scenic views", "Hill station atmosphere", "Natural beauty"],
        tips=["Great for escaping heat", "Bring warm clothes for evening", "Photography recommended"],
        best_time_to_visit="Year-round, especially summer for cool weather",
        time_needed="Half day to full day",
        images=[],
        nearby_places=[],
        related_places=["dang_chhillikot"],
        tags=["hill station", "viewpoint", "cool weather", "scenic", "retreat", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Accessible by road",
        phone=None,
        website=None,
        email=None,
        google_rating=4.3,
        tripadvisor_rating=4.1,
        keywords=["banglachuli", "hill station", "cool weather", "scenic", "viewpoint", "dang"]
    ),
    
    TourismPlace(
        id="dang_sonpathari",
        name="Sonpathari",
        name_nepali="सोनपथरी",
        category=PlaceCategory.NATURE,
        subcategories=["religious", "scenic", "nature", "spiritual"],
        description="""Sonpathari is a religious and scenic spot known for its natural beauty in Dang District. This peaceful 
        location combines spiritual significance with stunning natural surroundings, making it a popular destination for both 
        religious pilgrims and nature lovers. The area features beautiful landscapes and offers a serene atmosphere for 
        meditation and contemplation. It's an ideal spot for those seeking both spiritual and natural experiences.""",
        short_description="Religious and scenic spot with natural beauty, perfect for spiritual and nature experiences.",
        location=Location(
            latitude=28.0833,
            longitude=82.4833,
            address="Sonpathari, Dang District",
            area="Sonpathari",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="6:00 AM - 6:00 PM",
            tuesday="6:00 AM - 6:00 PM",
            wednesday="6:00 AM - 6:00 PM",
            thursday="6:00 AM - 6:00 PM",
            friday="6:00 AM - 6:00 PM",
            saturday="6:00 AM - 6:00 PM",
            sunday="6:00 AM - 6:00 PM"
        ),
        price_info=PriceInfo(currency="NPR", nepali_citizen=0, saarc_citizen=0, foreign_tourist=0),
        highlights=["Religious significance", "Natural beauty", "Serene atmosphere", "Spiritual experience"],
        tips=["Respect religious customs", "Great for meditation", "Photography allowed"],
        best_time_to_visit="Year-round",
        time_needed="1-2 hours",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["religious", "scenic", "nature", "spiritual", "meditation", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Accessible",
        phone=None,
        website=None,
        email=None,
        google_rating=4.2,
        tripadvisor_rating=4.0,
        keywords=["sonpathari", "religious", "scenic", "nature", "spiritual", "dang"]
    ),
    
    TourismPlace(
        id="dang_deukhuri_valley",
        name="Deukhuri Valley",
        name_nepali="देउखुरी उपत्यका",
        category=PlaceCategory.NATURE,
        subcategories=["valley", "river", "traditional", "scenic"],
        description="""Deukhuri Valley offers opportunities to explore the Rapti river banks and traditional suspension bridges 
        in Dang District. This scenic valley is characterized by beautiful river landscapes and traditional architecture, 
        including iconic suspension bridges that are engineering marvels. The area provides excellent opportunities for nature 
        walks, river activities, and experiencing traditional Terai culture. It's a perfect destination for those interested in 
        both natural beauty and cultural heritage.""",
        short_description="Scenic valley with Rapti river banks and traditional suspension bridges.",
        location=Location(
            latitude=28.0667,
            longitude=82.4500,
            address="Deukhuri Valley, Dang District",
            area="Deukhuri",
            ward=None
        ),
        opening_hours=OpeningHours(
            monday="24 hours",
            tuesday="24 hours",
            wednesday="24 hours",
            thursday="24 hours",
            friday="24 hours",
            saturday="24 hours",
            sunday="24 hours"
        ),
        price_info=PriceInfo(currency="NPR", nepali_citizen=0, saarc_citizen=0, foreign_tourist=0),
        highlights=["Rapti river banks", "Traditional suspension bridges", "Scenic valley", "Cultural heritage"],
        tips=["Explore suspension bridges", "River walks recommended", "Photography opportunities"],
        best_time_to_visit="Year-round, especially dry season",
        time_needed="Half day",
        images=[],
        nearby_places=["dang_rapti_peace_park"],
        related_places=[],
        tags=["valley", "rapti river", "suspension bridge", "traditional", "scenic", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Valley accessible, bridges require caution",
        phone=None,
        website=None,
        email=None,
        google_rating=4.3,
        tripadvisor_rating=4.1,
        keywords=["deukhuri valley", "rapti river", "suspension bridge", "valley", "traditional", "dang"]
    ),
    
    # ============================================================================
    # DANG DISTRICT FOODS
    # ============================================================================
    
    TourismPlace(
        id="dang_food_dhikri",
        name="Dhikri",
        name_nepali="ढिक्री",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "traditional", "rice_cake", "essential"],
        description="""Dhikri is an essential Tharu dish - steamed rice flour cakes that are a staple of Tharu cuisine in Dang District. 
        These soft, fluffy cakes are made from rice flour and are typically served with various accompaniments like spicy chutneys, 
        lentil curry, or vegetables. Dhikri is a traditional dish that represents the rich culinary heritage of the Tharu community. 
        It's commonly prepared during festivals and special occasions but is also enjoyed as a daily meal. The dish is simple yet 
        flavorful and is a must-try for anyone visiting Dang to experience authentic Tharu cuisine.""",
        short_description="Essential Tharu dish - steamed rice flour cakes, a staple of Tharu cuisine.",
        location=Location(latitude=28.0667, longitude=82.4833, address="Dang District", area="Dang", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$", notes="Available at local restaurants and homestays"),
        highlights=["Traditional Tharu dish", "Steamed rice flour cakes", "Essential Tharu cuisine", "Festival food"],
        tips=["Try with spicy chutney", "Best at local Tharu restaurants", "Ask for traditional preparation"],
        best_time_to_visit="Year-round, especially during festivals",
        time_needed="Meal time",
        images=[],
        nearby_places=[],
        related_places=["dang_tharu_homestay"],
        tags=["dhikri", "tharu food", "rice cake", "traditional", "dang", "cuisine"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at restaurants",
        phone=None,
        website=None,
        email=None,
        google_rating=4.5,
        tripadvisor_rating=4.3,
        keywords=["dhikri", "tharu food", "rice cake", "traditional", "dang", "cuisine", "steamed"]
    ),
    
    TourismPlace(
        id="dang_food_ghonghi",
        name="Ghonghi",
        name_nepali="घोङी",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "seafood", "traditional", "spicy"],
        description="""Ghonghi is a traditional Tharu delicacy - water snails cooked in flaxseed and local spices. This unique dish 
        is a specialty of Dang District and represents the resourceful culinary traditions of the Tharu people. The snails are 
        carefully prepared and cooked with aromatic spices, creating a flavorful and distinctive dish. Ghonghi is typically served 
        as a curry or dry preparation and is enjoyed with rice or traditional bread. It's a must-try for adventurous food lovers 
        seeking authentic Tharu flavors.""",
        short_description="Traditional Tharu delicacy - water snails cooked in flaxseed and local spices.",
        location=Location(latitude=28.0667, longitude=82.4833, address="Dang District", area="Dang", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$$", notes="Specialty dish, available at select restaurants"),
        highlights=["Water snails", "Traditional Tharu delicacy", "Flaxseed preparation", "Unique flavor"],
        tips=["Try at authentic Tharu restaurants", "Best with rice", "Adventurous food lovers"],
        best_time_to_visit="Year-round",
        time_needed="Meal time",
        images=[],
        nearby_places=[],
        related_places=["dang_tharu_homestay"],
        tags=["ghonghi", "water snails", "tharu food", "traditional", "dang", "delicacy"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at select restaurants",
        phone=None,
        website=None,
        email=None,
        google_rating=4.4,
        tripadvisor_rating=4.2,
        keywords=["ghonghi", "water snails", "tharu food", "traditional", "dang", "flaxseed", "spices"]
    ),
    
    TourismPlace(
        id="dang_food_anadi_rice",
        name="Anadi Rice (Chichar)",
        name_nepali="अनाडी चामल (चिचर)",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "rice", "sticky_rice", "festival"],
        description="""Anadi Rice, also known as Chichar, is sticky steamed rice that is a staple for festivals in Dang District. 
        This special variety of rice has a unique sticky texture and is traditionally prepared during important Tharu festivals and 
        celebrations. The rice is steamed to perfection and is often served with various curries, pickles, or traditional 
        accompaniments. Anadi Rice holds cultural significance in Tharu traditions and is an essential part of festive meals. 
        It's a must-try to experience authentic Tharu festival cuisine.""",
        short_description="Sticky steamed rice, a staple for Tharu festivals and celebrations.",
        location=Location(latitude=28.0667, longitude=82.4833, address="Dang District", area="Dang", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$", notes="Especially available during festivals"),
        highlights=["Sticky rice variety", "Festival staple", "Traditional preparation", "Cultural significance"],
        tips=["Best during festivals", "Try with traditional curries", "Experience Tharu culture"],
        best_time_to_visit="During Tharu festivals",
        time_needed="Meal time",
        images=[],
        nearby_places=[],
        related_places=["dang_tharu_homestay"],
        tags=["anadi rice", "chichar", "sticky rice", "tharu food", "festival", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at restaurants and homestays",
        phone=None,
        website=None,
        email=None,
        google_rating=4.4,
        tripadvisor_rating=4.2,
        keywords=["anadi rice", "chichar", "sticky rice", "tharu food", "festival", "dang"]
    ),
    
    TourismPlace(
        id="dang_food_khariya",
        name="Khariya (Patushni)",
        name_nepali="खरिया (पतुश्नी)",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "vegetable", "traditional", "fried"],
        description="""Khariya, also known as Patushni, is a traditional Tharu dish made from taro/colocasia leaves stuffed with 
        lentils and spices, then fried. This flavorful preparation showcases the Tharu community's expertise in using local 
        ingredients. The dish combines the earthy flavor of colocasia leaves with spiced lentils, creating a unique and delicious 
        combination. Khariya is typically served as a side dish or snack and is enjoyed for its rich flavors and nutritional value. 
        It's a must-try for those interested in traditional Tharu vegetable preparations.""",
        short_description="Taro/colocasia leaves stuffed with lentils and spices, then fried - traditional Tharu dish.",
        location=Location(latitude=28.0667, longitude=82.4833, address="Dang District", area="Dang", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$", notes="Available at local restaurants"),
        highlights=["Colocasia leaves", "Stuffed with lentils", "Traditional preparation", "Fried dish"],
        tips=["Try at Tharu restaurants", "Great as side dish", "Nutritious and flavorful"],
        best_time_to_visit="Year-round",
        time_needed="Meal time",
        images=[],
        nearby_places=[],
        related_places=["dang_tharu_homestay"],
        tags=["khariya", "patushni", "colocasia", "tharu food", "traditional", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at restaurants",
        phone=None,
        website=None,
        email=None,
        google_rating=4.3,
        tripadvisor_rating=4.1,
        keywords=["khariya", "patushni", "colocasia", "taro leaves", "tharu food", "dang"]
    ),
    
    TourismPlace(
        id="dang_food_bagiya",
        name="Bagiya",
        name_nepali="बगिया",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "dumpling", "rice_flour", "traditional"],
        description="""Bagiya are rice flour dumplings stuffed with lentils or potatoes, a traditional Tharu dish from Dang District. 
        These delicious dumplings are similar to momos but have a distinct Tharu preparation style. The outer layer is made from 
        rice flour, giving them a unique texture, while the filling can be lentils, potatoes, or a combination of both. Bagiya 
        are typically steamed and served with spicy chutneys or curries. They're a popular snack and meal option in Tharu 
        households and restaurants.""",
        short_description="Rice flour dumplings stuffed with lentils or potatoes - traditional Tharu dish.",
        location=Location(latitude=28.0667, longitude=82.4833, address="Dang District", area="Dang", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$", notes="Available at local restaurants"),
        highlights=["Rice flour dumplings", "Lentil or potato filling", "Traditional Tharu style", "Steamed preparation"],
        tips=["Try with spicy chutney", "Similar to momos but unique", "Great snack option"],
        best_time_to_visit="Year-round",
        time_needed="Meal or snack time",
        images=[],
        nearby_places=[],
        related_places=["dang_tharu_homestay"],
        tags=["bagiya", "dumpling", "rice flour", "tharu food", "traditional", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at restaurants",
        phone=None,
        website=None,
        email=None,
        google_rating=4.4,
        tripadvisor_rating=4.2,
        keywords=["bagiya", "dumpling", "rice flour", "tharu food", "traditional", "dang", "lentil"]
    ),
    
    TourismPlace(
        id="dang_food_sidhara",
        name="Sidhara",
        name_nepali="सिधारा",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "fish", "dried", "traditional"],
        description="""Sidhara are sun-dried fish cakes made with taro stems and spices, a traditional Tharu delicacy from Dang 
        District. This unique preparation involves drying fish and combining it with taro stems and aromatic spices to create 
        flavorful cakes. Sidhara is a preserved food item that can be stored and used over time, showcasing the Tharu community's 
        traditional food preservation techniques. The dish has a distinctive flavor profile and is typically cooked as a curry or 
        fried preparation. It's a must-try for those interested in traditional Tharu preserved foods.""",
        short_description="Sun-dried fish cakes made with taro stems and spices - traditional Tharu preserved food.",
        location=Location(latitude=28.0667, longitude=82.4833, address="Dang District", area="Dang", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$$", notes="Specialty preserved food"),
        highlights=["Sun-dried fish", "Taro stems", "Traditional preservation", "Unique flavor"],
        tips=["Try at authentic Tharu restaurants", "Distinctive taste", "Traditional preservation method"],
        best_time_to_visit="Year-round",
        time_needed="Meal time",
        images=[],
        nearby_places=[],
        related_places=["dang_tharu_homestay"],
        tags=["sidhara", "fish cake", "dried fish", "tharu food", "traditional", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at select restaurants",
        phone=None,
        website=None,
        email=None,
        google_rating=4.3,
        tripadvisor_rating=4.1,
        keywords=["sidhara", "fish cake", "dried fish", "taro stems", "tharu food", "dang"]
    ),
    
    TourismPlace(
        id="dang_food_pakuwa",
        name="Pakuwa",
        name_nepali="पकुवा",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "bbq", "meat", "traditional"],
        description="""Pakuwa is traditional BBQ pork or wild boar marinated in local spices, a popular Tharu dish in Dang District. 
        This flavorful meat preparation involves marinating pork or wild boar with aromatic local spices and then grilling or 
        barbecuing it to perfection. The dish has a rich, smoky flavor and is typically served with rice, traditional bread, or 
        as part of a larger meal. Pakuwa is especially popular during festivals and special occasions, representing the Tharu 
        community's expertise in meat preparation.""",
        short_description="Traditional BBQ pork or wild boar marinated in local spices - popular Tharu meat dish.",
        location=Location(latitude=28.0667, longitude=82.4833, address="Dang District", area="Dang", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$$", notes="Available at restaurants and festivals"),
        highlights=["BBQ preparation", "Pork or wild boar", "Local spice marinade", "Smoky flavor"],
        tips=["Try during festivals", "Best with rice", "Popular meat dish"],
        best_time_to_visit="Year-round, especially festivals",
        time_needed="Meal time",
        images=[],
        nearby_places=[],
        related_places=["dang_tharu_homestay"],
        tags=["pakuwa", "bbq", "pork", "wild boar", "tharu food", "traditional", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at restaurants",
        phone=None,
        website=None,
        email=None,
        google_rating=4.5,
        tripadvisor_rating=4.3,
        keywords=["pakuwa", "bbq", "pork", "wild boar", "tharu food", "dang", "spices"]
    ),
    
    TourismPlace(
        id="dang_food_gengta_chutney",
        name="Gengta (Kakhor) Chutney",
        name_nepali="गेंगटा (काखोर) चटनी",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "chutney", "crab", "spicy"],
        description="""Gengta, also known as Kakhor Chutney, is a spicy crab chutney or pickle that is a unique Tharu delicacy from 
        Dang District. This flavorful preparation involves cooking fresh crabs with local spices to create a tangy, spicy chutney 
        or pickle. The dish has a distinctive flavor profile and is typically served as a condiment or side dish with rice or 
        traditional bread. Gengta chutney showcases the Tharu community's expertise in using local ingredients and creating 
        flavorful accompaniments.""",
        short_description="Spicy crab chutney or pickle - unique Tharu delicacy with distinctive flavors.",
        location=Location(latitude=28.0667, longitude=82.4833, address="Dang District", area="Dang", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$$", notes="Specialty condiment"),
        highlights=["Crab preparation", "Spicy chutney", "Pickle style", "Unique flavor"],
        tips=["Try as condiment", "Spicy and flavorful", "Great with rice"],
        best_time_to_visit="Year-round",
        time_needed="Meal time",
        images=[],
        nearby_places=[],
        related_places=["dang_tharu_homestay"],
        tags=["gengta", "kakhor", "crab", "chutney", "tharu food", "traditional", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at select restaurants",
        phone=None,
        website=None,
        email=None,
        google_rating=4.3,
        tripadvisor_rating=4.1,
        keywords=["gengta", "kakhor", "crab chutney", "tharu food", "spicy", "dang"]
    ),
    
    TourismPlace(
        id="dang_food_parewak_sikar",
        name="Parewak Sikar",
        name_nepali="परेवाक सिकार",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "meat", "curry", "delicacy"],
        description="""Parewak Sikar is pigeon meat curry, a local delicacy in Dang District. This traditional Tharu dish involves 
        preparing pigeon meat in a flavorful curry with local spices and herbs. The dish has a rich, gamey flavor and is 
        considered a special treat in Tharu cuisine. Parewak Sikar is typically served with rice or traditional bread and is 
        especially popular during special occasions and festivals. It's a must-try for adventurous food lovers seeking 
        authentic Tharu meat preparations.""",
        short_description="Pigeon meat curry - local Tharu delicacy with rich, gamey flavors.",
        location=Location(latitude=28.0667, longitude=82.4833, address="Dang District", area="Dang", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$$$", notes="Specialty dish, available at select restaurants"),
        highlights=["Pigeon meat", "Traditional curry", "Local delicacy", "Gamey flavor"],
        tips=["Try at authentic restaurants", "Special occasion dish", "Rich flavors"],
        best_time_to_visit="Year-round, especially festivals",
        time_needed="Meal time",
        images=[],
        nearby_places=[],
        related_places=["dang_tharu_homestay"],
        tags=["parewak sikar", "pigeon", "curry", "tharu food", "delicacy", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at select restaurants",
        phone=None,
        website=None,
        email=None,
        google_rating=4.4,
        tripadvisor_rating=4.2,
        keywords=["parewak sikar", "pigeon", "curry", "tharu food", "delicacy", "dang"]
    ),
    
    TourismPlace(
        id="dang_food_jhingiya_machhari",
        name="Jhingiya Machhari",
        name_nepali="झिङिया माछरी",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "seafood", "shrimp", "traditional"],
        description="""Jhingiya Machhari is freshwater shrimp cooked dry or with gravy, a traditional Tharu dish from Dang District. 
        This flavorful seafood preparation showcases the Tharu community's expertise in cooking freshwater ingredients. The shrimp 
        can be prepared as a dry dish or in a flavorful gravy, both styles being popular. Jhingiya Machhari is typically served 
        with rice and is enjoyed for its fresh, distinctive flavors. It's a must-try for seafood lovers interested in traditional 
        Tharu cuisine.""",
        short_description="Freshwater shrimp cooked dry or with gravy - traditional Tharu seafood dish.",
        location=Location(latitude=28.0667, longitude=82.4833, address="Dang District", area="Dang", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$$", notes="Available at seafood restaurants"),
        highlights=["Freshwater shrimp", "Dry or gravy preparation", "Traditional Tharu style", "Fresh flavors"],
        tips=["Try both dry and gravy styles", "Best with rice", "Fresh seafood"],
        best_time_to_visit="Year-round",
        time_needed="Meal time",
        images=[],
        nearby_places=[],
        related_places=["dang_tharu_homestay"],
        tags=["jhingiya machhari", "shrimp", "seafood", "tharu food", "traditional", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at seafood restaurants",
        phone=None,
        website=None,
        email=None,
        google_rating=4.4,
        tripadvisor_rating=4.2,
        keywords=["jhingiya machhari", "shrimp", "freshwater", "tharu food", "dang", "seafood"]
    ),
    
    TourismPlace(
        id="dang_food_sipi",
        name="Sipi (Situwa)",
        name_nepali="सिपी (सितुवा)",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "seafood", "mussels", "traditional"],
        description="""Sipi, also known as Situwa, are freshwater mussels prepared in traditional Tharu style in Dang District. 
        This seafood dish involves cooking fresh mussels with local spices and herbs, creating a flavorful and distinctive 
        preparation. The mussels are typically prepared as a curry or dry dish and are enjoyed for their unique texture and flavors. 
        Sipi is a traditional Tharu seafood preparation that showcases the community's expertise in using freshwater ingredients.""",
        short_description="Freshwater mussels prepared in traditional Tharu style - flavorful seafood dish.",
        location=Location(latitude=28.0667, longitude=82.4833, address="Dang District", area="Dang", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$$", notes="Available at seafood restaurants"),
        highlights=["Freshwater mussels", "Traditional preparation", "Curry or dry style", "Unique flavors"],
        tips=["Try at seafood restaurants", "Distinctive texture", "Traditional Tharu style"],
        best_time_to_visit="Year-round",
        time_needed="Meal time",
        images=[],
        nearby_places=[],
        related_places=["dang_tharu_homestay"],
        tags=["sipi", "situwa", "mussels", "seafood", "tharu food", "traditional", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at seafood restaurants",
        phone=None,
        website=None,
        email=None,
        google_rating=4.3,
        tripadvisor_rating=4.1,
        keywords=["sipi", "situwa", "mussels", "freshwater", "tharu food", "dang"]
    ),
    
    TourismPlace(
        id="dang_food_bhakka",
        name="Bhakka",
        name_nepali="भक्का",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "rice_cake", "steamed", "winter"],
        description="""Bhakka is a fluffy steamed rice cake that is particularly popular in winter in Dang District. This 
        traditional Tharu dish is made from rice flour and is steamed to create a soft, fluffy texture. Bhakka is typically 
        enjoyed warm and is often served with spicy chutneys, curries, or sweet accompaniments. The dish is especially popular 
        during the winter months when warm, comforting foods are preferred. It's a simple yet delicious traditional Tharu 
        preparation.""",
        short_description="Fluffy steamed rice cake, especially popular during winter months.",
        location=Location(latitude=28.0667, longitude=82.4833, address="Dang District", area="Dang", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$", notes="Available at local restaurants"),
        highlights=["Steamed rice cake", "Fluffy texture", "Winter favorite", "Traditional preparation"],
        tips=["Best enjoyed warm", "Try with chutney or curry", "Popular in winter"],
        best_time_to_visit="Year-round, especially winter",
        time_needed="Meal or snack time",
        images=[],
        nearby_places=[],
        related_places=["dang_tharu_homestay"],
        tags=["bhakka", "rice cake", "steamed", "tharu food", "winter", "traditional", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at restaurants",
        phone=None,
        website=None,
        email=None,
        google_rating=4.4,
        tripadvisor_rating=4.2,
        keywords=["bhakka", "rice cake", "steamed", "tharu food", "winter", "dang"]
    ),
    
    TourismPlace(
        id="dang_food_mahuwa",
        name="Mahuwa",
        name_nepali="महुवा",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "liquor", "traditional", "alcoholic"],
        description="""Mahuwa is a traditional local liquor made from Mahuwa flowers, a specialty of Dang District. This unique 
        alcoholic beverage is crafted using traditional methods and the flowers of the Mahuwa tree. The liquor has a distinctive 
        flavor and is an important part of Tharu cultural traditions, especially during festivals and celebrations. Mahuwa is 
        typically consumed during special occasions and is considered a traditional drink of the Tharu community. It's a must-try 
        for those interested in experiencing authentic Tharu beverages and cultural traditions.""",
        short_description="Traditional local liquor made from Mahuwa flowers - Tharu cultural beverage.",
        location=Location(latitude=28.0667, longitude=82.4833, address="Dang District", area="Dang", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$$", notes="Traditional beverage, available at local establishments"),
        highlights=["Mahuwa flower liquor", "Traditional preparation", "Cultural significance", "Festival drink"],
        tips=["Try during festivals", "Traditional Tharu beverage", "Cultural experience"],
        best_time_to_visit="Year-round, especially festivals",
        time_needed="Drink time",
        images=[],
        nearby_places=[],
        related_places=["dang_tharu_homestay"],
        tags=["mahuwa", "liquor", "traditional", "tharu", "beverage", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at local establishments",
        phone=None,
        website=None,
        email=None,
        google_rating=4.3,
        tripadvisor_rating=4.1,
        keywords=["mahuwa", "liquor", "mahuwa flowers", "traditional", "tharu", "dang"]
    ),
    
    TourismPlace(
        id="dang_food_tilaur",
        name="Tilaur",
        name_nepali="तिलौर",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "snack", "fried", "crispy"],
        description="""Tilaur is a crispy deep-fried snack made from lentils, a popular Tharu snack in Dang District. This 
        traditional snack involves preparing lentils in a special way and deep-frying them to create a crispy, flavorful treat. 
        Tilaur is typically enjoyed as a snack or appetizer and is especially popular during festivals and gatherings. The snack 
        has a satisfying crunch and is often seasoned with local spices. It's a must-try for those interested in traditional Tharu 
        snacks and street food.""",
        short_description="Crispy deep-fried snack made from lentils - popular Tharu snack.",
        location=Location(latitude=28.0667, longitude=82.4833, address="Dang District", area="Dang", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$", notes="Available as snack"),
        highlights=["Lentil snack", "Deep-fried", "Crispy texture", "Traditional preparation"],
        tips=["Great as snack", "Try during festivals", "Crispy and flavorful"],
        best_time_to_visit="Year-round",
        time_needed="Snack time",
        images=[],
        nearby_places=[],
        related_places=["dang_tharu_homestay"],
        tags=["tilaur", "snack", "lentil", "fried", "tharu food", "traditional", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available as snack",
        phone=None,
        website=None,
        email=None,
        google_rating=4.3,
        tripadvisor_rating=4.1,
        keywords=["tilaur", "snack", "lentil", "fried", "tharu food", "dang", "crispy"]
    ),
    
    TourismPlace(
        id="dang_food_tharu_achar",
        name="Tharu Achar",
        name_nepali="थारू अचार",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "pickle", "fermented", "spicy"],
        description="""Tharu Achar are fermented spicy pickles unique to the Tharu region in Dang District. These traditional 
        pickles are made using various local ingredients like radish, bamboo shoots, or other vegetables, which are fermented and 
        spiced to create distinctive flavors. Tharu Achar is typically served as a condiment with meals and adds a tangy, spicy 
        element to the food. The pickles are an essential part of Tharu cuisine and showcase the community's expertise in food 
        preservation and flavor enhancement.""",
        short_description="Fermented spicy pickles unique to Tharu region - essential condiment in Tharu cuisine.",
        location=Location(latitude=28.0667, longitude=82.4833, address="Dang District", area="Dang", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$", notes="Available as condiment"),
        highlights=["Fermented pickles", "Spicy and tangy", "Traditional preservation", "Unique flavors"],
        tips=["Try with meals", "Essential Tharu condiment", "Various ingredients"],
        best_time_to_visit="Year-round",
        time_needed="Meal time",
        images=[],
        nearby_places=[],
        related_places=["dang_tharu_homestay"],
        tags=["tharu achar", "pickle", "fermented", "spicy", "tharu food", "traditional", "dang"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available as condiment",
        phone=None,
        website=None,
        email=None,
        google_rating=4.4,
        tripadvisor_rating=4.2,
        keywords=["tharu achar", "pickle", "fermented", "tharu food", "spicy", "dang"]
    ),
    
    # ============================================================================
    # KAILALI DISTRICT PLACES
    # ============================================================================
    
    TourismPlace(
        id="kailali_tikapur_garden",
        name="Tikapur Great Garden",
        name_nepali="टिकापुर महान बगैंचा",
        category=PlaceCategory.NATURE,
        subcategories=["garden", "park", "recreational", "well_maintained"],
        description="""Tikapur Great Garden is one of the largest and most well-maintained gardens in Nepal, located in Kailali 
        District. This expansive garden features beautifully landscaped areas, walking paths, water features, and diverse 
        plant collections. The garden is a popular recreational destination for families, nature lovers, and those seeking a 
        peaceful escape. It's particularly famous for its size and maintenance, making it a standout attraction in the Far-West 
        region of Nepal. The garden offers excellent opportunities for photography, relaxation, and enjoying nature.""",
        short_description="One of the largest and most well-maintained gardens in Nepal - major recreational destination.",
        location=Location(latitude=28.5167, longitude=81.1167, address="Tikapur, Kailali District", area="Tikapur", ward=None),
        opening_hours=OpeningHours(monday="6:00 AM - 7:00 PM", tuesday="6:00 AM - 7:00 PM", wednesday="6:00 AM - 7:00 PM", thursday="6:00 AM - 7:00 PM", friday="6:00 AM - 7:00 PM", saturday="6:00 AM - 7:00 PM", sunday="6:00 AM - 7:00 PM"),
        price_info=PriceInfo(currency="NPR", nepali_citizen=50, saarc_citizen=100, foreign_tourist=200),
        highlights=["Largest garden in Nepal", "Well-maintained", "Beautiful landscaping", "Recreational activities"],
        tips=["Great for families", "Photography opportunities", "Bring water and snacks"],
        best_time_to_visit="Year-round, especially morning and evening",
        time_needed="2-3 hours",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["garden", "park", "recreational", "tikapur", "kailali", "nature"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Garden accessible",
        phone=None,
        website=None,
        email=None,
        google_rating=4.6,
        tripadvisor_rating=4.4,
        keywords=["tikapur garden", "great garden", "garden", "tikapur", "kailali", "park"]
    ),
    
    TourismPlace(
        id="kailali_karnali_bridge",
        name="Karnali Bridge (Chisapani)",
        name_nepali="कर्णाली पुल (चिसापानी)",
        category=PlaceCategory.VIEWPOINT,
        subcategories=["bridge", "engineering", "sunset", "iconic"],
        description="""Karnali Bridge at Chisapani is an iconic single-tower cable-stayed bridge, one of Nepal's engineering 
        marvels. This impressive bridge spans the Karnali River and is renowned for its unique single-tower design. The bridge 
        offers spectacular views of the Karnali River and surrounding landscapes, making it especially popular for sunset viewing. 
        The area around the bridge is perfect for photography, enjoying river views, and experiencing this impressive piece of 
        infrastructure. Chisapani is also known for its strategic location and natural beauty.""",
        short_description="Iconic single-tower cable-stayed bridge - great for sunset views and photography.",
        location=Location(latitude=28.4833, longitude=81.0833, address="Chisapani, Kailali District", area="Chisapani", ward=None),
        opening_hours=OpeningHours(monday="24 hours", tuesday="24 hours", wednesday="24 hours", thursday="24 hours", friday="24 hours", saturday="24 hours", sunday="24 hours"),
        price_info=PriceInfo(currency="NPR", nepali_citizen=0, saarc_citizen=0, foreign_tourist=0),
        highlights=["Single-tower design", "Iconic bridge", "Sunset views", "Karnali River"],
        tips=["Best at sunset", "Photography recommended", "Enjoy river views"],
        best_time_to_visit="Evening for sunset",
        time_needed="1-2 hours",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["bridge", "karnali", "chisapani", "engineering", "sunset", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Bridge accessible",
        phone=None,
        website=None,
        email=None,
        google_rating=4.5,
        tripadvisor_rating=4.3,
        keywords=["karnali bridge", "chisapani", "bridge", "karnali river", "sunset", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_ghodaghodi_lake",
        name="Ghodaghodi Lake",
        name_nepali="घोडाघोडी ताल",
        category=PlaceCategory.NATURE,
        subcategories=["lake", "wetland", "ramsar", "bird_watching"],
        description="""Ghodaghodi Lake is a massive wetland complex and Ramsar site, perfect for bird watching in Kailali District. 
        This important wetland ecosystem is home to numerous bird species, both resident and migratory, making it a paradise for 
        bird watchers and nature enthusiasts. The lake complex features diverse aquatic habitats and supports rich biodiversity. 
        It's an excellent destination for those interested in wildlife, nature photography, and experiencing Nepal's wetland 
        ecosystems. The area is particularly vibrant during migration seasons when various bird species visit the lake.""",
        short_description="Massive wetland complex and Ramsar site - perfect for bird watching and nature observation.",
        location=Location(latitude=28.6833, longitude=80.9500, address="Kailali District", area="Ghodaghodi", ward=None),
        opening_hours=OpeningHours(monday="6:00 AM - 6:00 PM", tuesday="6:00 AM - 6:00 PM", wednesday="6:00 AM - 6:00 PM", thursday="6:00 AM - 6:00 PM", friday="6:00 AM - 6:00 PM", saturday="6:00 AM - 6:00 PM", sunday="6:00 AM - 6:00 PM"),
        price_info=PriceInfo(currency="NPR", nepali_citizen=50, saarc_citizen=100, foreign_tourist=200),
        highlights=["Ramsar site", "Bird watching paradise", "Wetland ecosystem", "Rich biodiversity"],
        tips=["Bring binoculars", "Best during migration season", "Respect wildlife"],
        best_time_to_visit="Migration seasons (winter and spring)",
        time_needed="Half day",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["lake", "wetland", "ramsar", "bird watching", "nature", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Lake accessible",
        phone=None,
        website=None,
        email=None,
        google_rating=4.5,
        tripadvisor_rating=4.3,
        keywords=["ghodaghodi lake", "wetland", "ramsar", "bird watching", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_dolphin_conservation",
        name="Dolphin Conservation Area",
        name_nepali="डल्फिन संरक्षण क्षेत्र",
        category=PlaceCategory.NATURE,
        subcategories=["wildlife", "conservation", "river", "dolphin"],
        description="""The Dolphin Conservation Area offers opportunities to spot Gangetic dolphins in the Mohana and Karnali 
        rivers in Kailali District. This important conservation area is dedicated to protecting the endangered Gangetic river 
        dolphins. Visitors can take boat rides or observe from riverbanks to spot these rare freshwater dolphins. The area is 
        significant for wildlife conservation and offers unique opportunities to see these fascinating marine mammals in their 
        natural habitat. It's a must-visit for wildlife enthusiasts and those interested in conservation efforts.""",
        short_description="Conservation area for spotting Gangetic dolphins in Mohana and Karnali rivers.",
        location=Location(latitude=28.5000, longitude=81.1000, address="Mohana/Karnali Rivers, Kailali District", area="Kailali", ward=None),
        opening_hours=OpeningHours(monday="6:00 AM - 6:00 PM", tuesday="6:00 AM - 6:00 PM", wednesday="6:00 AM - 6:00 PM", thursday="6:00 AM - 6:00 PM", friday="6:00 AM - 6:00 PM", saturday="6:00 AM - 6:00 PM", sunday="6:00 AM - 6:00 PM"),
        price_info=PriceInfo(currency="NPR", nepali_citizen=100, saarc_citizen=200, foreign_tourist=500, notes="Boat rides available"),
        highlights=["Gangetic dolphins", "Conservation area", "River wildlife", "Boat rides"],
        tips=["Best time: early morning", "Boat rides recommended", "Bring binoculars"],
        best_time_to_visit="Early morning or late afternoon",
        time_needed="2-3 hours",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["dolphin", "conservation", "wildlife", "river", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Boat access required",
        phone=None,
        website=None,
        email=None,
        google_rating=4.4,
        tripadvisor_rating=4.2,
        keywords=["dolphin", "gangetic dolphin", "conservation", "mohana river", "karnali", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_bhada_tharu_homestay",
        name="Bhada Tharu Homestay",
        name_nepali="भाडा थारू होमस्टे",
        category=PlaceCategory.CULTURAL,
        subcategories=["homestay", "tharu", "cultural", "authentic"],
        description="""Bhada Tharu Homestay offers an authentic experience of Tharu hospitality, food, and culture firsthand in 
        Kailali District. This homestay provides visitors with the opportunity to stay with local Tharu families and immerse 
        themselves in traditional Tharu lifestyle. Guests can participate in daily activities, learn about Tharu customs, 
        enjoy traditional Tharu cuisine, and experience authentic cultural practices. The homestay is an excellent way to support 
        local communities while gaining deep insights into Tharu culture and traditions.""",
        short_description="Authentic Tharu homestay experience with traditional hospitality, food, and culture.",
        location=Location(latitude=28.6833, longitude=80.9500, address="Bhada, Kailali District", area="Bhada", ward=None),
        opening_hours=OpeningHours(monday="24 hours", tuesday="24 hours", wednesday="24 hours", thursday="24 hours", friday="24 hours", saturday="24 hours", sunday="24 hours"),
        price_info=PriceInfo(currency="NPR", price_range="$$", notes="Typically 1000-2000 NPR per night including meals"),
        highlights=["Authentic Tharu culture", "Traditional hospitality", "Tharu cuisine", "Cultural immersion"],
        tips=["Book in advance", "Respect local customs", "Participate in activities"],
        best_time_to_visit="Year-round",
        time_needed="Overnight stay recommended",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["homestay", "tharu", "cultural", "authentic", "bhada", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Homestay accessible",
        phone=None,
        website=None,
        email=None,
        google_rating=4.6,
        tripadvisor_rating=4.4,
        keywords=["bhada tharu homestay", "homestay", "tharu", "cultural", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_shivpuri_dham",
        name="Shivpuri Dham",
        name_nepali="शिवपुरी धाम",
        category=PlaceCategory.TEMPLE,
        subcategories=["temple", "religious", "shiva", "major"],
        description="""Shivpuri Dham is a major religious site in Dhangadhi, Kailali District, featuring a towering Shiva statue. 
        This important Hindu temple complex is dedicated to Lord Shiva and attracts devotees from across the region. The site 
        features impressive architecture and a large Shiva statue that serves as a focal point. Shivpuri Dham is especially 
        vibrant during religious festivals and is a significant pilgrimage destination. The temple complex offers a peaceful 
        atmosphere for prayer and religious contemplation.""",
        short_description="Major religious site in Dhangadhi with towering Shiva statue - important pilgrimage destination.",
        location=Location(latitude=28.6833, longitude=80.6167, address="Dhangadhi, Kailali District", area="Dhangadhi", ward=None),
        opening_hours=OpeningHours(monday="5:00 AM - 8:00 PM", tuesday="5:00 AM - 8:00 PM", wednesday="5:00 AM - 8:00 PM", thursday="5:00 AM - 8:00 PM", friday="5:00 AM - 8:00 PM", saturday="5:00 AM - 8:00 PM", sunday="5:00 AM - 8:00 PM"),
        price_info=PriceInfo(currency="NPR", nepali_citizen=0, saarc_citizen=0, foreign_tourist=0),
        highlights=["Towering Shiva statue", "Major religious site", "Temple complex", "Pilgrimage destination"],
        tips=["Visit during festivals", "Respect temple customs", "Photography allowed"],
        best_time_to_visit="During festivals and special occasions",
        time_needed="1-2 hours",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["temple", "shiva", "religious", "dhangadhi", "pilgrimage", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi", "Sanskrit"],
        accessibility="Temple accessible",
        phone=None,
        website=None,
        email=None,
        google_rating=4.5,
        tripadvisor_rating=4.3,
        keywords=["shivpuri dham", "shiva", "temple", "dhangadhi", "religious", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_behadababa_temple",
        name="Behadababa Temple",
        name_nepali="बेहदाबाबा मन्दिर",
        category=PlaceCategory.TEMPLE,
        subcategories=["temple", "religious", "forest", "revered"],
        description="""Behadababa Temple is a revered shrine located in the middle of a forest in Kailali District. This 
        peaceful temple is surrounded by natural forest settings, creating a serene and spiritual atmosphere. The temple is 
        dedicated to a revered saint and attracts devotees seeking blessings and spiritual solace. The forest location adds to 
        the temple's peaceful ambiance, making it an ideal spot for meditation and religious contemplation. The journey to the 
        temple through the forest adds to the spiritual experience.""",
        short_description="Revered shrine in the middle of a forest - peaceful spiritual destination.",
        location=Location(latitude=28.6500, longitude=80.7000, address="Kailali District", area="Kailali", ward=None),
        opening_hours=OpeningHours(monday="6:00 AM - 7:00 PM", tuesday="6:00 AM - 7:00 PM", wednesday="6:00 AM - 7:00 PM", thursday="6:00 AM - 7:00 PM", friday="6:00 AM - 7:00 PM", saturday="6:00 AM - 7:00 PM", sunday="6:00 AM - 7:00 PM"),
        price_info=PriceInfo(currency="NPR", nepali_citizen=0, saarc_citizen=0, foreign_tourist=0),
        highlights=["Forest location", "Revered shrine", "Peaceful atmosphere", "Spiritual destination"],
        tips=["Respect forest environment", "Quiet meditation possible", "Nature walk included"],
        best_time_to_visit="Year-round",
        time_needed="1-2 hours",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["temple", "forest", "religious", "spiritual", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Requires forest walk",
        phone=None,
        website=None,
        email=None,
        google_rating=4.3,
        tripadvisor_rating=4.1,
        keywords=["behadababa temple", "temple", "forest", "religious", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_jakhor_taal",
        name="Jakhor Taal",
        name_nepali="जखोर ताल",
        category=PlaceCategory.NATURE,
        subcategories=["lake", "botanical_garden", "recreational", "nature"],
        description="""Jakhor Taal is a botanical garden and lake area in Dhangadhi, Kailali District. This beautiful natural 
        space combines a serene lake with well-maintained botanical gardens, creating a perfect recreational destination. The 
        area features diverse plant collections, walking paths, and peaceful lake views. Jakhor Taal is popular among locals and 
        visitors for relaxation, nature walks, and enjoying the natural beauty. It's an ideal spot for families, nature lovers, 
        and those seeking a peaceful escape.""",
        short_description="Botanical garden and lake area in Dhangadhi - perfect for recreation and nature appreciation.",
        location=Location(latitude=28.6833, longitude=80.6167, address="Dhangadhi, Kailali District", area="Dhangadhi", ward=None),
        opening_hours=OpeningHours(monday="6:00 AM - 7:00 PM", tuesday="6:00 AM - 7:00 PM", wednesday="6:00 AM - 7:00 PM", thursday="6:00 AM - 7:00 PM", friday="6:00 AM - 7:00 PM", saturday="6:00 AM - 7:00 PM", sunday="6:00 AM - 7:00 PM"),
        price_info=PriceInfo(currency="NPR", nepali_citizen=50, saarc_citizen=100, foreign_tourist=200),
        highlights=["Botanical garden", "Lake area", "Recreational space", "Natural beauty"],
        tips=["Great for families", "Nature walks", "Photography opportunities"],
        best_time_to_visit="Year-round, especially morning and evening",
        time_needed="1-2 hours",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["lake", "botanical garden", "recreational", "dhangadhi", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Garden accessible",
        phone=None,
        website=None,
        email=None,
        google_rating=4.4,
        tripadvisor_rating=4.2,
        keywords=["jakhor taal", "lake", "botanical garden", "dhangadhi", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_aircraft_museum",
        name="Aircraft Museum",
        name_nepali="विमान संग्रहालय",
        category=PlaceCategory.MUSEUM,
        subcategories=["museum", "aircraft", "unique", "dhangadhi"],
        description="""The Aircraft Museum in Dhangadhi features an actual decommissioned plane turned into a museum, a unique 
        attraction in Kailali District. This one-of-a-kind museum offers visitors the opportunity to explore a real aircraft 
        and learn about aviation history. The converted plane serves as an educational and entertainment space, making it a 
        fascinating destination for both children and adults. The museum is a unique addition to Dhangadhi's attractions and 
        offers an interesting perspective on repurposing and aviation.""",
        short_description="Unique museum featuring a decommissioned plane - fascinating aviation attraction.",
        location=Location(latitude=28.6833, longitude=80.6167, address="Dhangadhi, Kailali District", area="Dhangadhi", ward=None),
        opening_hours=OpeningHours(monday="9:00 AM - 5:00 PM", tuesday="9:00 AM - 5:00 PM", wednesday="9:00 AM - 5:00 PM", thursday="9:00 AM - 5:00 PM", friday="9:00 AM - 5:00 PM", saturday="9:00 AM - 5:00 PM", sunday="Closed"),
        price_info=PriceInfo(currency="NPR", nepali_citizen=50, saarc_citizen=100, foreign_tourist=200),
        highlights=["Decommissioned aircraft", "Unique museum", "Aviation history", "Educational"],
        tips=["Great for children", "Unique experience", "Photography allowed"],
        best_time_to_visit="Year-round",
        time_needed="1 hour",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["museum", "aircraft", "aviation", "unique", "dhangadhi", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi", "English"],
        accessibility="Museum accessible",
        phone=None,
        website=None,
        email=None,
        google_rating=4.3,
        tripadvisor_rating=4.1,
        keywords=["aircraft museum", "museum", "airplane", "dhangadhi", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_godawari_dham",
        name="Godawari Dham",
        name_nepali="गोदावरी धाम",
        category=PlaceCategory.TEMPLE,
        subcategories=["temple", "spiritual", "hanuman", "river"],
        description="""Godawari Dham is a spiritual site with a giant Hanuman statue and river in Kailali District. This important 
        religious destination features impressive architecture and a large statue of Lord Hanuman, making it a significant 
        pilgrimage site. The temple complex is located near a river, adding to its spiritual and natural ambiance. Godawari Dham 
        attracts devotees seeking blessings and spiritual experiences. The site offers a peaceful atmosphere for prayer and 
        religious contemplation.""",
        short_description="Spiritual site with giant Hanuman statue and river - important pilgrimage destination.",
        location=Location(latitude=28.6500, longitude=80.6500, address="Kailali District", area="Kailali", ward=None),
        opening_hours=OpeningHours(monday="5:00 AM - 8:00 PM", tuesday="5:00 AM - 8:00 PM", wednesday="5:00 AM - 8:00 PM", thursday="5:00 AM - 8:00 PM", friday="5:00 AM - 8:00 PM", saturday="5:00 AM - 8:00 PM", sunday="5:00 AM - 8:00 PM"),
        price_info=PriceInfo(currency="NPR", nepali_citizen=0, saarc_citizen=0, foreign_tourist=0),
        highlights=["Giant Hanuman statue", "Spiritual site", "River location", "Pilgrimage destination"],
        tips=["Visit during festivals", "Respect temple customs", "Enjoy river views"],
        best_time_to_visit="Year-round, especially festivals",
        time_needed="1-2 hours",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["temple", "hanuman", "spiritual", "river", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi", "Sanskrit"],
        accessibility="Temple accessible",
        phone=None,
        website=None,
        email=None,
        google_rating=4.4,
        tripadvisor_rating=4.2,
        keywords=["godawari dham", "hanuman", "temple", "spiritual", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_banana_restaurant",
        name="Banana Restaurant",
        name_nepali="केरा रेस्टुरेन्ट",
        category=PlaceCategory.RESTAURANT,
        subcategories=["restaurant", "unique", "banana", "tikapur"],
        description="""Banana Restaurant is a unique spot in Tikapur where everything is made of bananas, a one-of-a-kind 
        culinary experience in Kailali District. This innovative restaurant offers a complete menu featuring banana-based dishes, 
        from main courses to desserts and beverages. The restaurant showcases the creativity of using bananas in various culinary 
        preparations, making it a must-visit for food enthusiasts. It's a unique dining experience that highlights the local 
        banana production in the region and offers something truly different for visitors.""",
        short_description="Unique restaurant where everything is made of bananas - one-of-a-kind culinary experience.",
        location=Location(latitude=28.5167, longitude=81.1167, address="Tikapur, Kailali District", area="Tikapur", ward=None),
        opening_hours=OpeningHours(monday="9:00 AM - 9:00 PM", tuesday="9:00 AM - 9:00 PM", wednesday="9:00 AM - 9:00 PM", thursday="9:00 AM - 9:00 PM", friday="9:00 AM - 9:00 PM", saturday="9:00 AM - 9:00 PM", sunday="9:00 AM - 9:00 PM"),
        price_info=PriceInfo(currency="NPR", price_range="$$", notes="Unique banana-based menu"),
        highlights=["Everything banana-based", "Unique concept", "Innovative cuisine", "Local produce"],
        tips=["Try banana momo", "Unique dining experience", "Great for food lovers"],
        best_time_to_visit="Year-round",
        time_needed="Meal time",
        images=[],
        nearby_places=["kailali_tikapur_garden"],
        related_places=[],
        tags=["restaurant", "banana", "unique", "tikapur", "kailali", "culinary"],
        languages_spoken=["Nepali", "Tharu", "Hindi", "English"],
        accessibility="Restaurant accessible",
        phone=None,
        website=None,
        email=None,
        google_rating=4.5,
        tripadvisor_rating=4.3,
        keywords=["banana restaurant", "banana", "restaurant", "tikapur", "kailali", "unique"]
    ),
    
    TourismPlace(
        id="kailali_dhangadhi_park",
        name="Dhangadhi Park",
        name_nepali="धनगढी पार्क",
        category=PlaceCategory.NATURE,
        subcategories=["park", "recreational", "central", "local"],
        description="""Dhangadhi Park is a central recreational spot for locals and tourists in Dhangadhi, Kailali District. 
        This well-maintained park offers a peaceful environment for relaxation, family outings, and recreational activities. The 
        park features walking paths, green spaces, and facilities for various activities. It's a popular gathering place for the 
        local community and provides a pleasant escape in the heart of Dhangadhi. The park is ideal for morning walks, evening 
        strolls, and spending quality time with family and friends.""",
        short_description="Central recreational park in Dhangadhi - popular gathering spot for locals and tourists.",
        location=Location(latitude=28.6833, longitude=80.6167, address="Dhangadhi, Kailali District", area="Dhangadhi", ward=None),
        opening_hours=OpeningHours(monday="5:00 AM - 8:00 PM", tuesday="5:00 AM - 8:00 PM", wednesday="5:00 AM - 8:00 PM", thursday="5:00 AM - 8:00 PM", friday="5:00 AM - 8:00 PM", saturday="5:00 AM - 8:00 PM", sunday="5:00 AM - 8:00 PM"),
        price_info=PriceInfo(currency="NPR", nepali_citizen=0, saarc_citizen=0, foreign_tourist=0),
        highlights=["Central location", "Recreational activities", "Family-friendly", "Well-maintained"],
        tips=["Great for morning walks", "Family outings", "Evening relaxation"],
        best_time_to_visit="Year-round, especially morning and evening",
        time_needed="1-2 hours",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["park", "recreational", "dhangadhi", "central", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Park accessible",
        phone=None,
        website=None,
        email=None,
        google_rating=4.3,
        tripadvisor_rating=4.1,
        keywords=["dhangadhi park", "park", "recreational", "dhangadhi", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_mohana_river_corridor",
        name="Mohana River Corridor",
        name_nepali="मोहना नदी क्षेत्र",
        category=PlaceCategory.NATURE,
        subcategories=["river", "wildlife", "evening_walks", "border"],
        description="""The Mohana River Corridor is famous for evening walks and spotting wildlife near the border in Kailali 
        District. This scenic river area offers beautiful natural settings and opportunities to observe local wildlife. The 
        corridor is particularly popular for evening walks when the weather is pleasant and wildlife is more active. The area 
        provides a peaceful environment for nature appreciation and offers glimpses of the region's natural biodiversity. It's an 
        ideal destination for nature lovers and those seeking a relaxing outdoor experience.""",
        short_description="Scenic river corridor famous for evening walks and wildlife spotting near the border.",
        location=Location(latitude=28.5000, longitude=80.5000, address="Mohana River, Kailali District", area="Kailali", ward=None),
        opening_hours=OpeningHours(monday="24 hours", tuesday="24 hours", wednesday="24 hours", thursday="24 hours", friday="24 hours", saturday="24 hours", sunday="24 hours"),
        price_info=PriceInfo(currency="NPR", nepali_citizen=0, saarc_citizen=0, foreign_tourist=0),
        highlights=["River corridor", "Evening walks", "Wildlife spotting", "Scenic beauty"],
        tips=["Best in evening", "Wildlife observation", "Peaceful walks"],
        best_time_to_visit="Evening for walks and wildlife",
        time_needed="1-2 hours",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["river", "wildlife", "evening walks", "nature", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="River corridor accessible",
        phone=None,
        website=None,
        email=None,
        google_rating=4.4,
        tripadvisor_rating=4.2,
        keywords=["mohana river", "river corridor", "wildlife", "evening walks", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_bandevi_temple",
        name="Bandevi Temple",
        name_nepali="बन्देवी मन्दिर",
        category=PlaceCategory.TEMPLE,
        subcategories=["temple", "forest", "popular", "religious"],
        description="""Bandevi Temple is a popular temple located in the lush forests of Kailali District. This peaceful religious 
        site is surrounded by natural forest settings, creating a serene and spiritual atmosphere. The temple attracts devotees 
        seeking blessings and spiritual experiences. The forest location adds to the temple's peaceful ambiance, making it an 
        ideal spot for meditation and religious contemplation. The natural surroundings make it a beautiful destination 
        combining spirituality and nature.""",
        short_description="Popular temple in lush forests - peaceful spiritual destination with natural beauty.",
        location=Location(latitude=28.6500, longitude=80.7000, address="Kailali District", area="Kailali", ward=None),
        opening_hours=OpeningHours(monday="6:00 AM - 7:00 PM", tuesday="6:00 AM - 7:00 PM", wednesday="6:00 AM - 7:00 PM", thursday="6:00 AM - 7:00 PM", friday="6:00 AM - 7:00 PM", saturday="6:00 AM - 7:00 PM", sunday="6:00 AM - 7:00 PM"),
        price_info=PriceInfo(currency="NPR", nepali_citizen=0, saarc_citizen=0, foreign_tourist=0),
        highlights=["Forest location", "Popular temple", "Peaceful atmosphere", "Natural beauty"],
        tips=["Respect forest environment", "Quiet meditation", "Nature walk"],
        best_time_to_visit="Year-round",
        time_needed="1 hour",
        images=[],
        nearby_places=[],
        related_places=["kailali_behadababa_temple"],
        tags=["temple", "forest", "religious", "popular", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Requires forest walk",
        phone=None,
        website=None,
        email=None,
        google_rating=4.3,
        tripadvisor_rating=4.1,
        keywords=["bandevi temple", "temple", "forest", "religious", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_koilahi_lake",
        name="Koilahi Lake",
        name_nepali="कोइलाही ताल",
        category=PlaceCategory.NATURE,
        subcategories=["lake", "quiet", "nature", "less_commercial"],
        description="""Koilahi Lake is a quiet and less-commercialized lake perfect for nature lovers in Kailali District. This 
        peaceful natural lake offers a serene escape from more crowded tourist destinations. The lake provides opportunities for 
        quiet contemplation, nature observation, and enjoying the peaceful natural surroundings. It's an ideal destination for 
        those seeking a more authentic and less commercialized nature experience. The lake's tranquility makes it perfect for 
        relaxation and connecting with nature.""",
        short_description="Quiet and less-commercialized lake - perfect for nature lovers seeking tranquility.",
        location=Location(latitude=28.7000, longitude=80.7500, address="Kailali District", area="Kailali", ward=None),
        opening_hours=OpeningHours(monday="6:00 AM - 6:00 PM", tuesday="6:00 AM - 6:00 PM", wednesday="6:00 AM - 6:00 PM", thursday="6:00 AM - 6:00 PM", friday="6:00 AM - 6:00 PM", saturday="6:00 AM - 6:00 PM", sunday="6:00 AM - 6:00 PM"),
        price_info=PriceInfo(currency="NPR", nepali_citizen=0, saarc_citizen=0, foreign_tourist=0),
        highlights=["Quiet lake", "Less commercialized", "Natural beauty", "Tranquil atmosphere"],
        tips=["Perfect for quiet time", "Nature observation", "Peaceful escape"],
        best_time_to_visit="Year-round",
        time_needed="1-2 hours",
        images=[],
        nearby_places=[],
        related_places=["kailali_ghodaghodi_lake"],
        tags=["lake", "quiet", "nature", "tranquil", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Lake accessible",
        phone=None,
        website=None,
        email=None,
        google_rating=4.3,
        tripadvisor_rating=4.1,
        keywords=["koilahi lake", "lake", "quiet", "nature", "kailali"]
    ),
    
    # ============================================================================
    # KAILALI DISTRICT FOODS
    # ============================================================================
    
    TourismPlace(
        id="kailali_food_banana_momo",
        name="Banana Momo",
        name_nepali="केरा मोमो",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "momo", "banana", "unique", "tikapur"],
        description="""Banana Momo is unique to Tikapur, Kailali District - momos with savory banana filling, a one-of-a-kind 
        culinary innovation. This creative dish combines the traditional momo preparation with local banana produce, creating a 
        unique flavor profile. The banana filling is seasoned with local spices, creating a sweet and savory combination that's 
        distinctive to the region. Banana Momo is a must-try for food enthusiasts visiting Tikapur and represents the innovative 
        use of local ingredients in traditional preparations.""",
        short_description="Unique momos with savory banana filling - specialty of Tikapur, Kailali.",
        location=Location(latitude=28.5167, longitude=81.1167, address="Tikapur, Kailali District", area="Tikapur", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$", notes="Available at Banana Restaurant and local eateries"),
        highlights=["Unique banana filling", "Tikapur specialty", "Innovative cuisine", "Sweet and savory"],
        tips=["Try at Banana Restaurant", "Unique flavor experience", "Must-try in Tikapur"],
        best_time_to_visit="Year-round",
        time_needed="Meal or snack time",
        images=[],
        nearby_places=["kailali_banana_restaurant"],
        related_places=[],
        tags=["banana momo", "momo", "banana", "tikapur", "kailali", "unique"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at restaurants",
        phone=None,
        website=None,
        email=None,
        google_rating=4.5,
        tripadvisor_rating=4.3,
        keywords=["banana momo", "momo", "banana", "tikapur", "kailali", "unique"]
    ),
    
    TourismPlace(
        id="kailali_food_banana_chips",
        name="Banana Chips",
        name_nepali="केरा चिप्स",
        category=PlaceCategory.RESTAURANT,
        subcategories=["snack", "banana", "chips", "local"],
        description="""Banana Chips are freshly made crunchy chips from local banana plantations in Kailali District. These 
        delicious snacks are made from locally grown bananas, sliced thin and fried to perfection. The chips have a satisfying 
        crunch and are often seasoned with salt or spices. They're a popular local snack and are especially common in Tikapur 
        where banana production is significant. Banana chips make for a great snack while exploring the region and are a perfect 
        example of using local produce.""",
        short_description="Freshly made crunchy chips from local banana plantations - popular local snack.",
        location=Location(latitude=28.5167, longitude=81.1167, address="Tikapur, Kailali District", area="Tikapur", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$", notes="Available as snack"),
        highlights=["Freshly made", "Local bananas", "Crunchy texture", "Popular snack"],
        tips=["Great as snack", "Try fresh from vendors", "Perfect for travel"],
        best_time_to_visit="Year-round",
        time_needed="Snack time",
        images=[],
        nearby_places=["kailali_banana_restaurant"],
        related_places=[],
        tags=["banana chips", "snack", "chips", "banana", "tikapur", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available as snack",
        phone=None,
        website=None,
        email=None,
        google_rating=4.4,
        tripadvisor_rating=4.2,
        keywords=["banana chips", "chips", "banana", "snack", "tikapur", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_food_banana_wine",
        name="Banana Wine/Brandy",
        name_nepali="केरा वाइन/ब्रान्डी",
        category=PlaceCategory.RESTAURANT,
        subcategories=["beverage", "alcoholic", "banana", "local"],
        description="""Banana Wine and Brandy are local alcoholic beverages brewed from bananas in Kailali District. These unique 
        drinks are made using traditional methods and local banana produce, creating distinctive flavors. The wine and brandy are 
        popular local beverages, especially in Tikapur where banana production is significant. They represent the innovative use 
        of local ingredients in beverage production and are part of the region's culinary culture. These beverages are typically 
        enjoyed during festivals and special occasions.""",
        short_description="Local alcoholic beverages brewed from bananas - unique regional drinks.",
        location=Location(latitude=28.5167, longitude=81.1167, address="Tikapur, Kailali District", area="Tikapur", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$$", notes="Available at local establishments"),
        highlights=["Banana-based", "Local production", "Traditional methods", "Unique flavors"],
        tips=["Try at local establishments", "Cultural beverage", "Festival drink"],
        best_time_to_visit="Year-round, especially festivals",
        time_needed="Drink time",
        images=[],
        nearby_places=["kailali_banana_restaurant"],
        related_places=[],
        tags=["banana wine", "banana brandy", "beverage", "alcoholic", "tikapur", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at local establishments",
        phone=None,
        website=None,
        email=None,
        google_rating=4.3,
        tripadvisor_rating=4.1,
        keywords=["banana wine", "banana brandy", "beverage", "tikapur", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_food_karnali_fish",
        name="Karnali Fish",
        name_nepali="कर्णाली माछा",
        category=PlaceCategory.RESTAURANT,
        subcategories=["seafood", "fish", "river", "chisapani"],
        description="""Karnali Fish is fresh river fish (fried) from Chisapani, Kailali District. This delicious seafood dish 
        features fresh fish caught from the Karnali River, prepared in traditional style. The fish is typically fried to perfection 
        and served with rice, vegetables, and spicy chutneys. Karnali Fish is a popular dish in the region, especially in 
        Chisapani where the Karnali Bridge is located. It's a must-try for seafood lovers and represents the fresh, local produce 
        available in the area.""",
        short_description="Fresh river fish (fried) from Chisapani - popular local seafood dish.",
        location=Location(latitude=28.4833, longitude=81.0833, address="Chisapani, Kailali District", area="Chisapani", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$$", notes="Available at riverside restaurants"),
        highlights=["Fresh river fish", "Karnali River", "Fried preparation", "Local seafood"],
        tips=["Try at riverside restaurants", "Best with rice", "Fresh catch"],
        best_time_to_visit="Year-round",
        time_needed="Meal time",
        images=[],
        nearby_places=["kailali_karnali_bridge"],
        related_places=[],
        tags=["karnali fish", "fish", "seafood", "river", "chisapani", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at restaurants",
        phone=None,
        website=None,
        email=None,
        google_rating=4.5,
        tripadvisor_rating=4.3,
        keywords=["karnali fish", "fish", "river fish", "chisapani", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_food_ghonghi_kailali",
        name="Ghonghi (Kailali Style)",
        name_nepali="घोङी (कैलाली शैली)",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "seafood", "water_snails", "spicy"],
        description="""Ghonghi in Kailali style often has a spicier, thinner gravy than the Dang version, a regional variation of 
        the traditional Tharu delicacy. This water snail dish is prepared with local spices and cooking techniques that give it a 
        distinctive Kailali flavor profile. The spicier, thinner gravy sets it apart from other regional preparations, making it a 
        unique culinary experience. Ghonghi is a must-try for those interested in regional variations of Tharu cuisine and 
        adventurous food lovers.""",
        short_description="Water snails in spicier, thinner gravy - Kailali style variation of traditional Tharu dish.",
        location=Location(latitude=28.6833, longitude=80.6167, address="Kailali District", area="Kailali", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$$", notes="Available at Tharu restaurants"),
        highlights=["Spicier gravy", "Kailali style", "Water snails", "Regional variation"],
        tips=["Try at authentic restaurants", "Spicier than Dang version", "Unique regional flavor"],
        best_time_to_visit="Year-round",
        time_needed="Meal time",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["ghonghi", "water snails", "tharu food", "kailali style", "spicy", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at restaurants",
        phone=None,
        website=None,
        email=None,
        google_rating=4.4,
        tripadvisor_rating=4.2,
        keywords=["ghonghi", "water snails", "kailali style", "tharu food", "spicy", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_food_poka",
        name="Poka",
        name_nepali="पोका",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "special", "fermented", "leaf_wrapped"],
        description="""Poka is a special Tharu dish (fermented/leaf-wrapped) unique to Kailali District. This traditional 
        preparation involves wrapping ingredients in leaves and fermenting them, creating a distinctive flavor profile. Poka is 
        a specialty dish that showcases the Tharu community's expertise in food preservation and fermentation techniques. The 
        dish has a unique taste and texture that comes from the fermentation process. It's a must-try for those interested in 
        traditional Tharu food preservation methods and unique culinary experiences.""",
        short_description="Special Tharu dish (fermented/leaf-wrapped) - unique traditional preparation.",
        location=Location(latitude=28.6833, longitude=80.6167, address="Kailali District", area="Kailali", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$$", notes="Specialty dish, available at select restaurants"),
        highlights=["Fermented preparation", "Leaf-wrapped", "Traditional method", "Unique flavor"],
        tips=["Try at authentic restaurants", "Unique taste", "Traditional preservation"],
        best_time_to_visit="Year-round",
        time_needed="Meal time",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["poka", "tharu food", "fermented", "leaf wrapped", "traditional", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at select restaurants",
        phone=None,
        website=None,
        email=None,
        google_rating=4.3,
        tripadvisor_rating=4.1,
        keywords=["poka", "tharu food", "fermented", "leaf wrapped", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_food_dhikri_kailali",
        name="Dhikri (Kailali Style)",
        name_nepali="ढिक्री (कैलाली शैली)",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "rice_cake", "far_west", "traditional"],
        description="""Dhikri in Kailali is shaped differently (often longer) in the Far-West compared to Dang, a regional variation 
        of the essential Tharu dish. This steamed rice flour cake maintains the traditional preparation but has a distinct shape 
        that reflects regional preferences. The longer shape is characteristic of the Far-West region and represents the local 
        culinary traditions. Dhikri is a staple of Tharu cuisine and is enjoyed throughout the region with regional variations.""",
        short_description="Steamed rice flour cakes shaped longer in Far-West style - regional Tharu dish variation.",
        location=Location(latitude=28.6833, longitude=80.6167, address="Kailali District", area="Kailali", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$", notes="Available at local restaurants"),
        highlights=["Longer shape", "Far-West style", "Regional variation", "Traditional Tharu dish"],
        tips=["Try with chutney", "Regional variation", "Essential Tharu cuisine"],
        best_time_to_visit="Year-round",
        time_needed="Meal time",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["dhikri", "rice cake", "tharu food", "far west", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at restaurants",
        phone=None,
        website=None,
        email=None,
        google_rating=4.4,
        tripadvisor_rating=4.2,
        keywords=["dhikri", "rice cake", "far west", "tharu food", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_food_sidhara_kailali",
        name="Sidhara (Kailali)",
        name_nepali="सिधारा (कैलाली)",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "fish", "dried", "staple"],
        description="""Sidhara is dried fish cake, a staple in Kailali Tharu households. This traditional preserved food is made 
        by drying fish and combining it with taro stems and spices, creating flavorful cakes that can be stored and used over time. 
        Sidhara is an essential part of Tharu cuisine in Kailali and is typically prepared as a curry or fried dish. It represents 
        the Tharu community's traditional food preservation techniques and is a must-try for those interested in authentic Tharu 
        preserved foods.""",
        short_description="Dried fish cake - staple in Kailali Tharu households, traditional preserved food.",
        location=Location(latitude=28.6833, longitude=80.6167, address="Kailali District", area="Kailali", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$$", notes="Staple preserved food"),
        highlights=["Dried fish", "Traditional preservation", "Tharu staple", "Preserved food"],
        tips=["Try at Tharu restaurants", "Traditional preparation", "Essential Tharu food"],
        best_time_to_visit="Year-round",
        time_needed="Meal time",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["sidhara", "fish cake", "dried fish", "tharu food", "staple", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at restaurants",
        phone=None,
        website=None,
        email=None,
        google_rating=4.3,
        tripadvisor_rating=4.1,
        keywords=["sidhara", "fish cake", "dried fish", "tharu food", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_food_khariya_kailali",
        name="Khariya (Kailali)",
        name_nepali="खरिया (कैलाली)",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "vegetable", "colocasia", "savory"],
        description="""Khariya in Kailali are savory rolls of colocasia leaves, a traditional Tharu vegetable preparation. This 
        dish involves stuffing colocasia leaves with lentils and spices, then rolling and preparing them in traditional style. 
        Khariya is a flavorful vegetable dish that showcases the Tharu community's expertise in using local ingredients. It's 
        typically served as a side dish or part of a larger meal and is enjoyed for its rich flavors and nutritional value.""",
        short_description="Savory rolls of colocasia leaves - traditional Tharu vegetable preparation.",
        location=Location(latitude=28.6833, longitude=80.6167, address="Kailali District", area="Kailali", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$", notes="Available at local restaurants"),
        highlights=["Colocasia leaves", "Savory rolls", "Traditional preparation", "Vegetable dish"],
        tips=["Try at Tharu restaurants", "Great as side dish", "Nutritious and flavorful"],
        best_time_to_visit="Year-round",
        time_needed="Meal time",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["khariya", "colocasia", "tharu food", "vegetable", "traditional", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at restaurants",
        phone=None,
        website=None,
        email=None,
        google_rating=4.3,
        tripadvisor_rating=4.1,
        keywords=["khariya", "colocasia", "tharu food", "vegetable", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_food_chichar_kailali",
        name="Chichar (Kailali)",
        name_nepali="चिचर (कैलाली)",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "rice", "sticky_rice", "traditional"],
        description="""Chichar is steamed sticky rice, a traditional Tharu dish in Kailali District. This special variety of rice 
        has a unique sticky texture and is prepared using traditional methods. Chichar is typically served with various curries, 
        pickles, or traditional accompaniments and is an essential part of Tharu cuisine. The dish holds cultural significance 
        in Tharu traditions and is enjoyed during festivals and daily meals alike.""",
        short_description="Steamed sticky rice - traditional Tharu dish, essential part of Kailali cuisine.",
        location=Location(latitude=28.6833, longitude=80.6167, address="Kailali District", area="Kailali", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$", notes="Available at restaurants"),
        highlights=["Sticky rice", "Traditional preparation", "Tharu staple", "Cultural significance"],
        tips=["Try with curries", "Essential Tharu dish", "Festival food"],
        best_time_to_visit="Year-round, especially festivals",
        time_needed="Meal time",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["chichar", "sticky rice", "tharu food", "traditional", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at restaurants",
        phone=None,
        website=None,
        email=None,
        google_rating=4.4,
        tripadvisor_rating=4.2,
        keywords=["chichar", "sticky rice", "tharu food", "traditional", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_food_duck_curry",
        name="Local Duck Curry (Hash ko Masu)",
        name_nepali="हाँस को मासु",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "meat", "duck", "curry", "popular"],
        description="""Local Duck Curry, known as Hash ko Masu, is very popular in Dhangadhi and rural areas of Kailali District. 
        This flavorful meat dish features duck prepared in a rich curry with local spices and herbs. The curry has a distinctive 
        flavor profile and is typically served with rice or traditional bread. Duck curry is a popular dish in the region, 
        especially in Dhangadhi where it's a local favorite. It's a must-try for meat lovers interested in regional Tharu 
        cuisine.""",
        short_description="Very popular duck curry in Dhangadhi and rural areas - local favorite meat dish.",
        location=Location(latitude=28.6833, longitude=80.6167, address="Dhangadhi, Kailali District", area="Dhangadhi", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$$", notes="Popular at local restaurants"),
        highlights=["Duck curry", "Popular dish", "Dhangadhi favorite", "Rich flavors"],
        tips=["Try in Dhangadhi", "Best with rice", "Local favorite"],
        best_time_to_visit="Year-round",
        time_needed="Meal time",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["duck curry", "hash ko masu", "meat", "curry", "dhangadhi", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at restaurants",
        phone=None,
        website=None,
        email=None,
        google_rating=4.5,
        tripadvisor_rating=4.3,
        keywords=["duck curry", "hash ko masu", "duck", "dhangadhi", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_food_gengta_crab",
        name="Gengta (Crab)",
        name_nepali="गेंगटा (कञ्चा)",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "seafood", "crab", "snack"],
        description="""Gengta (Crab) in Kailali is often fried crispy as a snack with drinks, a popular way to enjoy this seafood 
        delicacy. The crab is prepared by frying it to a crispy texture, making it perfect as a snack or appetizer. This 
        preparation style is popular in the region and is often enjoyed with local beverages. Gengta represents the Tharu 
        community's expertise in seafood preparation and is a must-try for seafood lovers.""",
        short_description="Crab fried crispy as a snack with drinks - popular seafood preparation in Kailali.",
        location=Location(latitude=28.6833, longitude=80.6167, address="Kailali District", area="Kailali", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$$", notes="Available as snack"),
        highlights=["Crispy fried crab", "Snack preparation", "Popular with drinks", "Seafood delicacy"],
        tips=["Great as snack", "Try with local beverages", "Crispy texture"],
        best_time_to_visit="Year-round",
        time_needed="Snack time",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["gengta", "crab", "snack", "seafood", "tharu food", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available as snack",
        phone=None,
        website=None,
        email=None,
        google_rating=4.4,
        tripadvisor_rating=4.2,
        keywords=["gengta", "crab", "snack", "seafood", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_food_sipi_kailali",
        name="Sipi (Kailali Style)",
        name_nepali="सिपी (कैलाली शैली)",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "seafood", "mussels", "mustard"],
        description="""Sipi (Mussels) in Kailali are cooked in a spicy mustard-based gravy, a regional variation of the traditional 
        Tharu seafood dish. This preparation style uses mustard as a key ingredient, creating a distinctive spicy and tangy 
        flavor profile. The mussels are cooked in this flavorful gravy, making it a delicious and unique seafood preparation. 
        This Kailali style sets it apart from other regional variations and is a must-try for seafood enthusiasts.""",
        short_description="Mussels cooked in spicy mustard-based gravy - Kailali style regional variation.",
        location=Location(latitude=28.6833, longitude=80.6167, address="Kailali District", area="Kailali", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$$", notes="Available at seafood restaurants"),
        highlights=["Mustard-based gravy", "Spicy preparation", "Kailali style", "Regional variation"],
        tips=["Try at seafood restaurants", "Spicy and tangy", "Unique regional flavor"],
        best_time_to_visit="Year-round",
        time_needed="Meal time",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["sipi", "mussels", "mustard gravy", "tharu food", "kailali style", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at restaurants",
        phone=None,
        website=None,
        email=None,
        google_rating=4.4,
        tripadvisor_rating=4.2,
        keywords=["sipi", "mussels", "mustard gravy", "tharu food", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_food_tharu_achar_kailali",
        name="Tharu Achar (Kailali)",
        name_nepali="थारू अचार (कैलाली)",
        category=PlaceCategory.RESTAURANT,
        subcategories=["tharu_food", "pickle", "fermented", "spicy"],
        description="""Tharu Achar in Kailali is spicy fermented radish or bamboo shoot pickle, a staple condiment in Tharu 
        households. This traditional pickle is made using fermentation techniques and local spices, creating a tangy, spicy 
        condiment. The pickle can be made from radish or bamboo shoots, both being popular in the region. Tharu Achar is an 
        essential part of Tharu cuisine and is typically served with meals to add flavor and spice. It's a must-try for those 
        interested in traditional Tharu condiments and preserved foods.""",
        short_description="Spicy fermented radish or bamboo shoot pickle - essential Tharu condiment in Kailali.",
        location=Location(latitude=28.6833, longitude=80.6167, address="Kailali District", area="Kailali", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$", notes="Available as condiment"),
        highlights=["Fermented pickle", "Radish or bamboo shoot", "Spicy and tangy", "Essential condiment"],
        tips=["Try with meals", "Essential Tharu condiment", "Various ingredients"],
        best_time_to_visit="Year-round",
        time_needed="Meal time",
        images=[],
        nearby_places=[],
        related_places=[],
        tags=["tharu achar", "pickle", "fermented", "radish", "bamboo shoot", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available as condiment",
        phone=None,
        website=None,
        email=None,
        google_rating=4.4,
        tripadvisor_rating=4.2,
        keywords=["tharu achar", "pickle", "fermented", "radish", "bamboo shoot", "kailali"]
    ),
    
    TourismPlace(
        id="kailali_food_banana_lassi",
        name="Banana Lassi",
        name_nepali="केरा लस्सी",
        category=PlaceCategory.RESTAURANT,
        subcategories=["beverage", "lassi", "banana", "tikapur"],
        description="""Banana Lassi is a rich, creamy drink found in Tikapur's banana restaurants in Kailali District. This 
        unique beverage combines the traditional lassi (yogurt-based drink) with local banana produce, creating a sweet and creamy 
        drink. Banana Lassi is a popular beverage in Tikapur where banana production is significant, and it's a perfect example of 
        innovative use of local ingredients. The drink is refreshing and makes for a great accompaniment to meals or as a standalone 
        beverage.""",
        short_description="Rich, creamy banana lassi found in Tikapur's banana restaurants - unique regional beverage.",
        location=Location(latitude=28.5167, longitude=81.1167, address="Tikapur, Kailali District", area="Tikapur", ward=None),
        opening_hours=OpeningHours(monday="All day", tuesday="All day", wednesday="All day", thursday="All day", friday="All day", saturday="All day", sunday="All day"),
        price_info=PriceInfo(currency="NPR", price_range="$", notes="Available at banana restaurants"),
        highlights=["Banana-based", "Rich and creamy", "Tikapur specialty", "Refreshing drink"],
        tips=["Try at Banana Restaurant", "Great with meals", "Refreshing beverage"],
        best_time_to_visit="Year-round",
        time_needed="Drink time",
        images=[],
        nearby_places=["kailali_banana_restaurant"],
        related_places=[],
        tags=["banana lassi", "lassi", "banana", "beverage", "tikapur", "kailali"],
        languages_spoken=["Nepali", "Tharu", "Hindi"],
        accessibility="Available at restaurants",
        phone=None,
        website=None,
        email=None,
        google_rating=4.5,
        tripadvisor_rating=4.3,
        keywords=["banana lassi", "lassi", "banana", "tikapur", "kailali", "beverage"]
    ),
]


# ============================================================================
# EMBEDDING FUNCTIONS
# ============================================================================

def create_embedding_text(place: TourismPlace) -> str:
    """
    Create a rich text representation for embedding generation.
    Combines all relevant fields for semantic search.
    """
    parts = [
        f"Name: {place.name}",
        f"Category: {place.category.value}",
        f"Location: {place.location.area}, {place.location.address}",
        f"Description: {place.description}",
        f"Highlights: {', '.join(place.highlights)}",
        f"Tags: {', '.join(place.tags)}",
        f"Keywords: {', '.join(place.keywords)}",
        f"Tips: {', '.join(place.tips)}",
    ]
    
    if place.best_time_to_visit:
        parts.append(f"Best time to visit: {place.best_time_to_visit}")
    
    if place.subcategories:
        parts.append(f"Subcategories: {', '.join(place.subcategories)}")
    
    return " ".join(parts)


def generate_embedding_openai(text: str, api_key: str) -> List[float]:
    """Generate embeddings using OpenAI's API."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text
        )
        return response.data[0].embedding
    except ImportError:
        print("Please install openai: pip install openai")
        raise


def generate_embedding_sentence_transformers(text: str, model_name: str = "all-MiniLM-L6-v2") -> List[float]:
    """Generate embeddings using Sentence Transformers (local, free)."""
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(model_name)
        embedding = model.encode(text)
        return embedding.tolist()
    except ImportError:
        print("Please install sentence-transformers: pip install sentence-transformers")
        raise


def generate_embedding_cohere(text: str, api_key: str) -> List[float]:
    """Generate embeddings using Cohere's API."""
    try:
        import cohere
        co = cohere.Client(api_key)
        response = co.embed(
            texts=[text],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings[0]
    except ImportError:
        print("Please install cohere: pip install cohere")
        raise


# ============================================================================
# VECTOR DATABASE FUNCTIONS
# ============================================================================

def prepare_pinecone_data(places: List[TourismPlace], embeddings: List[List[float]]) -> List[Dict]:
    """Prepare data for Pinecone vector database."""
    vectors = []
    for place, embedding in zip(places, embeddings):
        vectors.append({
            "id": place.id,
            "values": embedding,
            "metadata": {
                "name": place.name,
                "category": place.category.value,
                "area": place.location.area,
                "latitude": place.location.latitude,
                "longitude": place.location.longitude,
                "short_description": place.short_description,
                "tags": place.tags,
                "google_rating": place.google_rating,
                "time_needed": place.time_needed,
                "price_foreign": place.price_info.foreign_tourist if place.price_info else None,
            }
        })
    return vectors


def prepare_qdrant_data(places: List[TourismPlace], embeddings: List[List[float]]) -> List[Dict]:
    """Prepare data for Qdrant vector database."""
    points = []
    for i, (place, embedding) in enumerate(zip(places, embeddings)):
        points.append({
            "id": i,
            "vector": embedding,
            "payload": {
                "place_id": place.id,
                "name": place.name,
                "name_nepali": place.name_nepali,
                "category": place.category.value,
                "area": place.location.area,
                "latitude": place.location.latitude,
                "longitude": place.location.longitude,
                "description": place.description,
                "short_description": place.short_description,
                "highlights": place.highlights,
                "tips": place.tips,
                "tags": place.tags,
                "google_rating": place.google_rating,
                "time_needed": place.time_needed,
            }
        })
    return points


def prepare_chroma_data(places: List[TourismPlace], embeddings: List[List[float]]) -> Dict:
    """Prepare data for ChromaDB."""
    return {
        "ids": [place.id for place in places],
        "embeddings": embeddings,
        "metadatas": [
            {
                "name": place.name,
                "category": place.category.value,
                "area": place.location.area,
                "latitude": str(place.location.latitude),
                "longitude": str(place.location.longitude),
                "short_description": place.short_description,
                "tags": ",".join(place.tags),
            }
            for place in places
        ],
        "documents": [create_embedding_text(place) for place in places]
    }


def save_faiss_index(embeddings: List[List[float]], output_path: str = "tourism_index.faiss"):
    """Save embeddings to a FAISS index (local vector search)."""
    try:
        import faiss
        import numpy as np
        
        vectors = np.array(embeddings).astype('float32')
        dimension = vectors.shape[1]
        
        # Create index
        index = faiss.IndexFlatL2(dimension)
        index.add(vectors)
        
        # Save index
        faiss.write_index(index, output_path)
        print(f"FAISS index saved to {output_path}")
        return index
    except ImportError:
        print("Please install faiss: pip install faiss-cpu")
        raise


# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

def export_to_json(places: List[TourismPlace], output_path: str = "tourism_data.json"):
    """Export tourism data to JSON format."""
    data = []
    for place in places:
        place_dict = asdict(place)
        place_dict["category"] = place.category.value
        data.append(place_dict)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Exported {len(places)} places to {output_path}")


def export_embeddings_json(places: List[TourismPlace], embeddings: List[List[float]], 
                           output_path: str = "tourism_embeddings.json"):
    """Export places with their embeddings to JSON."""
    data = []
    for place, embedding in zip(places, embeddings):
        data.append({
            "id": place.id,
            "name": place.name,
            "embedding": embedding,
            "metadata": {
                "category": place.category.value,
                "area": place.location.area,
                "tags": place.tags
            }
        })
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    
    print(f"Exported embeddings to {output_path}")


# ============================================================================
# iOS SWIFT EXPORT
# ============================================================================

def export_for_ios_coreml(places: List[TourismPlace], embeddings: List[List[float]],
                          output_path: str = "TourismData.swift"):
    """Generate Swift code for iOS app with embedded data."""
    swift_code = '''
import Foundation
import CoreML

// Auto-generated tourism data for iOS app
// Generated by kathmandu_tourism_vectorizer.py

struct TourismPlace: Codable, Identifiable {
    let id: String
    let name: String
    let nameNepali: String?
    let category: String
    let shortDescription: String
    let latitude: Double
    let longitude: Double
    let area: String
    let tags: [String]
    let highlights: [String]
    let tips: [String]
    let googleRating: Double?
    let timeNeeded: String?
    let embedding: [Float]
}

class TourismDataManager {
    static let shared = TourismDataManager()
    
    lazy var places: [TourismPlace] = {
        return loadPlaces()
    }()
    
    private func loadPlaces() -> [TourismPlace] {
        // Load from bundled JSON
        guard let url = Bundle.main.url(forResource: "tourism_data", withExtension: "json"),
              let data = try? Data(contentsOf: url),
              let places = try? JSONDecoder().decode([TourismPlace].self, from: data) else {
            return []
        }
        return places
    }
    
    // Cosine similarity search
    func search(query embedding: [Float], topK: Int = 5) -> [TourismPlace] {
        let similarities = places.map { place -> (TourismPlace, Float) in
            let similarity = cosineSimilarity(embedding, place.embedding)
            return (place, similarity)
        }
        
        return similarities
            .sorted { $0.1 > $1.1 }
            .prefix(topK)
            .map { $0.0 }
    }
    
    private func cosineSimilarity(_ a: [Float], _ b: [Float]) -> Float {
        guard a.count == b.count else { return 0 }
        
        var dotProduct: Float = 0
        var normA: Float = 0
        var normB: Float = 0
        
        for i in 0..<a.count {
            dotProduct += a[i] * b[i]
            normA += a[i] * a[i]
            normB += b[i] * b[i]
        }
        
        let denominator = sqrt(normA) * sqrt(normB)
        return denominator > 0 ? dotProduct / denominator : 0
    }
    
    // Filter by category
    func places(inCategory category: String) -> [TourismPlace] {
        return places.filter { $0.category == category }
    }
    
    // Filter by area
    func places(inArea area: String) -> [TourismPlace] {
        return places.filter { $0.area == area }
    }
    
    // Find nearby places
    func nearbyPlaces(latitude: Double, longitude: Double, radiusKm: Double = 2.0) -> [TourismPlace] {
        return places.filter { place in
            let distance = haversineDistance(
                lat1: latitude, lon1: longitude,
                lat2: place.latitude, lon2: place.longitude
            )
            return distance <= radiusKm
        }
    }
    
    private func haversineDistance(lat1: Double, lon1: Double, lat2: Double, lon2: Double) -> Double {
        let R = 6371.0 // Earth's radius in km
        let dLat = (lat2 - lat1) * .pi / 180
        let dLon = (lon2 - lon1) * .pi / 180
        let a = sin(dLat/2) * sin(dLat/2) +
                cos(lat1 * .pi / 180) * cos(lat2 * .pi / 180) *
                sin(dLon/2) * sin(dLon/2)
        let c = 2 * atan2(sqrt(a), sqrt(1-a))
        return R * c
    }
}
'''
    
    with open(output_path, 'w') as f:
        f.write(swift_code)
    
    print(f"Generated iOS Swift file: {output_path}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function to process tourism data and generate embeddings."""
    print("=" * 60)
    print("Kathmandu Tourism Data Vectorizer")
    print("=" * 60)
    
    # Step 1: Export raw data to JSON
    print("\n[1/4] Exporting tourism data to JSON...")
    export_to_json(TOURISM_DATA, "tourism_data.json")
    
    # Step 2: Generate embeddings
    print("\n[2/4] Generating embeddings...")
    print(f"    Using provider: {EMBEDDING_PROVIDER}")
    print(f"    Number of places: {len(TOURISM_DATA)}")
    
    embeddings = []
    
    # Choose your embedding method (uncomment one):
    
    # Option A: Use Sentence Transformers (free, local)
    for place in TOURISM_DATA:
        text = create_embedding_text(place)
        embedding = generate_embedding_sentence_transformers(text)
        embeddings.append(embedding)
        print(f"    Generated embedding for: {place.name}")
    
    # Option B: Use OpenAI (requires API key)
    # import os
    # api_key = os.getenv("OPENAI_API_KEY")
    # for place in TOURISM_DATA:
    #     text = create_embedding_text(place)
    #     embedding = generate_embedding_openai(text, api_key)
    #     embeddings.append(embedding)
    #     print(f"    Generated embedding for: {place.name}")
    
    # Step 3: Export embeddings
    print("\n[3/4] Exporting embeddings...")
    export_embeddings_json(TOURISM_DATA, embeddings, "tourism_embeddings.json")
    
    # Step 4: Prepare for vector database
    print("\n[4/4] Preparing vector database data...")
    
    # Choose your vector DB format:
    pinecone_data = prepare_pinecone_data(TOURISM_DATA, embeddings)
    with open("pinecone_vectors.json", 'w') as f:
        json.dump(pinecone_data, f)
    print("    Saved Pinecone format: pinecone_vectors.json")
    
    qdrant_data = prepare_qdrant_data(TOURISM_DATA, embeddings)
    with open("qdrant_points.json", 'w') as f:
        json.dump(qdrant_data, f)
    print("    Saved Qdrant format: qdrant_points.json")
    
    chroma_data = prepare_chroma_data(TOURISM_DATA, embeddings)
    with open("chroma_data.json", 'w') as f:
        json.dump(chroma_data, f)
    print("    Saved ChromaDB format: chroma_data.json")
    
    # Save FAISS index
    try:
        save_faiss_index(embeddings, "tourism_index.faiss")
    except ImportError:
        print("    Skipping FAISS (not installed)")
    
    # Generate iOS Swift code
    export_for_ios_coreml(TOURISM_DATA, embeddings, "TourismData.swift")
    
    print("\n" + "=" * 60)
    print("DONE! Generated files:")
    print("  - tourism_data.json (raw data)")
    print("  - tourism_embeddings.json (data + embeddings)")
    print("  - pinecone_vectors.json (Pinecone format)")
    print("  - qdrant_points.json (Qdrant format)")
    print("  - chroma_data.json (ChromaDB format)")
    print("  - tourism_index.faiss (FAISS index)")
    print("  - TourismData.swift (iOS code)")
    print("=" * 60)


if __name__ == "__main__":
    main()