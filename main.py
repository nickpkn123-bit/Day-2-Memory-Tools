"""
Personal Agent Twin with Memory and Tools - Day 2
==================================================
Modified to use OpenRouter instead of OpenAI
"""

from crewai import Agent, Task, Crew, LLM
from crewai.tools import BaseTool
from crewai_tools import DirectoryReadTool, FileReadTool, SerperDevTool
from pydantic import BaseModel, Field
from typing import Type
from dotenv import load_dotenv
import os

load_dotenv()

# ==============================================================================
# STEP 1: Configure LLM - OpenRouter
# ==============================================================================

llm = LLM(
    model="openrouter/openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.7,
)

# ==============================================================================
# STEP 2: Define Tools
# ==============================================================================

# Create blog-posts directory if it doesn't exist
os.makedirs("./blog-posts", exist_ok=True)

# Tool 1: Directory Reading
docs_tool = DirectoryReadTool(directory='./blog-posts')

# Tool 2: File Reading
file_tool = FileReadTool()

# Tool 3: Web Search (optional - requires SERPER_API_KEY)
search_tool = None
if os.getenv('SERPER_API_KEY'):
    search_tool = SerperDevTool()

# ==============================================================================
# STEP 3: Create Custom Tool
# ==============================================================================

class CalculatorInput(BaseModel):
    """Input schema for Calculator tool."""
    expression: str = Field(..., description="Mathematical expression to evaluate")

class CalculatorTool(BaseTool):
    name: str = "calculator"
    description: str = "Performs mathematical calculations. Use for any math operations."
    args_schema: Type[BaseModel] = CalculatorInput
    
    def _run(self, expression: str) -> str:
        try:
            result = eval(expression, {"__builtins__": {}}, {})
            return f"Result: {result}"
        except Exception as e:
            return f"Error: {str(e)}"

calculator_tool = CalculatorTool()

# ==============================================================================
# STEP 4: Create Agent
# ==============================================================================

available_tools = [docs_tool, file_tool, calculator_tool]
if search_tool:
    available_tools.append(search_tool)

my_agent_twin = Agent(
    role="Personal Digital Twin with Tools",
    
    goal="Answer questions about me and use tools when needed",
    
    backstory="""
    You are the digital twin of a student learning AI and CrewAI.
    
    Here's what you know about me:
    - I'm a student in the NANDA course learning about AI agents
    - I'm learning about AI agents, memory systems, and tools
    - My favorite programming language is Python
    - I'm building this as part of a 5-day intensive course
    
    TOOL CAPABILITIES:
    - DirectoryReadTool: Browse and list files in directories
    - FileReadTool: Read specific files
    - Calculator: Perform mathematical calculations
    - SerperDevTool: Web search (if API key configured)
    
    Use tools when you need external information or calculations.
    """,
    
    tools=available_tools,
    llm=llm,
    verbose=True,
)

# ==============================================================================
# STEP 5: Create Task
# ==============================================================================

answer_question_task = Task(
    description="""
    Answer the following question: {question}
    
    Use your tools when you need external information or calculations.
    Provide accurate, helpful responses.
    """,
    
    expected_output="A clear, helpful answer using tools as needed",
    
    agent=my_agent_twin,
)

# ==============================================================================
# STEP 6: Create Crew (memory=False to avoid OpenAI dependency)
# ==============================================================================

my_crew = Crew(
    agents=[my_agent_twin],
    tasks=[answer_question_task],
    memory=False,
    verbose=True,
)

# ==============================================================================
# STEP 7: Run
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("Personal Agent Twin - Day 2: Tools")
    print("="*70 + "\n")
    
    print("Ask me questions! I'll use tools when needed.")
    print("Type 'quit' to exit.\n")
    
    while True:
        question = input("You: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye!\n")
            break
        
        if not question:
            continue
        
        result = my_crew.kickoff(inputs={"question": question})
        print(f"\nAgent: {result.raw}\n")
