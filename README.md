# Starter Agent with GLM 4.7

Simple tool-calling agent for task automation using Zhipu AI's GLM-4 model with web search capabilities.

## Features

- File operations (read, write, list, copy, delete)
- File search by pattern
- Web search with swappable providers
- Conversation memory with semantic RAG search
- Custom tools for automation
- Error handling and retries
- Easy to extend with new tools
- LangSmith tracing support

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Copy `.env.example` file and add your Zhipu AI API key:

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
- "Copy data.csv to backup/data.csv"
- "Delete old files matching pattern logs/*.log"
- "Find all Python files in ./src and list them"

### Conversation Memory (RAG)

The agent uses semantic search over conversation history to find relevant past context.

#### Enable Memory

```bash
# In .env
ENABLE_MEMORY=true
MEMORY_FILE=.agent_memory.json
MAX_MEMORY_SIZE=10
```

#### How RAG Memory Works

1. **Vector Storage**: Each message is embedded into a 768-dimensional vector and stored in an in-memory vector store
2. **Semantic Search**: When a new task comes in, the agent searches the vector store for semantically similar past conversations
3. **Context Injection**: The top-k most relevant messages (default k=3) are provided as context to the LLM
4. **Automatic Persistence**: Messages are automatically saved to `.agent_memory.json` after each conversation

#### Memory Capabilities

- **Find Related Topics**: "What were we discussing about Python?" finds all coding discussions, even if words differ
- **Topic Tracking**: "My project uses X" finds configuration-related conversations across multiple sessions
- **Context Retrieval**: Only the most relevant conversations are provided, reducing noise in the context window
- **Size Management**: Keeps only the most recent N messages (configurable via MAX_MEMORY_SIZE)

#### Example with RAG Memory

```bash
# Enable memory
export ENABLE_MEMORY=true

# Run agent interactively
python main.py

# Start conversation
➤ Task: Remember my name is Alice
✅ Result: Hi Alice!

# Continue conversation
➤ Task: Tell me about LangChain
✅ Result: [Agent searches memory for relevant context about LangChain]

# Later - agent finds relevant past context
➤ Task: What did we discuss about LangChain earlier?
✅ Result: [Agent retrieves relevant LangChain conversations from memory]
```

#### Clear Memory

To clear conversation memory, delete `.agent_memory.json`:

```bash
rm .agent_memory.json
```

The agent will start with a fresh memory on the next run.

#### Notes

- **FakeEmbeddings** use random vectors, not true semantic similarity
- For better semantic search, upgrade to real embeddings (OpenAI, local models)
- For production, consider persistent vector stores (Chroma, FAISS, Pinecone)
- Each conversation turn creates 2 documents (user + assistant messages)

### Web Search + File Operations
- "Search for latest Python best practices and save to best_practices.md"
- "Find information about LangChain agents and create summary.md"

### Conversation Memory
- "Remember my name is Alice"
- "What did we discuss earlier?"
- "Add task to my todo list"
- "Show me all pending items"

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

## LangSmith Observability

Enable LangSmith tracing for detailed monitoring:

### 1. Get LangSmith API Key
1. Go to https://smith.langchain.com
2. Create account and get API key
3. Add to `.env`:
```bash
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_TRACING=true
LANGCHAIN_PROJECT=starter-agent
```

### 2. View Traces
After running agent, view traces at:
https://smith.langchain.com

### 3. Benefits
- Debug agent decisions
- Monitor token usage and costs
- Track tool invocation performance
- Share and replay traces for debugging

## Conversation Memory (RAG)

The agent uses semantic search over conversation history to provide relevant context.

### Enable Memory

Add to `.env`:
```bash
ENABLE_MEMORY=true
MEMORY_FILE=.agent_memory.json
MAX_MEMORY_SIZE=10
```

### How It Works

1. Each conversation is stored as a document in an in-memory vector store
2. Messages are embedded into 768-dimensional vectors using FakeEmbeddings
3. When a new task comes in, the vector store is searched for semantically similar conversations
4. Top-k most relevant messages are provided as context to the LLM
5. Memory is automatically saved to `.agent_memory.json`

### Example Usage

```bash
# Agent semantically searches for relevant past context
➤ Task: Remember my name is Alice
✅ Result: Got it, Alice!

# Later, agent retrieves relevant context
➤ Task: What is my name?
✅ Result: Your name is Alice.

# Agent can find related topics
➤ Task: What were we discussing about Python?
✅ Result: [Searches memory for Python-related conversations and provides summary]
```

### Benefits

- **Semantic Search**: Finds related conversations even with different wording
- **Context-Aware**: Provides relevant past information without full history dump
- **Efficient**: Only retrieves top-k most relevant messages
- **Extensible**: Can add document retrieval (knowledge base) later

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
