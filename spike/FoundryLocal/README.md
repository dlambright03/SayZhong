# Azure AI Foundry Local Integration

This spike implementation demonstrates how to integrate Azure AI Foundry Local with Semantic Kernel for local AI development, specifically designed for the SayZhong Mandarin learning project.

## Overview

Azure AI Foundry Local allows you to run AI models locally on your device, providing:
- **Privacy**: Data never leaves your device
- **Cost efficiency**: No API costs after setup
- **Offline capability**: Works without internet after model download
- **Development**: Perfect for local development and testing

## Features

- ✅ **FoundryManager**: Wrapper for managing Foundry Local services
- ✅ **Semantic Kernel Integration**: Full SK support with local models
- ✅ **Plugin Support**: Custom plugins for language learning
- ✅ **Streaming Responses**: Real-time AI responses
- ✅ **Error Handling**: Comprehensive error management
- ✅ **Testing**: Full test coverage following TDD

## Prerequisites

### System Requirements
- **OS**: Windows 10/11, macOS, or Linux
- **Python**: 3.11 or higher
- **RAM**: Minimum 8GB, Recommended 16GB
- **Storage**: 3GB free (minimum), 15GB free (recommended)
- **GPU**: Optional but recommended for better performance

### Installation

1. **Run the setup script**:
   ```bash
   python setup.py
   ```

2. **Install Foundry Local CLI** (if not already installed):
   
   **Windows**:
   ```bash
   winget install Microsoft.FoundryLocal
   ```
   
   **macOS**:
   ```bash
   brew tap microsoft/foundrylocal
   brew install foundrylocal
   ```
   
   **Linux**:
   ```bash
   wget https://aka.ms/foundry-local-installer -O foundry-local-installer.sh
   chmod +x foundry-local-installer.sh
   ./foundry-local-installer.sh
   ```

   **Dev Container/Codespaces**:
   ```bash
   # For development/testing without full installation
   cd /workspaces/SayZhong/spike/FoundryLocal
   PYTHONPATH=. python examples/basic_chat_demo.py
   ```

3. **Verify installation**:
   ```bash
   foundry --help
   ```

## Quick Start

### 1. Start Foundry Local with a model

```bash
foundry model run phi-3.5-mini
```

The model will download automatically (may take a few minutes).

### 2. Run the basic chat example

**With Foundry Local installed**:
```bash
cd /workspaces/SayZhong/spike/FoundryLocal
PYTHONPATH=. python examples/basic_chat.py
```

**Demo mode (without Foundry Local)**:
```bash
cd /workspaces/SayZhong/spike/FoundryLocal
PYTHONPATH=. python examples/basic_chat_demo.py
```

### 3. Try the Mandarin learning example

```bash
cd /workspaces/SayZhong/spike/FoundryLocal
PYTHONPATH=. python examples/semantic_kernel_integration.py
```

## Dev Container Usage

If you're working in a dev container (like GitHub Codespaces), you have optimized options for resource efficiency:

### 🥇 Demo Mode (Recommended for Daily Development)
```bash
cd /workspaces/SayZhong/spike/FoundryLocal
pip install -r requirements.txt
PYTHONPATH=. python examples/basic_chat_demo.py
```
**Benefits**: Instant startup, minimal resources (~100MB), perfect for development workflow.

### 🥈 AI Testing Mode (For Integration Testing)
```bash
# Start sidecar container when real AI testing is needed
cd /workspaces/SayZhong
docker-compose -f .devcontainer/docker-compose.ai-testing.yml --profile ai-testing up -d foundry-local

# Run real AI examples
cd spike/FoundryLocal
PYTHONPATH=. python examples/basic_chat.py

# Stop to save resources when done
docker-compose -f .devcontainer/docker-compose.ai-testing.yml --profile ai-testing down
```
**Benefits**: Real AI behavior, isolated resources, team-friendly.

### 📚 Detailed Guide
For comprehensive dev container integration instructions, see:
- [Dev Container Integration Guide](../../docs/dev-container-foundry-integration.md)
- [Resource Efficiency Comparison](../../docs/dev-container-foundry-comparison.md)

### 🛠️ Management Script
Use the helper script for easy AI testing management:
```bash
# Start AI testing mode
/workspaces/SayZhong/scripts/foundry-local-dev.sh start

# Check status and resource usage
/workspaces/SayZhong/scripts/foundry-local-dev.sh status

# Stop to save resources
/workspaces/SayZhong/scripts/foundry-local-dev.sh stop
```

## Usage Examples

### Basic Chat
```python
from src.foundry_manager import FoundryManager
from src.semantic_kernel_service import SemanticKernelFoundryService

# Initialize Foundry Local
foundry_manager = FoundryManager("phi-3.5-mini")

# Create Semantic Kernel service
sk_service = SemanticKernelFoundryService(foundry_manager)

# Chat with the AI
response = await sk_service.chat_completion("Hello, how are you?")
print(response)
```

### With Custom Plugins
```python
class MandarinLearningPlugin:
    @kernel_function(description="Translates text to Chinese")
    def translate_to_chinese(self, text: str) -> str:
        # Your translation logic here
        return f"Translation of '{text}'"

# Add plugin to kernel
plugin = MandarinLearningPlugin()
sk_service.add_plugin(plugin, "MandarinLearning")

# Use with function calling
response = await sk_service.chat_completion(
    "Translate 'hello' to Chinese", 
    enable_function_calling=True
)
```

### Streaming Responses
```python
async for chunk in sk_service.streaming_chat_completion("Tell me about China"):
    print(chunk, end="", flush=True)
```

## Project Structure

```
spike/FoundryLocal/
├── README.md                     # This file
├── requirements.txt              # Python dependencies
├── setup.py                      # Setup script
├── src/
│   ├── __init__.py
│   ├── foundry_manager.py        # Foundry Local wrapper
│   └── semantic_kernel_service.py # SK integration
├── examples/
│   ├── basic_chat.py            # Simple chat example
│   ├── streaming_example.py     # Streaming chat
│   └── semantic_kernel_integration.py # SK with plugins
└── tests/
    ├── __init__.py
    ├── test_foundry_manager.py
    └── test_semantic_kernel_integration.py
```

## Available Models

List available models:
```bash
foundry model list
```

Common models for language learning:
- `phi-3.5-mini` - Fast, efficient for basic conversations
- `phi-3.5-medium` - Better quality, more resource intensive

## SayZhong Integration Opportunities

This spike demonstrates several opportunities for the SayZhong project:

### 1. **Conversational Practice**
- Local AI for safe Mandarin conversation practice
- No data leaves the device - important for student privacy
- Cost-effective for educational institutions

### 2. **Pronunciation Feedback**
- Process audio locally for immediate feedback
- Custom plugins for phonetic analysis
- Offline capability for classroom use

### 3. **Personalized Learning**
- AI-powered adaptive learning paths
- Custom vocabulary recommendations
- Progress tracking with local data storage

### 4. **Content Generation**
- Generate practice exercises
- Create contextual examples
- Develop reading comprehension materials

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=src --cov-report=html
```

## Troubleshooting

### Common Issues

1. **"foundry_local_sdk not installed"**
   ```bash
   pip install foundry-local-sdk
   ```

2. **"Foundry Local service not available"**
   - Ensure Foundry Local CLI is installed
   - Run: `foundry model run phi-3.5-mini`
   - Check if model is downloaded: `foundry model list`

3. **"semantic-kernel not installed"**
   ```bash
   pip install semantic-kernel
   ```

4. **Model download fails**
   - Check internet connection
   - Ensure sufficient disk space
   - Try a different model: `foundry model run phi-3.5-mini`

### Performance Tips

1. **Use GPU acceleration** when available
2. **Increase RAM** for better performance with larger models
3. **Use SSD storage** for faster model loading
4. **Close other applications** to free up resources

## Development

### Adding New Features

1. **Write tests first** (following TDD):
   ```python
   def test_new_feature():
       # Test implementation
       pass
   ```

2. **Implement the feature**:
   ```python
   def new_feature():
       # Implementation
       pass
   ```

3. **Run tests**:
   ```bash
   pytest tests/
   ```

### Contributing

1. Follow the existing code structure
2. Write comprehensive tests
3. Update documentation
4. Ensure all tests pass

## Security Considerations

- All processing happens locally
- No data transmitted to external services
- API keys are only used for local authentication
- Model downloads are verified by Microsoft

## Performance Benchmarks

| Model | RAM Usage | Response Time | Quality |
|-------|-----------|---------------|---------|
| phi-3.5-mini | ~4GB | ~1-2s | Good |
| phi-3.5-medium | ~8GB | ~2-4s | Better |

*Benchmarks on 16GB RAM, M1 MacBook Pro*

## Future Enhancements

- [ ] Voice input/output integration
- [ ] Chinese character recognition
- [ ] Tone analysis for pronunciation
- [ ] Integration with SayZhong database
- [ ] Batch processing capabilities
- [ ] Model fine-tuning for Mandarin

## License

This spike implementation is part of the SayZhong project and follows the same licensing terms.

## Support

For issues related to:
- **Foundry Local**: Check Microsoft documentation
- **Semantic Kernel**: Visit the SK GitHub repository
- **This implementation**: Create an issue in the SayZhong repository
