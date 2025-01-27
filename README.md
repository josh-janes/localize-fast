# localizefast: CLI Translation Utility

A command-line tool to translate text files while preserving directory structure using Ollama's local AI models.

## Description

Translates files in a directory while maintaining folder structure. Features:
- Mirror directory structure with translated content
- HTML-aware translation preserving markup
- Progress UI with colored status updates
- Chunked translation for large files
- Supports any language supported by Ollama models

## Installation Instructions

### Prerequisites
- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running
- Required models downloaded (e.g., `llama2`)

### All Platforms

```pip install requests colorama```

## Mac

# Install Python if needed
```brew install python```
# Start Ollama
```ollama serve```

## Linux

# Install Python
```sudo apt-get install python3 python3-pip```

# Start Ollama (systemd example)
```systemctl start ollama```

## Windows

Install Python from python.org

Add Python to PATH during installation

Run in PowerShell:

```pip install requests beautifulsoup4 colorama```

ollama serve

## Basic Usage

```python localizefast.py [source_dir] [input_lang] [output_lang] [output_base] [options]```

# Example: Translate docs to Spanish
```python localizefast.py ./documents en es ./translations --model llama2```

Options:

    --model: Specify Ollama model (default: llama2)

    --chunk-size: Set max characters per chunk (default: 4000)

Output Structure:
Copy

translations/
└── es/
    └── [mirrored source structure]

## Troubleshooting
Ollama Connection Issues
bash
Copy

# Verify Ollama is running
curl http://localhost:11434

# Expected response: "Ollama is running"

# Model Not Found

Download required model
```ollama pull llama2```

File Permission Errors

    On Linux/Mac: Use sudo for system-wide installs

    On Windows: Run PowerShell as Administrator

Incomplete Translations

    Reduce chunk size: --chunk-size 2000

    Check model documentation for token limits


Note: Always keep the Ollama server running during translations. Monitor system resources when processing large directories.