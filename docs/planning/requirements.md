# SayZhong Requirements Document

## Project Overview

**SayZhong** is a Python 3.11 Streamlit application designed to help English speakers learn Mandarin Chinese through text-based, AI-powered interactive learning experiences.

### Target Audience
- English speakers who want to learn Mandarin Chinese
- Beginners to intermediate learners
- Users who prefer text-based learning over audio-based approaches

## Unique Value Proposition

SayZhong differentiates itself from existing Mandarin learning apps (HelloChinese, Duolingo, Rocket Chinese) by:

1. **AI-Powered Personalized Learning**: Adaptive learning paths that adjust to individual user progress
2. **Text-Based Tone Mastery**: Simplified, effective tone learning using pinyin and phonetic pronunciations
3. **Smart Vocabulary Focus**: Emphasis on common, high-frequency words with optimized spaced repetition
4. **AI Conversation Partner**: Text-based dialogue practice with contextual explanations

## Core Learning Philosophy

Based on research in `docs/research/methods.md` and `docs/research/software.md`, SayZhong focuses on:

- **Common vocabulary and pronunciation first** (foundation building)
- **Tone mastery as critical** for meaningful communication
- **Spaced repetition effectiveness** for long-term retention
- **Conversational practice** for practical application

## MVP Features (Priority Order)

### 1. AI-Powered Vocabulary Learning
- **Smart flashcards** with AI-optimized spaced repetition
- **High-frequency vocabulary** focus based on learning research
- **Pinyin with tone marks** (mā, má, mǎ, mà)
- **Phonetic pronunciation guides** (English approximations)
- **Progress tracking** with AI insights

### 2. Text-Based Tone Learning
- **Simplified tone visualization** using pinyin tone marks
- **Phonetic pronunciation guides** for English speakers
- **AI Phonetic Tutor** that generates English approximations
- **Contextual tone explanations** showing meaning changes

### 3. AI Conversation Scenarios
- **Text-based chat** with AI tutor
- **Practical dialogue practice** scenarios
- **Context-aware explanations** of grammar and usage
- **Adaptive difficulty** based on user performance

### 4. Progress Analytics
- **AI-powered progress analysis** identifying weak areas
- **Personalized recommendations** for focus topics
- **Learning streak tracking** for engagement
- **Performance insights** and study suggestions

## Technical Requirements

### Core Technology Stack
- **Python 3.11** (primary development language)
- **Streamlit** (web application framework)
- **Semantic Kernel** (AI orchestration and integration framework)
- **Azure OpenAI Service** (GPT models for conversational AI and content generation)
- **Azure Data Lake Storage Gen2** (persistent data storage for user progress and content)
- **Chinese Text Processing Libraries** (jieba, pypinyin for language support)

### AI/ML Architecture
- **Semantic Kernel Framework**: Orchestrates AI interactions and maintains conversation memory
- **Azure OpenAI Integration**: Powers conversational AI tutor and adaptive learning
- **Function Calling**: Enables structured AI responses for educational content
- **Memory Management**: Maintains learning context across sessions
- **Plugin Architecture**: Extensible AI modules for different learning features

### State Management Strategy
1. **Session State Layer**: `st.session_state` for current UI state and active learning session
2. **Custom State Manager**: Bridge component between Streamlit and Azure Data Lake
3. **Persistent Storage Layer**: Azure Data Lake for user progress, vocabulary data, and learning analytics
4. **AI Memory Layer**: Semantic Kernel memory for conversation context and learning history

### Data Storage Architecture
**Azure Data Lake Structure**:
```
/users/{user_id}/
  /progress/
    vocabulary_progress.json
    lesson_completion.json
    performance_metrics.json
  /sessions/
    session_logs.json
/content/
  /vocabulary/
    high_frequency_words.json
    lessons_data.json
  /conversations/
    scenario_templates.json
```

### AI Agent Components
1. **Adaptive Learning AI**: Analyzes user performance using Azure OpenAI to adjust difficulty
2. **Conversational AI Tutor**: Semantic Kernel-powered chat for explanations and Q&A
3. **Content Curation AI**: Azure OpenAI selects optimal vocabulary based on user level
4. **Progress Analysis AI**: Identifies weak areas and generates personalized recommendations
5. **Phonetic Tutor AI**: Generates English phonetic approximations for tone practice

### Integration Architecture
```
Streamlit UI ↔ Custom State Manager ↔ Azure Data Lake Storage
            ↔ Semantic Kernel ↔ Azure OpenAI Service
```

### Development Methodology
- **Test Driven Development (TDD)** approach
- **Tests in `tests/` directory** for all new features including AI integration
- **Code coverage requirements** for quality assurance (>90%)
- **Azure SDK integration** for cloud services
- **Semantic Kernel testing** for AI agent reliability

## Content Requirements

### Vocabulary Data
- **Curated high-frequency word lists** with pinyin and tone marks
- **English translations** and contextual usage examples
- **Phonetic pronunciation guides** for English speakers
- **Progressive difficulty levels** from basic to intermediate

### Learning Content
- **AI-generated practice scenarios** for conversation
- **Grammar explanations** with contextual examples
- **Cultural context** where relevant for understanding
- **Smart content progression** based on spaced repetition research

### Data Sources Strategy
- **Open-source Mandarin datasets** with proper licensing stored in Azure Data Lake
- **Curated vocabulary lists** focused on conversational Mandarin (HSK levels 1-4)
- **Custom content creation** for phonetic guides and explanations
- **Azure Data Lake hierarchical storage** for scalable content management
- **Semantic Kernel content plugins** for dynamic AI-generated practice scenarios

### Technical Data Requirements
- **User Authentication**: Azure AD integration for secure access
- **Data Persistence**: Azure Data Lake Storage Gen2 for reliability and analytics
- **State Synchronization**: Custom state manager for Streamlit-Azure integration
- **AI Context Management**: Semantic Kernel memory for conversation continuity
- **Performance Optimization**: Caching strategies for vocabulary and content delivery

## User Experience Requirements

### Interface Design
- **Clean, text-focused interface** optimized for learning
- **Intuitive navigation** between learning modules
- **Mobile-responsive design** for accessibility
- **Minimal cognitive load** to focus on learning content

### Learning Flow
- **Onboarding assessment** to determine starting level
- **Daily learning sessions** with AI-optimized content
- **Progress visualization** showing advancement
- **Achievement system** for motivation

## Success Criteria

### MVP Success Metrics
- **User engagement**: Daily active learning sessions
- **Learning effectiveness**: Vocabulary retention rates
- **Feature adoption**: Usage of tone learning and AI conversation
- **User satisfaction**: Feedback on learning experience

### Technical Success Criteria
- **Performance**: Fast response times for AI interactions (<2 seconds)
- **Reliability**: Stable application with minimal downtime (99%+ uptime)
- **Scalability**: Support for growing user base with Azure cloud scaling
- **Code quality**: Comprehensive test coverage (>90%)
- **AI Reliability**: Consistent and accurate AI responses for educational content
- **Data Security**: Azure-compliant user data protection and privacy

## Technical Implementation Details

### Required Python Packages
- **semantic-kernel**: AI orchestration framework
- **azure-storage-file-datalake**: Azure Data Lake integration
- **azure-identity**: Azure authentication
- **streamlit**: Web application framework
- **jieba**: Chinese text segmentation
- **pypinyin**: Pinyin conversion and tone handling
- **pytest**: Testing framework

### Azure Services Configuration
- **Azure OpenAI Service**: GPT-4 model deployment for conversational AI
- **Azure Data Lake Storage Gen2**: Hierarchical data storage
- **Azure Active Directory**: User authentication and authorization
- **Azure Monitor**: Application performance monitoring

### State Management Implementation
```python
# Custom State Manager Bridge
class SayZhongStateManager:
    def __init__(self):
        self.session_state = st.session_state
        self.azure_storage = AzureDataLakeClient()
        self.semantic_kernel = SemanticKernel()
    
    def sync_user_progress(self, user_id):
        # Sync between Streamlit session and Azure storage
        pass
    
    def get_ai_context(self, user_id):
        # Retrieve conversation context from Semantic Kernel
        pass
```

### Semantic Kernel Plugin Architecture
- **VocabularyPlugin**: Manages vocabulary learning and spaced repetition
- **TonePlugin**: Handles tone learning with phonetic approximations
- **ConversationPlugin**: Powers AI conversation scenarios
- **ProgressPlugin**: Analyzes learning progress and recommendations

## Future Expansion Opportunities

### Phase 2 Features
- **Character writing practice** (visual stroke order)
- **Advanced conversation scenarios** with cultural context
- **Community features** for learner interaction
- **Mobile app development** for enhanced accessibility

### Integration Possibilities
- **Voice synthesis** for pronunciation examples (future audio support)
- **Learning management systems** for educational institutions
- **Progress sharing** with tutors or learning partners

## Research Foundation

This requirements document is based on comprehensive research:

- **Learning Methods Research** (`docs/research/methods.md`): Evidence-based approaches for English speakers learning Mandarin
- **Software Analysis** (`docs/research/software.md`): Competitive analysis of existing Mandarin learning applications
- **User Requirements Discussion** (`docs/conversations/2025-05-23-requirements-planning.md`): Detailed planning conversation and decision rationale

## Development Phases

### Phase 1: MVP Core Features
1. Basic vocabulary flashcards with spaced repetition
2. Text-based tone learning with pinyin and phonetics
3. Simple progress tracking
4. Basic AI conversation scenarios

### Phase 2: AI Enhancement
1. Advanced adaptive learning algorithms
2. Sophisticated conversation AI
3. Detailed progress analytics
4. Personalized learning path optimization

### Phase 3: Advanced Features
1. Extended vocabulary and content library
2. Advanced conversation scenarios
3. Community and social features
4. Mobile application development

---

*This requirements document serves as the foundation for SayZhong development and should be updated as features are implemented and user feedback is incorporated.*
