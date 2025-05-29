# ADR-010: Content Management & Curriculum Architecture

**Status:** Proposed  
**Date:** 2025-05-27  
**Deciders:** SayZhong Development Team  
**Technical Story:** Content Management & Curriculum Framework for Mandarin Learning

## Context

The SayZhong application requires a comprehensive content management and curriculum architecture to support effective Mandarin language learning. This architecture must handle Mandarin-specific content types, provide structured learning paths, support adaptive curriculum sequencing, and integrate with the learning effectiveness feedback loop (ADR-009).

### Key Requirements

1. **Mandarin-Specific Content Models**: Support for tones and pinyin
2. **Curriculum Framework**: Structured learning paths with skill trees and prerequisites
3. **Content Effectiveness Integration**: Track content performance and enable A/B testing
4. **Adaptive Sequencing**: Support dynamic curriculum adjustment based on learner progress
5. **Assessment Integration**: Support various assessment types for Mandarin proficiency

### Related ADRs

- **ADR-001**: AI Framework Architecture (Semantic Kernel integration)
- **ADR-003**: Data Storage Architecture (Azure Data Lake content storage)
- **ADR-008**: Performance & Scalability (content delivery optimization)
- **ADR-009**: Learning Effectiveness Feedback Loop (content effectiveness tracking)

## Decision

We will implement a multi-layered content management and curriculum architecture consisting of:

1. **Content Models Layer**: Mandarin-specific content structures
2. **Curriculum Framework Layer**: Learning path and skill tree management
3. **Content Effectiveness Layer**: Performance tracking and optimization
4. **Delivery Engine Layer**: Content sequencing and personalization

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Content Delivery Engine                  │
├─────────────────────────────────────────────────────────────┤
│  Curriculum Framework  │     Content Effectiveness         │
│  - Skill Trees         │     - Performance Analytics       │
│  - Learning Paths      │     - A/B Testing                 │
│  - Prerequisites       │     - Content Optimization        │
├─────────────────────────────────────────────────────────────┤
│                     Content Models Layer                    │
│  - Vocabulary   - Conversations  - Pronunciation - Grammar │
│  - Assessments  - Media                                    │
├─────────────────────────────────────────────────────────────┤
│              Storage Layer (Azure Data Lake)                │
└─────────────────────────────────────────────────────────────┘
```

## Content Models Layer

### Core Content Types

#### 1. Vocabulary Content
```python
@dataclass
class VocabularyItem:
    id: str
    simplified: str          # 简体字
    traditional: str         # 繁体字
    pinyin: str             # Standard pinyin with tone marks
    pinyin_numeric: str     # Pinyin with numeric tones (ma1, ma2...)
    phonetic_english: str   # English phonetic approximation (e.g., "mah" for ma1)
    tone_pattern: List[int] # [1, 2, 3, 4, 0] for neutral
    english_definitions: List[str]
    part_of_speech: str
    hsk_level: Optional[int]
    frequency_rank: Optional[int]
    usage_examples: List['ExampleUsage']
    audio_pronunciation: str  # Audio file reference
    difficulty_level: float
    learning_tags: List[str]
    created_at: datetime
    updated_at: datetime
```

#### 2. Conversation Content
```python
@dataclass
class ConversationContent:
    id: str
    title: str
    scenario: str           # Restaurant, Shopping, etc.
    dialogue_lines: List['DialogueLine']
    learning_objectives: List[str]
    prerequisite_vocabulary: List[str]  # VocabularyItem IDs
    difficulty_level: float
    estimated_duration: int  # minutes
    interaction_patterns: List['InteractionPattern']
    assessment_questions: List['AssessmentQuestion']
    audio_files: Dict[str, str]  # speaker_id -> audio_file
    video_content: Optional[str]
    created_at: datetime
    updated_at: datetime

@dataclass
class DialogueLine:
    speaker_id: str
    speaker_name: str
    chinese_text: str
    pinyin: str
    phonetic_english: str   # English phonetic approximation
    english_translation: str
    pronunciation_tips: Optional[str]
    tone_emphasis: List[int]  # Which characters to emphasize
    interaction_type: str     # question, response, statement
```

#### 3. Pronunciation Content
```python
@dataclass
class PronunciationContent:
    id: str
    target_sound: str      # The sound being taught
    sound_type: str        # tone, initial, final, combination
    native_audio: str      # Native speaker audio
    slow_audio: str        # Slowed down version
    tone_contour: Optional[List[float]]  # F0 frequency data
    mouth_position: Optional[str]  # Diagram/video reference
    similar_sounds: List[str]  # Confusing sounds
    practice_words: List[str]  # VocabularyItem IDs
    tongue_twisters: List[str]
    difficulty_level: float
    feedback_criteria: 'PronunciationFeedbackCriteria'
    created_at: datetime
    updated_at: datetime
```

### Assessment Content Models

```python
@dataclass
class AssessmentContent:
    id: str
    assessment_type: str   # vocabulary, listening, speaking, pronunciation
    title: str
    instructions: str
    questions: List['AssessmentQuestion']
    scoring_criteria: 'ScoringCriteria'
    time_limit: Optional[int]  # seconds
    prerequisite_content: List[str]  # Content IDs
    target_skills: List[str]
    difficulty_level: float
    adaptive_parameters: 'AdaptiveAssessmentConfig'
    created_at: datetime
    updated_at: datetime

@dataclass
class AssessmentQuestion:
    id: str
    question_type: str     # multiple_choice, audio_match, tone_recognition
    prompt: str
    chinese_text: Optional[str]
    audio_prompt: Optional[str]
    visual_prompt: Optional[str]
    answer_options: List['AnswerOption']
    correct_answer: str
    explanation: str
    difficulty_weight: float
    tags: List[str]
```

## Curriculum Framework Layer

### Skill Tree Architecture

```python
@dataclass
class SkillTree:
    id: str
    name: str
    description: str
    root_skills: List[str]  # SkillNode IDs
    learning_objectives: List[str]
    estimated_completion_time: int  # hours
    difficulty_progression: str  # linear, exponential, adaptive
    assessment_strategy: str
    created_at: datetime
    updated_at: datetime

@dataclass
class SkillNode:
    id: str
    skill_name: str
    skill_type: str        # vocabulary, grammar, pronunciation, conversation
    description: str
    prerequisites: List[str]  # SkillNode IDs
    content_items: List['ContentReference']
    assessments: List[str]  # AssessmentContent IDs
    mastery_criteria: 'MasteryCriteria'
    estimated_study_time: int  # minutes
    difficulty_level: float
    practical_importance: float
    connections: List['SkillConnection']
    metadata: Dict[str, Any]

@dataclass
class ContentReference:
    content_id: str
    content_type: str      # vocabulary, conversation, pronunciation, etc.
    learning_role: str     # introduction, practice, reinforcement
    presentation_order: int
    required: bool
    adaptive_weight: float  # For dynamic content selection

@dataclass
class MasteryCriteria:
    accuracy_threshold: float     # 0.8 = 80% accuracy
    consistency_sessions: int     # Number of consistent sessions
    retention_period: int         # Days to maintain performance
    speed_requirements: Optional[float]
```

### Learning Path Management

```python
@dataclass
class LearningPath:
    id: str
    name: str
    description: str
    target_proficiency: str  # HSK1, HSK2, conversational, business
    skill_sequence: List['PathSegment']
    estimated_duration: int  # weeks
    personalization_factors: List[str]
    assessment_milestones: List['MilestoneAssessment']
    adaptive_branching: 'AdaptiveBranchingConfig'
    success_metrics: List[str]
    created_at: datetime
    updated_at: datetime

@dataclass
class PathSegment:
    segment_id: str
    segment_name: str
    skills: List[str]      # SkillNode IDs
    estimated_duration: int  # days
    completion_criteria: 'SegmentCompletionCriteria'
    optional_enrichment: List[str]  # Additional content IDs
    difficulty_progression: float

@dataclass
class AdaptiveBranchingConfig:
    branching_points: List['BranchingPoint']
    fallback_strategies: List[str]
    acceleration_criteria: 'AccelerationCriteria'
    remediation_triggers: 'RemediationTriggers'

@dataclass
class BranchingPoint:
    trigger_skill: str     # SkillNode ID
    condition: str         # struggling, excelling, interest_shift
    alternative_paths: List[str]  # LearningPath IDs
    recommendation_logic: str
```

## Content Effectiveness Layer

### Performance Tracking Models

```python
@dataclass
class ContentPerformanceMetrics:
    content_id: str
    content_type: str
    total_interactions: int
    success_rate: float
    average_completion_time: float
    retention_rate: float    # After 24h, 7d, 30d
    engagement_score: float
    difficulty_perception: float
    user_satisfaction: float
    skip_rate: float
    replay_rate: float
    help_request_rate: float
    performance_by_user_segment: Dict[str, 'SegmentMetrics']
    temporal_trends: List['PerformanceTrend']
    last_updated: datetime

@dataclass
class ContentOptimizationSuggestion:
    content_id: str
    optimization_type: str  # difficulty_adjustment, content_enhancement, sequencing
    priority: str          # high, medium, low
    rationale: str
    suggested_changes: List[str]
    expected_improvement: float
    implementation_effort: str
    a_b_test_candidate: bool
    created_at: datetime
```

### A/B Testing Framework

```python
@dataclass
class ContentExperiment:
    experiment_id: str
    experiment_name: str
    hypothesis: str
    content_variants: List['ContentVariant']
    target_metrics: List[str]
    user_segmentation: 'ExperimentSegmentation'
    duration: int          # days
    sample_size: int
    statistical_power: float
    status: str           # planning, running, analyzing, completed
    results: Optional['ExperimentResults']
    created_at: datetime

@dataclass
class ContentVariant:
    variant_id: str
    variant_name: str
    content_modifications: List['ContentModification']
    expected_outcome: str
    control_group: bool
    traffic_allocation: float  # 0.0 to 1.0

@dataclass
class ContentModification:
    modification_type: str  # text_change, audio_change, sequence_change
    field_path: str        # JSON path to modified field
    original_value: Any
    modified_value: Any
    rationale: str
```

## Content Delivery Engine

### Personalization Engine

```python
@dataclass
class PersonalizationProfile:
    user_id: str
    learning_style: str    # visual, auditory, kinesthetic, mixed
    pace_preference: str   # fast, medium, slow, adaptive
    prior_knowledge: Dict[str, float]  # skill -> proficiency
    attention_span: int    # minutes
    preferred_content_types: List[str]
    difficulty_tolerance: float
    mistake_sensitivity: str
    motivation_triggers: List[str]
    schedule_constraints: 'ScheduleConstraints'
    accessibility_needs: List[str]
    last_updated: datetime

@dataclass
class ContentRecommendation:
    user_id: str
    session_id: str
    recommended_content: List['RecommendedItem']
    reasoning: str
    confidence_score: float
    alternative_options: List['RecommendedItem']
    session_objectives: List[str]
    estimated_session_duration: int
    difficulty_progression: str
    generated_at: datetime

@dataclass
class RecommendedItem:
    content_id: str
    content_type: str
    recommendation_reason: str
    priority_score: float
    estimated_duration: int
    difficulty_match: float
    prerequisite_satisfaction: float
    novelty_factor: float
```

### Dynamic Sequencing Engine

```python
class ContentSequencingEngine:
    """
    Manages dynamic content sequencing based on learner performance,
    preferences, and curriculum objectives.
    """
    
    async def generate_sequence(
        self,
        user_profile: PersonalizationProfile,
        session_context: SessionContext,
        learning_objectives: List[str]
    ) -> ContentSequence:
        """Generate optimal content sequence for user session."""
        pass
    
    async def adapt_sequence(
        self,
        current_sequence: ContentSequence,
        performance_data: List[LearningInteraction],
        real_time_feedback: Dict[str, Any]
    ) -> ContentSequence:
        """Adapt sequence based on real-time learning data."""
        pass
    
    async def handle_mastery_acceleration(
        self,
        user_id: str,
        mastered_skills: List[str]
    ) -> List[ContentReference]:
        """Recommend advanced content for accelerated learners."""
        pass
    
    async def handle_remediation(
        self,
        user_id: str,
        struggling_areas: List[str]
    ) -> List[ContentReference]:
        """Provide remediation content for struggling areas."""
        pass
```

## Storage Architecture

### Azure Data Lake Structure

```
/content/
├── vocabulary/
│   ├── items/              # VocabularyItem JSON files
│   ├── audio/              # Pronunciation audio files
│   └── images/             # Visual aids
├── conversations/
│   ├── scenarios/          # ConversationContent JSON files
│   ├── audio/              # Dialogue audio files
│   └── videos/             # Contextual videos
├── pronunciation/
│   ├── lessons/            # PronunciationContent JSON files
│   ├── native_audio/       # Native speaker samples
│   └── tone_contours/      # F0 frequency data
├── assessments/
│   ├── questions/          # AssessmentContent JSON files
│   ├── audio_prompts/      # Assessment audio
│   └── answer_keys/        # Scoring information
└── curriculum/
    ├── skill_trees/        # SkillTree definitions
    ├── learning_paths/     # LearningPath configurations
    └── experiments/        # A/B testing configurations

/analytics/
├── content_performance/    # ContentPerformanceMetrics
├── user_interactions/      # Learning interaction logs
├── experiment_results/     # A/B testing results
└── optimization_suggestions/  # Content optimization data

/cache/
├── personalization/        # Cached user profiles
├── recommendations/        # Cached content recommendations
└── sequences/             # Pre-generated content sequences
```

## Integration Points

### With Learning Effectiveness (ADR-009)

```python
class ContentEffectivenessIntegration:
    """Integration with learning effectiveness feedback loop."""
    
    async def analyze_content_effectiveness(
        self,
        content_items: List[str],
        interaction_data: List[LearningInteraction],
        time_window: timedelta
    ) -> List[ContentPerformanceMetrics]:
        """Analyze effectiveness of specific content items."""
        pass
    
    async def recommend_content_optimizations(
        self,
        performance_metrics: List[ContentPerformanceMetrics],
        global_trends: GlobalEffectivenessMetrics
    ) -> List[ContentOptimizationSuggestion]:
        """Generate content optimization recommendations."""
        pass
    
    async def trigger_adaptive_sequencing(
        self,
        user_id: str,
        effectiveness_analysis: EffectivenessAnalysis
    ) -> ContentSequence:
        """Trigger dynamic content sequence adjustment."""
        pass
```

### With AI Framework (ADR-001)

```python
@kernel_function(
    description="Generate personalized content recommendations",
    name="generate_content_recommendations"
)
async def generate_content_recommendations(
    user_profile: str,
    learning_objectives: str,
    session_context: str
) -> str:
    """Semantic Kernel function for AI-powered content recommendation."""
    pass
```

## Implementation Strategy

### Phase 1: Core Content Models (Weeks 1-2)
1. Implement basic content model classes
2. Create content validation framework
3. Set up Azure Data Lake storage structure
4. Implement content CRUD operations

### Phase 2: Curriculum Framework (Weeks 3-4)
1. Implement skill tree and learning path models
2. Create prerequisite validation system
3. Build mastery criteria evaluation
4. Implement basic content sequencing

### Phase 3: Effectiveness Integration (Weeks 5-6)
1. Integrate with learning effectiveness analyzer
2. Implement content performance tracking
3. Create optimization suggestion engine
4. Build A/B testing framework

### Phase 4: Personalization Engine (Weeks 7-8)
1. Implement user profiling system
2. Create recommendation algorithms
3. Build dynamic sequencing engine
4. Integrate pronunciation analysis

### Phase 5: Advanced Features (Weeks 9-10)
1. Implement advanced adaptive algorithms
2. Create pronunciation refinement features
3. Build assessment integration
4. Optimize performance and caching

## Success Metrics

### Content Quality Metrics
- **Content Effectiveness Score**: Average learning outcome improvement per content item (>15% improvement)
- **Engagement Rate**: Percentage of content completed vs. started (>85%)
- **Retention Rate**: Knowledge retention after 7 days (>75%)

### Curriculum Effectiveness Metrics
- **Learning Path Completion**: Percentage of users completing learning paths (>70%)
- **Skill Mastery Rate**: Average time to achieve skill mastery (reduce by 20%)
- **Prerequisite Accuracy**: Correct prerequisite sequencing (>95%)
- **Adaptive Branching Success**: Improved outcomes from adaptive paths (>10% improvement)

### Personalization Metrics
- **Recommendation Accuracy**: User acceptance of content recommendations (>80%)
- **Session Satisfaction**: User-rated session quality (>4.0/5.0)
- **Time to Proficiency**: Reduced time to reach target proficiency levels (>15% reduction)

### Technical Performance Metrics
- **Content Delivery Latency**: Sub-200ms content recommendation generation
- **Storage Efficiency**: Optimized content storage and retrieval (<100MB per user profile)
- **Scalability**: Support for 10,000+ concurrent content requests
- **Cache Hit Rate**: >90% cache hit rate for personalized recommendations

## Risks and Mitigation

### Content Quality Risks
- **Risk**: Inconsistent content quality across different creators
- **Mitigation**: Implement comprehensive content validation framework and peer review process

### Scalability Risks
- **Risk**: Content recommendation performance degradation at scale
- **Mitigation**: Implement intelligent caching and pre-computation strategies

### Personalization Risks
- **Risk**: Over-personalization leading to learning gaps
- **Mitigation**: Maintain core curriculum requirements and regular assessment checkpoints

## Decision Rationale

This architecture provides:

1. **Comprehensive Mandarin Support**: Specialized models for tones and pronunciation
2. **Flexible Curriculum Framework**: Supports both structured and adaptive learning paths
3. **Data-Driven Optimization**: Enables continuous content improvement through effectiveness tracking
4. **Scalable Personalization**: Efficient algorithms for large-scale personalized content delivery
5. **Future Extensibility**: Modular design supports future enhancements and additional languages

The architecture integrates seamlessly with existing ADRs while providing the foundational content framework needed for effective Mandarin language learning.

## Status

**Current Status**: Proposed  
**Next Steps**: 
1. Review and approval of architecture design
2. Begin Phase 1 implementation (Core Content Models)
3. Create detailed implementation plan with task breakdown
4. Set up development environment and testing framework

**Dependencies**: 
- ADR-011 (UI/Learning Experience) for content presentation layer
- ADR-012 (Assessment & Progress Tracking) for assessment integration
- ADR-009 (Learning Effectiveness) for feedback loop integration