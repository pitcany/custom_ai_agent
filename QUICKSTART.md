# Quick Start Guide

## 1. Activate Virtual Environment

```bash
cd /Users/yannik/starter-agent
source venv/bin/activate
```

## 2. Add Your API Key

Edit `.env` file and add your Zhipu AI API key:

```bash
nano .env
```

Replace `your_z_ai_api_key_here` with your actual API key.

## 3. Run Tests

Verify everything works:

```bash
# Test all tools
python -m tests.test_tools

# Test search
python -m tests.test_search_tools
```

## 4. Run Agent

### Interactive Mode
```bash
python main.py
```

Then type your tasks interactively:
```
➤ Task: What is the current time?
⏳ Processing...
✅ Result: The current time is 2026-01-19 18:16:42
```

### Single Task
```bash
python main.py -t "Write 'Hello World' to greeting.txt"
```

### Example Tasks

#### File Operations
```
➤ Task: Create a file called test.md with content '# Test'
✅ Result: Successfully wrote to test.md
```

#### Web Search
```
➤ Task: Search for Python best practices
⏳ Processing...
✅ Result: [agent performs web search and creates summary]
```

#### Combined Tasks
```
➤ Task: Search for 'LangChain tutorial', save results to notes.md
✅ Result: Successfully wrote to notes.md
```

## 5. Switching Search Providers

### Use Tavily (Better Quality)

Edit `.env`:
```bash
TAVILY_API_KEY=your_tavily_key
SEARCH_PROVIDER=tavily
```

Restart agent to use new provider.

### Use DuckDuckGo (Default - Free)

Edit `.env`:
```bash
SEARCH_PROVIDER=duckduckgo
```

## 6. Adding Custom Tools

Create a new tool in `tools/custom_tools.py`:

```python
from langchain.tools import tool

@tool
def my_custom_tool(param: str) -> str:
    """Description of what the tool does.
    
    Args:
        param: Description of parameter.
    
    Returns:
        Result description.
    """
    return f"Processed: {param}"
```

Then add it to `agent.py`:
```python
from tools import my_custom_tool

# In __init__ of TaskAutomationAgent:
self.tools = [
    read_file,
    write_file,
    # ... existing tools ...
    my_custom_tool,  # Add your tool here
]
```

## 7. Troubleshooting

### Import Errors

If you see import errors, make sure virtual environment is activated:

```bash
source venv/bin/activate
```

### API Key Errors

Ensure `ZHIPUAI_API_KEY` is set in `.env`:

```bash
cat .env | grep ZHIPUAI_API_KEY
```

Should show your key (not the placeholder).

### Pydantic Warning

You'll see a warning about Pydantic V1. This is normal and doesn't affect functionality.

## 8. Next Steps

1. **Explore Tools**: Try all available tools with different tasks
2. **Build Your Own**: Add custom tools for your specific use cases
3. **Upgrade Provider**: Get Tavily API key for better search quality
4. **Read Docs**: Check LangChain and Zhipu AI documentation for advanced features

## Common Tasks

- Write/read files
- Search web for information
- Get current timestamp
- List directory contents
- Log events to file
- Send notifications (extend to Slack/Email)

For more details, see `README.md`.
