"""
Generate embeddings for emergency contacts
==========================================
Creates vector embeddings for emergency contacts to enable semantic search.
"""
import json
from sentence_transformers import SentenceTransformer
from emergency_contacts import EMERGENCY_CONTACTS

def create_emergency_contact_text(contact) -> str:
    """Create text representation for embedding."""
    parts = [
        f"Name: {contact.name}",
        f"Phone: {contact.phone}",
        f"Category: {contact.category}",
        f"Location: {contact.location}",
        f"Description: {contact.description}",
    ]
    
    if contact.available_24_7:
        parts.append("Available 24/7")
    
    if contact.languages:
        parts.append(f"Languages: {', '.join(contact.languages)}")
    
    if contact.additional_info:
        parts.append(f"Additional: {contact.additional_info}")
    
    return " ".join(parts)

def generate_emergency_embeddings():
    """Generate embeddings for all emergency contacts."""
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    embeddings_data = []
    
    for contact in EMERGENCY_CONTACTS:
        text = create_emergency_contact_text(contact)
        embedding = model.encode(text, convert_to_numpy=True)
        
        embeddings_data.append({
            "name": contact.name,
            "phone": contact.phone,
            "category": contact.category,
            "location": contact.location,
            "description": contact.description,
            "available_24_7": contact.available_24_7,
            "languages": contact.languages,
            "additional_info": contact.additional_info,
            "embedding": embedding.tolist()
        })
    
    # Save to JSON
    with open("emergency_contacts_embeddings.json", "w", encoding="utf-8") as f:
        json.dump(embeddings_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generated embeddings for {len(embeddings_data)} emergency contacts")
    print(f"   Saved to: emergency_contacts_embeddings.json")
    
    return embeddings_data

if __name__ == "__main__":
    generate_emergency_embeddings()
