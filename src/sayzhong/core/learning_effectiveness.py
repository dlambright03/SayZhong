"""
Learning effectiveness feedback loop core components.

This module implements the core components for analyzing learning effectiveness
and adapting lesson plans based on data-driven insights.
"""

import asyncio
import json
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class LearningDifficulty(Enum):
    """Learning difficulty levels."""

    BEGINNER = "beginner"
    ELEMENTARY = "elementary"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    NATIVE = "native"


class ContentType(Enum):
    """Types of learning content."""

    VOCABULARY = "vocabulary"
    GRAMMAR = "grammar"
    CONVERSATION = "conversation"
    LISTENING = "listening"
    READING = "reading"
    WRITING = "writing"


class AdaptationType(Enum):
    """Types of lesson adaptations."""

    DIFFICULTY_INCREASE = "difficulty_increase"
    DIFFICULTY_DECREASE = "difficulty_decrease"
    CONTENT_CHANGE = "content_change"
    PACING_ADJUSTMENT = "pacing_adjustment"
    METHOD_CHANGE = "method_change"
    ADDITIONAL_PRACTICE = "additional_practice"


@dataclass
class LearningInteraction:
    """Represents a single learning interaction."""

    interaction_id: str
    user_id: str
    session_id: str
    timestamp: datetime
    content_id: str
    content_type: ContentType
    difficulty_level: LearningDifficulty

    # Interaction details
    question: str
    user_answer: str
    correct_answer: str
    is_correct: bool
    response_time_seconds: float
    confidence_level: Optional[float] = None  # 0.0 to 1.0
    hints_used: int = 0
    attempts: int = 1

    # Context
    previous_attempts: List[str] = field(default_factory=list)
    session_position: int = 0  # Position in current session
    time_since_last_review: Optional[timedelta] = None


@dataclass
class LearningEffectivenessMetrics:
    """Comprehensive learning effectiveness metrics for a user."""

    user_id: str
    session_id: str
    timestamp: datetime

    # Immediate Effectiveness
    accuracy_rate: float  # Correct answers / total answers
    response_time_avg: float  # Average time per question
    confidence_score: float  # User-reported or inferred confidence
    engagement_duration: float  # Time spent in focused learning

    # Learning Progression
    difficulty_progression: float  # Rate of difficulty increase
    retention_rate: float  # Performance on previously learned content
    mastery_speed: float  # Time to achieve mastery
    knowledge_transfer: float  # Application to new contexts

    # Behavioral Patterns
    session_frequency: float  # Learning session consistency
    optimal_session_length: float  # Most effective session duration
    preferred_content_types: List[ContentType]  # Most effective content formats
    peak_learning_times: List[str]  # Most effective learning times

    # Long-term Outcomes
    spaced_repetition_effectiveness: float
    long_term_retention: float  # Retention after 1 week, 1 month
    skill_transfer_rate: float  # Application to real conversations


@dataclass
class GlobalEffectivenessMetrics:
    """Global effectiveness metrics across all users."""

    content_id: str
    methodology: str
    timestamp: datetime

    # Content Effectiveness
    average_success_rate: float
    completion_rate: float
    user_satisfaction: float
    time_to_mastery: float

    # Methodology Effectiveness
    learning_velocity: float
    retention_durability: float
    transfer_effectiveness: float
    engagement_quality: float

    # Cohort Analysis
    beginner_effectiveness: float
    intermediate_effectiveness: float
    advanced_effectiveness: float
    demographic_patterns: Dict[str, float]


@dataclass
class LearningPattern:
    """Identified learning pattern."""

    pattern_id: str
    pattern_type: str
    description: str
    effectiveness_score: float
    frequency: int
    applicable_users: List[str]
    conditions: Dict[str, Any]
    outcomes: Dict[str, float]


@dataclass
class LessonPlan:
    """Adaptive lesson plan."""

    plan_id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    # Plan structure
    learning_objectives: List[str]
    content_sequence: List[Dict[str, Any]]
    difficulty_progression: List[LearningDifficulty]
    estimated_duration: timedelta

    # Adaptation parameters
    adaptation_triggers: Dict[str, Any]
    personalization_factors: Dict[str, float]
    expected_effectiveness: float

    # Tracking
    actual_effectiveness: Optional[float] = None
    adaptations_made: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class LessonAdjustment:
    """Real-time lesson adjustment."""

    adjustment_id: str
    session_id: str
    timestamp: datetime
    adaptation_type: AdaptationType
    trigger_reason: str

    # Adjustment details
    content_changes: Dict[str, Any]
    difficulty_change: Optional[int] = None  # -2 to +2
    pacing_multiplier: float = 1.0
    additional_content: List[str] = field(default_factory=list)

    # Tracking
    effectiveness_impact: Optional[float] = None
    user_response: Optional[str] = None


@dataclass
class EffectivenessAnalysis:
    """Result of learning effectiveness analysis."""

    user_id: str
    analysis_timestamp: datetime
    timeframe_days: int

    # Analysis results
    immediate_effectiveness: float
    retention_effectiveness: float
    progression_effectiveness: float
    overall_effectiveness: float

    # Identified patterns
    learning_patterns: List[LearningPattern]
    strengths: List[str]
    improvement_areas: List[str]

    # Recommendations
    recommended_adaptations: List[Dict[str, Any]]
    optimal_content_types: List[ContentType]
    optimal_difficulty_progression: float
    recommended_session_length: timedelta


@dataclass
class GlobalEffectivenessAnalysis:
    """Global effectiveness analysis results."""

    analysis_timestamp: datetime
    timeframe_days: int
    total_users_analyzed: int

    # Global metrics
    global_metrics: GlobalEffectivenessMetrics
    successful_patterns: List[LearningPattern]
    best_practices: List[Dict[str, Any]]
    improvement_opportunities: List[Dict[str, Any]]

    # Content insights
    most_effective_content: List[str]
    least_effective_content: List[str]
    content_optimization_suggestions: Dict[str, List[str]]


class LearningEffectivenessAnalyzer(ABC):
    """Abstract base class for learning effectiveness analysis."""

    @abstractmethod
    async def analyze_user_effectiveness(
        self, user_id: str, timeframe_days: int = 30
    ) -> EffectivenessAnalysis:
        """Analyze learning effectiveness for a specific user."""
        pass

    @abstractmethod
    async def analyze_global_effectiveness(
        self, timeframe_days: int = 30
    ) -> GlobalEffectivenessAnalysis:
        """Analyze learning effectiveness across all users."""
        pass

    @abstractmethod
    async def calculate_real_time_effectiveness(
        self, interactions: List[LearningInteraction]
    ) -> float:
        """Calculate real-time effectiveness score from recent interactions."""
        pass

    @abstractmethod
    async def identify_learning_patterns(
        self, user_data: Dict[str, Any]
    ) -> List[LearningPattern]:
        """Identify learning patterns from user data."""
        pass


class AdaptiveLessonPlanner(ABC):
    """Abstract base class for adaptive lesson planning."""

    @abstractmethod
    async def generate_personalized_lesson(
        self, user_id: str, learning_objectives: List[str]
    ) -> LessonPlan:
        """Generate a personalized lesson plan based on effectiveness analysis."""
        pass

    @abstractmethod
    async def adapt_lesson_real_time(
        self, session_id: str, current_performance: Dict[str, Any]
    ) -> Optional[LessonAdjustment]:
        """Adapt lesson plan in real-time based on current performance."""
        pass

    @abstractmethod
    async def optimize_content_sequence(
        self, content_items: List[Dict[str, Any]], user_profile: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Optimize the sequence of content based on user profile."""
        pass


class FeedbackLoopOrchestrator(ABC):
    """Abstract base class for orchestrating the feedback loop."""

    @abstractmethod
    async def process_learning_interaction(
        self, interaction: LearningInteraction
    ) -> None:
        """Process a learning interaction and trigger adaptations as needed."""
        pass

    @abstractmethod
    async def run_batch_optimization(self) -> None:
        """Run periodic batch optimization based on accumulated feedback."""
        pass

    @abstractmethod
    async def evaluate_adaptation_effectiveness(
        self, adaptation: LessonAdjustment, post_adaptation_performance: Dict[str, Any]
    ) -> float:
        """Evaluate the effectiveness of a lesson adaptation."""
        pass


# Utility functions


def calculate_learning_velocity(
    interactions: List[LearningInteraction], timeframe_hours: float = 24.0
) -> float:
    """Calculate learning velocity based on recent interactions."""
    if not interactions:
        return 0.0

    # Calculate correct answers per hour
    correct_answers = sum(1 for i in interactions if i.is_correct)
    return correct_answers / timeframe_hours


def calculate_retention_rate(
    review_interactions: List[LearningInteraction],
    initial_interactions: List[LearningInteraction],
) -> float:
    """Calculate retention rate by comparing review performance to initial learning."""
    if not review_interactions or not initial_interactions:
        return 0.0

    initial_accuracy = sum(1 for i in initial_interactions if i.is_correct) / len(
        initial_interactions
    )
    review_accuracy = sum(1 for i in review_interactions if i.is_correct) / len(
        review_interactions
    )

    # Retention rate is how well performance is maintained
    return min(review_accuracy / initial_accuracy if initial_accuracy > 0 else 0.0, 1.0)


def calculate_difficulty_progression_rate(
    interactions: List[LearningInteraction], timeframe_days: int = 7
) -> float:
    """Calculate the rate of difficulty progression."""
    if len(interactions) < 2:
        return 0.0

    # Sort by timestamp
    sorted_interactions = sorted(interactions, key=lambda x: x.timestamp)

    difficulty_values = {
        LearningDifficulty.BEGINNER: 1,
        LearningDifficulty.ELEMENTARY: 2,
        LearningDifficulty.INTERMEDIATE: 3,
        LearningDifficulty.ADVANCED: 4,
        LearningDifficulty.NATIVE: 5,
    }

    start_difficulty = difficulty_values[sorted_interactions[0].difficulty_level]
    end_difficulty = difficulty_values[sorted_interactions[-1].difficulty_level]

    progression = end_difficulty - start_difficulty
    return progression / timeframe_days


def estimate_mastery_time(
    interactions: List[LearningInteraction], mastery_threshold: float = 0.85
) -> Optional[timedelta]:
    """Estimate time to achieve mastery based on learning trajectory."""
    if not interactions:
        return None

    # Calculate rolling accuracy
    window_size = min(10, len(interactions))
    recent_interactions = interactions[-window_size:]
    current_accuracy = sum(1 for i in recent_interactions if i.is_correct) / len(
        recent_interactions
    )

    if current_accuracy >= mastery_threshold:
        return timedelta(0)  # Already achieved mastery

    # Simple linear projection (could be enhanced with ML)
    if len(interactions) > 1:
        time_elapsed = interactions[-1].timestamp - interactions[0].timestamp
        improvement_rate = current_accuracy / time_elapsed.total_seconds()

        if improvement_rate > 0:
            remaining_improvement = mastery_threshold - current_accuracy
            estimated_seconds = remaining_improvement / improvement_rate
            return timedelta(seconds=estimated_seconds)

    return None


def generate_interaction_id() -> str:
    """Generate a unique interaction ID."""
    return f"interaction_{uuid.uuid4().hex[:12]}"


def generate_session_id() -> str:
    """Generate a unique session ID."""
    return f"session_{uuid.uuid4().hex[:12]}"


def generate_plan_id() -> str:
    """Generate a unique lesson plan ID."""
    return f"plan_{uuid.uuid4().hex[:12]}"


def generate_adjustment_id() -> str:
    """Generate a unique adjustment ID."""
    return f"adjustment_{uuid.uuid4().hex[:12]}"
