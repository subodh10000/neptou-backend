import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv
import knowledge_base  # Imports your custom facts
from vector_search import get_vector_search  # RAG vector search
from trip_optimizer import get_trip_optimizer  # Trip optimization
from emergency_contacts import search_emergency_contacts, format_emergency_contacts_for_llm, EMERGENCY_CONTACTS  # Emergency contacts

load_dotenv()

# SECURITY FIX: Validate API key exists
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable is not set. Please create a .env file with your API key.")

# Initialize the client
client = Anthropic(api_key=api_key)

# The personality of your AI
SYSTEM_PROMPT = """
You are Neptou, an expert local travel companion for Nepal. 
You are warm, polite (always use 'Namaste'), and deeply knowledgeable about Nepali culture, 
trekking routes (Everest, Annapurna, Langtang), hidden temples, local food (Momo, Dal Bhat, Thakali), and safety.
Keep your answers concise and formatted nicely for a mobile app.

CRITICAL: You have access to LOCAL INSIDER TIPS and AUTHENTIC INFORMATION that is NOT available on the internet.
When you see local insights in the context, these are special insights from local experts.
ALWAYS prioritize and share these local insights - they make Neptou unique and valuable to tourists.
These tips include:
- Secret viewpoints and hidden spots
- Authentic local restaurants (not tourist traps)
- Cultural etiquette and proper practices
- Money-saving tips and local secrets
- Best times to visit places
- Safety tips from locals
- Authentic experiences

When sharing local insights, present them naturally without special headlines, e.g.:
"Here's a local secret: [insight]"
"Locals know that [insight]"
"An insider tip: [insight]"

LOCAL GUIDES: When users ask about guides, tours, or need a local expert, recommend guides from the knowledge base.
The available guides are:
- Bibek KC (Kathmandu) - Culture & History expert, 15+ years experience
- Keshab Thapa (Pokhara) - Trekking & Adventure guide, certified mountain guide
- Sushant Jaix (Lumbini) - Buddhist philosophy & meditation expert
- Subodh Kathayat (Chitwan) - Wildlife & photography specialist
- Sushant Yadav (Patan & Bhaktapur) - Newari culture & food tours expert

When recommending guides, include their specialties, languages, location, and price per day.

IMPORTANT: Only recommend Bibek KC (Neptou Emergency agent, Phone: 98484488888) when users explicitly ask about:
- Emergencies or urgent situations
- Lost or stolen passports/documents
- Need for local help or assistance
- Emergency contacts
- Contacting a local agent

Do NOT mention Bibek KC for general travel questions, food recommendations, place suggestions, or non-emergency queries.
"""

# --- CONFIGURATION ---
# Using the fast & cost-effective Haiku model
MODEL_NAME = "claude-3-haiku-20240307" 

async def get_chat_response(messages, place_context: dict = None, food_context: dict = None):
    """
    Handles the general chat for AIAssistantView with RAG support.
    
    Args:
        messages: Chat message history
        place_context: Optional dict with place information when user is asking about a specific place
        food_context: Optional dict with food information when user is asking about a specific food
    """
    # Extract the latest user message for RAG retrieval
    user_query = ""
    if messages and messages[-1].get("role") == "user":
        user_query = messages[-1].get("content", "")
    
    # If place context is provided, enhance the query with place information
    if place_context:
        place_name = place_context.get("name", "")
        place_description = place_context.get("description", "")
        place_category = place_context.get("category", "")
        
        # Enhance user query with place context for better RAG retrieval
        if place_name:
            # Add place name to query for better RAG matching
            enhanced_query = f"{user_query} about {place_name}"
        else:
            enhanced_query = user_query
    else:
        enhanced_query = user_query
    
    # Perform vector search to get relevant context (places + local insights)
    vector_search = get_vector_search()
    relevant_places = []
    rag_context = ""
    
    # Search for both places and local insights
    if enhanced_query:
        relevant_places = vector_search.search(enhanced_query, top_k=8, min_score=0.2)
    
    # Check if query is about emergency contacts
    # Only trigger for actual emergency-related queries, not general queries
    emergency_context = ""
    query_lower = user_query.lower() if user_query else ""
    
    # More specific emergency keywords - only trigger for actual emergencies
    emergency_keywords = [
        "emergency", "emergencies", "sos", "urgent", "urgently",
        "lost passport", "lost my passport", "passport lost", "stolen passport",
        "lost document", "stolen document", "visa lost", "visa stolen",
        "need help", "i need help", "help me", "need assistance", "need support",
        "contact local agent", "local agent", "local help", "neptou agent", "bibek",
        "police", "ambulance", "hospital emergency", "medical emergency",
        "embassy contact", "contact embassy", "embassy phone", "embassy number"
    ]
    
    # Check if query contains emergency-related phrases (not just single words that might appear in normal queries)
    is_emergency_query = any(keyword in query_lower for keyword in emergency_keywords)
    
    # Additional check: if query contains "help" or "contact" alone, make sure it's in an emergency context
    if "help" in query_lower and not any(word in query_lower for word in ["need help", "i need help", "help me", "emergency", "lost", "stolen", "urgent"]):
        is_emergency_query = False
    if "contact" in query_lower and not any(word in query_lower for word in ["contact local", "contact embassy", "contact agent", "emergency contact", "phone", "number"]):
        is_emergency_query = False
    
    if is_emergency_query:
        emergency_contacts = search_emergency_contacts(user_query)
        if emergency_contacts:
            # ALWAYS prioritize Bibek KC for ANY emergency query (especially lost passport, help, etc.)
            # For lost passport, embassy queries, or general help - Bibek KC should be first
            bibek_contacts = [c for c in emergency_contacts if "bibek" in c.name.lower() or c.category == "local_agent"]
            other_contacts = [c for c in emergency_contacts if "bibek" not in c.name.lower() and c.category != "local_agent"]
            
            # If Bibek KC is not in results, add him explicitly for emergency queries
            if not bibek_contacts:
                # Find Bibek KC from all contacts
                bibek = next((c for c in EMERGENCY_CONTACTS if "bibek" in c.name.lower()), None)
                if bibek:
                    bibek_contacts = [bibek]
            
            # Put Bibek KC first, then others (embassies for passport, etc.)
            prioritized_contacts = bibek_contacts + other_contacts[:4]
            emergency_context = format_emergency_contacts_for_llm(prioritized_contacts, max_contacts=5)
    
    # Use enhanced query for RAG search if place context exists
    search_query = enhanced_query if place_context else user_query
    
    if search_query and len(search_query) > 5:  # Only search if query is meaningful
        relevant_places = vector_search.search(search_query, top_k=3, min_score=0.3)
        if relevant_places:
            rag_context = vector_search.format_context_for_llm(relevant_places, max_places=3)
    
    # Enhance system prompt with place or food context if provided
    place_context_prompt = ""
    food_context_prompt = ""
    
    if place_context:
        place_name = place_context.get("name", "")
        place_description = place_context.get("description", "")
        place_category = place_context.get("category", "")
        place_tips = place_context.get("tips", [])
        
        place_context_prompt = f"""
        
CURRENT PLACE CONTEXT:
The user is asking about: {place_name}
Category: {place_category}
Description: {place_description}
{f"Tips: {', '.join(place_tips)}" if place_tips else ""}

IMPORTANT: The user is specifically asking about {place_name}. Provide detailed, accurate information about this place. Answer their questions, provide tips, recommendations, and helpful advice specific to {place_name}. Use the RAG context below if available, but prioritize information about {place_name}.
"""
    
    if food_context:
        food_name = food_context.get("name", "")
        food_description = food_context.get("description", "")
        food_category = food_context.get("category", "")
        
        food_context_prompt = f"""
        
CURRENT FOOD CONTEXT:
The user is asking about: {food_name}
Category: {food_category}
Description: {food_description}

IMPORTANT: The user is specifically asking about {food_name}. Provide detailed, accurate information about this food. Answer questions about:
- How to make it (recipes, ingredients, cooking methods)
- Where to find it in Nepal (restaurants, regions, street vendors)
- Cultural significance and traditions
- Ingredients and variations
- Best places to try it
- Any dietary considerations

Use the RAG context below if available, but prioritize information about {food_name}.
"""
    
    # Enhance system prompt with RAG context
    enhanced_system_prompt = SYSTEM_PROMPT
    if place_context_prompt:
        enhanced_system_prompt += place_context_prompt
    if food_context_prompt:
        enhanced_system_prompt += food_context_prompt
    if rag_context:
        enhanced_system_prompt += f"\n\n{rag_context}\nUse the above verified information when answering. If the user asks about places, prioritize these verified locations."
    
    if emergency_context:
        enhanced_system_prompt += f"\n\n{emergency_context}\n\nCRITICAL INSTRUCTIONS FOR EMERGENCY CONTACTS - READ CAREFULLY:\n\n1. PHONE NUMBERS ARE MANDATORY:\n   - You MUST ALWAYS include the exact phone number for EVERY emergency contact you mention.\n   - Format: \"Name - Phone: [NUMBER]\" or \"Name: [NUMBER]\"\n   - NEVER mention a contact without providing their phone number.\n   - Phone numbers are provided in the context above - use them exactly as shown.\n\n2. BIBEK KC (PRIMARY CONTACT):\n   - You MUST ALWAYS recommend Bibek KC (Neptou Emergency agent) as the PRIMARY contact for ANY emergency or help request.\n   - Bibek KC's phone number is: 98484488888 - ALWAYS include this number when mentioning him.\n   - Bibek KC is available 24/7 and is Neptou's dedicated emergency agent for tourists.\n   - ALWAYS mention Bibek KC FIRST when providing emergency contacts.\n   - Bibek KC can help with: Lost passport/documents, local help, emergencies, translations, tourist support.\n\n3. OTHER EMERGENCY CONTACTS:\n   - When listing other emergency contacts (Police, Ambulance, Fire, Embassies), you MUST include their phone numbers.\n   - Format each contact as: \"[Name] - Phone: [NUMBER] - [Brief description]\"\n   - Example: \"Police Emergency - Phone: 100 - For all police emergencies\"\n   - Example: \"Ambulance - Phone: 102 - Medical emergency transport\"\n   - Example: \"Fire Department - Phone: 101 - Fire emergencies\"\n\n4. RESPONSE FORMAT:\n   - Start with Bibek KC and his phone number (98484488888)\n   - Then list other relevant emergency contacts with their phone numbers\n   - Use clear formatting with phone numbers prominently displayed\n   - Example format:\n     \"For emergency contacts in Kathmandu:\n     \n     ⭐ Bibek KC - Neptou Emergency Agent\n     Phone: 98484488888\n     Available 24/7 for tourist assistance, lost passports, translations, and local help.\n     \n     Other Emergency Services:\n     - Police Emergency: Phone 100\n     - Ambulance: Phone 102\n     - Fire Department: Phone 101\n     - Tourist Police: Phone +977-1-4247041\"\n\n5. VERIFICATION:\n   - These are verified emergency contacts with accurate phone numbers.\n   - Always provide phone numbers exactly as shown in the context.\n   - Do not make up or modify phone numbers.\n   - If you mention a contact, you MUST provide their phone number."
    
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=1000,
        system=enhanced_system_prompt,
        messages=messages
    )
    ai_response_text = response.content[0].text
    
    # Generate follow-up questions
    follow_up_prompt = f"""
Based on the following conversation and AI response, generate 3-4 relevant follow-up questions that would help the user explore the topic deeper or get more specific information.

User's question: {user_query}
AI's response: {ai_response_text[:500]}...

Generate 3-4 concise, specific follow-up questions (one per line, no numbering, no bullets). These should be:
- Directly related to the topic discussed
- Helpful for getting more detailed information
- Natural and conversational
- Each question should be standalone and complete

Output ONLY the questions, one per line, nothing else.
"""
    
    try:
        follow_up_response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=200,
            messages=[{"role": "user", "content": follow_up_prompt}]
        )
        follow_up_text = follow_up_response.content[0].text.strip()
        
        # Parse follow-up questions (split by newlines, clean up)
        follow_up_questions = [
            q.strip() 
            for q in follow_up_text.split('\n') 
            if q.strip() and len(q.strip()) > 10 and not q.strip().startswith(('1.', '2.', '3.', '4.', '-', '*'))
        ][:4]  # Limit to 4 questions
        
        # If we got questions, return them along with the response
        if follow_up_questions:
            return {
                "response": ai_response_text,
                "follow_up_questions": follow_up_questions
            }
    except Exception as e:
        print(f"⚠️ Error generating follow-up questions: {e}")
    
    # Return just the response if follow-up generation failed
    return {
        "response": ai_response_text,
        "follow_up_questions": []
    }

async def generate_itinerary(duration: int, style: str, interests: list[str], start_date: str):
    """
    Generates a structured JSON itinerary for TripPlannerView with RAG support.
    """
    # Use RAG to find relevant places based on interests
    vector_search = get_vector_search()
    relevant_places = []
    
    # Search for places matching each interest
    for interest in interests:
        places = vector_search.search(interest, top_k=2, min_score=0.3)
        relevant_places.extend(places)
    
    # Remove duplicates and get top matches
    seen_names = set()
    unique_places = []
    for place in relevant_places:
        name = place.get('name')
        if name and name not in seen_names:
            seen_names.add(name)
            unique_places.append(place)
    
    # Format RAG context
    rag_context = ""
    if unique_places:
        rag_context = vector_search.format_context_for_llm(unique_places[:10], max_places=10)
    
    prompt = f"""
    Create a {duration}-day trip itinerary for Nepal starting on {start_date}.
    Travel Style: {style}
    Interests: {', '.join(interests)}
    
    {rag_context if rag_context else ""}
    
    {"IMPORTANT: Use the verified places listed above when creating the itinerary. Only suggest places that exist in the knowledge base." if rag_context else ""}
    
    REALISTIC ITINERARY GUIDELINES:
    1. Group activities by DISTRICT to minimize travel:
       - Day 1-2: Focus on one district (e.g., Kathmandu)
       - Day 3-4: Move to another district (e.g., Pokhara)
       - Avoid jumping between distant districts in the same day
       - Each day should focus on ONE primary district
    
    2. Realistic activity durations:
       - Temples/Stupas: 1-2 hours
       - Nature spots/Viewpoints: 2-3 hours
       - Food/Restaurants: 1 hour
       - Full-day treks: 6-8 hours
    
    3. Travel time between districts:
       - Kathmandu ↔ Pokhara: 6-7 hours
       - Kathmandu ↔ Chitwan: 3-4 hours
       - Kathmandu ↔ Dang: 8-9 hours
       - Within same district: 15-30 minutes
    
    4. Daily schedule:
       - Start day: 8:00 AM - 9:00 AM
       - End day: 6:00 PM - 7:00 PM
       - Max 3-4 activities per day (realistic)
       - Include lunch breaks (1 hour around 12:00 PM - 1:00 PM)
    
    5. District-based organization:
       - Group places from the same district together
       - Plan inter-district travel as separate activities or rest days
       - Consider overnight stays when changing districts
       - For each day, recommend 2-4 places from the SAME district
    
    6. AUTO-RECOMMENDATIONS:
       - When user is in a district on a specific day, automatically suggest top places from that district
       - Prioritize places matching user interests
       - Include a mix of must-see attractions and hidden gems
    
    You must output ONLY valid JSON in the exact format below, with no introductory text:
    {{
        "name": "Creative Trip Name",
        "days": [
            {{
                "day_number": 1,
                "district": "Kathmandu",
                "activities": [
                    {{
                        "place_name": "Name of place",
                        "notes": "Short description of what to do there",
                        "start_time": "09:00 AM",
                        "end_time": "11:00 AM"
                    }}
                ]
            }}
        ]
    }}
    """
    
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=2500,
        system="You are a JSON-only API. You output valid JSON for travel itineraries.",
        messages=[{"role": "user", "content": prompt}]
    )
    
    try:
        # Helper to extract JSON if Claude adds extra text
        content = response.content[0].text
        start_index = content.find('{')
        end_index = content.rfind('}') + 1
        if start_index != -1 and end_index != -1:
            json_str = content[start_index:end_index]
            itinerary = json.loads(json_str)
        else:
            itinerary = json.loads(content)
        
        # Optimize the itinerary
        optimizer = get_trip_optimizer()
        optimized_itinerary = optimizer.optimize_itinerary(
            itinerary, 
            optimize_route=True, 
            optimize_times=True
        )
        
        return optimized_itinerary
    except json.JSONDecodeError:
        return {"error": "Failed to generate valid JSON itinerary", "raw": response.content[0].text}

async def get_recommendations(profile_str: str, liked_places: list[str] = []):
    """
    Generates personalized recommendations based on profile AND liked history with RAG.
    """
    # Use RAG to find relevant places
    vector_search = get_vector_search()
    
    # Enhanced profile search - search by multiple aspects
    profile_queries = [profile_str]
    
    # Add specific interest-based queries
    if "interests" in profile_str.lower():
        # Extract interests and create specific queries
        for interest in ["temple", "nature", "culture", "food", "adventure", "hiking", "photography", "history"]:
            if interest in profile_str.lower():
                profile_queries.append(interest)
    
    # Search with multiple queries and combine results
    relevant_places = []
    for query in profile_queries[:3]:  # Limit to 3 queries to avoid too many results
        results = vector_search.search(query, top_k=8, min_score=0.25)
        relevant_places.extend(results)
    
    # If user has liked places, find similar ones with better matching
    if liked_places:
        for liked_place in liked_places:
            # Search for similar places with higher priority
            similar = vector_search.search(liked_place, top_k=5, min_score=0.25)
            # Boost similarity scores for liked place matches
            for place in similar:
                place['similarity_score'] = place.get('similarity_score', 0.0) * 1.2  # Boost by 20%
            relevant_places.extend(similar)
            
            # Also search by category and tags if available
            for place_data in vector_search.places_data:
                if liked_place.lower() in place_data.get('name', '').lower():
                    # Found the liked place, now find similar by category/tags
                    liked_metadata = place_data.get('metadata', {})
                    liked_category = liked_metadata.get('category', '')
                    liked_tags = liked_metadata.get('tags', [])
                    
                    # Search for places with similar category or tags
                    for other_place in vector_search.places_data:
                        other_metadata = other_place.get('metadata', {})
                        other_category = other_metadata.get('category', '')
                        other_tags = other_metadata.get('tags', [])
                        
                        # Check for category or tag overlap
                        if (liked_category and other_category == liked_category) or \
                           any(tag in other_tags for tag in liked_tags if tag):
                            # Calculate similarity
                            if 'embedding' in other_place and 'embedding' in place_data:
                                try:
                                    import numpy as np
                                    vec1 = np.array(place_data['embedding'])
                                    vec2 = np.array(other_place['embedding'])
                                    similarity = float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
                                    if similarity >= 0.25 and other_place.get('name', '').lower() != liked_place.lower():
                                        other_place['similarity_score'] = similarity * 1.1  # Slight boost
                                        relevant_places.append(other_place)
                                except Exception:
                                    pass  # Skip if similarity calculation fails
                    break
    
    # Remove duplicates and places already liked, sort by similarity
    seen_names = set()
    unique_places = []
    liked_lower = [p.lower() for p in liked_places]
    
    for place in relevant_places:
        name = place.get('name', '')
        if name and name.lower() not in seen_names and name.lower() not in liked_lower:
            seen_names.add(name.lower())
            unique_places.append(place)
    
    # Sort by similarity score (highest first)
    unique_places.sort(key=lambda x: x.get('similarity_score', 0.0), reverse=True)
    
    # Format RAG context - prioritize diverse results
    rag_context = ""
    if unique_places:
        # Ensure diversity: take top result from different categories
        diverse_places = []
        seen_categories = set()
        
        # First pass: get top result from each category
        for place in unique_places:
            category = place.get('metadata', {}).get('category', 'other')
            if category not in seen_categories:
                diverse_places.append(place)
                seen_categories.add(category)
                if len(diverse_places) >= 8:
                    break
        
        # Second pass: fill remaining slots with highest scores
        for place in unique_places:
            if place not in diverse_places and len(diverse_places) < 10:
                diverse_places.append(place)
        
        rag_context = vector_search.format_context_for_llm(diverse_places[:10], max_places=10)
    
    # Enhanced prompt that adapts to user behavior
    learning_context = ""
    if liked_places:
        # Analyze patterns in liked places
        liked_places_str = ', '.join(liked_places[:5])  # Limit to 5 for context
        learning_context = f"""
        CRITICAL - PERSONALIZATION FROM USER HISTORY:
        The user has previously liked/saved these places: {liked_places_str}.
        
        YOUR TASK:
        1. Analyze the COMMON PATTERNS in these liked places:
           - What categories do they prefer? (temples, nature, food, culture, adventure)
           - What characteristics? (quiet, scenic, historic, authentic, popular, hidden)
           - What themes? (religious, natural beauty, local culture, adventure)
        
        2. Recommend 5-7 NEW places that:
           - Match the identified patterns and preferences
           - Are NOT in the liked list
           - Include a mix: 2-3 similar to liked places, 1-2 slightly different (to expand interests), 1-2 hidden gems
           - Are diverse (not all same category)
        
        3. For each recommendation, provide a SPECIFIC reason that references:
           - Why it matches their preferences
           - What makes it similar to or complementary to their liked places
           - What unique value it offers
        """
    else:
        learning_context = """
        RECOMMENDATION STRATEGY FOR NEW USER:
        - Suggest a diverse mix of 5-7 places covering different categories
        - Include: 2-3 popular must-see places, 2-3 hidden gems, 1-2 based on their specific interests
        - Ensure variety: temples, nature, culture, food, adventure
        - Prioritize places that match their travel style (budget/luxury/adventure/cultural)
        """

    prompt = f"""
    You are Neptou's AI travel recommendation expert for Nepal. Generate personalized place recommendations.
    
    USER PROFILE:
    {profile_str}
    
    {learning_context}
    
    VERIFIED PLACES DATABASE:
    {rag_context if rag_context else "No specific places found in database. Use general knowledge of Nepal tourism."}
    
    CRITICAL REQUIREMENTS:
    1. {"ONLY recommend places from the verified knowledge base above. Do NOT make up or invent places." if rag_context else "Recommend well-known places in Nepal that match the profile."}
    2. Ensure DIVERSITY: Mix of categories (temples, nature, culture, food, adventure)
    3. Match TRAVEL STYLE: Budget-friendly for budget travelers, luxury for luxury seekers, etc.
    4. Include HIDDEN GEMS: At least 2-3 lesser-known authentic spots
    5. Provide SPECIFIC reasons that directly reference the user's profile or liked places
    6. Match scores should reflect true relevance (0.7-0.95 range)
    
    Return ONLY a JSON array (no other text). Format:
    [
        {{
            "name": "Exact Place Name from Database",
            "reason": "Specific reason referencing their profile/interests/liked places. Be concrete and personal.",
            "match_score": 0.85,
            "category": "Nature/Culture/Adventure/Food/Temple",
            "is_hidden_gem": true
        }}
    ]
    
    Return 5-7 recommendations, prioritized by relevance to the user.
    """
    
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=2000,  # Increased for better recommendations
        system="You are Neptou's expert travel recommendation AI for Nepal. Always return valid JSON arrays. Be specific and personal in your recommendations.",
        messages=[{"role": "user", "content": prompt}]
    )
    
    try:
        content = response.content[0].text
        start_index = content.find('[')
        end_index = content.rfind(']') + 1
        if start_index != -1 and end_index != -1:
            json_str = content[start_index:end_index]
            return json.loads(json_str)
        return json.loads(content)
    except:
        return []

async def get_destination_guide(profile_str: str, locations: list[str]):
    """
    Generates a full guide using RAG vector search + static knowledge base.
    """
    # 1. Use RAG to find relevant places for these locations
    vector_search = get_vector_search()
    relevant_places = []
    
    # Search for places in each location
    for location in locations:
        # Search by location name
        places = vector_search.search(location, top_k=5, min_score=0.25)
        relevant_places.extend(places)
        
        # Also search by combining location + profile
        combined_query = f"{location} {profile_str}"
        places2 = vector_search.search(combined_query, top_k=3, min_score=0.3)
        relevant_places.extend(places2)
    
    # Remove duplicates
    seen_names = set()
    unique_places = []
    for place in relevant_places:
        name = place.get('name')
        if name and name not in seen_names:
            seen_names.add(name)
            unique_places.append(place)
    
    # Format RAG context
    rag_context = ""
    if unique_places:
        rag_context = vector_search.format_context_for_llm(unique_places[:15], max_places=15)
    
    # 2. Also fetch static city context from knowledge_base.py
    trusted_facts = knowledge_base.get_city_context(locations)
    
    loc_str = ", ".join(locations)
    
    prompt = f"""
    The user is visiting: {loc_str}.
    User Profile: {profile_str}
    
    Use the following VERIFIED INFORMATION to generate the guide. Do not hallucinate places that don't exist.
    
    {rag_context if rag_context else ""}
    
    {trusted_facts}
    
    Based on the profile and the verified facts above, return ONLY a JSON object with 4 keys: 'foods', 'places', 'events', 'guides'.
    Prioritize places from the verified knowledge base.
    Format:
    {{
        "foods": [{{ "name": "Name", "location": "City", "description": "...", "reason": "..." }}],
        "places": [{{ "name": "Name", "location": "City", "description": "...", "reason": "..." }}],
        "events": [{{ "name": "Name", "location": "City", "description": "...", "reason": "..." }}],
        "guides": [{{ "name": "Name", "location": "City", "description": "...", "reason": "..." }}]
    }}
    """
    
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=2000,
        system="You are a JSON-only API.",
        messages=[{"role": "user", "content": prompt}]
    )
    
    try:
        content = response.content[0].text
        start_index = content.find('{')
        end_index = content.rfind('}') + 1
        if start_index != -1 and end_index != -1:
            return json.loads(content[start_index:end_index])
        return json.loads(content)
    except:
        return {"foods": [], "places": [], "events": [], "guides": []}

async def optimize_existing_itinerary(itinerary: dict):
    """
    Optimize an existing itinerary by reordering activities and optimizing time slots.
    
    Args:
        itinerary: Existing itinerary dict with "name" and "days" keys
    
    Returns:
        Optimized itinerary
    """
    try:
        optimizer = get_trip_optimizer()
        optimized = optimizer.optimize_itinerary(
            itinerary,
            optimize_route=True,
            optimize_times=True
        )
        return optimized
    except Exception as e:
        print(f"❌ OPTIMIZATION ERROR: {e}")
        return {"error": "Failed to optimize itinerary", "original": itinerary}