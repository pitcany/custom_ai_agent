from langchain_community.chat_models import ChatZhipuAI
from langchain.agents import create_agent
from tools import read_file, write_file, list_directory
from tools import get_current_time, send_notification, append_to_log
from tools import search_web
from config import Config


class TaskAutomationAgent:
    def __init__(self, config=None):
        if config is None:
            config = Config

        self.llm = ChatZhipuAI(model=config.MODEL_NAME, temperature=config.TEMPERATURE)

        search_provider = config.get_search_provider()

        self.tools = [
            read_file,
            write_file,
            list_directory,
            get_current_time,
            send_notification,
            append_to_log,
            search_web,
        ]

        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=(
                f"You are a helpful task automation assistant with web access. "
                f"Search provider: {Config.SEARCH_PROVIDER}. "
                "Use web_search to look up current information when needed. "
                "Use file tools to manage data. "
                "Always confirm when a task is complete."
            ),
        )

    def run(self, task: str) -> dict:
        """Execute a task and return result."""
        try:
            result = self.agent.invoke(
                {"messages": [{"role": "user", "content": task}]}
            )
            return {
                "success": True,
                "output": result.get("messages", [])[-1].content
                if result.get("messages")
                else "",
                "steps": result.get("messages", []),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def add_tool(self, tool_func):
        """Add a custom tool to the agent."""
        self.tools.append(tool_func)
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=(
                f"You are a helpful task automation assistant with web access. "
                f"Search provider: {Config.SEARCH_PROVIDER}. "
                "Use web_search to look up current information when needed. "
                "Use file tools to manage data. "
                "Always confirm when a task is complete."
            ),
        )
