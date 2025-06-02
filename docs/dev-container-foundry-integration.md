# Azure AI Foundry Local: Dev Container Integration Guide

This document provides instructions for using Azure AI Foundry Local in the SayZhong dev container environment with optimal resource efficiency.

## Quick Start (Recommended: Demo Mode)

For daily development, use the demo mode which provides immediate functionality without resource overhead:

```bash
cd /workspaces/SayZhong/spike/FoundryLocal
pip install -r requirements.txt
PYTHONPATH=. python examples/basic_chat_demo.py
```

**Benefits:**
- ✅ Instant startup (<1 minute)
- ✅ Minimal resource usage (~100MB)
- ✅ Works offline
- ✅ Perfect for development workflow

## AI Testing Mode (Optional Sidecar)

When you need to test with real AI models (integration testing, AI behavior validation):

### 1. Start the Foundry Local Sidecar

```bash
# From the project root
cd /workspaces/SayZhong
docker-compose -f .devcontainer/docker-compose.ai-testing.yml --profile ai-testing up -d foundry-local
```

### 2. Wait for Model Download (First Time Only)

```bash
# Check startup progress
docker-compose -f .devcontainer/docker-compose.ai-testing.yml logs -f foundry-local

# Wait for "Model loaded successfully" message
# This may take 5-10 minutes for initial model download
```

### 3. Run Real AI Examples

```bash
cd /workspaces/SayZhong/spike/FoundryLocal
PYTHONPATH=. python examples/basic_chat.py
```

### 4. Stop AI Testing When Done

```bash
# Stop the sidecar to free up resources
docker-compose -f .devcontainer/docker-compose.ai-testing.yml --profile ai-testing down
```

## Resource Requirements

| Mode | RAM Usage | CPU Usage | Storage | Startup Time |
|------|-----------|-----------|---------|--------------|
| **Demo Mode** | +100MB | +5% | +10MB | <1 min |
| **AI Testing** | +8GB | +50% | +5GB | 5-10 min |

## When to Use Each Mode

### Use Demo Mode For:
- ✅ Feature development
- ✅ Business logic testing
- ✅ UI/UX development
- ✅ Integration with Semantic Kernel (mocked)
- ✅ Daily development workflow

### Use AI Testing Mode For:
- ✅ Integration testing
- ✅ AI response validation
- ✅ Model behavior testing
- ✅ Performance testing with real AI
- ✅ Pre-production validation

## Configuration Details

### Demo Mode Configuration

The demo mode uses `FoundryManager(test_mode=True)` which:
- Simulates AI responses with realistic delays
- Provides contextual responses based on user input
- Supports all Semantic Kernel integration patterns
- Includes error handling simulation

### AI Testing Configuration

The sidecar container is configured with:
- **Model**: phi-3.5-mini (4GB RAM, good quality)
- **Memory Limit**: 8GB container limit
- **CPU Limit**: 2 cores maximum
- **Health Checks**: Automatic startup verification
- **Persistence**: Models cached between restarts

## Troubleshooting

### Demo Mode Issues

1. **Import errors**:
   ```bash
   # Ensure PYTHONPATH is set
   export PYTHONPATH=/workspaces/SayZhong/spike/FoundryLocal
   ```

2. **Module not found**:
   ```bash
   # Install requirements
   pip install -r requirements.txt
   ```

### AI Testing Mode Issues

1. **Container won't start**:
   ```bash
   # Check Docker status
   docker ps -a
   
   # Check logs
   docker-compose -f .devcontainer/docker-compose.ai-testing.yml logs foundry-local
   ```

2. **Model download stuck**:
   ```bash
   # Restart with fresh download
   docker-compose -f .devcontainer/docker-compose.ai-testing.yml down -v
   docker-compose -f .devcontainer/docker-compose.ai-testing.yml --profile ai-testing up -d
   ```

3. **Out of memory**:
   ```bash
   # Check available resources
   docker stats
   
   # Consider using smaller model in docker-compose.ai-testing.yml:
   # Change FOUNDRY_MODEL=phi-3.5-mini to a smaller variant if available
   ```

### Resource Monitoring

Monitor resource usage during AI testing:

```bash
# Check container resource usage
docker stats sayzhong-foundry-local

# Check system resources
htop
# or
top
```

## Development Workflow

### Standard Development (90% of time)
```bash
# Use demo mode for fast iteration
cd /workspaces/SayZhong/spike/FoundryLocal
PYTHONPATH=. python examples/basic_chat_demo.py
```

### Integration Testing (10% of time)
```bash
# Start AI testing when needed
docker-compose -f .devcontainer/docker-compose.ai-testing.yml --profile ai-testing up -d foundry-local

# Run real AI tests
PYTHONPATH=. python examples/basic_chat.py

# Stop when done to save resources
docker-compose -f .devcontainer/docker-compose.ai-testing.yml --profile ai-testing down
```

## Team Guidelines

### For Individual Developers:
- **Use Demo Mode** for daily development
- **Only start AI Testing** when specifically needed
- **Stop AI Testing containers** when finished to save team resources

### For Team Leads:
- Monitor cloud resource usage if using hosted dev containers
- Consider shared AI testing instances for team collaboration
- Budget additional resources only when AI testing is actively needed

### For CI/CD:
- Use Demo Mode for most automated tests
- Use AI Testing Mode only for integration test suites
- Consider scheduled AI testing rather than per-commit testing

## Cost Optimization

### Local Development (Codespaces/Cloud):
- Demo Mode: ~$0 additional cost
- AI Testing: ~$2-5 per hour of active use

### On-Premise Development:
- Demo Mode: No additional resources needed
- AI Testing: Requires 8GB+ RAM, may impact other applications

## Security Considerations

### Demo Mode:
- ✅ No external network calls
- ✅ No model downloads required
- ✅ No sensitive data processing

### AI Testing Mode:
- ✅ All processing happens locally in container
- ✅ No data sent to external services
- ✅ Models downloaded from Microsoft-verified sources
- ⚠️ Requires Docker daemon access (standard for dev containers)

## Future Enhancements

Planned improvements for this integration:
- [ ] Automatic resource scaling based on usage
- [ ] Shared team instances for AI testing
- [ ] Integration with SayZhong's test suite
- [ ] Performance metrics and monitoring
- [ ] Alternative lightweight models for development

For questions or issues with this setup, please refer to the main project documentation or create an issue in the SayZhong repository.
