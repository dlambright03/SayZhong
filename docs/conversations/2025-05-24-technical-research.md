# Technical Research Discussion - 2025-05-24

## Topic
Researching specific technical implementations for SayZhong based on user's technology preferences.

## User Technology Choices

### AI/ML Framework
**User Choice:** Semantic Kernel to communicate with Azure OpenAI service

### Data Storage
**User Choice:** Azure Data Lake for storage

### State Management
**User Request:** Suggestions for state management in Streamlit context

## Research Needed

1. **Semantic Kernel Integration**
   - Python SDK capabilities and setup
   - Azure OpenAI integration patterns
   - Best practices for educational applications

2. **Azure Data Lake Storage**
   - Integration with Python applications
   - Storage patterns for user progress and vocabulary data
   - Authentication and security considerations

3. **Streamlit State Management**
   - Session state capabilities
   - Persistent storage integration
   - User session handling for learning applications

## Research Findings

### Semantic Kernel + Azure OpenAI

**Capabilities:**
- **Python SDK**: Full support for Python 3.11
- **Azure OpenAI Integration**: Native support for GPT models
- **Function Calling**: Perfect for AI tutoring agents
- **Memory Management**: Built-in conversation memory
- **Plugins Architecture**: Extensible for learning modules

**Benefits for SayZhong:**
- **AI Conversation Partner**: Natural dialogue with context retention
- **Adaptive Learning**: Can analyze user responses and adjust difficulty
- **Content Generation**: Generate practice scenarios dynamically
- **Personalization**: Maintain user learning context across sessions

### Azure Data Lake Storage Gen2

**Capabilities:**
- **Hierarchical Storage**: Organize by user/lessons/progress
- **Python SDK**: Azure Storage libraries for seamless integration
- **Security**: Azure AD integration for user authentication
- **Analytics**: Integration with Azure Analytics services
- **Cost-effective**: Pay-per-use model suitable for educational apps

**Storage Structure for SayZhong:**
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

### Streamlit State Management Options

**Built-in Options:**
1. **st.session_state**: In-memory session state (resets on refresh)
2. **st.cache_data**: Caching with TTL for performance
3. **st.cache_resource**: Persistent resource caching

**Recommended Approach for SayZhong:**
- **st.session_state**: Current learning session data
- **Azure Data Lake**: Persistent user progress and content
- **Semantic Kernel Memory**: AI conversation context
- **Custom State Manager**: Bridge between Streamlit and Azure storage

## Implementation Recommendations

### State Management Strategy
1. **Session Layer**: st.session_state for current UI state
2. **Progress Layer**: Azure Data Lake for persistent user data
3. **AI Memory Layer**: Semantic Kernel memory for conversation context
4. **Content Layer**: Azure Data Lake for vocabulary and lessons

### Integration Architecture
```
Streamlit UI -> Custom State Manager -> Azure Data Lake
            -> Semantic Kernel -> Azure OpenAI
```

## Next Steps
Update requirements.md with specific technical choices and implementation details.
