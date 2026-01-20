import sys

sys.path.insert(0, "..")


def test_imports():
    """Test that all tools can be imported."""
    try:
        from tools import read_file, write_file, list_directory
        from tools import get_current_time, send_notification, append_to_log
        from tools import search_web

        print("✅ All tools imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def test_config():
    """Test that config can be loaded."""
    try:
        from config import Config

        print(
            f"✅ Config loaded: Model={Config.MODEL_NAME}, Provider={Config.SEARCH_PROVIDER}"
        )
        return True
    except Exception as e:
        print(f"❌ Config load failed: {e}")
        return False


def test_agent_creation():
    """Test that agent can be instantiated."""
    try:
        from agent import TaskAutomationAgent
        from config import Config

        agent = TaskAutomationAgent(Config)
        print(f"✅ Agent created with {len(agent.tools)} tools")
        print(f"   Tools: {[tool.name for tool in agent.tools]}")
        return True
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return False


if __name__ == "__main__":
    all_passed = True
    all_passed &= test_imports()
    all_passed &= test_config()
    all_passed &= test_agent_creation()

    if all_passed:
        print("\n🎉 All tests passed!")
    else:
        print("\n❌ Some tests failed")
