# neptou-backend/knowledge_base.py

NEPAL_KNOWLEDGE = {
    "kathmandu": {
        "description": "The capital city, a living museum of temples and courtyards.",
        "highlights": ["Swayambhunath", "Pashupatinath", "Boudhanath", "Durbar Squares"],
        "food": ["Newari Khaja Set", "Juju Dhau", "Yomari"],
        "hidden_gems": ["Garden of Dreams", "Kopan Monastery"]
    },
    "pokhara": {
        "description": "The city of lakes and the gateway to the Annapurna circuit.",
        "highlights": ["Phewa Lake", "Sarangkot", "World Peace Pagoda"],
        "food": ["Thakali Set", "Fresh Lake Fish"],
        "hidden_gems": ["Begnas Lake", "Methlang"]
    },
    "lalitpur": {
        "description": "Historically known as Patan, the city of fine arts.",
        "highlights": ["Patan Durbar Square", "Krishna Mandir", "Golden Temple"],
        "food": ["Wo (Lentil Patties)", "Chatamari"],
        "hidden_gems": ["Pimbahal Pond", "Mahabouddha Temple"]
    },
    "bhaktapur": {
        "description": "The city of devotees, preserved in its medieval form.",
        "highlights": ["Nyatapola Temple", "55 Window Palace", "Pottery Square"],
        "food": ["Juju Dhau (King Curd)", "Bara"],
        "hidden_gems": ["Siddha Pokhari", "Dattatreya Square"]
    },
    "dang": {
        "description": "The largest inner valley of Asia, rich in Tharu culture. Located in the Terai region, Dang is known for its fertile plains, traditional Tharu villages, and unique cultural heritage.",
        "highlights": ["Dharapani (World's tallest Trishul)", "Jakhera Lake", "Tharu Cultural Museum", "Rapti River", "Salyan Gadhi", "Bageshwori Temple"],
        "food": ["Dhikri (steamed rice flour rolls)", "Ghonghi (snail curry)", "Anadi Rice (red rice)", "Sidhara (dried fish curry)", "Bhakka (rice flour dumplings)", "Gundruk (fermented leafy greens)", "Masaura (dried lentil balls)", "Tharu Thali (traditional platter)", "Bhatmas (soybean curry)", "Kachila (raw minced meat)"],
        "hidden_gems": ["Chamera Gupha (Bat Cave)", "Purandhara Waterfall", "Rani Tal (Queen's Pond)", "Dang Valley Viewpoint", "Tharu Homestays", "Salyan Gadhi Fort"]
    },
    "kailali": {
        "description": "The gateway to Far-West Nepal, known for Tikapur Park and Tharu heritage.",
        "highlights": ["Tikapur Great Garden", "Karnali Bridge", "Dolphin Conservation Area"],
        "food": ["Tharu Cuisine", "Local Fish"],
        "hidden_gems": ["Ghodaghodi Lake (Wetland)", "Mohana River Corridor"]
    }
}

def get_city_context(city_names: list[str]) -> str:
    """
    Builds a text summary of the requested cities to feed into the AI.
    """
    context_text = ""
    for city in city_names:
        city_key = city.lower().strip()
        if city_key in NEPAL_KNOWLEDGE:
            data = NEPAL_KNOWLEDGE[city_key]
            context_text += f"\n[FACTS ABOUT {city.upper()}]\n"
            context_text += f"Description: {data['description']}\n"
            context_text += f"Top Highlights: {', '.join(data['highlights'])}\n"
            context_text += f"Must-Try Food: {', '.join(data['food'])}\n"
            context_text += f"Hidden Gems: {', '.join(data['hidden_gems'])}\n"
            
    return context_text