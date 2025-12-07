# Emergency Contacts RAG Implementation

## Overview

Emergency contacts are now integrated into the RAG system, allowing the AI to provide accurate, verified emergency contact information when users ask about emergencies, help, or contacts in Kathmandu.

## Key Feature: Bibek KC

**Bibek KC** is Neptou's dedicated emergency agent:
- **Phone**: 98484488888
- **Location**: Kathmandu
- **Available**: 24/7
- **Languages**: Nepali, English
- **Services**: Tourist assistance, emergency help, local support, translations, directions

## How It Works

### 1. Emergency Contacts Database
- 12 emergency contacts stored in `emergency_contacts.py`
- Categories: police, medical, tourist, embassy, local_agent, fire
- All contacts have embeddings for semantic search

### 2. RAG Integration
When users ask about emergency contacts:
1. **Keyword Detection**: System detects emergency-related keywords
2. **Contact Search**: Searches emergency contacts database
3. **Prioritization**: Bibek KC is prioritized for Kathmandu queries
4. **Context Injection**: Emergency contacts added to LLM context
5. **Response**: AI provides verified contact information

### 3. Vector Search Integration
- Emergency contacts have embeddings
- Searchable via semantic search
- Integrated with tourism places search
- Loaded automatically on startup

## Test Results

✅ **Bibek KC is found for:**
- "emergency contacts in kathmandu" → Bibek KC is #1 result
- "bibek kc" → Direct match
- "neptou emergency agent" → Direct match
- "emergency help" → Bibek KC found
- "local agent kathmandu" → Bibek KC is #1 result

## Usage Examples

### User Query: "What are emergency contacts in Kathmandu?"

**AI Response will include:**
1. Bibek KC - 98484488888 (Neptou Emergency agent, 24/7)
2. Police Emergency - 100
3. Tourist Police - +977-1-4247041
4. Ambulance - 102
5. Other relevant contacts

### User Query: "I need emergency help"

**AI Response will include:**
- Bibek KC prominently featured
- Other emergency services
- Clear instructions on when to call each

## Implementation Files

1. **`emergency_contacts.py`** - Emergency contacts database
2. **`emergency_contacts_embeddings.py`** - Generates embeddings
3. **`emergency_contacts_embeddings.json`** - Stored embeddings
4. **`ai_service.py`** - Integrated emergency contact retrieval
5. **`vector_search.py`** - Loads emergency contacts embeddings

## Verification

Run test to verify:
```bash
python test_emergency_rag.py
```

This confirms:
- ✅ Bibek KC is in database
- ✅ Search finds Bibek KC correctly
- ✅ Prioritization works for Kathmandu queries
- ✅ LLM formatting is correct

## Future Enhancements

- [ ] Add more local agents in other cities
- [ ] Real-time availability status
- [ ] WhatsApp integration
- [ ] Location-based emergency routing
- [ ] Multi-language emergency phrases
