from pydantic import BaseModel
from typing import List, Optional

# --- Chat Models ---
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: Optional[str] = None  # Support single message from iOS app
    history: Optional[List[ChatMessage]] = None  # Make optional to support both formats
    place_context: Optional[dict] = None  # Optional place context when user asks about a specific place
    food_context: Optional[dict] = None  # Optional food context when user asks about a specific food

# --- Trip Planning Models ---
class TripRequest(BaseModel):
    duration: int
    travel_style: str
    interests: List[str]
    start_date: str

# --- Recommendation Models ---
class UserProfileRequest(BaseModel):
    name: str
    travel_style: str
    interests: List[str]
    liked_places: Optional[List[str]] = []  # Places the user has liked/saved

# --- Destination Guide Models ---
class DestinationGuideRequest(BaseModel):
    travel_style: str
    interests: List[str]
    locations: List[str]  # List of cities/locations to visit

# --- Trip Optimization Models ---
class OptimizeItineraryRequest(BaseModel):
    itinerary: dict  # The existing itinerary to optimize

# --- Search Models ---
class SearchRequest(BaseModel):
    query: str  # Search query text
    limit: Optional[int] = 20  # Maximum number of results