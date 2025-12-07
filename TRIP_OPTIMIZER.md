# Trip Optimizer Documentation

## Overview

The Trip Optimizer module automatically optimizes travel itineraries by:
- **Route Optimization**: Reorders activities to minimize travel distance using nearest neighbor algorithm
- **Time Slot Optimization**: Automatically schedules activities with proper time gaps and travel time
- **Travel Time Calculation**: Estimates travel time between places using Haversine distance formula
- **Activity Balancing**: Distributes activities evenly across days

## Features

### 1. Route Optimization
- Uses nearest neighbor algorithm (greedy approach)
- Minimizes total travel distance
- Considers location coordinates from knowledge base
- Handles activities without location data gracefully

### 2. Time Slot Optimization
- Automatically schedules activities with logical time gaps
- Accounts for travel time between consecutive activities
- Default activity duration: 2 hours
- Configurable day start time (default: 9:00 AM)

### 3. Travel Time Estimation
- Calculates distance using Haversine formula (great circle distance)
- Estimates travel time based on transport mode:
  - Car: 40 km/h (urban/rural mix)
  - Walking: 5 km/h
  - Public Transport: 25 km/h
- Returns travel time in minutes

## API Integration

### Automatic Optimization
All itineraries generated via `/api/plan-trip` are automatically optimized.

### Manual Optimization
Use `/api/optimize-itinerary` to optimize an existing itinerary:

```json
POST /api/optimize-itinerary
{
  "itinerary": {
    "name": "My Trip",
    "days": [
      {
        "day_number": 1,
        "activities": [
          {
            "place_name": "Pashupatinath Temple",
            "notes": "Visit temple",
            "start_time": "09:00 AM",
            "end_time": "11:00 AM"
          }
        ]
      }
    ]
  }
}
```

## How It Works

### Step 1: Location Lookup
For each activity, the optimizer:
1. Searches `tourism_data.json` for place coordinates
2. Falls back to vector search if not found
3. Extracts latitude, longitude, area, and category

### Step 2: Route Optimization
1. Filters activities with valid locations
2. Uses nearest neighbor algorithm:
   - Start from first activity or specified start location
   - Find nearest unvisited activity
   - Add to optimized route
   - Repeat until all activities are ordered

### Step 3: Time Optimization
1. Parses existing time slots (if available)
2. Calculates travel time between consecutive activities
3. Schedules activities with proper gaps:
   - Activity duration (from existing or default 2 hours)
   - Travel time to next activity
4. Formats times in "HH:MM AM/PM" format

### Step 4: Return Optimized Itinerary
Returns the same structure as input, but with:
- Reordered activities (route optimized)
- Updated time slots (time optimized)
- All original data preserved

## Example

**Before Optimization:**
```json
{
  "day_number": 1,
  "activities": [
    {"place_name": "Boudhanath Stupa", "start_time": "09:00 AM"},
    {"place_name": "Pashupatinath Temple", "start_time": "10:00 AM"},
    {"place_name": "Swayambhunath", "start_time": "11:00 AM"}
  ]
}
```

**After Optimization:**
```json
{
  "day_number": 1,
  "activities": [
    {"place_name": "Pashupatinath Temple", "start_time": "09:00 AM", "end_time": "11:00 AM"},
    {"place_name": "Boudhanath Stupa", "start_time": "11:15 AM", "end_time": "01:15 PM"},
    {"place_name": "Swayambhunath", "start_time": "01:30 PM", "end_time": "03:30 PM"}
  ]
}
```

Note: Activities are reordered by proximity, and times include travel time.

## iOS Integration

The Swift `TripPlannerView` automatically:
1. Calls `/api/plan-trip` which returns optimized itinerary
2. Parses JSON response into `Trip` model
3. Displays optimized schedule with proper time slots
4. Shows travel time between activities (if available)

## Configuration

### Adjustable Parameters

In `trip_optimizer.py`:

```python
# Default activity duration (minutes)
default_activity_duration = 120  # 2 hours

# Day start time
day_start = "09:00 AM"

# Transport speeds (km/h)
speeds = {
    "car": 40,
    "walk": 5,
    "public": 25
}
```

## Limitations

1. **Location Data**: Requires coordinates in `tourism_data.json` or vector database
2. **Simple Algorithm**: Uses greedy nearest neighbor (not optimal TSP solution)
3. **Fixed Speeds**: Uses average speeds, doesn't account for traffic
4. **No Real-time Data**: Doesn't use live traffic or transit schedules

## Future Enhancements

- [ ] Use actual Google Maps/Directions API for accurate travel times
- [ ] Implement optimal TSP algorithm (2-opt, simulated annealing)
- [ ] Consider opening hours when scheduling
- [ ] Account for meal times and breaks
- [ ] Multi-modal transportation (walk + bus + taxi)
- [ ] Real-time traffic data integration
