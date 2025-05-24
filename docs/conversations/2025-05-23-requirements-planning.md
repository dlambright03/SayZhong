# Requirements Planning Discussion - 2025-05-23

## Topic
Creating a requirements.md file for SayZhong - a Python Streamlit app for English speakers learning Mandarin.

## Research Available
- `/docs/research/methods.md`: Effective Mandarin learning methods
- `/docs/research/software.md`: Existing Mandarin learning software analysis

## Key Questions for Requirements Definition

Based on the research provided, I need the following information to create an accurate requirements.md:

### 1. Target Audience & Learning Level
- Primary user: Complete beginners or multiple proficiency levels?
- Age group focus?

### 2. Core Learning Focus Priority
From research, most effective methods are:
- Pronunciation and tones (critical)
- Conversational practice
- Audio-based learning
- Spaced repetition vocabulary

Which should be MVP primary focus?

### 3. Unique Value Proposition
Existing apps (HelloChinese, Duolingo, Rocket Chinese) already exist.
What makes SayZhong different?

### 4. Technical Scope for MVP
Which features to prioritize first in Streamlit:
- Tone practice with audio feedback?
- Vocabulary flashcards with spaced repetition?
- Basic conversation scenarios?
- Character writing practice?
- Progress tracking?

### 5. Content Strategy
- Create own content or integrate existing APIs/datasets?
- Need native speaker audio recordings?
- Include cultural context?

## Additional Research Needed
1. Voice/Audio Technology for Mandarin
2. Mandarin Language Data sources
3. Streamlit capabilities for language learning

## Next Steps
Await user responses to questions, then create requirements.md plan for approval.

## User Responses

### 1. Target Audience & Learning Level
**User Answer:** English speakers that want to learn Mandarin

### Recommendations Based on Research

Based on the research in `docs/research/methods.md` and `docs/research/software.md`, here are my recommendations:

#### 2. Core Learning Focus Priority
**Recommendation:** **Pronunciation and Tones** as MVP primary focus
- Research shows this is critical for Mandarin - "Without mastering tones, even basic conversations can become confusing or unintelligible"
- Most existing apps are weak in this area (Duolingo has "weak tone instruction")
- Aligns with research emphasis on audio-based learning

#### 3. Unique Value Proposition
**Recommendation:** Focus on **Tone Mastery with Real-time Feedback**
- Research gap: Existing apps have limited tone instruction
- HelloChinese is good but "less suitable for advanced learners"
- SayZhong could specialize in tone accuracy with immediate audio feedback

#### 4. Technical Scope for MVP
**Recommendation Priority Order:**
1. **Tone practice with audio feedback** (primary differentiator)
2. **Basic vocabulary with tone emphasis** (foundation building)
3. **Simple progress tracking** (user engagement)
4. **Basic conversation scenarios** (future expansion)

#### 5. Content Strategy
**Recommendation:** 
- Start with **curated vocabulary datasets** (open source)
- **Record own audio** for consistent tone examples
- Focus on **high-frequency words** from research (spaced repetition principle)

#### Additional Research Needed Before Requirements
1. **Python audio libraries** for tone detection/feedback
2. **Mandarin datasets** with tone markings
3. **Streamlit audio capabilities** for recording/playback

Do you approve these recommendations to proceed with requirements.md creation?

## User Clarification & Direction Change

**User Input:** "I dont want to do anything involving audio, it should all be text based. Is there any places that we could leverage AI agents?"

### Revised Recommendations Based on Text-Only Approach

#### 2. Core Learning Focus Priority (REVISED)
**New Recommendation:** **Visual Tone Recognition & Character Learning**
- Focus on **text-based tone visualization** (tone marks, color coding)
- **Character stroke order and structure** (visual learning)
- **Pinyin with tone marks** emphasis
- Research shows spaced repetition is effective - perfect for text-based flashcards

#### 3. Unique Value Proposition (REVISED)
**New Recommendation:** **AI-Powered Personalized Learning Paths**
- **AI tutoring agent** that adapts to user's learning pace
- **Smart spaced repetition** using AI to optimize review timing
- **Context-aware explanations** of grammar and usage
- **AI conversation partner** for text-based dialogue practice

#### 4. Technical Scope for MVP (REVISED)
**New Priority Order:**
1. **AI-powered flashcards with spaced repetition** (core learning engine)
2. **Visual tone learning** (color-coded pinyin, tone pattern recognition)
3. **AI conversation scenarios** (text-based chat with AI tutor)
4. **Progress tracking with AI insights** (personalized recommendations)

#### AI Agent Opportunities Based on Research
1. **Adaptive Learning AI**: Analyzes user performance to adjust difficulty
2. **Conversational AI Tutor**: Provides explanations and answers questions
3. **Content Curation AI**: Selects optimal vocabulary based on user level
4. **Progress Analysis AI**: Identifies weak areas and suggests focus topics

#### 5. Content Strategy (REVISED)
- **Curated text datasets** with pinyin and tone marks
- **AI-generated practice scenarios** for conversation
- **Smart content progression** based on research's spaced repetition principles

Do you approve this revised text-based + AI approach for requirements.md creation?

## Additional User Input

**User Input:** "To help with tones, maybe include phonetic pronunciations along with the pinyin"

### Enhanced Tone Learning Approach

**Excellent addition!** This aligns perfectly with the research showing tone mastery is critical. Enhanced recommendation:

#### Visual Tone Learning (ENHANCED)
1. **Pinyin with tone marks** (mā, má, mǎ, mà)
2. **Phonetic pronunciation guides** (English approximations: "mah" rising, "mah" falling)
3. **Color-coded tone visualization** (tone 1: red, tone 2: yellow, etc.)
4. **Tone pattern graphics** (visual curves showing pitch changes)

#### AI Agent Enhancement for Tones
- **AI Phonetic Tutor**: Generates English phonetic approximations for tone practice
- **Tone Pattern Recognition AI**: Helps users understand tone relationships
- **Contextual Tone Explanations**: AI explains why tone changes meaning

This multi-modal text approach (pinyin + phonetics + colors + patterns) addresses the research gap in existing apps' "weak tone instruction" while remaining completely text-based.

**Ready to create requirements.md with this enhanced tone learning approach?**

## Final User Input

**User Input:** "I think for tone learning 1 and 2 should be enough. I dont think we need colors or visual curves"

### Final Tone Learning Approach (SIMPLIFIED)

**Agreed!** Keeping it simple and focused. Final approach:

#### Visual Tone Learning (FINAL)
1. **Pinyin with tone marks** (mā, má, mǎ, mà)
2. **Phonetic pronunciation guides** (English approximations: "mah" rising, "mah" falling)

#### AI Agent Focus for Tones
- **AI Phonetic Tutor**: Generates English phonetic approximations for tone practice
- **Contextual Tone Explanations**: AI explains why tone changes meaning

This simplified text approach (pinyin + phonetics) directly addresses the research gap in existing apps' "weak tone instruction" while staying clean and user-friendly.

**Proceeding to create requirements.md with this finalized approach.**

## Final User Input

**User Input:** "I do think the approach of learning common vocabulary and pronunciation is important first"

### Confirmed Final Approach

**Perfect alignment with research!** The research emphasizes:
- **High-frequency words** for effective spaced repetition
- **Pronunciation and tones** as critical foundation
- **Vocabulary building** as core learning method

Final MVP priority confirmed:
1. **Common vocabulary with pronunciation** (pinyin + phonetics)
2. **AI-powered spaced repetition** for vocabulary retention
3. **Text-based tone learning** (simplified approach)
4. **AI conversation scenarios** for practice

**Creating requirements.md now with this research-backed approach.**
