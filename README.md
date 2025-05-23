# SayZhong

A Python application for learning Mandarin Chinese conversationally, designed specifically for English speakers.

## Features

- 🎯 Conversational focus for practical learning
- 🔊 Pronunciation and tone training tools
- 📚 Phrasebook and vocabulary management
- 🤖 AI-powered learning assistance
- 📊 Progress tracking and analytics

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/SayZhong.git
cd SayZhong
```

2. Set up the development environment:
```bash
python scripts/setup_dev.py
```

3. Copy environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run tests to verify installation:
```bash
python -m pytest
```

### Development with DevContainer

This project includes a VS Code DevContainer for consistent development environments:

1. Open the project in VS Code
2. Install the "Dev Containers" extension
3. Press `Ctrl+Shift+P` and select "Dev Containers: Reopen in Container"
4. The container will build and install all dependencies automatically

## Development

### Running Tests

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Run specific test file
python -m pytest tests/test_package.py
```

### Code Quality

```bash
# Format code
make format

# Run linting
make lint

# Check formatting
make format-check
```

### Development Server

```bash
# Start development environment
make dev
# or
python scripts/run_dev.py
```

## Project Structure

```
SayZhong/
├── src/sayzhong/          # Main package
│   ├── core/              # Core functionality
│   ├── models/            # Data models
│   └── utils/             # Utility functions
├── tests/                 # Test files
├── docs/                  # Documentation
│   ├── research/          # Research notes
│   └── conversations/     # AI conversations
├── scripts/               # Development scripts
└── .devcontainer/         # VS Code DevContainer config
```

## Research

This project is based on comprehensive research into effective Mandarin learning methods:

- [Learning Methods](docs/research/methods.md) - Research-backed approaches for English speakers
- [Software Comparison](docs/research/software.md) - Analysis of existing Mandarin learning tools

## Contributing

We use Test Driven Development (TDD):

1. Write tests for new features first
2. Implement the feature to make tests pass
3. Update documentation and README

See our [Development Guide](docs/development/setup.md) for detailed contribution guidelines.

## Issue Tracking

We use GitHub Issues to track bugs and feature requests:

- 🐛 **Bug Reports**: [Create a bug report](https://github.com/your-username/SayZhong/issues/new?template=bug_report.md)
- 💡 **Feature Requests**: [Request a feature](https://github.com/your-username/SayZhong/issues/new?template=feature_request.md)
- ❓ **Questions**: For usage questions, please use [Stack Overflow](https://stackoverflow.com/questions/tagged/sayzhong) with the `sayzhong` tag

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Research sources and methodology documentation in `docs/research/`
- Built with modern Python development best practices
- Designed for English speakers learning Mandarin Chinese