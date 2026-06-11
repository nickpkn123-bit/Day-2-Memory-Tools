# Day 2: Memory and Tools

Goal: Extend your Day 1 agent with memory capabilities and tool integration

## What You'll Learn

- How to enable memory in CrewAI agents
- Understanding the four memory types (Short-Term, Long-Term, Entity, Contextual)
- Integrating tools from the CrewAI tools collection
- Creating custom tools with BaseTool
- Using RAG-based tools (WebsiteSearch, YouTubeVideoSearch)

## Objectives

- [ ] Enable memory in your agent
- [ ] Add tools from CrewAI collection
- [ ] Create a custom tool
- [ ] Test memory persistence across conversation
- [ ] Understand when agents use tools vs memory

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment

```bash
cp env_example.txt .env
# Edit .env and add your OPENAI_API_KEY
```

Optional: Add SERPER_API_KEY for web search (free at serper.dev)

### 3. Create Sample Content

Create a `blog-posts` directory with sample files for the tools to read:

```bash
mkdir blog-posts
echo "Sample blog post content" > blog-posts/example.md
```

### 4. Run Your Agent

```bash
python main.py
```

## Understanding Memory

### How Memory Works in CrewAI

According to the [CrewAI Memory documentation](https://docs.crewai.com/concepts/memory), CrewAI provides four types of memory:

#### 1. Short-Term Memory

- **Purpose**: Temporarily stores recent interactions during the current execution
- **Technology**: Uses RAG (Retrieval-Augmented Generation)
- **Scope**: Current session only
- **Example**: "Remember when you said your name was Alex?"

#### 2. Long-Term Memory

- **Purpose**: Preserves valuable insights across multiple sessions
- **Technology**: Persistent storage
- **Scope**: Survives program restarts
- **Example**: "Last week you mentioned you prefer detailed explanations"

#### 3. Entity Memory

- **Purpose**: Captures information about entities (people, places, concepts)
- **Technology**: Uses RAG for entity storage and retrieval
- **Scope**: Tracks relationships and attributes
- **Example**: "NANDA is a platform for agent collaboration at projectnanda.org"

#### 4. Contextual Memory

- **Purpose**: Maintains coherence by combining all memory types
- **Technology**: Memory fusion layer
- **Scope**: Integrates short-term, long-term, and entity memory
- **Example**: Combines "what we just discussed" + "what I know about you" + "entities mentioned"

### Enabling Memory

To enable all memory types, simply set `memory=True` in your Crew:

```python
crew = Crew(
    agents=[my_agent],
    tasks=[my_task],
    memory=True  # Enables all 4 memory types
)
```

## Understanding Tools

### Tools from CrewAI Collection

According to the [CrewAI Tools documentation](https://docs.crewai.com/concepts/tools), tools extend agent capabilities. This implementation includes:

#### 1. DirectoryReadTool

```python
from crewai_tools import DirectoryReadTool
docs_tool = DirectoryReadTool(directory='./blog-posts')
```

**Purpose**: Browse and list files in a directory
**Use case**: Agent needs to see what files are available

#### 2. FileReadTool

```python
from crewai_tools import FileReadTool
file_tool = FileReadTool()
```

**Purpose**: Read contents of specific files
**Use case**: Agent needs to access file contents

#### 3. WebsiteSearchTool (RAG-based)

```python
from crewai_tools import WebsiteSearchTool
web_rag_tool = WebsiteSearchTool()
```

**Purpose**: Search and extract content from websites using RAG
**Use case**: Agent needs to research a specific website

#### 4. YouTubeVideoSearchTool (RAG-based)

```python
from crewai_tools import YoutubeVideoSearchTool
youtube_tool = YoutubeVideoSearchTool()
```

**Purpose**: Search within YouTube video transcripts using RAG
**Use case**: Agent needs to find information in videos

#### 5. SerperDevTool

```python
from crewai_tools import SerperDevTool
search_tool = SerperDevTool()
```

**Purpose**: Web search via Serper API
**Use case**: Agent needs current information from the internet
**Requires**: SERPER_API_KEY in .env (free at serper.dev)

### Creating Custom Tools

According to the CrewAI documentation, create custom tools by extending BaseTool:

```python
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

# Define input schema
class MyToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument")

# Create tool class
class MyCustomTool(BaseTool):
    name: str = "my_tool_name"
    description: str = "What this tool does. LLM uses this to decide when to use the tool."
    args_schema: Type[BaseModel] = MyToolInput
    
    def _run(self, argument: str) -> str:
        # Your tool's logic here
        return "Tool result"

# Instantiate and add to agent
my_tool = MyCustomTool()
agent = Agent(..., tools=[my_tool])
```

### Adding Tools to Agent

Add tools to your agent using the `tools` parameter:

```python
agent = Agent(
    role="Research Assistant",
    goal="Help with research tasks",
    backstory="...",
    tools=[docs_tool, file_tool, search_tool],  # Add your tools here
    llm=llm
)
```

## Code Structure

The `main.py` file follows this structure:

1. **LLM Configuration**: Same as Day 1
2. **Tool Initialization**: Set up all tools
3. **Custom Tool Creation**: Define custom tools (optional)
4. **Agent Creation**: Add backstory, tools, and configure agent
5. **Task Definition**: Define what agent should do
6. **Crew Creation**: Enable memory with `memory=True`
7. **Execution**: Run interactive loop

## Testing Your Implementation

### Test Memory

```
You: "My name is Alex"
Agent: [Stores in short-term and entity memory]

You: "What's my name?"
Agent: [Retrieves from memory]
Expected: "Your name is Alex"
```

### Test Tools

```
You: "What files are in the blog-posts directory?"
Agent: [Uses DirectoryReadTool]
Expected: Lists files in directory

You: "Calculate 123 * 456"
Agent: [Uses CalculatorTool]
Expected: Shows result of calculation
```

### Test Memory Persistence

1. Run the program and tell it something: "I prefer concise answers"
2. Exit the program
3. Run again and ask: "How should you respond to me?"
4. Expected: Agent remembers your preference (long-term memory)

## Customization Guide

### Adding Your Own Tools

1. Browse CrewAI tools: https://docs.crewai.com/tools
2. Import the tool: `from crewai_tools import ToolName`
3. Initialize: `my_tool = ToolName(config)`
4. Add to agent's tools list

### Creating Your Own Custom Tool

Follow the template in `main.py`:

1. Define input schema with Pydantic
2. Create class extending BaseTool
3. Set name, description, args_schema
4. Implement `_run` method
5. Instantiate and add to agent

### Modifying Memory Behavior

Memory is automatic when `memory=True`. To customize:

```python
crew = Crew(
    agents=[agent],
    tasks=[task],
    memory=True,
    # Optional memory configuration
    # See: https://docs.crewai.com/concepts/memory
)
```

## Inspecting Memory Storage

### Where Memory is Stored

CrewAI stores memory in a platform-specific location following OS conventions:

**macOS:** `~/Library/Application Support/day-2/`
**Linux:** `~/.local/share/day-2/`
**Windows:** `C:\Users\{username}\AppData\Local\day-2\`

The directory structure:
```
~/Library/Application Support/day-2/
├── short_term/                       # Short-term memory (ChromaDB)
├── entities/                         # Entity memory (ChromaDB)
├── long_term_memory_storage.db       # Long-term memory (SQLite)
└── latest_kickoff_task_outputs.db    # Task outputs (SQLite)
```

### View What's Stored

Run the memory inspector:

```bash
python inspect_memory.py
```

This will show:
- What memory types have data
- How many files are stored
- Location of memory storage

### Clear Memory

To start fresh:

```bash
python inspect_memory.py clear
```

Or manually delete the directory (on macOS):

```bash
rm -rf ~/Library/Application\ Support/day-2/
```

### Understanding Memory Storage

Memory is stored as vector embeddings, not plain text. You won't see your exact conversations in readable format. The embeddings are used for similarity search when the agent needs to recall information.

**Memory files contain**:
- Vector embeddings of conversations
- Metadata about entities
- Timestamps and context
- Relationships between information

## Troubleshooting

**Memory not working**
- Verify `memory=True` in Crew initialization
- Check that conversation is long enough for memory to activate
- Try explicit memory tests (tell agent something, then ask about it)

**Tools not working**
- Check tool is in agent's tools list
- Verify API keys in .env for tools that require them
- Make sure task description hints at tool usage
- Check tool initialization has no errors

**SerperDevTool not available**
- This is optional - get free API key at serper.dev
- Add SERPER_API_KEY to .env file
- Agent will work without it, just won't have web search

**Files not found**
- Create blog-posts directory: `mkdir blog-posts`
- Add sample files for DirectoryReadTool and FileReadTool

## Resources

- [CrewAI Memory Documentation](https://docs.crewai.com/concepts/memory)
- [CrewAI Tools Documentation](https://docs.crewai.com/concepts/tools)
- [CrewAI Tools Collection](https://docs.crewai.com/tools)
- [Serper API](https://serper.dev) - Free web search API

## Checklist

Before moving to Day 3:
- [ ] Agent has memory enabled
- [ ] Agent uses at least 3 tools successfully
- [ ] Created at least 1 custom tool
- [ ] Tested memory persistence
- [ ] Agent remembers information from conversation
- [ ] Agent uses tools appropriately
- [ ] Understand when agent uses tools vs memory vs knowledge

## Next Steps

Ready for Day 3? Head to `../day-3/` to learn about deployment and production patterns.
