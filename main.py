from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import ai_service
import schemas
import models
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Neptou API")

# SECURITY FIX: Restrict CORS origins instead of allowing all
# In production, replace with your actual iOS app's origin or use environment variable
# For development: Allow localhost and local network IPs for iPhone access
def get_local_ip():
    """Get local IP address for CORS configuration."""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return None

local_ip = get_local_ip()
default_origins = ["http://localhost:8000", "http://127.0.0.1:8000"]
if local_ip:
    default_origins.append(f"http://{local_ip}:8000")

# Allow all origins for development (iPhone simulator and physical device)
# In production, replace with specific allowed origins
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",") if os.getenv("ALLOWED_ORIGINS") else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Allows localhost, local IP, and all origins for development
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Added OPTIONS for CORS preflight
    allow_headers=["Content-Type", "Authorization", "Accept"],  # Added Accept header
)

@app.get("/")
def read_root():
    return {"message": "Namaste! Neptou Backend is running.", "version": "2.0"}

@app.post("/api/chat")
async def chat(request: schemas.ChatRequest):
    """Chat with the AI Assistant"""
    
    # Handle both formats: single message or history
    if request.message and not request.history:
        # iOS app format: convert single message to history
        messages = [{"role": "user", "content": request.message}]
    elif request.history:
        # Existing format: use history
        messages = [{"role": m.role, "content": m.content} for m in request.history]
    else:
        raise HTTPException(status_code=400, detail="Either 'message' or 'history' must be provided")
    
    # SECURITY FIX: Input validation
    if not messages:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    # Validate message content length to prevent abuse
    for msg in messages:
        if len(msg.get("content", "")) > 10000:  # Reasonable limit
            raise HTTPException(status_code=400, detail="Message too long (max 10000 characters)")
        if msg.get("role") not in ["user", "assistant"]:
            raise HTTPException(status_code=400, detail="Invalid message role")
    
    try:
        # Get place and food context if provided
        place_context = request.place_context if request.place_context else None
        food_context = request.food_context if request.food_context else None
        result = await ai_service.get_chat_response(messages, place_context=place_context, food_context=food_context)
        
        # Handle both dict (with follow-up questions) and string (legacy) responses
        if isinstance(result, dict):
            return result
        else:
            # Legacy format - just return the text
            return {"response": result, "follow_up_questions": []}
    except ValueError as e:
        # SECURITY FIX: Don't expose internal error details
        print(f"❌ CHAT ERROR: {e}")
        raise HTTPException(status_code=400, detail="Invalid request format")
    except Exception as e:
        print(f"❌ CHAT ERROR: {e}")
        # SECURITY FIX: Generic error message for users
        raise HTTPException(status_code=500, detail="An error occurred processing your request")

@app.post("/api/plan-trip")
async def plan_trip(request: schemas.TripRequest):
    """Generate a full itinerary"""
    # SECURITY FIX: Input validation
    if request.duration < 1 or request.duration > 30:
        raise HTTPException(status_code=400, detail="Duration must be between 1 and 30 days")
    
    if not request.travel_style or len(request.travel_style) > 50:
        raise HTTPException(status_code=400, detail="Invalid travel style")
    
    if not request.interests or len(request.interests) > 20:
        raise HTTPException(status_code=400, detail="Too many interests (max 20)")
    
    try:
        itinerary = await ai_service.generate_itinerary(
            request.duration, 
            request.travel_style, 
            request.interests, 
            request.start_date
        )
        # Check if the AI service returned a specific error structure
        if isinstance(itinerary, dict) and "error" in itinerary:
             print(f"❌ ITINERARY GENERATION ERROR: {itinerary}")
             raise HTTPException(status_code=500, detail="Failed to generate itinerary")
             
        return itinerary
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ PLAN TRIP ERROR: {e}")
        # SECURITY FIX: Generic error message
        raise HTTPException(status_code=500, detail="An error occurred generating your itinerary")

@app.post("/api/recommendations")
async def recommendations(user: schemas.UserProfileRequest):
    """Get personalized place picks"""
    # SECURITY FIX: Input validation
    if not user.name or len(user.name) > 100:
        raise HTTPException(status_code=400, detail="Invalid name")
    
    if not user.travel_style or len(user.travel_style) > 50:
        raise HTTPException(status_code=400, detail="Invalid travel style")
    
    if len(user.interests) > 20:
        raise HTTPException(status_code=400, detail="Too many interests (max 20)")
    
    try:
        profile_str = f"Style: {user.travel_style}, Interests: {', '.join(user.interests)}"
        liked_places = user.liked_places if user.liked_places else []
        recs = await ai_service.get_recommendations(profile_str, liked_places=liked_places)
        return recs
    except Exception as e:
        print(f"❌ RECOMMENDATIONS ERROR: {e}")
        # SECURITY FIX: Generic error message
        raise HTTPException(status_code=500, detail="An error occurred generating recommendations")

@app.post("/api/optimize-itinerary")
async def optimize_itinerary(request: schemas.OptimizeItineraryRequest):
    """Optimize an existing itinerary by reordering activities and optimizing time slots"""
    # SECURITY FIX: Input validation
    if not request.itinerary:
        raise HTTPException(status_code=400, detail="Itinerary cannot be empty")
    
    if not isinstance(request.itinerary, dict):
        raise HTTPException(status_code=400, detail="Invalid itinerary format")
    
    try:
        optimized = await ai_service.optimize_existing_itinerary(request.itinerary)
        
        if isinstance(optimized, dict) and "error" in optimized:
            print(f"❌ OPTIMIZATION ERROR: {optimized}")
            raise HTTPException(status_code=500, detail="Failed to optimize itinerary")
        
        return optimized
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ OPTIMIZE ITINERARY ERROR: {e}")
        raise HTTPException(status_code=500, detail="An error occurred optimizing your itinerary")

@app.post("/api/destination-guide")
async def destination_guide(request: schemas.DestinationGuideRequest):
    """Get comprehensive destination guide with RAG-powered recommendations"""
    # SECURITY FIX: Input validation
    if not request.travel_style or len(request.travel_style) > 50:
        raise HTTPException(status_code=400, detail="Invalid travel style")
    
    if len(request.interests) > 20:
        raise HTTPException(status_code=400, detail="Too many interests (max 20)")
    
    if not request.locations or len(request.locations) > 10:
        raise HTTPException(status_code=400, detail="Invalid locations (max 10)")
    
    # Validate location names
    for location in request.locations:
        if len(location) > 100:
            raise HTTPException(status_code=400, detail="Location name too long")
    
    try:
        profile_str = f"Style: {request.travel_style}, Interests: {', '.join(request.interests)}"
        guide = await ai_service.get_destination_guide(profile_str, request.locations)
        
        # Check if the AI service returned a specific error structure
        if isinstance(guide, dict) and "error" in guide:
            print(f"❌ DESTINATION GUIDE ERROR: {guide}")
            raise HTTPException(status_code=500, detail="Failed to generate destination guide")
        
        return guide
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ DESTINATION GUIDE ERROR: {e}")
        # SECURITY FIX: Generic error message
        raise HTTPException(status_code=500, detail="An error occurred generating destination guide")

@app.get("/api/places")
async def get_places(
    category: str = None,
    area: str = None,
    search: str = None,
    limit: int = 100
):
    """
    Get all places with optional filtering.
    Returns comprehensive place data from tourism_data.json
    """
    import json
    import os
    
    try:
        # Load tourism_data.json
        data_file = os.path.join(os.path.dirname(__file__), "tourism_data.json")
        if not os.path.exists(data_file):
            raise HTTPException(status_code=404, detail="Places data not found")
        
        with open(data_file, 'r', encoding='utf-8') as f:
            places_data = json.load(f)
        
        # Apply filters
        filtered = places_data
        
        if category:
            filtered = [p for p in filtered if p.get('category', '').lower() == category.lower()]
        
        if area:
            filtered = [p for p in filtered if p.get('location', {}).get('area', '').lower() == area.lower()]
        
        if search:
            search_lower = search.lower()
            filtered = [p for p in filtered if 
                       search_lower in p.get('name', '').lower() or
                       search_lower in p.get('description', '').lower() or
                       search_lower in p.get('name_nepali', '').lower()]
        
        # Limit results
        filtered = filtered[:limit]
        
        return {
            "places": filtered,
            "count": len(filtered),
            "total": len(places_data)
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ GET PLACES ERROR: {e}")
        raise HTTPException(status_code=500, detail="An error occurred fetching places")

@app.post("/api/search")
async def search_places(request: schemas.SearchRequest):
    """
    RAG-powered semantic search for places using vector embeddings.
    Returns places that semantically match the search query.
    """
    # SECURITY FIX: Input validation
    if not request.query or len(request.query) > 200:
        raise HTTPException(status_code=400, detail="Invalid search query (max 200 characters)")
    
    try:
        from vector_search import get_vector_search
        
        vector_search = get_vector_search()
        
        # Perform semantic search
        results = vector_search.search(request.query, top_k=request.limit or 20, min_score=0.2)
        
        # Format results for response
        search_results = []
        for result in results:
            place_info = {
                "name": result.get('name', ''),
                "category": result.get('metadata', {}).get('category', ''),
                "area": result.get('metadata', {}).get('area', ''),
                "similarity_score": result.get('similarity_score', 0.0),
                "description": result.get('metadata', {}).get('description', ''),
                "tags": result.get('metadata', {}).get('tags', [])
            }
            search_results.append(place_info)
        
        return {
            "query": request.query,
            "results": search_results,
            "count": len(search_results)
        }
    except Exception as e:
        print(f"❌ SEARCH ERROR: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during search")

if __name__ == "__main__":
    import uvicorn
    # This runs the server on all network interfaces (0.0.0.0) so your phone can reach it
    # Support PORT environment variable for cloud platforms
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)