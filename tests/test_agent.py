import sys

sys.path.insert(0, "..")
from agent import TaskAutomationAgent
from config import Config


def test_basic_task():
    """Test agent with simple task."""
    agent = TaskAutomationAgent(Config)
    result = agent.run("What is the current time?")
    assert result["success"] == True
    assert "20" in result["output"] or "202" in result["output"]
    print("✅ Basic task test passed")


def test_file_task():
    """Test agent with file operation."""
    agent = TaskAutomationAgent(Config)
    result = agent.run("Write 'Hello from agent' to a file called test_output.txt")
    assert result["success"] == True
    assert "test_output.txt" in result["output"].lower()
    print("✅ File task test passed")


def test_custom_tool():
    """Test agent with custom tool."""
    from langchain.tools import tool

    @tool
    def calculate_square(x: int) -> int:
        """Calculate the square of a number."""
        return x * x

    agent = TaskAutomationAgent(Config)
    agent.add_tool(calculate_square)
    result = agent.run("Calculate the square of 5")
    assert result["success"] == True
    assert "25" in result["output"]
    print("✅ Custom tool test passed")


if __name__ == "__main__":
    test_basic_task()
    test_file_task()
    test_custom_tool()
    print("\n🎉 All agent tests passed!")
