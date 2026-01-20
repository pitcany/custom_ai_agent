# Starter Agent with GLM 4.7

Simple tool-calling agent for task automation using Zhipu AI's GLM-4 model with web search capabilities.

## Features

- File operations (read, write, list)
- Web search with swappable providers
- Custom tools for automation
- Error handling and retries
- Easy to extend with new tools

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Copy `.env` file and add your Zhipu AI API key:

```bash
cp .env.example .env
# Edit .env and add: ZHIPUAI_API_KEY=your_key_here
```

### 3. Run Tests

```bash
# Test tools
python tests/test_tools.py

# Test search functionality
python tests/test_search_tools.py

# Test agent
python tests/test_agent.py
```

## Usage

### Interactive Mode

```bash
python main.py
```

Then enter your tasks interactively.

### Single Task Mode

```bash
python main.py -t "Search for 'LangChain agents' and save a summary to langchain_summary.md"
```

### Single Task with Verbose Output

```bash
python main.py -t "Write current time to timestamp.txt" -v
```

## Web Search Providers

### DuckDuckGo (Default - Free)

No additional configuration needed. Works out of the box.

```bash
# .env
ZHIPUAI_API_KEY=your_key
SEARCH_PROVIDER=duckduckgo
```

### Tavily (Higher Quality)

Requires Tavily API key. Better for production use.

```bash
# .env
ZHIPUAI_API_KEY=your_key
TAVILY_API_KEY=your_tavily_key
SEARCH_PROVIDER=tavily
```

Get API key at: https://tavily.com/

### Adding Custom Providers

1. Create `tools/search_providers/yourprovider.py`
2. Implement `SearchProvider` interface
3. Add to `config.py.get_search_provider()` method
4. Update `.env` with `SEARCH_PROVIDER=yourprovider`

## Example Tasks

### File Operations
- "Read report.txt and extract key metrics"
- "Create summary.md with bullet points from data.csv"

### Web Search + File Operations
- "Search for latest Python best practices and save to best_practices.md"
- "Find information about LangChain agents and create summary.md"

### Automation
- "Check if backup.log exists and append timestamp"
- "Generate daily_report.md with today's date and status"

### Combined Tasks
- "Search for 'LangChain tutorial', read result summaries, create study_notes.md"

## Project Structure

```
starter-agent/
├── .env                  # API keys and configuration
├── config.py              # Configuration loader
├── agent.py               # Main agent class
├── main.py                # Entry point
├── tools/                 # Custom tools
│   ├── file_tools.py       # File operations
│   ├── custom_tools.py     # Automation utilities
│   ├── search_tools.py     # Search management
│   └── search_providers/   # Search providers
│       ├── duckduckgo.py   # Default (free)
│       └── tavily.py       # Upgrade option
└── tests/                 # Test files
    ├── test_tools.py
    ├── test_search_tools.py
    └── test_agent.py
```

## Troubleshooting

### API Key Errors

Make sure `ZHIPUAI_API_KEY` is set in `.env` or environment variables.

### Search Errors

- DuckDuckGo: Should work without any configuration
- Tavily: Ensure `TAVILY_API_KEY` is valid and not expired

### Import Errors

Reinstall dependencies:

```bash
pip install --upgrade -r requirements.txt
```

## License

MIT
