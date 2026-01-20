import sys

sys.path.insert(0, "..")
import tempfile
from pathlib import Path
from datetime import datetime


def test_rag_memory_creation():
    """Test RAG memory creation and initialization."""
    from tools.memory_manager import ConversationRAGMemory

    with tempfile.TemporaryDirectory() as tmpdir:
        mem_file = Path(tmpdir) / "test_rag.json"
        memory = ConversationRAGMemory(memory_file=str(mem_file), max_size=5)

        # Should create vector store
        assert memory.vectorstore is not None
        print("✅ RAG memory creation test passed")


def test_add_messages():
    """Test adding messages to RAG memory."""
    from tools.memory_manager import ConversationRAGMemory

    with tempfile.TemporaryDirectory() as tmpdir:
        mem_file = Path(tmpdir) / "test_rag.json"
        memory = ConversationRAGMemory(memory_file=str(mem_file))

        # Add messages
        memory.add_messages(
            [
                {"role": "user", "content": "What is Python?"},
                {"role": "assistant", "content": "Python is a programming language"},
            ]
        )

        # Verify messages were added
        all_docs = memory.vectorstore.similarity_search("", k=10)
        assert len(all_docs) >= 2

        print("✅ Add messages test passed")


def test_retrieve_context():
    """Test retrieving relevant context."""
    from tools.memory_manager import ConversationRAGMemory

    with tempfile.TemporaryDirectory() as tmpdir:
        mem_file = Path(tmpdir) / "test_rag.json"

        # Create memory and add conversation
        memory = ConversationRAGMemory(memory_file=str(mem_file))
        memory.add_messages(
            [
                {"role": "user", "content": "I like Python"},
                {"role": "assistant", "content": "Python is great!"},
                {"role": "user", "content": "Tell me about Java"},
                {"role": "assistant", "content": "Java is also a popular language"},
                {"role": "user", "content": "What about C++?"},
                {
                    "role": "assistant",
                    "content": "C++ is powerful for systems programming",
                },
            ]
        )

        # Search for relevant context about programming languages
        context = memory.retrieve_relevant_context(
            query="What languages do you know?", k=2
        )

        # Should find Python and/or Java conversations
        assert "Python" in context or "programming" in context.lower()
        assert "relevant conversation" in context.lower()

        print("✅ Retrieve context test passed")


def test_size_limit():
    """Test memory enforces size limit."""
    from tools.memory_manager import ConversationRAGMemory

    with tempfile.TemporaryDirectory() as tmpdir:
        mem_file = Path(tmpdir) / "test_rag.json"
        memory = ConversationRAGMemory(memory_file=str(mem_file), max_size=3)

        # Add more messages than limit
        for i in range(10):
            memory.add_messages([{"role": "user", "content": f"Message {i}"}])

        # Verify only 3 messages kept (max_size=3)
        all_docs = memory.vectorstore.similarity_search("", k=10)
        assert len(all_docs) <= 3

        print("✅ Size limit test passed")


def test_persistence():
    """Test saving and loading RAG memory."""
    from tools.memory_manager import ConversationRAGMemory

    with tempfile.TemporaryDirectory() as tmpdir:
        mem_file = Path(tmpdir) / "test_rag.json"

        # Create first instance and add messages
        memory1 = ConversationRAGMemory(memory_file=str(mem_file))
        memory1.add_messages([{"role": "user", "content": "Test message"}])

        # Create new instance and verify loading
        memory2 = ConversationRAGMemory(memory_file=str(mem_file))
        all_docs = memory2.vectorstore.similarity_search("", k=10)

        assert len(all_docs) >= 1
        assert "Test message" in str(all_docs)

        print("✅ Persistence test passed")


if __name__ == "__main__":
    test_rag_memory_creation()
    test_add_messages()
    test_retrieve_context()
    test_size_limit()
    test_persistence()
    print("\n🎉 All RAG memory tests passed!")
