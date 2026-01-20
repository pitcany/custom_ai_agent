from langchain_community.chat_models import ChatZhipuAI
from langchain.agents import create_agent
from tools import (
    read_file,
    write_file,
    list_directory,
    copy_file,
    delete_file,
    search_files,
    get_current_time,
    send_notification,
    append_to_log,
    search_web,
)
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
            copy_file,
            delete_file,
            search_files,
            get_current_time,
            send_notification,
            append_to_log,
            search_web,
        ]

        self.memory = None
        if config.ENABLE_MEMORY:
            from tools.memory_manager import ConversationRAGMemory

            self.memory = ConversationRAGMemory(
                memory_file=config.MEMORY_FILE, max_size=config.MAX_MEMORY_SIZE
            )

        system_prompt = (
            f"You are a helpful task automation assistant with web access. "
            f"Search provider: {Config.SEARCH_PROVIDER}. "
            "Use web_search to look up current information when needed. "
            "Use file tools to manage data. "
        )
        if config.ENABLE_MEMORY:
            system_prompt += " You have access to conversation memory with semantic search capabilities. "
            system_prompt += "Use relevant past context when answering."
        system_prompt += "Always confirm when a task is complete."

        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=system_prompt,
        )

    def run(self, task: str) -> dict:
        """Execute task and return result with RAG context."""
        try:
            # Get relevant conversation context using semantic search
            context = ""
            context_retrieved = False
            if self.memory:
                context = self.memory.retrieve_relevant_context(query=task, k=3)
                context_retrieved = len(context.split("\n")) > 0 if context else False

            # Format task with context
            full_task = task
            if context:
                full_task = f"{context}\n\nCurrent task: {task}"

            messages = [{"role": "user", "content": full_task}]
            result = self.agent.invoke({"messages": messages})

            # Save conversation to memory
            if self.memory and result.get("messages"):
                user_msg = {"role": "user", "content": task}
                assistant_msg = {
                    "role": "assistant",
                    "content": result["messages"][-1].content,
                }
                self.memory.add_messages([user_msg, assistant_msg])

            return {
                "success": True,
                "output": result.get("messages", [])[-1].content
                if result.get("messages")
                else "",
                "memory_enabled": self.memory is not None,
                "context_used": context_retrieved,
                "context_retrieved": len(context.split("\n")) if context else 0,
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
            ),
        )
