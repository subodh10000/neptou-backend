# RAG Implementation Guide

## Overview

This project now has **full RAG (Retrieval-Augmented Generation) integration** that enhances AI responses with verified knowledge from your tourism database.

## Architecture

### Components

1. **`vector_search.py`** - Vector search engine
   - Loads embeddings from `tourism_embeddings.json`
   - Performs semantic search using cosine similarity
   - Formats results for LLM context

2. **`ai_service.py`** - Enhanced AI service with RAG
   - All functions now use vector search before calling LLM
   - Retrieves relevant places based on user queries
   - Injects verified context into prompts

3. **`main.py`** - API endpoints
   - `/api/chat` - Chat with RAG support
   - `/api/plan-trip` - Itinerary generation with RAG
   - `/api/recommendations` - Recommendations with RAG
   - `/api/destination-guide` - NEW: Comprehensive destination guide

## How RAG Works

### Flow Diagram

```
User Query
    ↓
Vector Search (semantic similarity)
    ↓
Retrieve Top-K Relevant Places
    ↓
Format Context for LLM
    ↓
LLM (Claude) with Context
    ↓
Response with Verified Information
```

### Example: Chat with RAG

1. User asks: "Where can I find peaceful temples?"
2. Vector search finds: Boudhanath Stupa, Swayambhunath, Garden of Dreams
3. Context injected: "Relevant places: Boudhanath Stupa (Buddhist, meditation)..."
4. LLM responds using verified places from knowledge base

### Example: Itinerary Generation

1. User interests: ["temples", "food", "nature"]
2. Vector search for each interest finds relevant places
3. LLM creates itinerary using verified places only
4. No hallucinated locations!

## API Endpoints

### 1. Chat (`POST /api/chat`)
- **RAG**: Searches for relevant places based on user's latest message
- **Context**: Injects top 3 relevant places into system prompt
- **Fallback**: Works without embeddings (graceful degradation)

### 2. Plan Trip (`POST /api/plan-trip`)
- **RAG**: Searches for places matching each interest
- **Context**: Provides up to 10 verified places for itinerary
- **Benefit**: Only suggests real places from knowledge base

### 3. Recommendations (`POST /api/recommendations`)
- **RAG**: Searches based on user profile and liked places
- **Context**: Provides up to 8 verified recommendations
- **Benefit**: Personalized suggestions from verified database

### 4. Destination Guide (`POST /api/destination-guide`) - NEW
- **RAG**: Searches for places in specified locations
- **Context**: Combines vector search + static knowledge base
- **Returns**: Comprehensive guide with foods, places, events, guides

**Request Format:**
```json
{
  "travel_style": "budget",
  "interests": ["temples", "food"],
  "locations": ["kathmandu", "pokhara"]
}
```

## Setup

### Prerequisites

1. **Generate Embeddings** (if not already done):
   ```bash
   python kathmandu_tourism_vectorizer.py
   ```
   This creates `tourism_embeddings.json`

2. **Install Dependencies**:
   ```bash
   pip install sentence-transformers numpy
   ```

### Verification

Run the test script:
```bash
python test_rag_integration.py
```

## Configuration

### Vector Search Parameters

In `ai_service.py`, you can adjust:

- **`top_k`**: Number of results to retrieve (default: 3-10)
- **`min_score`**: Minimum similarity threshold (default: 0.25-0.3)
- **`max_places`**: Max places in context (default: 3-15)

### Embedding Model

Currently using: `all-MiniLM-L6-v2` (384 dimensions)

To change, update `EMBEDDING_MODEL` in `vector_search.py` and regenerate embeddings.

## Benefits

✅ **Accurate**: Only suggests verified places from knowledge base  
✅ **Contextual**: Understands semantic meaning, not just keywords  
✅ **Personalized**: Finds places matching user's vibe/interests  
✅ **Graceful**: Works even if embeddings aren't loaded  
✅ **Scalable**: Can easily add more places to knowledge base  

## Troubleshooting

### "Vector search not available"
- Check if `tourism_embeddings.json` exists
- Run `kathmandu_tourism_vectorizer.py` to generate embeddings
- System will work without RAG (graceful degradation)

### Low-quality results
- Adjust `min_score` threshold (lower = more results)
- Increase `top_k` for more context
- Check if embeddings were generated correctly

### Performance issues
- Reduce `top_k` and `max_places` in context
- Consider using a vector database (Pinecone/Qdrant) for large datasets
- Current implementation uses in-memory search (fine for <1000 places)

## Future Enhancements

- [ ] Add vector database integration (Pinecone/Qdrant)
- [ ] Implement hybrid search (keyword + semantic)
- [ ] Add caching for frequent queries
- [ ] Support multiple embedding models
- [ ] Add relevance feedback learning
