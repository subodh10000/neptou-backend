# Quick Guide: Adding Local Insights

## One-Time Setup

1. **Make sure dependencies are installed:**
   ```bash
   cd neptou-backend
   pip install sentence-transformers numpy
   ```

2. **Add your local insights to `local_insights.json`**

3. **Run the script:**
   ```bash
   python3 add_local_insights.py
   ```

4. **Restart your backend server**

## Adding New Insights

Just edit `local_insights.json` and add entries like this:

```json
{
  "id": "local_insight_021",
  "title": "Your Local Secret",
  "category": "practical_tips",
  "district": "Kathmandu",
  "content": "Detailed insider information here...",
  "tags": ["tag1", "tag2"],
  "authenticity_level": "local_expert"
}
```

Then run `python3 add_local_insights.py` again.

## Categories Available

- `cultural_tips` - Temple etiquette, festivals, customs
- `food_culture` - Eating practices, hidden restaurants
- `practical_tips` - Money, transportation, communication
- `safety_tips` - Safety advice, precautions
- `accommodation` - Hotels, homestays, staying tips
- `transportation` - Buses, taxis, local transport
- `adventure` - Trekking, paragliding, activities
- `wildlife` - Animal spotting, nature tips
- `viewpoint_tips` - Best spots for views/photos

## Example: Adding a New Insight

Let's say you want to add a tip about bargaining in Pokhara:

1. Open `local_insights.json`
2. Add this to the `local_insights` array:

```json
{
  "id": "local_insight_021",
  "title": "Pokhara Lakeside Bargaining",
  "category": "practical_tips",
  "district": "Pokhara",
  "content": "In Pokhara Lakeside, prices are inflated 3-5x for tourists. Always bargain, but do it with a smile. Start at 40% of asking price. For souvenirs, the best deals are in the small shops behind the main street, not the front shops. Local tip: If you're buying multiple items, ask for 'set price' - they'll give you a better deal.",
  "tags": ["bargaining", "shopping", "pokhara", "lakeside", "budget"],
  "authenticity_level": "local_expert"
}
```

3. Save the file
4. Run: `python3 add_local_insights.py`
5. Restart server

That's it! The AI will now know this tip and share it when relevant.
