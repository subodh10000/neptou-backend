"""
Emergency Contacts Data
=======================
Emergency contact information for tourists in Nepal.
This data is used by RAG system to provide accurate emergency information.
"""
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class EmergencyContact:
    """Represents an emergency contact."""
    name: str
    phone: str
    category: str  # "police", "medical", "tourist", "embassy", "local_agent"
    location: str  # City or area
    description: str
    available_24_7: bool = False
    languages: List[str] = None
    additional_info: Optional[str] = None
    
    def __post_init__(self):
        if self.languages is None:
            self.languages = ["Nepali", "English"]

# Emergency Contacts Database
EMERGENCY_CONTACTS: List[EmergencyContact] = [
    # Neptou Emergency Agent
    EmergencyContact(
        name="Bibek KC",
        phone="98484488888",
        category="local_agent",
        location="Kathmandu",
        description="Neptou Emergency agent - Available for tourist assistance, emergency help, and local support in Kathmandu. Speaks Nepali and English.",
        available_24_7=True,
        languages=["Nepali", "English"],
        additional_info="Neptou's dedicated emergency contact for tourists. Can assist with directions, emergencies, translations, and local help."
    ),
    
    # Police & Security
    EmergencyContact(
        name="Police Emergency",
        phone="100",
        category="police",
        location="Nepal-wide",
        description="General police emergency number for all emergencies requiring police assistance.",
        available_24_7=True,
        languages=["Nepali", "English", "Hindi"]
    ),
    
    EmergencyContact(
        name="Tourist Police",
        phone="+977-1-4247041",
        category="tourist",
        location="Kathmandu",
        description="24/7 tourist police service. Specialized help for tourists with translation services and tourist-specific issues.",
        available_24_7=True,
        languages=["Nepali", "English", "Hindi", "Chinese"]
    ),
    
    # Medical
    EmergencyContact(
        name="Ambulance",
        phone="102",
        category="medical",
        location="Nepal-wide",
        description="Medical emergency ambulance service. Call for medical emergencies requiring immediate transport to hospital.",
        available_24_7=True,
        languages=["Nepali", "English"]
    ),
    
    EmergencyContact(
        name="CIWEC Clinic",
        phone="+977-1-4424111",
        category="medical",
        location="Kathmandu",
        description="Travel medicine clinic specializing in travel-related health issues, vaccinations, and altitude sickness treatment.",
        available_24_7=False,
        languages=["Nepali", "English"],
        additional_info="Open 9 AM - 5 PM. Best for travel health consultations."
    ),
    
    EmergencyContact(
        name="Norvic International Hospital",
        phone="+977-1-5970123",
        category="medical",
        location="Kathmandu",
        description="International standard hospital with 24/7 emergency services. English-speaking staff available.",
        available_24_7=True,
        languages=["Nepali", "English"]
    ),
    
    # Fire & Other
    EmergencyContact(
        name="Fire Department",
        phone="101",
        category="fire",
        location="Nepal-wide",
        description="Fire emergency service. Call for fire emergencies.",
        available_24_7=True,
        languages=["Nepali", "English"]
    ),
    
    # Tourism Board
    EmergencyContact(
        name="Nepal Tourism Board",
        phone="+977-1-4256909",
        category="tourist",
        location="Kathmandu",
        description="Official tourism board. Information about tourism, permits, and general tourist assistance.",
        available_24_7=False,
        languages=["Nepali", "English"],
        additional_info="Open 9 AM - 5 PM, Sunday-Friday"
    ),
    
    # Embassies (Major ones)
    EmergencyContact(
        name="US Embassy",
        phone="+977-1-4234000",
        category="embassy",
        location="Kathmandu",
        description="US Embassy in Kathmandu. Emergency assistance for US citizens.",
        available_24_7=True,
        languages=["English", "Nepali"]
    ),
    
    EmergencyContact(
        name="UK Embassy",
        phone="+977-1-4410583",
        category="embassy",
        location="Kathmandu",
        description="British Embassy in Kathmandu. Emergency assistance for UK citizens.",
        available_24_7=True,
        languages=["English", "Nepali"]
    ),
    
    EmergencyContact(
        name="Indian Embassy",
        phone="+977-1-4410900",
        category="embassy",
        location="Kathmandu",
        description="Indian Embassy in Kathmandu. Emergency assistance for Indian citizens.",
        available_24_7=True,
        languages=["Hindi", "English", "Nepali"]
    ),
    
    EmergencyContact(
        name="Chinese Embassy",
        phone="+977-1-4411740",
        category="embassy",
        location="Kathmandu",
        description="Chinese Embassy in Kathmandu. Emergency assistance for Chinese citizens.",
        available_24_7=True,
        languages=["Chinese", "English", "Nepali"]
    ),
]

def get_emergency_contacts_by_location(location: str = None) -> List[EmergencyContact]:
    """
    Get emergency contacts filtered by location.
    
    Args:
        location: City name (e.g., "Kathmandu") or None for all
    
    Returns:
        List of emergency contacts
    """
    if location:
        location_lower = location.lower()
        return [
            contact for contact in EMERGENCY_CONTACTS
            if location_lower in contact.location.lower()
        ]
    return EMERGENCY_CONTACTS

def get_emergency_contacts_by_category(category: str) -> List[EmergencyContact]:
    """
    Get emergency contacts by category.
    
    Args:
        category: Category like "police", "medical", "tourist", "embassy", "local_agent"
    
    Returns:
        List of emergency contacts
    """
    return [
        contact for contact in EMERGENCY_CONTACTS
        if contact.category == category
    ]

def format_emergency_contacts_for_llm(contacts: List[EmergencyContact], max_contacts: int = 10) -> str:
    """
    Format emergency contacts for LLM context.
    Prioritizes Bibek KC and makes him prominent.
    
    Args:
        contacts: List of emergency contacts
        max_contacts: Maximum number of contacts to include
    
    Returns:
        Formatted string for LLM
    """
    if not contacts:
        return ""
    
    # Separate Bibek KC from others
    bibek_contacts = [c for c in contacts if "bibek" in c.name.lower()]
    other_contacts = [c for c in contacts if "bibek" not in c.name.lower()]
    
    # Reorder: Bibek KC first, then others
    prioritized_contacts = bibek_contacts + other_contacts
    
    context_parts = ["\n[EMERGENCY CONTACTS - VERIFIED INFORMATION]"]
    
    for contact in prioritized_contacts[:max_contacts]:
        # Special formatting for Bibek KC
        if "bibek" in contact.name.lower():
            context_parts.append(f"\n⭐ {contact.name} - NEPTOU EMERGENCY AGENT (RECOMMENDED FIRST)")
            context_parts.append(f"📞 PHONE NUMBER: {contact.phone} (CRITICAL - ALWAYS INCLUDE THIS NUMBER)")
            context_parts.append(f"Category: {contact.category}")
            context_parts.append(f"Location: {contact.location}")
            context_parts.append(f"Description: {contact.description}")
            context_parts.append("Available: 24/7")
            context_parts.append("IMPORTANT: Bibek KC is Neptou's dedicated emergency agent. He can help with lost passports, emergencies, translations, local support, and tourist assistance.")
            if contact.languages:
                context_parts.append(f"Languages: {', '.join(contact.languages)}")
            if contact.additional_info:
                context_parts.append(f"Additional Info: {contact.additional_info}")
        else:
            context_parts.append(f"\n{contact.name}")
            context_parts.append(f"📞 PHONE NUMBER: {contact.phone} (CRITICAL - ALWAYS INCLUDE THIS NUMBER)")
            context_parts.append(f"Category: {contact.category}")
            context_parts.append(f"Location: {contact.location}")
            context_parts.append(f"Description: {contact.description}")
            if contact.available_24_7:
                context_parts.append("Available: 24/7")
            if contact.languages:
                context_parts.append(f"Languages: {', '.join(contact.languages)}")
            if contact.additional_info:
                context_parts.append(f"Additional Info: {contact.additional_info}")
        context_parts.append("")
    
    return "\n".join(context_parts)

def search_emergency_contacts(query: str) -> List[EmergencyContact]:
    """
    Search emergency contacts by query text.
    
    Args:
        query: Search query (e.g., "emergency kathmandu", "police", "medical")
    
    Returns:
        List of matching emergency contacts
    """
    query_lower = query.lower()
    results = []
    
    for contact in EMERGENCY_CONTACTS:
        score = 0
        
        # Check name
        if query_lower in contact.name.lower():
            score += 3
        
        # Check location
        if query_lower in contact.location.lower() or "kathmandu" in query_lower:
            score += 2
        
        # Check category
        if query_lower in contact.category or any(keyword in query_lower for keyword in ["police", "medical", "ambulance", "fire", "embassy", "tourist"]):
            score += 2
        
        # Check description
        if query_lower in contact.description.lower():
            score += 1
        
        # Special handling for "bibek" or "neptou" - HIGH PRIORITY
        if "bibek" in query_lower or "neptou" in query_lower or "local agent" in query_lower:
            if contact.category == "local_agent" or "bibek" in contact.name.lower():
                score += 10  # Very high priority
        
        # Boost score for lost passport, help, assistance queries - Bibek KC should be prioritized
        if any(keyword in query_lower for keyword in ["lost", "passport", "help", "assistance", "support", "need"]) and contact.category == "local_agent":
            score += 8  # High priority for Bibek KC
        
        # Boost score for Kathmandu emergency queries
        if ("kathmandu" in query_lower or "emergency" in query_lower) and contact.category == "local_agent":
            score += 5
        
        # Boost for embassy-related queries (lost passport) - but still prioritize Bibek KC
        if ("passport" in query_lower or "embassy" in query_lower) and contact.category == "local_agent":
            score += 7  # High priority - Bibek can help with passport issues
        
        if score > 0:
            results.append((score, contact))
    
    # Sort by score and return contacts
    results.sort(key=lambda x: x[0], reverse=True)
    return [contact for _, contact in results]
