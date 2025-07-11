# Coder CLI

A modular CLI-powered AI toolchain that turns specs into scaffolds, code, and docs — using LLMs like GPT to supercharge software development.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![CLI Tool](https://img.shields.io/badge/CLI-Tool-green)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow)


## Overview

Built with Python + Click, this CLI wraps specialized AI agents to handle different stages of software creation.

Coder CLI is designed for devs who prefer terminal-first workflows and want full control over LLM-driven codegen, with local execution optional.

- **SpecAgent**: Converts high-level ideas into structured technical specifications
- **ScaffoldAgent**: Generates project structure and starter files based on specifications
- **DevAgent**: Writes, refactors, or enhances code across multiple files
- **DocAgent**: Creates documentation for your project
- **CriticAgent**: Reviews and provides feedback on your code

## Installation

1. Clone this repository
2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `config.yaml` file based on the example:
   ```bash
   cp config.yaml.example config.yaml
   ```
5. Update `config.yaml` with your OpenAI API key and other settings

## Configuration

Edit the `config.yaml` file with your settings:

```yaml
model: gpt-4-turbo # or deepseek-chat, llama3, etc.
openai_api_base: https://openrouter.ai/api/v1 # example: https://api.openai.com/v1 or local server
openai_api_key: your_api_key_here
```

## Usage

### Coder CLI Commands

```bash
# Generate a project specification from a brief idea
python coder.py spec "Create a web app for tracking TV shows" --format json

# Or use a markdown file with detailed requirements
python coder.py spec --file project_brief.md --format markdown

# Generate project scaffold from a spec file
python coder.py scaffold --file output/spec.json

# Parse scaffold markdown into actual files
python coder.py parse-scaffold --file output/scaffold.md --outdir my_project

# Run DevAgent to perform specific tasks on your code
python coder.py dev --task "Add authentication to the login page" --context my_project

# Parse DevAgent output into actual file changes
python coder.py parse-dev --file output/dev_output.md --outdir my_project
```

### Examples

```bash
# Generate a project spec for a simple TV show tracker
python coder.py spec "TV show tracker app with user login and watch history" --format json

# Generate project structure from the spec
python coder.py scaffold --file output/spec.json

# Create the project files
python coder.py parse-scaffold --file output/scaffold.md --outdir CheckInTV

# Add a feature with DevAgent
python coder.py dev --task "Add season filter to the show list" --context CheckInTV

# Apply the changes
python coder.py parse-dev --file output/dev_output.md --outdir CheckInTV
```

## Project Structure

```
/
├── agents/       # Agent implementation code
├── memory/       # Memory persistence for agents
├── prompts/      # System prompts for each agent type
├── output/       # Generated files and outputs
├── templates/    # Templates used by agents
├── coder.py      # Main CLI application
└── config.yaml   # Configuration settings
```

## Notes

- Files generated in the `output` directory are ignored by git (see .gitignore)
- The system requires an OpenAI API key or compatible endpoint
- Currently supports JSON and Markdown output formats

## Roadmap
- [ ] Add support for local LLMs (Ollama)
- [ ] Git diff-based parse-dev strategy
- [ ] Plugin architecture for custom agents

## License

[MIT License](LICENSE)
