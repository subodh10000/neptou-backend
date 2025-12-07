"""
Trip Optimizer Module
====================
Optimizes trip itineraries by:
- Route optimization (minimize travel distance)
- Time slot optimization (avoid conflicts, balance activities)
- Travel time calculation
- Activity grouping by location
"""
import math
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from vector_search import get_vector_search

@dataclass
class PlaceLocation:
    """Represents a place with location data."""
    name: str
    latitude: float
    longitude: float
    area: str
    time_needed: Optional[str] = None  # e.g., "2-3 hours"
    category: Optional[str] = None

@dataclass
class Activity:
    """Represents an activity in the itinerary."""
    place_name: str
    notes: str
    start_time: str
    end_time: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    area: Optional[str] = None

class TripOptimizer:
    """Optimizes trip itineraries."""
    
    def __init__(self):
        self.vector_search = get_vector_search()
    
    def haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the great circle distance between two points on Earth (in km).
        Uses the Haversine formula.
        """
        R = 6371  # Earth's radius in kilometers
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)
        
        c = 2 * math.asin(math.sqrt(a))
        return R * c
    
    def estimate_travel_time(self, distance_km: float, transport_mode: str = "car", 
                             from_district: str = None, to_district: str = None) -> int:
        """
        Estimate travel time in minutes based on distance.
        More realistic estimates considering inter-district travel.
        
        Args:
            distance_km: Distance in kilometers
            transport_mode: "car", "walk", "public"
            from_district: Source district name
            to_district: Destination district name
        
        Returns:
            Travel time in minutes
        """
        # Inter-district travel (longer distances)
        if from_district and to_district and from_district != to_district:
            # Major inter-district routes
            inter_district_routes = {
                ("Kathmandu", "Pokhara"): 360,  # 6 hours by bus
                ("Pokhara", "Kathmandu"): 360,
                ("Kathmandu", "Chitwan"): 180,  # 3 hours
                ("Chitwan", "Kathmandu"): 180,
                ("Kathmandu", "Dang"): 480,  # 8 hours
                ("Dang", "Kathmandu"): 480,
                ("Kathmandu", "Kailali"): 720,  # 12 hours
                ("Kailali", "Kathmandu"): 720,
                ("Pokhara", "Chitwan"): 180,  # 3 hours
                ("Chitwan", "Pokhara"): 180,
            }
            
            route_key = (from_district, to_district)
            if route_key in inter_district_routes:
                return inter_district_routes[route_key]
        
        # Local travel within district
        # Average speeds (km/h) - more realistic for Nepal
        speeds = {
            "car": 35,      # Slower in Nepal due to road conditions
            "walk": 4,      # Walking speed
            "public": 20   # Public transport (buses are slower)
        }
        
        speed = speeds.get(transport_mode, 35)
        time_hours = distance_km / speed
        
        # Add buffer time for traffic, stops, etc.
        buffer_multiplier = 1.3  # 30% buffer for realistic estimates
        time_hours *= buffer_multiplier
        
        return max(int(time_hours * 60), 15)  # Minimum 15 minutes
    
    def get_place_location(self, place_name: str) -> Optional[PlaceLocation]:
        """Get location data for a place from the knowledge base."""
        import json
        import os
        
        # Try to load from tourism_data.json directly for more complete data
        try:
            data_file = os.path.join(os.path.dirname(__file__), "tourism_data.json")
            if os.path.exists(data_file):
                with open(data_file, 'r', encoding='utf-8') as f:
                    places_data = json.load(f)
                
                # Search for matching place
                for place_data in places_data:
                    if place_data.get('name', '').lower() == place_name.lower():
                        location_data = place_data.get('location', {})
                        lat = location_data.get('latitude')
                        lon = location_data.get('longitude')
                        area = location_data.get('area', 'Unknown')
                        category = place_data.get('category', 'Unknown')
                        time_needed = place_data.get('time_needed')
                        
                        if lat and lon:
                            return PlaceLocation(
                                name=place_name,
                                latitude=lat,
                                longitude=lon,
                                area=area,
                                category=category,
                                time_needed=time_needed
                            )
        except Exception as e:
            print(f"Error loading tourism_data.json: {e}")
        
        # Fallback: Search in vector database
        results = self.vector_search.search(place_name, top_k=1, min_score=0.5)
        
        if results:
            place = results[0]
            metadata = place.get('metadata', {})
            
            # Try to get coordinates from metadata
            lat = metadata.get('latitude')
            lon = metadata.get('longitude')
            area = metadata.get('area', 'Unknown')
            category = metadata.get('category', 'Unknown')
            
            if lat and lon:
                return PlaceLocation(
                    name=place_name,
                    latitude=lat,
                    longitude=lon,
                    area=area,
                    category=category
                )
        
        return None
    
    def optimize_route_order(self, activities: List[Activity], start_location: Optional[Tuple[float, float]] = None) -> List[Activity]:
        """
        Optimize the order of activities to minimize travel distance.
        Groups by district first, then optimizes within each district.
        Uses nearest neighbor algorithm (greedy approach).
        
        Args:
            activities: List of activities with location data
            start_location: Optional starting point (lat, lon)
        
        Returns:
            Reordered list of activities (grouped by district)
        """
        if len(activities) <= 1:
            return activities
        
        # Filter activities with valid locations
        activities_with_locations = []
        activities_without_locations = []
        
        for activity in activities:
            if activity.latitude and activity.longitude:
                activities_with_locations.append(activity)
            else:
                activities_without_locations.append(activity)
        
        if not activities_with_locations:
            return activities  # Can't optimize without locations
        
        # Group by district first (more realistic)
        activities_by_district = {}
        for activity in activities_with_locations:
            district = getattr(activity, 'area', None) or "Other"
            if district not in activities_by_district:
                activities_by_district[district] = []
            activities_by_district[district].append(activity)
        
        # Optimize within each district, then combine
        optimized = []
        
        # If no start location, use first activity's location
        if not start_location:
            start_location = (activities_with_locations[0].latitude, activities_with_locations[0].longitude)
        
        current_location = start_location
        
        # Process districts (prioritize districts with more activities)
        sorted_districts = sorted(activities_by_district.items(), key=lambda x: -len(x[1]))
        
        for district, district_activities in sorted_districts:
            # Optimize within this district using nearest neighbor
            remaining = district_activities.copy()
            
            while remaining:
                # Find nearest unvisited activity in this district
                nearest_idx = 0
                nearest_distance = float('inf')
                
                for i, activity in enumerate(remaining):
                    distance = self.haversine_distance(
                        current_location[0], current_location[1],
                        activity.latitude, activity.longitude
                    )
                    
                    if distance < nearest_distance:
                        nearest_distance = distance
                        nearest_idx = i
                
                # Add nearest activity to optimized list
                nearest_activity = remaining.pop(nearest_idx)
                optimized.append(nearest_activity)
                current_location = (nearest_activity.latitude, nearest_activity.longitude)
        
        # Add activities without locations at the end
        optimized.extend(activities_without_locations)
        
        return optimized
    
    def calculate_travel_times(self, activities: List[Activity]) -> List[Dict]:
        """
        Calculate travel times between consecutive activities.
        Uses district information for more realistic estimates.
        
        Returns:
            List of travel time info dicts
        """
        travel_times = []
        
        for i in range(len(activities) - 1):
            current = activities[i]
            next_activity = activities[i + 1]
            
            if current.latitude and current.longitude and next_activity.latitude and next_activity.longitude:
                distance = self.haversine_distance(
                    current.latitude, current.longitude,
                    next_activity.latitude, next_activity.longitude
                )
                
                # Get districts for more realistic travel time
                from_district = current.area if hasattr(current, 'area') and current.area else None
                to_district = next_activity.area if hasattr(next_activity, 'area') and next_activity.area else None
                
                travel_time_min = self.estimate_travel_time(
                    distance, 
                    transport_mode="car",
                    from_district=from_district,
                    to_district=to_district
                )
                
                travel_times.append({
                    "from": current.place_name,
                    "to": next_activity.place_name,
                    "distance_km": round(distance, 2),
                    "travel_time_minutes": travel_time_min
                })
            else:
                travel_times.append({
                    "from": current.place_name,
                    "to": next_activity.place_name,
                    "distance_km": None,
                    "travel_time_minutes": None
                })
        
        return travel_times
    
    def optimize_time_slots(self, activities: List[Activity], day_start: str = "09:00 AM", 
                           default_activity_duration: int = 120) -> List[Activity]:
        """
        Optimize time slots for activities to avoid conflicts and ensure logical flow.
        More realistic with proper activity durations and travel times.
        CRITICAL: Prevents overlapping times and validates geographic feasibility.
        
        Args:
            activities: List of activities
            day_start: Start time for the day (e.g., "09:00 AM")
            default_activity_duration: Default duration in minutes
        
        Returns:
            Activities with optimized time slots (no overlaps)
        """
        from datetime import datetime, timedelta
        
        if not activities:
            return []
        
        # Remove duplicates by place name
        seen_places = set()
        unique_activities = []
        for act in activities:
            if act.place_name not in seen_places:
                seen_places.add(act.place_name)
                unique_activities.append(act)
        activities = unique_activities
        
        # Parse start time
        try:
            start_time = datetime.strptime(day_start, "%I:%M %p")
        except:
            start_time = datetime.strptime("09:00 AM", "%I:%M %p")
        
        optimized_activities = []
        current_time = start_time
        max_end_time = datetime.strptime("08:00 PM", "%I:%M %p")  # Don't schedule after 8 PM
        
        # Realistic activity durations based on category (if available)
        def get_realistic_duration(activity: Activity, default: int) -> int:
            """Get realistic duration based on place type and distance."""
            # If it's a temple/culture site: 1-2 hours
            # If it's nature/viewpoint: 2-3 hours
            # If it's food: 1 hour
            # Default: 2 hours
            area = getattr(activity, 'area', None) or ""
            place_name = activity.place_name.lower()
            
            if any(word in place_name for word in ["temple", "stupa", "durbar", "monastery"]):
                return 90  # 1.5 hours for temples
            elif any(word in place_name for word in ["lake", "park", "viewpoint", "hill"]):
                return 150  # 2.5 hours for nature spots
            elif any(word in place_name for word in ["restaurant", "cafe", "food"]):
                return 60  # 1 hour for food
            else:
                return default
        
        for i, activity in enumerate(activities):
            # Get realistic duration
            duration = get_realistic_duration(activity, default_activity_duration)
            
            # Add travel time if not first activity
            travel_time = 0
            if i > 0 and activity.latitude and activity.longitude:
                prev_activity = activities[i - 1]
                if prev_activity.latitude and prev_activity.longitude:
                    distance = self.haversine_distance(
                        prev_activity.latitude, prev_activity.longitude,
                        activity.latitude, activity.longitude
                    )
                    
                    # Get districts for realistic travel time
                    from_district = getattr(prev_activity, 'area', None)
                    to_district = getattr(activity, 'area', None)
                    
                    travel_time = self.estimate_travel_time(
                        distance,
                        transport_mode="car",
                        from_district=from_district,
                        to_district=to_district
                    )
            
            # Set optimized times with travel time
            new_start = current_time + timedelta(minutes=travel_time)
            new_end = new_start + timedelta(minutes=duration)
            
            # Validate: Don't schedule activities too late (after 8 PM)
            if new_start >= max_end_time:
                # Skip this activity if it would go too late
                print(f"⚠️ Skipping {activity.place_name} - would start too late ({new_start.strftime('%I:%M %p')})")
                continue
            
            # Validate: Ensure end time doesn't exceed max
            if new_end > max_end_time:
                # Adjust duration to fit within day
                new_end = max_end_time
                duration = int((new_end - new_start).total_seconds() / 60)
                if duration < 30:  # Minimum 30 minutes
                    print(f"⚠️ Skipping {activity.place_name} - not enough time")
                    continue
            
            # Validate: Check for overlaps with already scheduled activities
            has_overlap = False
            for existing in optimized_activities:
                existing_start = datetime.strptime(existing.start_time, "%I:%M %p")
                existing_end = datetime.strptime(existing.end_time, "%I:%M %p")
                
                # Check if times overlap
                if (new_start < existing_end and new_end > existing_start):
                    has_overlap = True
                    # Adjust start time to be after existing activity
                    new_start = existing_end + timedelta(minutes=15)  # 15 min buffer
                    new_end = new_start + timedelta(minutes=duration)
                    
                    # Re-check if still valid
                    if new_start >= max_end_time:
                        print(f"⚠️ Skipping {activity.place_name} - no time after resolving overlap")
                        has_overlap = True  # Mark to skip
                        break
            
            if has_overlap and new_start >= max_end_time:
                continue
            
            # Create optimized activity
            optimized_activity = Activity(
                place_name=activity.place_name,
                notes=activity.notes,
                start_time=new_start.strftime("%I:%M %p"),
                end_time=new_end.strftime("%I:%M %p"),
                latitude=activity.latitude,
                longitude=activity.longitude,
                area=activity.area
            )
            
            optimized_activities.append(optimized_activity)
            current_time = new_end
        
        return optimized_activities
    
    def balance_activities_per_day(self, all_activities: List[Activity], num_days: int) -> List[List[Activity]]:
        """
        Distribute activities across days to balance the schedule.
        
        Args:
            all_activities: All activities to distribute
            num_days: Number of days
        
        Returns:
            List of activity lists, one per day
        """
        if num_days <= 0:
            return [all_activities]
        
        activities_per_day = len(all_activities) // num_days
        remainder = len(all_activities) % num_days
        
        days = []
        start_idx = 0
        
        for day in range(num_days):
            # Distribute remainder across first few days
            count = activities_per_day + (1 if day < remainder else 0)
            end_idx = start_idx + count
            
            day_activities = all_activities[start_idx:end_idx]
            days.append(day_activities)
            
            start_idx = end_idx
        
        return days
    
    def optimize_itinerary(self, itinerary: Dict, optimize_route: bool = True, 
                          optimize_times: bool = True, auto_recommend: bool = True) -> Dict:
        """
        Optimize a complete itinerary with validation and conflict resolution.
        
        Args:
            itinerary: Itinerary dict with "name" and "days" keys
            optimize_route: Whether to optimize route order
            optimize_times: Whether to optimize time slots
            auto_recommend: Whether to auto-recommend places for days with few activities
        
        Returns:
            Optimized itinerary
        """
        optimized_days = []
        
        for day_data in itinerary.get("days", []):
            day_number = day_data.get("day_number", 1)
            activities_data = day_data.get("activities", [])
            day_district = day_data.get("district")  # Get district for this day if specified
            
            # Remove duplicates first
            seen_places = set()
            unique_activities_data = []
            for act_data in activities_data:
                place_name = act_data.get("place_name", "").strip()
                if place_name and place_name not in seen_places:
                    seen_places.add(place_name)
                    unique_activities_data.append(act_data)
            
            # Convert to Activity objects and get locations
            activities = []
            for act_data in unique_activities_data:
                place_name = act_data.get("place_name", "").strip()
                if not place_name:
                    continue
                    
                location = self.get_place_location(place_name)
                
                # Extract district from area
                district = None
                if location and location.area:
                    district = self._extract_district_from_area(location.area, place_name)
                
                activity = Activity(
                    place_name=place_name,
                    notes=act_data.get("notes", ""),
                    start_time=act_data.get("start_time", "09:00 AM"),
                    end_time=act_data.get("end_time", "11:00 AM"),
                    latitude=location.latitude if location else None,
                    longitude=location.longitude if location else None,
                    area=district or (location.area if location else None)
                )
                activities.append(activity)
            
            # Validate and filter activities by district if day_district is set
            if day_district:
                # Only keep activities in the same district
                activities = [act for act in activities if act.area == day_district]
            
            # Auto-recommend places if day has few activities and district is known
            if auto_recommend and len(activities) < 2:
                # Determine district for this day
                district_for_day = day_district
                if not district_for_day and activities:
                    # Get district from existing activities
                    districts = [act.area for act in activities if act.area]
                    if districts:
                        district_for_day = max(set(districts), key=districts.count)  # Most common district
                
                if district_for_day:
                    # Recommend top places from this district (exclude already added)
                    existing_place_names = [act.place_name for act in activities]
                    recommended = self._recommend_places_for_district(district_for_day, existing_places=existing_place_names)
                    
                    # Add recommendations (limit to fill up to 3-4 activities per day)
                    num_to_add = min(3 - len(activities), len(recommended))
                    for rec_place in recommended[:num_to_add]:
                        if rec_place not in existing_place_names:  # Double-check no duplicates
                            location = self.get_place_location(rec_place)
                            district = None
                            if location and location.area:
                                district = self._extract_district_from_area(location.area, rec_place)
                            
                            activities.append(Activity(
                                place_name=rec_place,
                                notes=f"Recommended place in {district_for_day}",
                                start_time="02:00 PM",  # Default afternoon time (will be optimized)
                                end_time="04:00 PM",
                                latitude=location.latitude if location else None,
                                longitude=location.longitude if location else None,
                                area=district
                            ))
                            existing_place_names.append(rec_place)  # Track to prevent duplicates
            
            # Group activities by district to prevent cross-district conflicts
            activities_by_district = {}
            for act in activities:
                district = act.area or "Unknown"
                if district not in activities_by_district:
                    activities_by_district[district] = []
                activities_by_district[district].append(act)
            
            # If multiple districts, prioritize the most common one for this day
            if len(activities_by_district) > 1:
                # Get the district with most activities
                main_district = max(activities_by_district.items(), key=lambda x: len(x[1]))[0]
                # Only keep activities from main district to avoid conflicts
                activities = activities_by_district[main_district]
                print(f"⚠️ Day {day_number}: Multiple districts detected. Using {main_district} only.")
            
            # Optimize route order
            if optimize_route and len(activities) > 1:
                activities = self.optimize_route_order(activities)
            
            # Optimize time slots (this will prevent overlaps)
            if optimize_times and activities:
                activities = self.optimize_time_slots(activities, day_start="09:00 AM")
            
            # Convert back to dict format
            optimized_activities = []
            for activity in activities:
                optimized_activities.append({
                    "place_name": activity.place_name,
                    "notes": activity.notes,
                    "start_time": activity.start_time,
                    "end_time": activity.end_time
                })
            
            # Determine final district for this day
            final_district = day_district
            if not final_district and activities:
                districts = [act.area for act in activities if act.area]
                if districts:
                    final_district = max(set(districts), key=districts.count)  # Most common district
            
            optimized_days.append({
                "day_number": day_number,
                "district": final_district,
                "activities": optimized_activities
            })
        
        return {
            "name": itinerary.get("name", "Optimized Trip"),
            "days": optimized_days
        }
    
    def _recommend_places_for_district(self, district: str, existing_places: list = None) -> list:
        """Recommend top places for a given district."""
        import json
        import os
        
        existing_places = existing_places or []
        recommended = []
        
        try:
            data_file = os.path.join(os.path.dirname(__file__), "tourism_data.json")
            if os.path.exists(data_file):
                with open(data_file, 'r', encoding='utf-8') as f:
                    places_data = json.load(f)
                
                # Filter places by district
                district_places = []
                for place_data in places_data:
                    location_data = place_data.get('location', {})
                    area = location_data.get('area', '')
                    place_name = place_data.get('name', '')
                    
                    # Check if place is in the target district
                    district_match = self._extract_district_from_area(area, place_name)
                    if district_match == district and place_name not in existing_places:
                        rating = place_data.get('google_rating') or place_data.get('rating', 0)
                        district_places.append((place_name, rating))
                
                # Sort by rating and return top places
                district_places.sort(key=lambda x: x[1], reverse=True)
                recommended = [name for name, _ in district_places[:5]]  # Top 5
        except Exception as e:
            print(f"Error recommending places: {e}")
        
        return recommended
    
    def _extract_district_from_area(self, area: str, place_name: str = "") -> str:
        """Extract main district name from area string."""
        area_lower = area.lower()
        name_lower = place_name.lower()
        
        # Map areas to main districts
        if "kathmandu" in area_lower or "thamel" in area_lower or "boudha" in area_lower or "gaushala" in area_lower or "swayambhu" in area_lower:
            return "Kathmandu"
        if "pokhara" in area_lower or "lakeside" in area_lower or "sarangkot" in area_lower:
            return "Pokhara"
        if "dang" in area_lower or "dang" in name_lower:
            return "Dang"
        if "kailali" in area_lower or "dhangadhi" in area_lower or "tikapur" in area_lower:
            return "Kailali"
        if "chitwan" in area_lower or "sauraha" in area_lower:
            return "Chitwan"
        if "lumbini" in area_lower:
            return "Lumbini"
        if "bhaktapur" in area_lower:
            return "Bhaktapur"
        if "patan" in area_lower:
            return "Patan"
        if "nagarkot" in area_lower:
            return "Nagarkot"
        
        return area  # Return original if no match


# Global instance
_optimizer_instance: Optional[TripOptimizer] = None

def get_trip_optimizer() -> TripOptimizer:
    """Get or create the global trip optimizer instance."""
    global _optimizer_instance
    if _optimizer_instance is None:
        _optimizer_instance = TripOptimizer()
    return _optimizer_instance
