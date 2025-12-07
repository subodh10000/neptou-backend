# Local Insights RAG System

## Overview

This system adds **authentic, local Nepal information** that isn't available on the internet to your RAG knowledge base. This makes Neptou unique by providing insider tips, cultural insights, and local secrets that only locals know.

## What's Included

The `local_insights.json` file contains 20+ local insights covering:

- **Cultural Tips**: Temple etiquette, festival timing, spiritual practices
- **Food Culture**: Authentic eating practices, hidden food spots, local secrets
- **Practical Tips**: Money exchange, bargaining, transportation, SIM cards
- **Safety Tips**: Monkey safety, street food safety, trekking tips
- **Hidden Gems**: Secret viewpoints, local restaurants, authentic experiences
- **Budget Tips**: How to save money, avoid tourist traps

## How to Add More Insights

### Step 1: Edit `local_insights.json`

Add new insights in this format:

```json
{
  "id": "local_insight_021",
  "title": "Your Insight Title",
  "category": "cultural_tips|food_culture|practical_tips|safety_tips|accommodation|transportation|adventure|wildlife",
  "district": "Kathmandu|Pokhara|Dang|Kailali|Bhaktapur|etc",
  "content": "Your detailed local insight here. This should be authentic information not found on the internet. Include specific details, prices, timings, locations, and local secrets.",
  "tags": ["tag1", "tag2", "tag3"],
  "authenticity_level": "local_expert"
}
```

### Step 2: Run the Script

```bash
cd neptou-backend
python3 add_local_insights.py
```

This will:
- Load all insights from `local_insights.json`
- Create embeddings for each insight
- Merge them with existing `tourism_embeddings.json`
- Make them searchable by the RAG system

### Step 3: Restart Backend

```bash
# Restart your server
uvicorn main:app --reload
```

## Example Insights to Add

### Cultural Insights
- Best times to visit specific temples
- Festival dates and how to participate
- Cultural etiquette and do's/don'ts
- Local customs and traditions

### Food Insights
- Hidden restaurants locals love
- Authentic food preparation methods
- Street food safety and best spots
- Local food prices and bargaining

### Practical Insights
- Transportation hacks
- Money-saving tips
- Local market secrets
- Communication tips (Nepali phrases)

### Adventure Insights
- Best trekking routes (lesser-known)
- Photography spots locals know
- Weather patterns and best seasons
- Equipment rental tips

## Testing

After adding insights, test with queries like:

- "best time to visit Pashupatinath"
- "where to exchange money in Thamel"
- "how to eat momos properly"
- "secret viewpoint in Pokhara"
- "Tharu homestay in Dang"

The AI should now include these local insights in responses!

## Current Insights (20)

1. Best Time to Visit Pashupatinath Temple
2. Thamel Money Exchange Secret
3. Momo Eating Etiquette
4. Boudhanath Stupa Walking Direction
5. Pokhara Lakeside Restaurant Secret
6. Sarangkot Sunrise Secret
7. Trekking Guide Hiring Secret
8. Dang Tharu Festival Timing
9. Kailali Banana Season
10. Bargaining in Nepal Markets
11. Temple Entry Fees - Local Secret
12. Bhaktapur Juju Dhau Secret
13. Monkey Temple - Safety Tips
14. Local Bus vs Tourist Bus
15. Tipping Culture in Nepal
16. Dang Tharu Homestay Experience
17. Kailali Dolphin Spotting Secret
18. Pokhara Paragliding - Local Secret
19. Kathmandu Street Food Safety
20. Nepal SIM Card Secret

## Tips for Writing Good Insights

1. **Be Specific**: Include exact locations, prices, times
2. **Be Authentic**: Only include information locals actually know
3. **Be Practical**: Focus on actionable tips
4. **Include Context**: Explain why this tip matters
5. **Add Details**: Specific names, prices, timings make it valuable

## Integration

The insights are automatically:
- ✅ Searchable via semantic search
- ✅ Included in AI responses when relevant
- ✅ Formatted specially as "LOCAL INSIDER TIPS"
- ✅ Tagged by district and category
- ✅ Prioritized in search results

## Next Steps

1. Add more insights based on your local knowledge
2. Test with real user queries
3. Refine insights based on what users ask about
4. Expand to more districts and categories
