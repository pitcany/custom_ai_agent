from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.embeddings import FakeEmbeddings
from pathlib import Path
import json
from typing import List, Dict, Optional
from datetime import datetime
from langchain_core.documents import Document


class ConversationRAGMemory:
    """RAG-based conversation memory using InMemoryVectorStore."""

    def __init__(self, memory_file: str = ".agent_memory.json", max_size: int = 10):
        self.memory_file = memory_file
        self.max_size = max_size
        self.embeddings = FakeEmbeddings(size=768)
        self.vectorstore = InMemoryVectorStore(embedding=self.embeddings)

        self.load_from_file()

    def load_from_file(self):
        """Load messages from JSON file and add to vector store."""
        if Path(self.memory_file).exists():
            with open(self.memory_file, "r") as f:
                data = json.load(f)
                messages = data.get("messages", [])

                for msg in messages:
                    doc = Document(
                        page_content=msg.get("content", ""),
                        metadata={
                            "role": msg.get("role", ""),
                            "timestamp": msg.get("timestamp", ""),
                        },
                    )
                    self.vectorstore.add_documents([doc])

                self._enforce_size_limit()

    def save_to_file(self):
        """Save all messages to JSON file."""
        all_docs = self.vectorstore.similarity_search("", k=100)

        messages = []
        for doc in all_docs:
            messages.append(
                {
                    "role": doc.metadata.get("role", ""),
                    "content": doc.page_content,
                    "timestamp": doc.metadata.get("timestamp", ""),
                }
            )

        messages = messages[-self.max_size :]

        Path(self.memory_file).parent.mkdir(parents=True, exist_ok=True)
        with open(self.memory_file, "w") as f:
            json.dump({"messages": messages}, f, indent=2)

    def add_messages(self, messages: List[Dict]):
        """Add new messages to conversation memory."""
        timestamp = datetime.now().isoformat()

        for msg in messages:
            doc = Document(
                page_content=msg.get("content", ""),
                metadata={"role": msg.get("role", ""), "timestamp": timestamp},
            )
            self.vectorstore.add_documents([doc])

        self._enforce_size_limit()
        self.save_to_file()

    def retrieve_relevant_context(self, query: str, k: int = 3) -> str:
        """Retrieve top-k most relevant messages for context."""
        try:
            # Search vector store for relevant documents
            relevant_docs = self.vectorstore.similarity_search(query, k=k)

            if not relevant_docs:
                return ""

            # Format as conversation history
            context_lines = []
            for doc in relevant_docs:
                role = doc.metadata.get("role", "")
                content = doc.page_content
                context_lines.append(f"{role}: {content}")

            return f"Relevant conversation:\n" + "\n".join(context_lines)
        except Exception as e:
            # Handle errors gracefully (e.g., vector store not initialized)
            return ""

    def _enforce_size_limit(self):
        """Keep only most recent max_size messages."""
        all_docs = self.vectorstore.similarity_search("", k=100)

        if len(all_docs) > self.max_size:
            recent_docs = all_docs[-self.max_size :]

            self.vectorstore = InMemoryVectorStore(embedding=self.embeddings)
            self.vectorstore.add_documents(recent_docs)

    def clear(self):
        """Clear all conversation history."""
        self.vectorstore = InMemoryVectorStore(embedding=self.embeddings)
        self.save_to_file()
