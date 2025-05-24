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

## Learning Session Optimization

### Optimal Session Structure (Based on Research)
Following research from `docs/research/optimal_learning.md`:

| Time Segment | Activity | Focus Area |
|--------------|----------|------------|
| 0-5 minutes | **Review Phase** | Spaced repetition flashcards (vocabulary, tones) |
| 5-15 minutes | **Core Learning** | New vocabulary or grammar with AI explanations |
| 15-25 minutes | **Practice Phase** | AI conversation scenarios or contextual exercises |
| 25-30 minutes | **Consolidation** | Progress review and next session preparation |

### Session Frequency and Duration
- **Recommended Duration**: 25-30 minutes per session (aligned with Pomodoro technique)
- **Daily Frequency**: 1-2 sessions for optimal progress
- **Weekly Structure**: Rotate focus areas (character learning, pronunciation, conversation, review)
- **Break Integration**: 5-minute breaks between sessions to prevent cognitive fatigue

## Assessment and Proficiency Standards

### HSK Alignment Strategy
Based on research from `docs/research/assessment_methods.md`:

| HSK Level | Vocabulary Count | SayZhong Integration |
|-----------|------------------|---------------------|
| HSK 1 | 150 words | Foundation vocabulary with tone mastery |
| HSK 2 | 300 words | Conversational scenarios introduction |
| HSK 3 | 600 words | Complex grammar and cultural context |
| HSK 4 | 1200 words | Advanced conversation and reading comprehension |

### Progress Assessment Methods
- **LexCHI Integration**: Quick vocabulary-based proficiency estimates
- **ACTFL Framework Alignment**: Speaking, listening, reading, and writing skill assessment
- **Self-Assessment Tools**: Regular progress check-ins with AI-powered recommendations
- **Performance Analytics**: Detailed tracking of vocabulary retention rates and conversation fluency

## Gamification Framework

### Research-Based Engagement Strategies
Implementing findings from `docs/research/gamification.md`:

#### Core Gamification Elements
- **Points System**: Earned through vocabulary mastery, conversation completion, and consistent practice
- **Achievement Badges**: Tone mastery, vocabulary milestones, conversation fluency, cultural knowledge
- **Progress Levels**: HSK-aligned advancement with unlockable content
- **Streak Tracking**: Daily practice consistency with motivational rewards

#### Advanced Engagement Features
- **Immediate Feedback**: Real-time corrections and explanations during learning
- **Adaptive Challenges**: AI-generated quests based on individual learning gaps
- **Story-Based Learning**: Contextual scenarios with narrative progression
- **Cultural Unlocks**: Access to cultural content and context as rewards for progress

### Learning Content
- **AI-generated practice scenarios** for conversation based on real-world contexts
- **Grammar explanations** with contextual examples using high-frequency vocabulary
- **Cultural context** integration where relevant for understanding nuanced usage
- **Smart content progression** using research-backed spaced repetition algorithms
- **Adaptive difficulty adjustment** based on user performance analytics and learning patterns

### Data Sources Strategy
- **Open Language Profiles (Zero to Hero)**: Primary vocabulary source with HSK-aligned content under CC-BY-SA license
- **CC-CEDICT Integration**: Community-maintained Chinese-English dictionary for comprehensive definitions
- **HSK Structured Curriculum**: Official vocabulary lists (HSK 1-4) for progressive difficulty levels
- **Custom Phonetic Content**: English approximation guides specifically developed for tone learning
- **Azure Data Lake Hierarchical Storage**: Scalable content management with organized vocabulary, lessons, and user progress
- **Semantic Kernel Content Plugins**: Dynamic AI-generated practice scenarios with contextual relevance

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
- **Initial Assessment**: HSK-aligned proficiency evaluation to determine optimal starting level
- **Structured Daily Sessions**: 25-30 minute focused learning periods following Pomodoro technique research
- **Gamified Progress System**: Points, badges, and streak tracking based on gamification research
- **Progress Visualization**: Real-time advancement tracking with weak area identification
- **Achievement Milestones**: HSK level progression markers with cultural context rewards

## Success Criteria

### MVP Success Metrics

#### Learning Effectiveness Metrics
- **Vocabulary Retention Rate**: >85% retention after 1 week using spaced repetition
- **Tone Accuracy Improvement**: Measurable improvement in tone recognition within 2 weeks
- **Session Completion Rate**: >80% of users completing recommended 25-30 minute sessions
- **HSK Level Progression**: Users advancing one HSK level within 3 months of consistent use

#### User Engagement Metrics
- **Daily Active Users**: Consistent daily learning sessions with >70% week-over-week retention
- **Feature Adoption**: >60% usage of tone learning and AI conversation features
- **Learning Streak Maintenance**: >50% of users maintaining 7+ day learning streaks
- **Session Frequency**: Average 5+ sessions per week per active user

#### User Satisfaction Metrics
- **Net Promoter Score (NPS)**: Target score of 50+ indicating strong user recommendation likelihood
- **Feature Satisfaction**: >4.0/5.0 rating for core features (vocabulary, tone learning, AI conversations)
- **User Feedback Quality**: Constructive feedback leading to iterative improvements
- **Support Request Volume**: <5% of users requiring technical support per month

### Technical Success Criteria

#### Performance Benchmarks
- **AI Response Time**: <2 seconds for AI conversation and explanation generation
- **Application Load Time**: <3 seconds for initial page load on standard internet connections
- **Session State Persistence**: 100% reliability in maintaining user progress across sessions
- **Data Synchronization**: <1 second latency for progress updates to Azure Data Lake

#### Reliability and Scalability
- **Application Uptime**: 99.5%+ availability with minimal planned downtime
- **Concurrent User Support**: Handle 100+ simultaneous users without performance degradation
- **Data Backup and Recovery**: 99.9% data integrity with automated backup procedures
- **Azure Service Integration**: Seamless operation with all Azure services under normal load

#### Code Quality and Maintenance
- **Test Coverage**: >90% code coverage with comprehensive unit and integration tests
- **AI Response Accuracy**: >95% appropriate and educational responses from AI agents
- **Security Compliance**: Zero critical security vulnerabilities and regular security audits
- **Documentation Quality**: Complete API documentation and user guides

### Long-term Success Indicators

#### Educational Impact
- **Learning Outcome Validation**: Independent assessment showing measurable Mandarin proficiency gains
- **User Skill Transfer**: Demonstrated ability to use learned vocabulary in real-world contexts
- **Retention Beyond Platform**: Users continuing Mandarin study beyond initial platform use
- **Educational Institution Adoption**: Integration requests from formal educational providers

#### Platform Growth and Sustainability
- **User Base Growth**: Sustained monthly user growth with organic referrals
- **Feature Request Quality**: User-driven feature requests indicating engagement and vision alignment
- **Community Development**: User-generated content and peer-to-peer learning interactions
- **Revenue Model Validation**: Sustainable financial model supporting continued development

## Technical Implementation Details

### Required Python Packages
- **semantic-kernel**: AI orchestration framework for Azure OpenAI integration
- **azure-storage-file-datalake**: Azure Data Lake Storage client library
- **azure-identity**: Azure authentication and credential management
- **streamlit**: Web application framework with session state management
- **jieba**: Chinese text segmentation for vocabulary processing
- **pypinyin**: Pinyin conversion with tone mark support and phonetic approximations
- **hanlp** (optional): Advanced Chinese NLP capabilities for content analysis
- **pytest**: Comprehensive testing framework for AI agent reliability
- **streamlit-authenticator**: Enhanced authentication for user session management

### Azure Services Configuration
- **Azure OpenAI Service**: GPT-4 model deployment for conversational AI
- **Azure Data Lake Storage Gen2**: Hierarchical data storage
- **Azure Active Directory**: User authentication and authorization
- **Azure Monitor**: Application performance monitoring

## Data Security and Privacy

### User Data Protection
- **Azure AD Integration**: Secure user authentication with multi-factor authentication support
- **Data Encryption**: End-to-end encryption for user progress and personal information
- **GDPR Compliance**: User data rights, deletion capabilities, and consent management
- **Privacy by Design**: Minimal data collection with explicit user consent

### Educational Data Privacy
- **FERPA Compliance**: Educational record privacy protection for institutional use
- **Student Data Protection**: Anonymized analytics and aggregated reporting
- **Parental Controls**: Age-appropriate data handling for younger learners
- **Data Retention Policies**: Clear guidelines for user data lifecycle management

### Security Architecture
- **Azure Security Standards**: Implementation of Azure security best practices
- **Secure API Communications**: HTTPS encryption for all data transmission
- **Access Control**: Role-based permissions for different user types
- **Audit Logging**: Comprehensive logging for security monitoring and compliance

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

### Phase 4: Advanced Learning Features (Future)
- **Character Writing Practice**: Visual stroke order with handwriting recognition
- **Audio Integration**: Text-to-speech with native speaker pronunciation examples
- **Advanced Cultural Context**: Regional dialects and cultural nuance explanations
- **Community Features**: Peer learning networks and conversation exchange

### Phase 5: Platform Expansion (Future)
- **Mobile Application**: Native iOS/Android apps with offline capabilities
- **VR/AR Integration**: Immersive cultural context and pronunciation practice
- **Educational Institution Integration**: LMS compatibility and progress sharing
- **Advanced Analytics**: Machine learning-powered learning path optimization

### Integration Possibilities
- **Learning Management Systems**: Integration with educational institutions
- **Language Exchange Platforms**: Connection with native speaker conversation partners
- **Cultural Content Platforms**: Partnership with Chinese cultural content providers
- **Assessment Services**: Integration with formal HSK testing preparation

## Research Gaps and Future Research Needs

### Identified Gaps from Research Analysis
Based on comprehensive review of all research files, the following areas need additional research:

#### Content and Methodology Gaps
- **Regional Dialect Integration**: Research needed on incorporating regional pronunciation variations
- **Advanced Grammar Pedagogy**: Deeper research on optimal grammar instruction sequencing
- **Cultural Context Integration**: Best practices for embedding cultural learning in language apps
- **Long-term Retention Studies**: Longitudinal effectiveness studies of text-based learning approaches

#### Technical Implementation Gaps
- **Streamlit Performance at Scale**: Research needed on handling large user bases
- **Advanced AI Conversation**: More sophisticated dialogue management beyond basic scenarios
- **Cross-platform State Synchronization**: Research on seamless multi-device learning experiences
- **Accessibility Features**: Research on supporting learners with different abilities and learning styles

#### Assessment and Analytics Gaps
- **Real-time Proficiency Modeling**: Dynamic assessment of user ability during learning
- **Predictive Learning Analytics**: Early identification of learning difficulties
- **Personalization Optimization**: Fine-tuning AI recommendations for individual learning styles
- **Cross-cultural Learning Patterns**: Research on different cultural approaches to Mandarin learning

### Recommended Future Research Topics
1. **Comparative Effectiveness Studies**: SayZhong approach vs. traditional audio-based methods
2. **Optimal AI Conversation Design**: Best practices for educational chatbot interactions
3. **Spaced Repetition Algorithm Optimization**: Custom algorithms for Mandarin-specific learning
4. **User Engagement Long-term Studies**: Factors affecting sustained learning motivation

## Research Foundation

This requirements document is based on comprehensive research across 13 specialized research files:

### Learning Methodology Research
- **Learning Methods** (`docs/research/methods.md`): Evidence-based approaches emphasizing tone mastery and spaced repetition
- **Assessment Methods** (`docs/research/assessment_methods.md`): HSK levels, ACTFL standards, and LexCHI proficiency measurements
- **Optimal Learning Sessions** (`docs/research/optimal_learning.md`): 25-30 minute focused sessions with Pomodoro technique
- **Gamification Strategies** (`docs/research/gamification.md`): Points/badges systems, immediate feedback, and adaptive learning paths

### Technical Implementation Research
- **Chinese Text Processing** (`docs/research/chinese_processing.md`): Jieba, pypinyin, HanLP, and THULAC libraries
- **Streamlit Capabilities** (`docs/research/streamlit.md`): Session state management, custom components, and performance optimization
- **Database Solutions** (`docs/research/database_tracking.md`): Azure Data Lake hierarchical storage for scalable user progress tracking
- **Phonetic Systems** (`docs/research/phonetic_approximations.md`): Hanyu Pinyin as the optimal standard for English speakers

### Content and Data Research
- **Vocabulary Datasets** (`docs/research/mandarin_vocab_datasets.md`): Open Language Profiles, CC-CEDICT, and HSK level data
- **Spaced Repetition Systems** (`docs/research/spaced_repetion.md`): Mandarin Blueprint, Pandanese, and Anki algorithms
- **Hybrid Learning Plans** (`docs/research/hybrind_learning_plan.md`): Combined approaches for character visualization and contextual learning
- **Sample Study Plans** (`docs/research/sample_study_plan.md`): Weekly structure with targeted daily skill focus

### Competitive Analysis
- **Software Comparison** (`docs/research/software.md`): Analysis of Rocket Chinese, HelloChinese, Duolingo limitations and opportunities

### Planning Documentation
- **Requirements Planning** (`docs/conversations/2025-05-23-requirements-planning.md`): Detailed user needs analysis
- **Technical Architecture** (`docs/conversations/2025-05-24-technical-research.md`): Technology stack implementation research

## Development Phases

### Phase 1: MVP Core Features (Weeks 1-8)
1. **Basic Vocabulary Learning**
   - HSK Level 1 vocabulary (150 words) with spaced repetition
   - Jieba and pypinyin integration for text processing
   - Azure Data Lake user progress storage setup
2. **Text-Based Tone Learning**
   - Hanyu Pinyin with tone marks implementation
   - English phonetic approximation system
   - AI-powered contextual tone explanations
3. **Simple Progress Tracking**
   - Session state management with Streamlit
   - Basic analytics dashboard
   - Learning streak and completion tracking
4. **Basic AI Conversation Scenarios**
   - Semantic Kernel integration with Azure OpenAI
   - Simple dialogue practice with contextual feedback

### Phase 2: Enhanced Learning System (Weeks 9-16)
1. **Advanced Spaced Repetition**
   - Hybrid algorithm combining Mandarin Blueprint and Anki approaches
   - Performance-based interval adjustment
   - Difficulty-based card sorting (Leitner system)
2. **Expanded Content Library**
   - HSK Levels 1-3 vocabulary (600+ words)
   - Structured conversation scenarios with cultural context
   - Grammar explanation integration
3. **Detailed Progress Analytics**
   - Azure Data Lake analytics queries
   - Personalized learning path recommendations
   - Weak area identification and targeted practice
4. **Advanced AI Features**
   - Semantic Kernel memory for conversation continuity
   - Adaptive content generation based on user performance
   - Real-time feedback and explanation system

### Phase 3: Advanced Features and Optimization (Weeks 17-24)
1. **Complete HSK 1-4 Integration**
   - Full vocabulary coverage (1200+ words)
   - Advanced conversation scenarios
   - Cultural context and practical usage examples
2. **Enhanced Gamification**
   - Comprehensive points and badges system
   - Social features and leaderboards (optional)
   - Achievement milestones with cultural rewards
3. **Performance Optimization**
   - Streamlit caching optimization
   - Azure Data Lake query optimization
   - Advanced session state management
4. **Assessment and Certification**
   - HSK-aligned assessment tools
   - Progress certification and reporting
   - Export capabilities for external use

---

*This requirements document serves as the foundation for SayZhong development and should be updated as features are implemented and user feedback is incorporated.*
