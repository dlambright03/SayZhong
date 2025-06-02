# Conversational Mandarin Focus Update - June 2, 2025

**Date**: June 2, 2025  
**Conversation Type**: Epic Planning Update  
**Context**: Updating Epic 000 (Proof of Concept) to focus on conversational Mandarin learning

## User Request
User clarified the learning goal: conversational Mandarin (not reading/writing), eliminating Chinese characters, using pinyin with tone markings, and adding English phonetic approximations for pronunciation guidance.

## Changes Made

### Removed Components
- Chinese characters (simplified and traditional)
- Visual tone learning system (Feature 000.3) - pinyin tone markings handle this
- Character component breakdown
- Reading/writing complexity

### Enhanced Components
- **English phonetic approximations** for pronunciation guidance
- **Conversational scenarios** expanded to 7-10 common speaking situations
- **Speaking confidence tracking** and progression analytics
- **Pronunciation guidance** through AI-powered phonetic approximations

### Updated Features

#### Feature 000.2: Core Vocabulary Learning System (8 story points)
- Format: Pinyin (tone marked) + English + Phonetic approximation
- Example: nǐ hǎo → "hello" → "nee how" (sounds like "knee" + "how")
- Focus on 1000 most common **spoken** Chinese words
- Conversational context emphasis

#### Feature 000.3: Conversational AI with Pronunciation Focus (10 story points)
- 7-10 conversation scenarios for common speaking situations
- Pronunciation tips using English phonetic approximations
- Speaking confidence building through progressive difficulty
- Cultural context for conversational etiquette

#### Feature 000.4: Conversational Comprehension Analytics (4 story points)
- Conversational mastery tracking
- Speaking confidence progression analytics
- Pronunciation accuracy self-assessment
- Conversational context retention measurement

#### Feature 000.5: Demo and Presentation Ready (3 story points)
- Focus on conversational learning effectiveness
- Phonetic approximation examples showcase
- Speaking vocabulary statistics

### Technology Stack Updates
- Removed tone visualization components
- Added phonetic approximation generation via Azure OpenAI
- Enhanced conversational AI prompts for pronunciation guidance
- Focus on conversational flow visualization

### Success Metrics Updates
- **Conversational Mastery**: 50+ words to "conversational confidence" per session
- **Phonetic Approximation Quality**: 4.5+ star rating for pronunciation helpfulness
- **Learning Effectiveness**: 80%+ retention for spoken words in conversational context

## Files Updated
- `/workspaces/SayZhong/docs/planning/epics/epic-000-proof-of-concept.md`

## Impact on Project
This change transforms the POC into a purely conversational learning tool, removing the complexity of Chinese character recognition while maintaining effective pronunciation guidance through English phonetic approximations. The approach aligns with spoken language learning goals and should be more accessible to English speakers.

## Data Requirements
Need to source/create dataset with:
- 1000 most common spoken Chinese words
- Accurate pinyin with tone markings (mā, má, mǎ, mà, ma)
- English translations
- English phonetic approximations (possibly AI-generated and validated)

## Next Steps
1. Source spoken Chinese vocabulary dataset with frequency rankings
2. Develop English phonetic approximation system (potentially using Azure OpenAI)
3. Design conversational scenarios for common speaking situations
4. Create pronunciation guidance UI without audio dependency
